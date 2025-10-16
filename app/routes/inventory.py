from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.product import Product
from app.models.inventory import Inventory

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

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
    warehouse = request.args.get('warehouse', '')
    
    query = Inventory.query
    
    if warehouse:
        query = query.filter(Inventory.warehouse == warehouse)
    
    pagination = query.order_by(Inventory.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

