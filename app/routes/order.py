from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.order import SalesOrder, ReturnOrder, DeliveryOrder
from datetime import datetime
import random

bp = Blueprint('order', __name__, url_prefix='/order')

def generate_order_no(prefix='SO'):
    """生成订单编号"""
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return f'{prefix}{date_str}{random_str}'

# ========== 销售订单 ==========
@bp.route('/sales')
@login_required
def sales_list():
    """销售订单列表页面"""
    return render_template('order/sales.html')

@bp.route('/api/sales/list')
@login_required
def get_sales_list():
    """获取销售订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    
    query = SalesOrder.query
    
    if status:
        query = query.filter(SalesOrder.status == status)
    
    pagination = query.order_by(SalesOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/sales/create', methods=['POST'])
@login_required
def create_sales():
    """创建销售订单"""
    data = request.get_json()
    
    order = SalesOrder(
        order_no=generate_order_no('SO'),
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name'),
        warehouse=data.get('warehouse'),
        total_amount=data.get('total_amount', 0),
        final_amount=data.get('final_amount', 0),
        items=data.get('items'),
        salesman_id=data.get('salesman_id', current_user.id),
        created_by=current_user.id
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': order.to_dict()})

# ========== 退货订单 ==========
@bp.route('/return')
@login_required
def return_list():
    """退货订单列表页面"""
    return render_template('order/return.html')

@bp.route('/api/return/list')
@login_required
def get_return_list():
    """获取退货订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = ReturnOrder.query.order_by(ReturnOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/return/create', methods=['POST'])
@login_required
def create_return():
    """创建退货订单"""
    data = request.get_json()
    
    order = ReturnOrder(
        order_no=generate_order_no('RO'),
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name'),
        warehouse=data.get('warehouse'),
        total_amount=data.get('total_amount', 0),
        items=data.get('items'),
        return_reason=data.get('return_reason'),
        salesman_id=data.get('salesman_id', current_user.id),
        created_by=current_user.id
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': order.to_dict()})

# ========== 发货订单 ==========
@bp.route('/delivery')
@login_required
def delivery_list():
    """发货订单列表页面"""
    return render_template('order/delivery.html')

@bp.route('/api/delivery/list')
@login_required
def get_delivery_list():
    """获取发货订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = DeliveryOrder.query.order_by(DeliveryOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

