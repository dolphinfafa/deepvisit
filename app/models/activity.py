from app import db
from datetime import datetime

class Activity(db.Model):
    """活动模型"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # 活动名称
    description = db.Column(db.Text)  # 活动描述
    status = db.Column(db.String(32), default='active')  # 活动状态：active/inactive
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_activities')
    reports = db.relationship('ActivityReport', backref='activity', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'participant_count': self.reports.count(),
            'created_by': self.creator.name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ActivityReport(db.Model):
    """活动上报记录模型"""
    __tablename__ = 'activity_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)  # 活动ID
    customer_name = db.Column(db.String(128), nullable=False)  # 参与客户名称
    customer_type = db.Column(db.String(32))  # 客户类型：terminal/distributor/kol
    customer_id = db.Column(db.Integer)  # 客户ID
    display_photo = db.Column(db.String(512))  # 活动陈列照片
    location_photo = db.Column(db.String(512))  # 门店定位照片
    payment_photo = db.Column(db.String(512))  # 活动兑付照片
    report_status = db.Column(db.String(32), default='pending')  # 上报状态：pending/approved/rejected
    remark = db.Column(db.Text)  # 备注
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上报人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    reporter = db.relationship('User', foreign_keys=[reported_by], backref='activity_reports')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'activity_name': self.activity.name if self.activity else None,
            'customer_name': self.customer_name,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'display_photo': self.display_photo,
            'location_photo': self.location_photo,
            'payment_photo': self.payment_photo,
            'report_status': self.report_status,
            'remark': self.remark,
            'reported_by': self.reporter.name if self.reporter else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
