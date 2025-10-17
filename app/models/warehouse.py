from app import db
from datetime import datetime

class Warehouse(db.Model):
    """仓库模型"""
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)  # 仓库编码
    name = db.Column(db.String(128), nullable=False)  # 仓库名称
    warehouse_type = db.Column(db.String(32), nullable=False)  # 仓库类型: qiguang/direct_sales
    address = db.Column(db.String(256))  # 仓库地址
    manager = db.Column(db.String(64))  # 仓库管理员
    phone = db.Column(db.String(20))  # 联系电话
    capacity = db.Column(db.Float)  # 仓库容量
    description = db.Column(db.Text)  # 描述
    is_active = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'warehouse_type': self.warehouse_type,
            'address': self.address,
            'manager': self.manager,
            'phone': self.phone,
            'capacity': self.capacity,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

