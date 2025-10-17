from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.order import SalesOrder, ReturnOrder, DeliveryOrder
from app.models.customer import Terminal, DirectDistributor, KOL
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.warehouse import Warehouse
from app.models.user import User
from datetime import datetime
import random
import json

bp = Blueprint('order', __name__, url_prefix='/order')

def generate_order_no(prefix='SO'):
    """生成订单编号"""
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return f'{prefix}{date_str}{random_str}'

def generate_delivery_no():
    """生成发货单号"""
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return f'DO{date_str}{random_str}'

def create_delivery_order_from_sales(sales_order):
    """从销售订单创建发货订单"""
    delivery_order = DeliveryOrder(
        order_no=generate_delivery_no(),
        sales_order_id=sales_order.id,
        sales_order_no=sales_order.order_no,
        customer_name=sales_order.customer_name,
        receiver_address=sales_order.receiver_address,
        warehouse=sales_order.warehouse,
        total_amount=sales_order.final_amount,
        items=sales_order.items,
        order_date=sales_order.order_date,
        delivery_date=sales_order.delivery_date,
        status='pending',
        salesman_id=sales_order.salesman_id
    )
    
    db.session.add(delivery_order)
    return delivery_order

# ========== 销售订单 ==========
@bp.route('/sales')
@login_required
def sales_list():
    """销售订单列表页面"""
    return render_template('order/sales.html')

@bp.route('/sales/create')
@login_required
def sales_create():
    """销售订单创建页面"""
    return render_template('order/sales_create.html')

@bp.route('/api/sales/list')
@login_required
def get_sales_list():
    """获取销售订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = SalesOrder.query
    
    if status:
        query = query.filter(SalesOrder.status == status)
    
    if search:
        query = query.filter(
            db.or_(
                SalesOrder.order_no.like(f'%{search}%'),
                SalesOrder.customer_name.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(SalesOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })

@bp.route('/api/sales/create', methods=['POST'])
@login_required
def create_sales():
    """创建销售订单"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['customer_type', 'customer_id', 'warehouse', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'缺少必填字段: {field}'})
        
        # 计算总金额
        total_amount = 0
        items = data.get('items', [])
        for item in items:
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            total_amount += quantity * price
        
        # 获取客户信息
        customer_name = ''
        receiver_address = ''
        if data.get('customer_type') == 'terminal':
            customer = Terminal.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        elif data.get('customer_type') == 'distributor':
            customer = DirectDistributor.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        elif data.get('customer_type') == 'kol':
            customer = KOL.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        
        order = SalesOrder(
            order_no=generate_order_no('SO'),
            customer_type=data.get('customer_type'),
            customer_id=data.get('customer_id'),
            customer_name=customer_name,
            receiver_address=receiver_address,
            warehouse=data.get('warehouse'),
            total_amount=total_amount,
            discount_amount=data.get('discount_amount', 0),
            final_amount=total_amount - data.get('discount_amount', 0),
            items=json.dumps(items, ensure_ascii=False),
            delivery_date=datetime.strptime(data.get('delivery_date'), '%Y-%m-%d').date() if data.get('delivery_date') else None,
            status='draft',
            approval_status='pending',
            salesman_id=current_user.id,
            created_by=current_user.id
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '订单创建成功', 'data': order.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建失败: {str(e)}'})

@bp.route('/api/sales/submit/<int:order_id>', methods=['POST'])
@login_required
def submit_sales_order(order_id):
    """提交订单审批"""
    try:
        order = SalesOrder.query.get_or_404(order_id)
        
        if order.status != 'draft':
            return jsonify({'success': False, 'message': '只能提交草稿状态的订单'})
        
        order.status = 'pending'
        order.approval_status = 'pending'
        db.session.commit()
        
        return jsonify({'success': True, 'message': '订单提交成功，等待审批'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'提交失败: {str(e)}'})

@bp.route('/api/sales/approve/<int:order_id>', methods=['POST'])
@login_required
def approve_sales_order(order_id):
    """审批订单"""
    try:
        data = request.get_json()
        order = SalesOrder.query.get_or_404(order_id)
        
        if order.status != 'pending':
            return jsonify({'success': False, 'message': '只能审批待审批状态的订单'})
        
        action = data.get('action')  # approve/reject
        comment = data.get('comment', '')
        
        if action == 'approve':
            order.status = 'approved'
            order.approval_status = 'approved'
            
            # 自动生成发货订单
            delivery_order = create_delivery_order_from_sales(order)
            
        elif action == 'reject':
            order.status = 'rejected'
            order.approval_status = 'rejected'
        else:
            return jsonify({'success': False, 'message': '无效的审批操作'})
        
        order.approval_comment = comment
        order.approved_by = current_user.id
        order.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        message = f'订单{action == "approve" and "审批通过" or "审批拒绝"}'
        if action == 'approve':
            message += f'，已自动生成发货订单：{delivery_order.order_no}'
        
        return jsonify({'success': True, 'message': message})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'审批失败: {str(e)}'})

