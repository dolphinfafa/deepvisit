from app import db
from datetime import datetime

class VisitPlan(db.Model):
    """拜访计划模型"""
    __tablename__ = 'visit_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 拜访人
    customer_type = db.Column(db.String(32), nullable=False)  # 客户类型
    customer_id = db.Column(db.Integer, nullable=False)  # 客户ID
    customer_name = db.Column(db.String(128))  # 客户名称
    visit_date = db.Column(db.Date, nullable=False)  # 拜访日期
    start_time = db.Column(db.Time)  # 开始时间
    end_time = db.Column(db.Time)  # 结束时间
    plan_content = db.Column(db.Text)  # 计划内容
    is_periodic = db.Column(db.Boolean, default=False)  # 是否周期性
    period_type = db.Column(db.String(32))  # 周期类型: daily/weekly/monthly
    status = db.Column(db.String(32), default='pending')  # pending/approved/rejected/completed
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], backref='visit_plans')
    
    def to_dict(self):
        return {
            'id': self.id,
            'visitor': self.visitor.name if self.visitor else None,
            'customer_name': self.customer_name,
            'visit_date': self.visit_date.isoformat() if self.visit_date else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'plan_content': self.plan_content,
            'status': self.status,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class VisitRoute(db.Model):
    """拜访路线模型"""
    __tablename__ = 'visit_routes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # 路线名称
    visitor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_list = db.Column(db.Text)  # JSON格式存储客户列表
    remark = db.Column(db.Text)
    approval_status = db.Column(db.String(32), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], backref='visit_routes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'visitor': self.visitor.name if self.visitor else None,
            'remark': self.remark,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class VisitRecord(db.Model):
    """拜访记录模型"""
    __tablename__ = 'visit_records'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('visit_plans.id'))  # 关联计划
    visitor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_type = db.Column(db.String(32), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(128))
    visit_type = db.Column(db.String(32))  # planned/temporary
    checkin_time = db.Column(db.DateTime)  # 签到时间
    checkin_latitude = db.Column(db.Float)  # 签到纬度
    checkin_longitude = db.Column(db.Float)  # 签到经度
    checkout_time = db.Column(db.DateTime)  # 签退时间
    checkout_latitude = db.Column(db.Float)
    checkout_longitude = db.Column(db.Float)
    visit_content = db.Column(db.Text)  # 拜访内容
    photos = db.Column(db.Text)  # JSON格式存储照片
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], backref='visit_records')
    plan = db.relationship('VisitPlan', backref='records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'visitor': self.visitor.name if self.visitor else None,
            'customer_name': self.customer_name,
            'visit_type': self.visit_type,
            'checkin_time': self.checkin_time.isoformat() if self.checkin_time else None,
            'checkout_time': self.checkout_time.isoformat() if self.checkout_time else None,
            'visit_content': self.visit_content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

