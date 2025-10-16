from app import db
from datetime import datetime

class Terminal(db.Model):
    """终端客户模型"""
    __tablename__ = 'terminals'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)  # 终端编码
    name = db.Column(db.String(128), nullable=False)  # 名称
    type = db.Column(db.String(32))  # 类型
    level = db.Column(db.String(32))  # 客户等级
    visit_frequency = db.Column(db.String(32))  # 拜访频率
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户经理
    assistant_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户协助员
    tags = db.Column(db.String(256))  # 标签
    supplier = db.Column(db.String(128))  # 供应商
    sales_area = db.Column(db.String(64))  # 销售区域
    cooperation_status = db.Column(db.String(32))  # 合作状态
    phone = db.Column(db.String(20))
    remark = db.Column(db.Text)  # 备注
    business_license = db.Column(db.String(256))  # 营业执照
    license_name = db.Column(db.String(128))  # 营业执照名称
    registration_no = db.Column(db.String(64))  # 工商注册号
    registration_date = db.Column(db.Date)  # 注册日期
    operator = db.Column(db.String(64))  # 经营者
    business_area = db.Column(db.Float)  # 营业面积
    business_hours = db.Column(db.String(64))  # 营业时间
    online_platform = db.Column(db.Boolean, default=False)  # 是否开通线上平台
    jurisdiction_dept = db.Column(db.String(64))  # 所属管辖部门
    ka_system = db.Column(db.String(64))  # KA系统
    region = db.Column(db.String(128))  # 地区
    address = db.Column(db.String(256))  # 详细地址
    latitude = db.Column(db.Float)  # 纬度
    longitude = db.Column(db.Float)  # 经度
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_terminals')
    assistant = db.relationship('User', foreign_keys=[assistant_id], backref='assisted_terminals')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'level': self.level,
            'visit_frequency': self.visit_frequency,
            'manager': self.manager.name if self.manager else None,
            'phone': self.phone,
            'address': self.address,
            'cooperation_status': self.cooperation_status,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DirectDistributor(db.Model):
    """直营商客户模型"""
    __tablename__ = 'direct_distributors'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(32))
    level = db.Column(db.String(32))
    visit_frequency = db.Column(db.String(32))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assistant_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(256))
    cooperation_status = db.Column(db.String(32))
    approval_status = db.Column(db.String(32), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_distributors')
    assistant = db.relationship('User', foreign_keys=[assistant_id], backref='assisted_distributors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'level': self.level,
            'manager': self.manager.name if self.manager else None,
            'phone': self.phone,
            'address': self.address,
            'cooperation_status': self.cooperation_status,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class KOL(db.Model):
    """KOL客户模型"""
    __tablename__ = 'kols'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    archive_type = db.Column(db.String(32))  # 档案属性
    consumer_type = db.Column(db.String(32))  # 消费者类型
    visit_frequency = db.Column(db.String(32))
    is_decision_maker = db.Column(db.Boolean, default=False)  # 是否下单决定人
    company = db.Column(db.String(128))  # 当前所在单位
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    hobby = db.Column(db.String(256))  # 个人爱好
    kol_level = db.Column(db.String(32))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    department = db.Column(db.String(64))
    city = db.Column(db.String(64))
    cooperation_status = db.Column(db.String(32))
    remark = db.Column(db.Text)
    profession = db.Column(db.String(64))  # 职业/职务
    age_group = db.Column(db.String(32))  # 年龄段
    drinking_frequency = db.Column(db.String(32))  # 饮酒频率
    drinking_scene = db.Column(db.String(64))  # 用酒场景
    address = db.Column(db.String(256))
    approval_status = db.Column(db.String(32), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_kols')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'phone': self.phone,
            'company': self.company,
            'profession': self.profession,
            'kol_level': self.kol_level,
            'manager': self.manager.name if self.manager else None,
            'cooperation_status': self.cooperation_status,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CustomerContact(db.Model):
    """客户联系人模型"""
    __tablename__ = 'customer_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_type = db.Column(db.String(32), nullable=False)  # terminal/distributor/kol
    customer_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)  # 是否主联系人
    position = db.Column(db.String(64))  # 职务
    remark = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'name': self.name,
            'phone': self.phone,
            'is_primary': self.is_primary,
            'position': self.position,
            'remark': self.remark
        }

