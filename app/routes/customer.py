from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.customer import Terminal, DirectDistributor, KOL, CustomerContact
from datetime import datetime

bp = Blueprint('customer', __name__, url_prefix='/customer')

# ========== 终端客户 ==========
@bp.route('/terminal')
@login_required
def terminal_list():
    """终端客户列表页面"""
    return render_template('customer/terminal.html')

@bp.route('/api/terminal/list')
@login_required
def get_terminal_list():
    """获取终端客户列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Terminal.query
    
    if search:
        query = query.filter(
            (Terminal.name.like(f'%{search}%')) |
            (Terminal.code.like(f'%{search}%')) |
            (Terminal.phone.like(f'%{search}%'))
        )
    
    if status:
        query = query.filter(Terminal.approval_status == status)
    
    pagination = query.order_by(Terminal.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page
    })

@bp.route('/api/terminal/create', methods=['POST'])
@login_required
def create_terminal():
    """创建终端客户"""
    data = request.get_json()
    
    terminal = Terminal(
        code=data.get('code'),
        name=data.get('name'),
        type=data.get('type'),
        level=data.get('level'),
        visit_frequency=data.get('visit_frequency'),
        manager_id=data.get('manager_id'),
        phone=data.get('phone'),
        address=data.get('address'),
        cooperation_status=data.get('cooperation_status', '合作中'),
        created_by=current_user.id
    )
    
    db.session.add(terminal)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': terminal.to_dict()})

@bp.route('/api/terminal/<int:id>', methods=['GET'])
@login_required
def get_terminal(id):
    """获取终端客户详情"""
    terminal = Terminal.query.get_or_404(id)
    return jsonify({'success': True, 'data': terminal.to_dict()})

@bp.route('/api/terminal/<int:id>', methods=['PUT'])
@login_required
def update_terminal(id):
    """更新终端客户"""
    terminal = Terminal.query.get_or_404(id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(terminal, key):
            setattr(terminal, key, value)
    
    db.session.commit()
    return jsonify({'success': True, 'message': '更新成功', 'data': terminal.to_dict()})

@bp.route('/api/terminal/<int:id>', methods=['DELETE'])
@login_required
def delete_terminal(id):
    """删除终端客户"""
    terminal = Terminal.query.get_or_404(id)
    db.session.delete(terminal)
    db.session.commit()
    return jsonify({'success': True, 'message': '删除成功'})

# ========== 直营商 ==========
@bp.route('/distributor')
@login_required
def distributor_list():
    """直营商列表页面"""
    return render_template('customer/distributor.html')

@bp.route('/api/distributor/list')
@login_required
def get_distributor_list():
    """获取直营商列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = DirectDistributor.query
    
    if search:
        query = query.filter(
            (DirectDistributor.name.like(f'%{search}%')) |
            (DirectDistributor.code.like(f'%{search}%'))
        )
    
    pagination = query.order_by(DirectDistributor.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/distributor/create', methods=['POST'])
@login_required
def create_distributor():
    """创建直营商"""
    data = request.get_json()
    
    distributor = DirectDistributor(
        code=data.get('code'),
        name=data.get('name'),
        type=data.get('type'),
        level=data.get('level'),
        manager_id=data.get('manager_id'),
        phone=data.get('phone'),
        address=data.get('address'),
        created_by=current_user.id
    )
    
    db.session.add(distributor)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': distributor.to_dict()})

# ========== KOL ==========
@bp.route('/kol')
@login_required
def kol_list():
    """KOL列表页面"""
    return render_template('customer/kol.html')

@bp.route('/api/kol/list')
@login_required
def get_kol_list():
    """获取KOL列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = KOL.query
    
    if search:
        query = query.filter(
            (KOL.name.like(f'%{search}%')) |
            (KOL.code.like(f'%{search}%'))
        )
    
    pagination = query.order_by(KOL.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/kol/create', methods=['POST'])
@login_required
def create_kol():
    """创建KOL"""
    data = request.get_json()
    
    kol = KOL(
        code=data.get('code'),
        name=data.get('name'),
        phone=data.get('phone'),
        company=data.get('company'),
        profession=data.get('profession'),
        manager_id=data.get('manager_id'),
        created_by=current_user.id
    )
    
    db.session.add(kol)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': kol.to_dict()})

# ========== 客户联系人 ==========
@bp.route('/contact')
@login_required
def contact_list():
    """客户联系人列表页面"""
    return render_template('customer/contact.html')

@bp.route('/api/contact/list')
@login_required
def get_contact_list():
    """获取客户联系人列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = CustomerContact.query.order_by(CustomerContact.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/contact/create', methods=['POST'])
@login_required
def create_contact():
    """创建客户联系人"""
    data = request.get_json()
    
    contact = CustomerContact(
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        name=data.get('name'),
        phone=data.get('phone'),
        is_primary=data.get('is_primary', False),
        position=data.get('position')
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': contact.to_dict()})

