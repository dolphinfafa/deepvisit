from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.purchase_order import PurchaseOrder
from werkzeug.utils import secure_filename
import os
import uuid
import json
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# ========== 供应商管理 ==========
@bp.route('/supplier')
@login_required
def supplier_list():
    """供应商列表页面"""
    return render_template('inventory/supplier.html')

@bp.route('/api/supplier/list')
@login_required
def get_supplier_list():
    """获取供应商列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Supplier.query
    
    if search:
        query = query.filter(
            (Supplier.name.like(f'%{search}%')) |
            (Supplier.code.like(f'%{search}%'))
        )
    
    pagination = query.order_by(Supplier.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/supplier/create', methods=['POST'])
@login_required
def create_supplier():
    """创建供应商"""
    data = request.get_json()
    
    supplier = Supplier(
        code=data.get('code'),
        name=data.get('name'),
        contact_person=data.get('contact_person'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        tax_number=data.get('tax_number'),
        bank_account=data.get('bank_account'),
        bank_name=data.get('bank_name'),
        payment_terms=data.get('payment_terms'),
        credit_limit=data.get('credit_limit', 0)
    )
    
    db.session.add(supplier)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': supplier.to_dict()})

# ========== 仓库管理 ==========
@bp.route('/warehouse')
@login_required
def warehouse_list():
    """仓库列表页面"""
    return render_template('inventory/warehouse.html')

@bp.route('/api/warehouse/list')
@login_required
def get_warehouse_list():
    """获取仓库列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    warehouse_type = request.args.get('warehouse_type', '')
    
    query = Warehouse.query
    
    if warehouse_type:
        query = query.filter(Warehouse.warehouse_type == warehouse_type)
    
    pagination = query.order_by(Warehouse.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/warehouse/create', methods=['POST'])
@login_required
def create_warehouse():
    """创建仓库"""
    data = request.get_json()
    
    warehouse = Warehouse(
        code=data.get('code'),
        name=data.get('name'),
        warehouse_type=data.get('warehouse_type'),
        address=data.get('address'),
        manager=data.get('manager'),
        phone=data.get('phone'),
        capacity=data.get('capacity'),
        description=data.get('description')
    )
    
    db.session.add(warehouse)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': warehouse.to_dict()})

# ========== 采购入库单管理 ==========
@bp.route('/purchase')
@login_required
def purchase_list():
    """采购入库单列表页面"""
    return render_template('inventory/purchase.html')

@bp.route('/api/purchase/list')
@login_required
def get_purchase_list():
    """获取采购入库单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    
    query = PurchaseOrder.query
    
    if status:
        query = query.filter(PurchaseOrder.status == status)
    
    pagination = query.order_by(PurchaseOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/purchase/create', methods=['POST'])
@login_required
def create_purchase_order():
    """创建采购入库单"""
    data = request.get_json()
    
    # 生成采购单号
    order_no = f"CG{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    purchase_order = PurchaseOrder(
        order_no=order_no,
        supplier_id=data.get('supplier_id'),
        supplier_name=data.get('supplier_name'),
        purchase_document=data.get('purchase_document'),
        document_date=datetime.strptime(data.get('document_date'), '%Y-%m-%d').date(),
        warehouse_id=data.get('warehouse_id'),
        warehouse_name=data.get('warehouse_name'),
        handler=data.get('handler'),
        items=json.dumps(data.get('items', [])),
        total_amount=data.get('total_amount', 0),
        created_by=current_user.id
    )
    
    db.session.add(purchase_order)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': purchase_order.to_dict()})

@bp.route('/api/purchase/approve/<int:purchase_id>', methods=['POST'])
@login_required
def approve_purchase_order(purchase_id):
    """审批采购入库单"""
    data = request.get_json()
    purchase_order = PurchaseOrder.query.get_or_404(purchase_id)
    
    purchase_order.approval_status = data.get('approval_status')
    purchase_order.approval_comment = data.get('approval_comment')
    purchase_order.approved_by = current_user.id
    purchase_order.approved_at = datetime.utcnow()
    
    if data.get('approval_status') == 'approved':
        purchase_order.status = 'approved'
        # 更新库存
        items = json.loads(purchase_order.items) if purchase_order.items else []
        for item in items:
            Inventory.update_stock(
                warehouse_id=purchase_order.warehouse_id,
                product_id=item['product_id'],
                quantity_change=item['quantity'],
                cost=item.get('cost', 0)
            )
    else:
        purchase_order.status = 'rejected'
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': '审批完成'})

# ========== 商品管理 ==========
@bp.route('/product')
@login_required
def product_list():
    """商品列表页面"""
    return render_template('inventory/product.html')

@bp.route('/api/product/list')
@login_required
def get_product_list():
    """获取商品列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    
    if search:
        query = query.filter(
            (Product.name.like(f'%{search}%')) |
            (Product.code.like(f'%{search}%'))
        )
    
    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/product/create', methods=['POST'])
@login_required
def create_product():
    """创建商品"""
    data = request.get_json()
    
    product = Product(
        code=data.get('code'),
        name=data.get('name'),
        specification=data.get('specification'),
        unit=data.get('unit'),
        category=data.get('category'),
        brand=data.get('brand'),
        type=data.get('type', 'own'),
        price=data.get('price', 0),
        cost=data.get('cost', 0)
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': product.to_dict()})

# ========== 库存管理 ==========
@bp.route('/stock')
@login_required
def stock_list():
    """库存列表页面"""
    return render_template('inventory/stock.html')

@bp.route('/api/stock/list')
@login_required
def get_stock_list():
    """获取库存列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    warehouse_type = request.args.get('warehouse_type', '')
    warehouse_id = request.args.get('warehouse_id', '')
    
    query = Inventory.query
    
    if warehouse_type:
        query = query.filter(Inventory.warehouse_type == warehouse_type)
    
    if warehouse_id:
        query = query.filter(Inventory.warehouse_id == warehouse_id)
    
    pagination = query.order_by(Inventory.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/stock/summary')
@login_required
def get_stock_summary():
    """获取库存汇总信息"""
    warehouse_type = request.args.get('warehouse_type', '')
    
    query = Inventory.query
    if warehouse_type:
        query = query.filter(Inventory.warehouse_type == warehouse_type)
    
    inventories = query.all()
    
    # 按仓库分组统计
    warehouse_summary = {}
    for inv in inventories:
        warehouse_name = inv.warehouse_name
        if warehouse_name not in warehouse_summary:
            warehouse_summary[warehouse_name] = {
                'warehouse_name': warehouse_name,
                'warehouse_type': inv.warehouse_type,
                'product_count': 0,
                'total_quantity': 0,
                'total_value': 0
            }
        
        warehouse_summary[warehouse_name]['product_count'] += 1
        warehouse_summary[warehouse_name]['total_quantity'] += inv.quantity
        warehouse_summary[warehouse_name]['total_value'] += inv.total_cost
    
    return jsonify({
        'success': True,
        'data': list(warehouse_summary.values())
    })

# ========== 文件上传 ==========
@bp.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'})
    
    if file:
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # 确保上传目录存在
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'message': '上传成功',
            'file_path': f'/static/uploads/{unique_filename}'
        })
    
    return jsonify({'success': False, 'message': '上传失败'})

