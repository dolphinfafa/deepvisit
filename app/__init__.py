from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    
    CORS(app)
    
    # 注册蓝图
    from app.routes import auth, customer, visit, order, inventory, system
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(visit.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(system.bp)
    
    # 注册主页路由
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        # 初始化默认数据
        from app.models.user import User
        from app.models.role import Role
        if not Role.query.first():
            init_default_data()
    
    return app

def init_default_data():
    """初始化默认数据"""
    from app.models.user import User
    from app.models.role import Role
    
    # 创建默认角色
    roles = [
        Role(name='超级管理员', code='admin', description='系统管理员'),
        Role(name='总经理', code='general_manager', description='总经理'),
        Role(name='部门经理', code='dept_manager', description='部门经理'),
        Role(name='客户经理', code='customer_manager', description='客户经理'),
        Role(name='业务员', code='salesman', description='业务员'),
    ]
    for role in roles:
        db.session.add(role)
    
    db.session.commit()
    
    # 创建默认管理员账号
    admin_role = Role.query.filter_by(code='admin').first()
    admin = User(
        username='admin',
        email='admin@deepvisit.com',
        name='系统管理员',
        phone='13800138000',
        role_id=admin_role.id
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

