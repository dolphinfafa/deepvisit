from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.role import Role

bp = Blueprint('system', __name__, url_prefix='/system')

# ========== 员工管理 ==========
@bp.route('/user')
@login_required
def user_list():
    """员工列表页面"""
    return render_template('system/user.html')

@bp.route('/api/user/list')
@login_required
def get_user_list():
    """获取员工列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.name.like(f'%{search}%')) |
            (User.username.like(f'%{search}%')) |
            (User.phone.like(f'%{search}%'))
        )
    
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/user/create', methods=['POST'])
@login_required
def create_user():
    """创建员工"""
    data = request.get_json()
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        name=data.get('name'),
        phone=data.get('phone'),
        department=data.get('department'),
        role_id=data.get('role_id')
    )
    user.set_password(data.get('password', '123456'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': user.to_dict()})

@bp.route('/api/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    """更新员工"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    for key, value in data.items():
        if key == 'password' and value:
            user.set_password(value)
        elif hasattr(user, key) and key != 'password_hash':
            setattr(user, key, value)
    
    db.session.commit()
    return jsonify({'success': True, 'message': '更新成功', 'data': user.to_dict()})

# ========== 角色管理 ==========
@bp.route('/role')
@login_required
def role_list():
    """角色列表页面"""
    return render_template('system/role.html')

@bp.route('/api/role/list')
@login_required
def get_role_list():
    """获取角色列表"""
    roles = Role.query.all()
    return jsonify({
        'success': True,
        'data': [role.to_dict() for role in roles]
    })

