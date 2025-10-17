from app import db
from datetime import datetime
import json

class PurchaseOrder(db.Model):
    """采购入库单模型"""
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False)  # 采购单号
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)  # 供应商ID
    supplier_name = db.Column(db.String(128))  # 供应商名称
    purchase_document = db.Column(db.String(256))  # 采购单据文件路径
    document_date = db.Column(db.Date, nullable=False)  # 单据日期
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)  # 入库仓库ID
    warehouse_name = db.Column(db.String(128))  # 入库仓库名称
    handler = db.Column(db.String(64), nullable=False)  # 经办人
    items = db.Column(db.Text)  # JSON格式存储采购商品清单
    total_amount = db.Column(db.Float, default=0)  # 总金额
    status = db.Column(db.String(32), default='draft')  # draft/pending/approved/rejected/completed/cancelled
    approval_status = db.Column(db.String(32), default='pending')  # pending/approved/rejected
    approval_comment = db.Column(db.Text)  # 审批意见
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 审批人
    approved_at = db.Column(db.DateTime)  # 审批时间
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    supplier = db.relationship('Supplier', backref='purchase_orders')
    warehouse = db.relationship('Warehouse', backref='purchase_orders')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_purchase_orders')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_purchase_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'purchase_document': self.purchase_document,
            'document_date': self.document_date.isoformat() if self.document_date else None,
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.warehouse_name,
            'handler': self.handler,
            'items': json.loads(self.items) if self.items else [],
            'total_amount': self.total_amount,
            'status': self.status,
            'approval_status': self.approval_status,
            'approval_comment': self.approval_comment,
            'approved_by': self.approver.name if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

