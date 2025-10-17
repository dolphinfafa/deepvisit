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
    visitor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 客户经理
    customer_list = db.Column(db.Text)  # JSON格式存储客户列表
    route_details = db.Column(db.Text)  # 路线详情（JSON格式存储路线顺序、距离等信息）
    remark = db.Column(db.Text)  # 备注
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态: pending/approved/rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审批人
    approved_at = db.Column(db.DateTime)  # 审批时间
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], backref='visit_routes')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_routes')
    
    def to_dict(self):
        import json
        customer_list = []
        route_details = {}
        
        try:
            if self.customer_list:
                customer_list = json.loads(self.customer_list)
            if self.route_details:
                route_details = json.loads(self.route_details)
        except (json.JSONDecodeError, TypeError):
            pass
            
        return {
            'id': self.id,
            'name': self.name,
            'visitor': self.visitor.name if self.visitor else None,
            'visitor_id': self.visitor_id,
            'customer_list': customer_list,
            'route_details': route_details,
            'remark': self.remark,
            'approval_status': self.approval_status,
            'approved_by': self.approver.name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
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
    customer_address = db.Column(db.String(255))  # 客户地址
    visit_frequency = db.Column(db.String(32))  # 拜访频率
    visit_type = db.Column(db.String(32))  # planned/temporary
    
    # 拜访内容
    visit_content = db.Column(db.Text)  # 拜访内容
    
    # 到场签到
    checkin_time = db.Column(db.DateTime)  # 签到时间
    checkin_latitude = db.Column(db.Float)  # 签到纬度
    checkin_longitude = db.Column(db.Float)  # 签到经度
    checkin_address = db.Column(db.String(255))  # 签到地点
    
    # 离开签到
    checkout_time = db.Column(db.DateTime)  # 签退时间
    checkout_latitude = db.Column(db.Float)
    checkout_longitude = db.Column(db.Float)
    checkout_address = db.Column(db.String(255))  # 签退地点
    
    # 铺货上报
    product_distribution_list = db.Column(db.Text)  # JSON格式存储商品铺货清单
    distribution_photos = db.Column(db.Text)  # JSON格式存储铺货现场照片
    distribution_remark = db.Column(db.Text)  # 铺货备注
    
    # 库存上报
    inventory_list = db.Column(db.Text)  # JSON格式存储商品库存清单
    inventory_photos = db.Column(db.Text)  # JSON格式存储库存现场照片
    inventory_remark = db.Column(db.Text)  # 库存备注
    
    # 竞品上报
    competitor_list = db.Column(db.Text)  # JSON格式存储竞品清单
    competitor_photos = db.Column(db.Text)  # JSON格式存储竞品现场照片
    competitor_remark = db.Column(db.Text)  # 竞品备注
    
    # 其他照片
    photos = db.Column(db.Text)  # JSON格式存储其他照片
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], backref='visit_records')
    plan = db.relationship('VisitPlan', backref='records')
    
    def to_dict(self):
        import json
        
        # 解析JSON字段
        product_distribution_list = []
        distribution_photos = []
        inventory_list = []
        inventory_photos = []
        competitor_list = []
        competitor_photos = []
        photos = []
        
        try:
            if self.product_distribution_list:
                product_distribution_list = json.loads(self.product_distribution_list)
            if self.distribution_photos:
                distribution_photos = json.loads(self.distribution_photos)
            if self.inventory_list:
                inventory_list = json.loads(self.inventory_list)
            if self.inventory_photos:
                inventory_photos = json.loads(self.inventory_photos)
            if self.competitor_list:
                competitor_list = json.loads(self.competitor_list)
            if self.competitor_photos:
                competitor_photos = json.loads(self.competitor_photos)
            if self.photos:
                photos = json.loads(self.photos)
        except (json.JSONDecodeError, TypeError):
            pass
        
        return {
            'id': self.id,
            'visitor': self.visitor.name if self.visitor else None,
            'visitor_id': self.visitor_id,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'visit_frequency': self.visit_frequency,
            'visit_type': self.visit_type,
            'visit_content': self.visit_content,
            'checkin_time': self.checkin_time.isoformat() if self.checkin_time else None,
            'checkin_address': self.checkin_address,
            'checkout_time': self.checkout_time.isoformat() if self.checkout_time else None,
            'checkout_address': self.checkout_address,
            'product_distribution_list': product_distribution_list,
            'distribution_photos': distribution_photos,
            'distribution_remark': self.distribution_remark,
            'inventory_list': inventory_list,
            'inventory_photos': inventory_photos,
            'inventory_remark': self.inventory_remark,
            'competitor_list': competitor_list,
            'competitor_photos': competitor_photos,
            'competitor_remark': self.competitor_remark,
            'photos': photos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

