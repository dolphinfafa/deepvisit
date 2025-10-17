from app import db
from datetime import datetime

class Inventory(db.Model):
    """库存模型"""
    __tablename__ = 'inventories'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)  # 仓库ID
    warehouse_name = db.Column(db.String(128))  # 仓库名称（冗余字段，便于查询）
    warehouse_type = db.Column(db.String(32))  # 仓库类型（冗余字段）
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)  # 数量
    cost = db.Column(db.Float, default=0)  # 成本
    total_cost = db.Column(db.Float, default=0)  # 总成本
    min_stock = db.Column(db.Integer, default=0)  # 最低库存
    max_stock = db.Column(db.Integer, default=0)  # 最高库存
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    warehouse = db.relationship('Warehouse', backref='inventories')
    product = db.relationship('Product', backref='inventories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.warehouse_name,
            'warehouse_type': self.warehouse_type,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'cost': self.cost,
            'total_cost': self.total_cost,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def update_stock(warehouse_id, product_id, quantity_change, cost=None):
        """更新库存数量"""
        inventory = Inventory.query.filter_by(
            warehouse_id=warehouse_id, 
            product_id=product_id
        ).first()
        
        # 获取仓库信息
        from app.models.warehouse import Warehouse
        warehouse = Warehouse.query.get(warehouse_id)
        
        if not inventory:
            # 创建新的库存记录
            inventory = Inventory(
                warehouse_id=warehouse_id,
                warehouse_name=warehouse.name if warehouse else '',
                warehouse_type=warehouse.warehouse_type if warehouse else '',
                product_id=product_id,
                quantity=quantity_change,
                cost=cost or 0,
                total_cost=(cost or 0) * quantity_change
            )
            db.session.add(inventory)
        else:
            # 更新现有库存
            inventory.quantity += quantity_change
            if cost:
                inventory.cost = cost
            inventory.total_cost = inventory.cost * inventory.quantity
            
            # 更新仓库信息（防止数据不一致）
            if warehouse:
                inventory.warehouse_name = warehouse.name
                inventory.warehouse_type = warehouse.warehouse_type
        
        inventory.updated_at = datetime.utcnow()
        db.session.commit()
        return inventory

