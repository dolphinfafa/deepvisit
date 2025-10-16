from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    """加载用户"""
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            if request.is_json:
                return jsonify({'success': True, 'message': '登录成功', 'user': user.to_dict()})
            flash('登录成功！', 'success')
            return redirect(url_for('main.dashboard'))
        
        if request.is_json:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
        flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """登出"""
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/user/info')
@login_required
def user_info():
    """获取当前用户信息"""
    return jsonify({'success': True, 'user': current_user.to_dict()})