@bp.route('/api/sales/<int:order_id>')
@login_required
def get_sales_order(order_id):
    """获取订单详情"""
    order = SalesOrder.query.get_or_404(order_id)
    return jsonify({'success': True, 'data': order.to_dict()})

@bp.route('/api/customers/<customer_type>')
@login_required
def get_customers(customer_type):
    """获取客户列表"""
    customers = []
    if customer_type == 'terminal':
        customers = Terminal.query.filter_by(approval_status='approved').all()
    elif customer_type == 'distributor':
        customers = DirectDistributor.query.filter_by(approval_status='approved').all()
    elif customer_type == 'kol':
        customers = KOL.query.all()
    
    return jsonify({
        'success': True,
        'data': [customer.to_dict() for customer in customers]
    })

@bp.route('/api/products')
@login_required
def get_products():
    """获取商品列表"""
    products = Product.query.filter_by(is_active=True).all()
    return jsonify({
        'success': True,
        'data': [product.to_dict() for product in products]
    })

@bp.route('/api/inventory/<warehouse>')
@login_required
def get_inventory(warehouse):
    """获取指定仓库的库存"""
    inventory = Inventory.query.filter_by(warehouse=warehouse).all()
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in inventory]
    })

# ========== 退货订单 ==========
@bp.route('/return')
@login_required
def return_list():
    """退货订单列表页面"""
    return render_template('order/return.html')

@bp.route('/return/create')
@login_required
def return_create():
    """退货订单创建页面"""
    return render_template('order/return_create.html')

@bp.route('/api/return/list')
@login_required
def get_return_list():
    """获取退货订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = ReturnOrder.query
    
    if status:
        query = query.filter(ReturnOrder.status == status)
    
    if search:
        query = query.filter(
            db.or_(
                ReturnOrder.order_no.like(f'%{search}%'),
                ReturnOrder.customer_name.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(ReturnOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })

@bp.route('/api/return/create', methods=['POST'])
@login_required
def create_return():
    """创建退货订单"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['return_type', 'customer_type', 'customer_id', 'warehouse', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'缺少必填字段: {field}'})
        
        # 计算总金额
        total_amount = 0
        items = data.get('items', [])
        for item in items:
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            total_amount += quantity * price
        
        # 获取客户信息
        customer_name = ''
        receiver_address = ''
        if data.get('customer_type') == 'terminal':
            customer = Terminal.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        elif data.get('customer_type') == 'distributor':
            customer = DirectDistributor.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        elif data.get('customer_type') == 'kol':
            customer = KOL.query.get(data.get('customer_id'))
            if customer:
                customer_name = customer.name
                receiver_address = customer.receiver_address or ''
        
        order = ReturnOrder(
            order_no=generate_order_no('RO'),
            return_type=data.get('return_type'),
            sales_order_id=data.get('sales_order_id'),
            customer_type=data.get('customer_type'),
            customer_id=data.get('customer_id'),
            customer_name=customer_name,
            receiver_address=receiver_address,
            warehouse=data.get('warehouse'),
            total_amount=total_amount,
            items=json.dumps(items, ensure_ascii=False),
            return_reason=data.get('return_reason', ''),
            status='draft',
            approval_status='pending',
            salesman_id=current_user.id,
            created_by=current_user.id
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '退货订单创建成功', 'data': order.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建失败: {str(e)}'})

@bp.route('/api/return/submit/<int:order_id>', methods=['POST'])
@login_required
def submit_return_order(order_id):
    """提交退货订单审批"""
    try:
        order = ReturnOrder.query.get_or_404(order_id)
        
        if order.status != 'draft':
            return jsonify({'success': False, 'message': '只能提交草稿状态的订单'})
        
        order.status = 'pending'
        order.approval_status = 'pending'
        db.session.commit()
        
        return jsonify({'success': True, 'message': '退货订单提交成功，等待审批'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'提交失败: {str(e)}'})

@bp.route('/api/return/approve/<int:order_id>', methods=['POST'])
@login_required
def approve_return_order(order_id):
    """审批退货订单"""
    try:
        data = request.get_json()
        order = ReturnOrder.query.get_or_404(order_id)
        
        if order.status != 'pending':
            return jsonify({'success': False, 'message': '只能审批待审批状态的订单'})
        
        action = data.get('action')  # approve/reject
        comment = data.get('comment', '')
        
        if action == 'approve':
            order.status = 'approved'
            order.approval_status = 'approved'
        elif action == 'reject':
            order.status = 'rejected'
            order.approval_status = 'rejected'
        else:
            return jsonify({'success': False, 'message': '无效的审批操作'})
        
        order.approval_comment = comment
        order.approved_by = current_user.id
        order.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'退货订单{action == "approve" and "审批通过" or "审批拒绝"}'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'审批失败: {str(e)}'})

@bp.route('/api/return/<int:order_id>')
@login_required
def get_return_order(order_id):
    """获取退货订单详情"""
    order = ReturnOrder.query.get_or_404(order_id)
    return jsonify({'success': True, 'data': order.to_dict()})

