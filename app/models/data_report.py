from app import db
from datetime import datetime
import uuid

class DisplayReport(db.Model):
    """铺货上报模型"""
    __tablename__ = 'display_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(64), unique=True, nullable=False)  # 上报编码
    report_date = db.Column(db.Date, nullable=False)  # 上报日期
    customer_name = db.Column(db.String(128), nullable=False)  # 客户名称
    customer_type = db.Column(db.String(32))  # 客户类型：terminal/distributor/kol
    customer_level = db.Column(db.String(32))  # 客户等级
    customer_manager = db.Column(db.String(128))  # 客户经理
    product_code = db.Column(db.String(64), nullable=False)  # 商品编码
    product_name = db.Column(db.String(128), nullable=False)  # 商品名称
    specification = db.Column(db.String(64))  # 规格
    product_type = db.Column(db.String(32))  # 商品类型
    brand = db.Column(db.String(64))  # 品牌
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上报人
    remark = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reported_by], backref='display_reports', lazy='select')
    
    def __init__(self, **kwargs):
        super(DisplayReport, self).__init__(**kwargs)
        if not self.report_code:
            # 生成上报编码：DIS + 时间戳 + 4位随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(uuid.uuid4().int)[:4]
            self.report_code = f'DIS{timestamp}{random_suffix}'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'report_code': self.report_code,
            'report_date': self.report_date.isoformat() if self.report_date else None,
            'customer_name': self.customer_name,
            'customer_type': self.customer_type,
            'customer_level': self.customer_level,
            'customer_manager': self.customer_manager,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'specification': self.specification,
            'product_type': self.product_type,
            'brand': self.brand,
            'reported_by': self.reporter.name if self.reporter else None,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class InventoryReport(db.Model):
    """库存上报模型"""
    __tablename__ = 'inventory_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(64), unique=True, nullable=False)  # 上报编码
    customer_name = db.Column(db.String(128), nullable=False)  # 客户名称
    product_name = db.Column(db.String(128), nullable=False)  # 商品名称
    specification = db.Column(db.String(64))  # 规格
    product_code = db.Column(db.String(64))  # 商品编码
    quantity = db.Column(db.Integer, nullable=False)  # 库存数量
    remark = db.Column(db.Text)  # 备注
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上报人
    report_time = db.Column(db.DateTime, default=datetime.utcnow)  # 上报时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reported_by], backref='inventory_reports', lazy='select')
    
    def __init__(self, **kwargs):
        super(InventoryReport, self).__init__(**kwargs)
        if not self.report_code:
            # 生成上报编码：INV + 时间戳 + 4位随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(uuid.uuid4().int)[:4]
            self.report_code = f'INV{timestamp}{random_suffix}'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'report_code': self.report_code,
            'customer_name': self.customer_name,
            'product_name': self.product_name,
            'specification': self.specification,
            'product_code': self.product_code,
            'quantity': self.quantity,
            'remark': self.remark,
            'reported_by': self.reporter.name if self.reporter else None,
            'report_time': self.report_time.isoformat() if self.report_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CompetitorReport(db.Model):
    """竞品上报模型"""
    __tablename__ = 'competitor_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(64), unique=True, nullable=False)  # 上报编码
    competitor_name = db.Column(db.String(128), nullable=False)  # 竞品名称
    product_name = db.Column(db.String(128))  # 商品名称（我方商品）
    remark = db.Column(db.Text)  # 备注
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上报人
    report_time = db.Column(db.DateTime, default=datetime.utcnow)  # 上报时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reported_by], backref='competitor_reports', lazy='select')
    
    def __init__(self, **kwargs):
        super(CompetitorReport, self).__init__(**kwargs)
        if not self.report_code:
            # 生成上报编码：CMP + 时间戳 + 4位随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(uuid.uuid4().int)[:4]
            self.report_code = f'CMP{timestamp}{random_suffix}'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'report_code': self.report_code,
            'competitor_name': self.competitor_name,
            'product_name': self.product_name,
            'remark': self.remark,
            'reported_by': self.reporter.name if self.reporter else None,
            'report_time': self.report_time.isoformat() if self.report_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

