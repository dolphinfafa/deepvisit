from app import db
from datetime import datetime
import json

class SalesOrder(db.Model):
    """销售订单模型"""
    __tablename__ = 'sales_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)  # 订单编号
    customer_type = db.Column(db.String(32), nullable=False)  # 客户类型: terminal/distributor/kol
    customer_id = db.Column(db.Integer, nullable=False)  # 客户ID
    customer_name = db.Column(db.String(128))  # 客户名称
    receiver_address = db.Column(db.String(256))  # 收货地址
    warehouse = db.Column(db.String(64))  # 发货仓库
    total_amount = db.Column(db.Float, default=0)  # 总金额
    discount_amount = db.Column(db.Float, default=0)  # 优惠金额
    final_amount = db.Column(db.Float, default=0)  # 最终金额
    items = db.Column(db.Text)  # JSON格式存储订单明细
    order_date = db.Column(db.DateTime, default=datetime.utcnow)  # 下单时间
    delivery_date = db.Column(db.Date)  # 交货日期
    status = db.Column(db.String(32), default='draft')  # draft/pending/approved/rejected/delivered/cancelled
    approval_status = db.Column(db.String(32), default='pending')  # pending/approved/rejected
    approval_comment = db.Column(db.Text)  # 审批意见
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审批人
    approved_at = db.Column(db.DateTime)  # 审批时间
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 客户经理
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='sales_orders')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'receiver_address': self.receiver_address,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'discount_amount': self.discount_amount,
            'final_amount': self.final_amount,
            'items': json.loads(self.items) if self.items else [],
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'status': self.status,
            'approval_status': self.approval_status,
            'approval_comment': self.approval_comment,
            'approved_by': self.approver.name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'salesman': self.salesman.name if self.salesman else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ReturnOrder(db.Model):
    """退货订单模型"""
    __tablename__ = 'return_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)
    return_type = db.Column(db.String(32), nullable=False)  # 退货方式: sales_order/direct
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))  # 关联销售订单ID
    customer_type = db.Column(db.String(32), nullable=False)  # 客户类型: terminal/distributor/kol
    customer_id = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(128))
    receiver_address = db.Column(db.String(256))  # 收货地址
    warehouse = db.Column(db.String(64))  # 收货仓库
    total_amount = db.Column(db.Float, default=0)
    items = db.Column(db.Text)  # JSON格式存储退货明细
    return_reason = db.Column(db.Text)  # 退货原因
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32), default='draft')  # draft/pending/approved/rejected/shipped/confirmed/cancelled
    approval_status = db.Column(db.String(32), default='pending')  # pending/approved/rejected
    approval_comment = db.Column(db.Text)  # 审批意见
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审批人
    approved_at = db.Column(db.DateTime)  # 审批时间
    receive_voucher = db.Column(db.String(256))  # 退货接收凭证图片
    receive_comment = db.Column(db.Text)  # 接收备注
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 接收人
    received_at = db.Column(db.DateTime)  # 接收时间
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 业务员
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='return_orders')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_return_orders')
    receiver = db.relationship('User', foreign_keys=[received_by], backref='received_return_orders')
    sales_order = db.relationship('SalesOrder', backref='return_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'return_type': self.return_type,
            'sales_order_id': self.sales_order_id,
            'sales_order_no': self.sales_order.order_no if self.sales_order else None,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'receiver_address': self.receiver_address,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'items': json.loads(self.items) if self.items else [],
            'return_reason': self.return_reason,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'status': self.status,
            'approval_status': self.approval_status,
            'approval_comment': self.approval_comment,
            'approved_by': self.approver.name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'receive_voucher': self.receive_voucher,
            'receive_comment': self.receive_comment,
            'received_by': self.receiver.name if self.receiver else None,
            'received_at': self.received_at.isoformat() if self.received_at else None,
            'salesman': self.salesman.name if self.salesman else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DeliveryOrder(db.Model):
    """发货订单模型"""
    __tablename__ = 'delivery_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)  # 发货单号
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))  # 关联销售订单
    sales_order_no = db.Column(db.String(64))  # 订单编号
    customer_name = db.Column(db.String(128))  # 客户名称
    receiver_address = db.Column(db.String(256))  # 收货地址
    warehouse = db.Column(db.String(64))  # 发货仓库
    total_amount = db.Column(db.Float, default=0)  # 金额
    items = db.Column(db.Text)  # JSON格式存储发货商品清单
    order_date = db.Column(db.DateTime, default=datetime.utcnow)  # 下单时间
    delivery_date = db.Column(db.Date)  # 交货日期
    status = db.Column(db.String(32), default='pending')  # pending/shipped/completed
    outbound_voucher = db.Column(db.String(256))  # 出库凭证图片
    outbound_comment = db.Column(db.Text)  # 出库备注
    shipped_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 发货人
    shipped_at = db.Column(db.DateTime)  # 发货时间
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 业务员
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sales_order = db.relationship('SalesOrder', backref='delivery_orders')
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='delivery_orders')
    shipper = db.relationship('User', foreign_keys=[shipped_by], backref='shipped_delivery_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'sales_order_id': self.sales_order_id,
            'sales_order_no': self.sales_order_no,
            'customer_name': self.customer_name,
            'receiver_address': self.receiver_address,
            'warehouse': self.warehouse,
            'total_amount': self.total_amount,
            'items': json.loads(self.items) if self.items else [],
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'status': self.status,
            'outbound_voucher': self.outbound_voucher,
            'outbound_comment': self.outbound_comment,
            'shipped_by': self.shipper.name if self.shipper else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'salesman': self.salesman.name if self.salesman else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

