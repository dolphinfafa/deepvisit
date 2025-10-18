from app import db
from datetime import datetime
import uuid

class Activity(db.Model):
    """活动模型"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_code = db.Column(db.String(64), unique=True, nullable=False)  # 活动编码
    name = db.Column(db.String(128), nullable=False)  # 活动名称
    activity_type = db.Column(db.String(32))  # 活动类型：付费陈列、新网点开发、消费联谊
    execution_start_date = db.Column(db.Date)  # 执行周期-开始日期
    execution_end_date = db.Column(db.Date)  # 执行周期-结束日期
    description = db.Column(db.Text)  # 活动说明
    require_application = db.Column(db.String(16))  # 是否需要申请参与：需要、不需要
    customer_scope = db.Column(db.String(32))  # 参与客户范围：不限制、终端客户、经销商客户
    product_scope = db.Column(db.String(32))  # 参与活动商品：全部商品、指定具体商品、指定商品类型
    product_details = db.Column(db.Text)  # 指定商品详情（JSON格式）
    payment_method = db.Column(db.String(32))  # 兑付方式：仅现金、仅商品、现金或商品、不限
    settlement_method = db.Column(db.String(32))  # 结案方式：单次结案、月度结案、季度结案、半年度结案
    application_start_date = db.Column(db.Date)  # 活动申请周期-开始日期
    application_end_date = db.Column(db.Date)  # 活动申请周期-结束日期
    cost_share_ratio = db.Column(db.Float)  # 费用分摊比例
    customer_signature = db.Column(db.String(32))  # 客户签收：手写签收、拍照签收
    status = db.Column(db.String(32), default='active')  # 活动状态：active/inactive/draft
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_activities', lazy='select')
    reports = db.relationship('ActivityReport', backref='activity', lazy='dynamic')
    applications = db.relationship('ActivityApplication', backref='activity', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Activity, self).__init__(**kwargs)
        if not self.activity_code:
            # 生成活动编码：ACT + 时间戳 + 4位随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(uuid.uuid4().int)[:4]
            self.activity_code = f'ACT{timestamp}{random_suffix}'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'activity_code': self.activity_code,
            'name': self.name,
            'activity_type': self.activity_type,
            'execution_start_date': self.execution_start_date.isoformat() if self.execution_start_date else None,
            'execution_end_date': self.execution_end_date.isoformat() if self.execution_end_date else None,
            'description': self.description,
            'require_application': self.require_application,
            'customer_scope': self.customer_scope,
            'product_scope': self.product_scope,
            'payment_method': self.payment_method,
            'settlement_method': self.settlement_method,
            'application_start_date': self.application_start_date.isoformat() if self.application_start_date else None,
            'application_end_date': self.application_end_date.isoformat() if self.application_end_date else None,
            'cost_share_ratio': self.cost_share_ratio,
            'customer_signature': self.customer_signature,
            'status': self.status,
            'participant_count': self.reports.count(),
            'application_count': self.applications.count() if hasattr(self, 'applications') else 0,
            'created_by': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ActivityApplication(db.Model):
    """活动申请模型"""
    __tablename__ = 'activity_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)  # 活动ID
    customer_name = db.Column(db.String(128), nullable=False)  # 申请客户名称
    customer_type = db.Column(db.String(32))  # 客户类型：terminal/distributor/kol
    customer_id = db.Column(db.Integer)  # 客户ID
    application_status = db.Column(db.String(32), default='pending')  # 申请状态：pending/approved/rejected
    remark = db.Column(db.Text)  # 备注
    applied_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 申请人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    applicant = db.relationship('User', foreign_keys=[applied_by], backref='activity_applications', lazy='select')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'activity_name': self.activity.name if self.activity else None,
            'customer_name': self.customer_name,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'application_status': self.application_status,
            'remark': self.remark,
            'applied_by': self.applicant.name if self.applicant else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ActivityReport(db.Model):
    """活动上报记录模型"""
    __tablename__ = 'activity_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_order_no = db.Column(db.String(64), unique=True)  # 兑付单号
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)  # 活动ID
    application_no = db.Column(db.String(64))  # 申请单号
    customer_name = db.Column(db.String(128), nullable=False)  # 参与客户名称
    customer_code = db.Column(db.String(64))  # 客户编码
    customer_type = db.Column(db.String(32))  # 客户类型：terminal/distributor/kol
    customer_id = db.Column(db.Integer)  # 客户ID
    address = db.Column(db.String(256))  # 详细地址
    account_manager = db.Column(db.String(128))  # 客户经理
    display_photo = db.Column(db.String(512))  # 活动陈列照片
    location_photo = db.Column(db.String(512))  # 门店定位照片
    payment_photo = db.Column(db.String(512))  # 活动兑付照片
    signature_method = db.Column(db.String(32))  # 签收方式：手写签收、拍照签收
    signature_photo = db.Column(db.String(512))  # 签收照片
    report_status = db.Column(db.String(32), default='pending')  # 兑付状态：pending/approved/rejected
    remark = db.Column(db.Text)  # 备注
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上报人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reported_by], backref='activity_reports', lazy='select')
    
    def __init__(self, **kwargs):
        super(ActivityReport, self).__init__(**kwargs)
        if not self.payment_order_no:
            # 生成兑付单号：PAY + 时间戳 + 4位随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_suffix = str(uuid.uuid4().int)[:4]
            self.payment_order_no = f'PAY{timestamp}{random_suffix}'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'payment_order_no': self.payment_order_no,
            'activity_id': self.activity_id,
            'activity_name': self.activity.name if self.activity else None,
            'activity_code': self.activity.activity_code if self.activity else None,
            'application_no': self.application_no,
            'customer_name': self.customer_name,
            'customer_code': self.customer_code,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'address': self.address,
            'account_manager': self.account_manager,
            'execution_period': f"{self.activity.execution_start_date.strftime('%Y-%m-%d') if self.activity.execution_start_date else ''} ~ {self.activity.execution_end_date.strftime('%Y-%m-%d') if self.activity.execution_end_date else ''}" if self.activity else None,
            'display_photo': self.display_photo,
            'location_photo': self.location_photo,
            'payment_photo': self.payment_photo,
            'signature_method': self.signature_method,
            'signature_photo': self.signature_photo,
            'report_status': self.report_status,
            'remark': self.remark,
            'reported_by': self.reporter.name if self.reporter else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
