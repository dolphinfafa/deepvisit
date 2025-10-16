from app import db
from datetime import datetime

class Inventory(db.Model):
    """库存模型"""
    __tablename__ = 'inventories'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse = db.Column(db.String(64), nullable=False)  # 仓库
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)  # 数量
    cost = db.Column(db.Float, default=0)  # 成本
    total_cost = db.Column(db.Float, default=0)  # 总成本
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = db.relationship('Product', backref='inventories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'warehouse': self.warehouse,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'cost': self.cost,
            'total_cost': self.total_cost,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

