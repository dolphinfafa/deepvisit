from app import db
from datetime import datetime

class Product(db.Model):
    """商品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)  # 商品编码
    name = db.Column(db.String(128), nullable=False)  # 商品名称
    specification = db.Column(db.String(64))  # 规格
    unit = db.Column(db.String(32))  # 单位
    category = db.Column(db.String(64))  # 分类
    brand = db.Column(db.String(64))  # 品牌
    type = db.Column(db.String(32))  # 类型: own/competitor
    price = db.Column(db.Float, default=0)  # 价格
    cost = db.Column(db.Float, default=0)  # 成本
    image = db.Column(db.String(256))  # 图片
    description = db.Column(db.Text)  # 描述
    is_active = db.Column(db.Boolean, default=True)  # 是否启用
    is_display = db.Column(db.Boolean, default=False)  # 是否铺货上报商品
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'specification': self.specification,
            'unit': self.unit,
            'category': self.category,
            'brand': self.brand,
            'type': self.type,
            'price': self.price,
            'cost': self.cost,
            'is_active': self.is_active,
            'is_display': self.is_display
        }

