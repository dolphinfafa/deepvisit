from app import db
from datetime import datetime

class SalesOrder(db.Model):
    """销售订单模型"""
    __tablename__ = 'sales_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)  # 订单编号
    customer_type = db.Column(db.String(32), nullable=False)  # 客户类型
    customer_id = db.Column(db.Integer, nullable=False)  # 客户ID
    customer_name = db.Column(db.String(128))  # 客户名称
    warehouse = db.Column(db.String(64))  # 发货仓库
    total_amount = db.Column(db.Float, default=0)  # 总金额
    discount_amount = db.Column(db.Float, default=0)  # 优惠金额
    final_amount = db.Column(db.Float, default=0)  # 最终金额
    items = db.Column(db.Text)  # JSON格式存储订单明细
    order_date = db.Column(db.DateTime, default=datetime.utcnow)  # 下单时间
    delivery_date = db.Column(db.Date)  # 交货日期
    status = db.Column(db.String(32), default='pending')  # pending/approved/rejected/delivered
    approval_status = db.Column(db.String(32), default='pending')  # 审批状态
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 业务员
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='sales_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'status': self.status,
            'approval_status': self.approval_status,
            'salesman': self.salesman.name if self.salesman else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ReturnOrder(db.Model):
    """退货订单模型"""
    __tablename__ = 'return_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)
    customer_type = db.Column(db.String(32), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(128))
    warehouse = db.Column(db.String(64))
    total_amount = db.Column(db.Float, default=0)
    items = db.Column(db.Text)  # JSON格式存储退货明细
    return_reason = db.Column(db.Text)  # 退货原因
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32), default='pending')
    approval_status = db.Column(db.String(32), default='pending')
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='return_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'return_reason': self.return_reason,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'status': self.status,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DeliveryOrder(db.Model):
    """发货订单模型"""
    __tablename__ = 'delivery_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))  # 关联销售订单
    customer_name = db.Column(db.String(128))
    warehouse = db.Column(db.String(64))
    total_amount = db.Column(db.Float, default=0)
    items = db.Column(db.Text)  # JSON格式存储发货明细
    delivery_date = db.Column(db.Date)
    status = db.Column(db.String(32), default='pending')  # pending/confirmed/shipped
    receipt_image = db.Column(db.String(256))  # 接收清单图片
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sales_order = db.relationship('SalesOrder', backref='delivery_orders')
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='delivery_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_name': self.customer_name,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