@bp.route('/api/sales-orders/<customer_type>/<int:customer_id>')
@login_required
def get_customer_sales_orders(customer_type, customer_id):
    """获取客户的销售订单列表"""
    query = SalesOrder.query.filter_by(
        customer_type=customer_type,
        customer_id=customer_id,
        status='approved'
    )
    
    orders = query.order_by(SalesOrder.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': [order.to_dict() for order in orders]
    })

@bp.route('/api/return/confirm/<int:order_id>', methods=['POST'])
@login_required
def confirm_return_order(order_id):
    """确认退货订单（上传接收凭证）"""
    try:
        data = request.get_json()
        order = ReturnOrder.query.get_or_404(order_id)
        
        if order.status != 'approved':
            return jsonify({'success': False, 'message': '只能确认已审批的退货订单'})
        
        receive_voucher = data.get('receive_voucher', '')
        receive_comment = data.get('receive_comment', '')
        
        if not receive_voucher:
            return jsonify({'success': False, 'message': '请上传退货接收凭证'})
        
        # 更新库存 - 增加库存（退货入库）
        items = json.loads(order.items) if order.items else []
        for item in items:
            # 查找对应的仓库
            warehouse = Warehouse.query.filter_by(name=order.warehouse).first()
            if warehouse:
                Inventory.update_stock(
                    warehouse_id=warehouse.id,
                    product_id=item['product_id'],
                    quantity_change=item['quantity']  # 正数表示增加库存
                )
        
        order.status = 'confirmed'
        order.receive_voucher = receive_voucher
        order.receive_comment = receive_comment
        order.received_by = current_user.id
        order.received_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '退货确认成功', 'data': order.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'确认失败: {str(e)}'})

@bp.route('/api/return/upload-voucher', methods=['POST'])
@login_required
def upload_return_voucher():
    """上传退货接收凭证"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有上传文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        if file:
            # 这里可以实现文件上传逻辑，暂时返回模拟路径
            import uuid
            filename = f"return_voucher_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
            file_path = f"/uploads/return_vouchers/{filename}"
            
            # 在实际项目中，这里应该保存文件到服务器
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return jsonify({
                'success': True, 
                'message': '文件上传成功', 
                'file_path': file_path,
                'filename': filename
            })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})

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
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = DeliveryOrder.query
    
    if status:
        query = query.filter(DeliveryOrder.status == status)
    
    if search:
        query = query.filter(
            db.or_(
                DeliveryOrder.order_no.like(f'%{search}%'),
                DeliveryOrder.sales_order_no.like(f'%{search}%'),
                DeliveryOrder.customer_name.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(DeliveryOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })

@bp.route('/api/delivery/<int:order_id>')
@login_required
def get_delivery_order(order_id):
    """获取发货订单详情"""
    order = DeliveryOrder.query.get_or_404(order_id)
    return jsonify({'success': True, 'data': order.to_dict()})

@bp.route('/api/delivery/ship/<int:order_id>', methods=['POST'])
@login_required
def ship_delivery_order(order_id):
    """发货确认（提交出库凭证）"""
    try:
        data = request.get_json()
        order = DeliveryOrder.query.get_or_404(order_id)
        
        if order.status != 'pending':
            return jsonify({'success': False, 'message': '只能对待发货状态的订单进行发货确认'})
        
        outbound_voucher = data.get('outbound_voucher', '')
        outbound_comment = data.get('outbound_comment', '')
        
        if not outbound_voucher:
            return jsonify({'success': False, 'message': '请上传出库凭证'})
        
        # 更新库存 - 减少库存
        items = json.loads(order.items) if order.items else []
        for item in items:
            # 查找对应的仓库
            warehouse = Warehouse.query.filter_by(name=order.warehouse).first()
            if warehouse:
                Inventory.update_stock(
                    warehouse_id=warehouse.id,
                    product_id=item['product_id'],
                    quantity_change=-item['quantity']  # 负数表示减少库存
                )
        
        order.status = 'shipped'
        order.outbound_voucher = outbound_voucher
        order.outbound_comment = outbound_comment
        order.shipped_by = current_user.id
        order.shipped_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '发货确认成功', 'data': order.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'发货确认失败: {str(e)}'})

@bp.route('/api/delivery/complete/<int:order_id>', methods=['POST'])
@login_required
def complete_delivery_order(order_id):
    """完成发货订单"""
    try:
        order = DeliveryOrder.query.get_or_404(order_id)
        
        if order.status != 'shipped':
            return jsonify({'success': False, 'message': '只能完成已发货的订单'})
        
        order.status = 'completed'
        db.session.commit()
        
        return jsonify({'success': True, 'message': '发货订单完成', 'data': order.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'完成订单失败: {str(e)}'})

@bp.route('/api/delivery/upload-voucher', methods=['POST'])
@login_required
def upload_delivery_voucher():
    """上传出库凭证"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有上传文件'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'})
        
        if file:
            # 这里可以实现文件上传逻辑，暂时返回模拟路径
            import uuid
            filename = f"delivery_voucher_{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
            file_path = f"/uploads/delivery_vouchers/{filename}"
            
            # 在实际项目中，这里应该保存文件到服务器
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return jsonify({
                'success': True, 
                'message': '文件上传成功', 
                'file_path': file_path,
                'filename': filename
            })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})

