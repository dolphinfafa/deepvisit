from app import db
from datetime import datetime

class Supplier(db.Model):
    """供应商模型"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)  # 供应商编码
    name = db.Column(db.String(128), nullable=False)  # 供应商名称
    contact_person = db.Column(db.String(64))  # 联系人
    phone = db.Column(db.String(20))  # 联系电话
    email = db.Column(db.String(120))  # 邮箱
    address = db.Column(db.String(256))  # 地址
    tax_number = db.Column(db.String(64))  # 税号
    bank_account = db.Column(db.String(64))  # 银行账户
    bank_name = db.Column(db.String(128))  # 开户银行
    payment_terms = db.Column(db.String(128))  # 付款条件
    credit_limit = db.Column(db.Float, default=0)  # 信用额度
    is_active = db.Column(db.Boolean, default=True)  # 是否启用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'contact_person': self.contact_person,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'tax_number': self.tax_number,
            'bank_account': self.bank_account,
            'bank_name': self.bank_name,
            'payment_terms': self.payment_terms,
            'credit_limit': self.credit_limit,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

