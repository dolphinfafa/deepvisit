from app import db
from datetime import datetime

class Terminal(db.Model):
    """终端客户模型"""
    __tablename__ = 'terminals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # 终端名称
    code = db.Column(db.String(64), unique=True, nullable=False)  # 终端客户编码
    type = db.Column(db.String(32))  # 终端类型
    level = db.Column(db.String(32))  # 客户等级
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户经理
    assistant_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户协助员
    sales_area = db.Column(db.String(64))  # 销售区域
    tags = db.Column(db.String(256))  # 终端标签
    supplier = db.Column(db.String(128))  # 供货商
    cooperation_status = db.Column(db.String(32))  # 合作状态
    phone = db.Column(db.String(20))  # 手机号
    remark = db.Column(db.Text)  # 备注
    visit_frequency = db.Column(db.String(32))  # 拜访频率
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态
    business_license = db.Column(db.String(256))  # 营业执照
    license_name = db.Column(db.String(128))  # 营业执照名称
    registration_no = db.Column(db.String(64))  # 工商注册号
    registration_date = db.Column(db.Date)  # 注册日期
    operator = db.Column(db.String(64))  # 经营者
    receiver_name = db.Column(db.String(64))  # 收货人姓名
    receiver_phone = db.Column(db.String(20))  # 收货人手机号
    receiver_address = db.Column(db.String(256))  # 收货地址
    detail_address = db.Column(db.String(256))  # 详细地址
    contact_name = db.Column(db.String(64))  # 联系人姓名
    contact_phone = db.Column(db.String(20))  # 联系人手机号
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_terminals', lazy='select')
    assistant = db.relationship('User', foreign_keys=[assistant_id], backref='assisted_terminals', lazy='select')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.type,
            'level': self.level,
            'manager': self.manager.name if self.manager else None,
            'assistant': self.assistant.name if self.assistant else None,
            'sales_area': self.sales_area,
            'tags': self.tags,
            'supplier': self.supplier,
            'cooperation_status': self.cooperation_status,
            'phone': self.phone,
            'remark': self.remark,
            'visit_frequency': self.visit_frequency,
            'approval_status': self.approval_status,
            'business_license': self.business_license,
            'license_name': self.license_name,
            'registration_no': self.registration_no,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'operator': self.operator,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'receiver_address': self.receiver_address,
            'detail_address': self.detail_address,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DirectDistributor(db.Model):
    """直营商客户模型"""
    __tablename__ = 'direct_distributors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # 直营商名称
    code = db.Column(db.String(64), unique=True, nullable=False)  # 直营商客户编码
    type = db.Column(db.String(32))  # 直营商类型
    level = db.Column(db.String(32))  # 客户等级
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户经理
    assistant_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户协助员
    sales_area = db.Column(db.String(64))  # 销售区域
    tags = db.Column(db.String(256))  # 直营商标签
    supplier = db.Column(db.String(128))  # 供货商
    cooperation_status = db.Column(db.String(32))  # 合作状态
    phone = db.Column(db.String(20))  # 手机号
    remark = db.Column(db.Text)  # 备注
    visit_frequency = db.Column(db.String(32))  # 拜访频率
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态
    business_license = db.Column(db.String(256))  # 营业执照
    license_name = db.Column(db.String(128))  # 营业执照名称
    registration_no = db.Column(db.String(64))  # 工商注册号
    registration_date = db.Column(db.Date)  # 注册日期
    operator = db.Column(db.String(64))  # 经营者
    receiver_name = db.Column(db.String(64))  # 收货人姓名
    receiver_phone = db.Column(db.String(20))  # 收货人手机号
    receiver_address = db.Column(db.String(256))  # 收货地址
    detail_address = db.Column(db.String(256))  # 详细地址
    contact_name = db.Column(db.String(64))  # 联系人姓名
    contact_phone = db.Column(db.String(20))  # 联系人手机号
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_distributors', lazy='select')
    assistant = db.relationship('User', foreign_keys=[assistant_id], backref='assisted_distributors', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.type,
            'level': self.level,
            'manager': self.manager.name if self.manager else None,
            'assistant': self.assistant.name if self.assistant else None,
            'sales_area': self.sales_area,
            'tags': self.tags,
            'supplier': self.supplier,
            'cooperation_status': self.cooperation_status,
            'phone': self.phone,
            'remark': self.remark,
            'visit_frequency': self.visit_frequency,
            'approval_status': self.approval_status,
            'business_license': self.business_license,
            'license_name': self.license_name,
            'registration_no': self.registration_no,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None,
            'operator': self.operator,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'receiver_address': self.receiver_address,
            'detail_address': self.detail_address,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class KOL(db.Model):
    """KOL客户模型"""
    __tablename__ = 'kols'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)  # KOL编码
    name = db.Column(db.String(128), nullable=False)  # KOL姓名
    consumer_type = db.Column(db.String(32))  # 消费者类型
    gender = db.Column(db.String(10))  # 性别
    phone = db.Column(db.String(20))  # 电话
    age_group = db.Column(db.String(32))  # 年龄段
    kol_tags = db.Column(db.String(256))  # KOL标签
    birthday = db.Column(db.Date)  # 生日
    location = db.Column(db.String(128))  # 所在地
    profession = db.Column(db.String(64))  # 职业
    drinking_frequency = db.Column(db.String(32))  # 饮酒频率
    drinking_scene = db.Column(db.String(64))  # 用酒场景
    cooperation_status = db.Column(db.String(32))  # 合作状态
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户经理
    position_note = db.Column(db.String(256))  # 标注位置
    province = db.Column(db.String(64))  # 省
    city = db.Column(db.String(64))  # 市
    district = db.Column(db.String(64))  # 区
    street = db.Column(db.String(128))  # 街道
    detail_address = db.Column(db.String(256))  # 详细地址
    hobbies = db.Column(db.String(256))  # 个人爱好
    remark = db.Column(db.Text)  # 备注
    receiver_name = db.Column(db.String(64))  # 收货人姓名
    receiver_phone = db.Column(db.String(20))  # 收货人手机
    receiver_address = db.Column(db.String(256))  # 收货地址
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    manager = db.relationship('User', foreign_keys=[manager_id], backref='managed_kols', lazy='select')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'consumer_type': self.consumer_type,
            'gender': self.gender,
            'phone': self.phone,
            'age_group': self.age_group,
            'kol_tags': self.kol_tags,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'location': self.location,
            'profession': self.profession,
            'drinking_frequency': self.drinking_frequency,
            'drinking_scene': self.drinking_scene,
            'cooperation_status': self.cooperation_status,
            'manager': self.manager.name if self.manager else None,
            'position_note': self.position_note,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'street': self.street,
            'detail_address': self.detail_address,
            'hobbies': self.hobbies,
            'remark': self.remark,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'receiver_address': self.receiver_address,
            'creator': self.creator.name if hasattr(self, 'creator') and self.creator else None,
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

