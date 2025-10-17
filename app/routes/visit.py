from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.visit import VisitPlan, VisitRoute, VisitRecord
from app.models.user import User
from datetime import datetime

bp = Blueprint('visit', __name__, url_prefix='/visit')

# ========== 拜访计划 ==========
@bp.route('/plan')
@login_required
def plan_list():
    """拜访计划列表页面"""
    return render_template('visit/plan.html')

@bp.route('/api/plan/list')
@login_required
def get_plan_list():
    """获取拜访计划列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    approval_status = request.args.get('approval_status', '')
    visitor_id = request.args.get('visitor_id', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = VisitPlan.query
    
    # 状态筛选
    if status:
        query = query.filter(VisitPlan.status == status)
    
    # 审批状态筛选
    if approval_status:
        query = query.filter(VisitPlan.approval_status == approval_status)
    
    # 拜访人筛选
    if visitor_id:
        query = query.filter(VisitPlan.visitor_id == visitor_id)
    
    # 时间范围筛选
    if start_date:
        query = query.filter(VisitPlan.visit_date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(VisitPlan.visit_date <= datetime.fromisoformat(end_date).date())
    
    pagination = query.order_by(VisitPlan.visit_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/plan/create', methods=['POST'])
@login_required
def create_plan():
    """创建拜访计划"""
    data = request.get_json()
    
    plan = VisitPlan(
        visitor_id=data.get('visitor_id', current_user.id),
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name'),
        visit_date=datetime.fromisoformat(data.get('visit_date')),
        plan_content=data.get('plan_content'),
        created_by=current_user.id
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': plan.to_dict()})

@bp.route('/api/users/list')
@login_required
def get_users_list():
    """获取用户列表（用于选择拜访人）"""
    users = User.query.filter(User.is_active == True).all()
    return jsonify({
        'success': True,
        'data': [{'id': user.id, 'name': user.name, 'department': user.department} for user in users]
    })

# ========== 拜访路线 ==========
@bp.route('/route')
@login_required
def route_list():
    """拜访路线列表页面"""
    return render_template('visit/route.html')

@bp.route('/api/route/list')
@login_required
def get_route_list():
    """获取拜访路线列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    visitor_id = request.args.get('visitor_id', '')
    approval_status = request.args.get('approval_status', '')
    name = request.args.get('name', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = VisitRoute.query
    
    # 客户经理筛选
    if visitor_id:
        query = query.filter(VisitRoute.visitor_id == visitor_id)
    
    # 审批状态筛选
    if approval_status:
        query = query.filter(VisitRoute.approval_status == approval_status)
    
    # 路线名称筛选
    if name:
        query = query.filter(VisitRoute.name.like(f'%{name}%'))
    
    # 时间范围筛选
    if start_date:
        query = query.filter(VisitRoute.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(VisitRoute.created_at <= datetime.fromisoformat(end_date))
    
    pagination = query.order_by(VisitRoute.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/route/create', methods=['POST'])
@login_required
def create_route():
    """创建拜访路线"""
    data = request.get_json()
    
    import json
    
    # 处理客户列表
    customer_list = data.get('customer_list', [])
    if isinstance(customer_list, list):
        customer_list_json = json.dumps(customer_list, ensure_ascii=False)
    else:
        customer_list_json = customer_list
    
    # 处理路线详情
    route_details = data.get('route_details', {})
    if isinstance(route_details, dict):
        route_details_json = json.dumps(route_details, ensure_ascii=False)
    else:
        route_details_json = route_details
    
    route = VisitRoute(
        name=data.get('name'),
        visitor_id=data.get('visitor_id', current_user.id),
        customer_list=customer_list_json,
        route_details=route_details_json,
        remark=data.get('remark'),
        created_by=current_user.id
    )
    
    db.session.add(route)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': route.to_dict()})

@bp.route('/api/route/<int:route_id>/approve', methods=['POST'])
@login_required
def approve_route(route_id):
    """审批拜访路线"""
    data = request.get_json()
    action = data.get('action')  # approve/reject
    
    route = VisitRoute.query.get_or_404(route_id)
    
    if action == 'approve':
        route.approval_status = 'approved'
        route.approved_by = current_user.id
        route.approved_at = datetime.utcnow()
        message = '审批通过'
    elif action == 'reject':
        route.approval_status = 'rejected'
        route.approved_by = current_user.id
        route.approved_at = datetime.utcnow()
        message = '审批拒绝'
    else:
        return jsonify({'success': False, 'message': '无效的操作'})
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': message, 'data': route.to_dict()})

@bp.route('/api/customers/list')
@login_required
def get_customers_list():
    """获取所有客户列表（用于路线规划）"""
    from app.models.customer import Terminal, DirectDistributor, KOL
    
    customers = []
    
    # 获取终端客户
    terminals = Terminal.query.all()
    for terminal in terminals:
        customers.append({
            'id': terminal.id,
            'name': terminal.name,
            'type': 'terminal',
            'type_name': '终端客户',
            'code': terminal.code,
            'address': terminal.detail_address,
            'phone': terminal.phone,
            'manager': terminal.manager.name if terminal.manager else None
        })
    
    # 获取直营商客户
    distributors = DirectDistributor.query.all()
    for distributor in distributors:
        customers.append({
            'id': distributor.id,
            'name': distributor.name,
            'type': 'distributor',
            'type_name': '直营商客户',
            'code': distributor.code,
            'address': distributor.detail_address,
            'phone': distributor.phone,
            'manager': distributor.manager.name if distributor.manager else None
        })
    
    # 获取KOL客户
    kols = KOL.query.all()
    for kol in kols:
        customers.append({
            'id': kol.id,
            'name': kol.name,
            'type': 'kol',
            'type_name': 'KOL客户',
            'code': kol.code,
            'address': kol.detail_address,
            'phone': kol.phone,
            'manager': kol.manager.name if kol.manager else None
        })
    
    return jsonify({
        'success': True,
        'data': customers
    })

# ========== 逾期拜访列表 ==========
@bp.route('/overdue')
@login_required
def overdue_list():
    """逾期拜访列表页面"""
    return render_template('visit/overdue.html')

@bp.route('/api/overdue/list')
@login_required
def get_overdue_list():
    """获取逾期拜访列表"""
    from app.models.customer import Terminal, DirectDistributor
    from datetime import datetime, timedelta
    
    overdue_customers = []
    
    # 获取终端客户
    terminals = Terminal.query.filter(Terminal.manager_id.isnot(None)).all()
    for terminal in terminals:
        if terminal.visit_frequency and terminal.manager:
            overdue_days = calculate_overdue_days(terminal.id, 'terminal', terminal.visit_frequency)
            if overdue_days > 0:
                overdue_customers.append({
                    'customer_name': terminal.name,
                    'customer_code': terminal.code,
                    'customer_address': terminal.detail_address or terminal.receiver_address or '无地址',
                    'manager': terminal.manager.name,
                    'visit_frequency': terminal.visit_frequency,
                    'overdue_days': overdue_days,
                    'customer_type': 'terminal',
                    'customer_type_name': '终端客户',
                    'last_visit_date': get_last_visit_date(terminal.id, 'terminal')
                })
    
    # 获取直营商客户
    distributors = DirectDistributor.query.filter(DirectDistributor.manager_id.isnot(None)).all()
    for distributor in distributors:
        if distributor.visit_frequency and distributor.manager:
            overdue_days = calculate_overdue_days(distributor.id, 'distributor', distributor.visit_frequency)
            if overdue_days > 0:
                overdue_customers.append({
                    'customer_name': distributor.name,
                    'customer_code': distributor.code,
                    'customer_address': distributor.detail_address or distributor.receiver_address or '无地址',
                    'manager': distributor.manager.name,
                    'visit_frequency': distributor.visit_frequency,
                    'overdue_days': overdue_days,
                    'customer_type': 'distributor',
                    'customer_type_name': '直营商客户',
                    'last_visit_date': get_last_visit_date(distributor.id, 'distributor')
                })
    
    # 按逾期天数排序
    overdue_customers.sort(key=lambda x: x['overdue_days'], reverse=True)
    
    return jsonify({
        'success': True,
        'data': overdue_customers,
        'total': len(overdue_customers)
    })

def calculate_overdue_days(customer_id, customer_type, visit_frequency):
    """计算逾期天数"""
    from datetime import datetime, timedelta
    
    # 获取最后一次拜访记录
    last_visit = VisitRecord.query.filter(
        VisitRecord.customer_id == customer_id,
        VisitRecord.customer_type == customer_type
    ).order_by(VisitRecord.created_at.desc()).first()
    
    if not last_visit:
        # 如果没有拜访记录，从客户创建时间开始计算
        from app.models.customer import Terminal, DirectDistributor
        if customer_type == 'terminal':
            customer = Terminal.query.get(customer_id)
        else:
            customer = DirectDistributor.query.get(customer_id)
        
        if customer:
            days_since_creation = (datetime.now() - customer.created_at).days
            return max(0, days_since_creation - get_frequency_days(visit_frequency))
        return 0
    
    # 计算距离最后一次拜访的天数
    days_since_last_visit = (datetime.now() - last_visit.created_at).days
    
    # 获取拜访频率对应的天数
    frequency_days = get_frequency_days(visit_frequency)
    
    # 计算逾期天数
    overdue_days = max(0, days_since_last_visit - frequency_days)
    
    return overdue_days

def get_frequency_days(visit_frequency):
    """将拜访频率转换为天数"""
    frequency_map = {
        'daily': 1,           # 每日
        'weekly': 7,          # 每周
        'biweekly': 14,       # 每两周
        'monthly': 30,        # 每月
        'bimonthly': 60,      # 每两月
        'quarterly': 90,      # 每季度
        'semiannual': 180,    # 每半年
        'annual': 365         # 每年
    }
    
    # 处理数字格式的频率（如 "7天", "30天"）
    if isinstance(visit_frequency, str):
        if '天' in visit_frequency:
            try:
                return int(visit_frequency.replace('天', ''))
            except ValueError:
                pass
        elif '周' in visit_frequency:
            try:
                weeks = int(visit_frequency.replace('周', ''))
                return weeks * 7
            except ValueError:
                pass
        elif '月' in visit_frequency:
            try:
                months = int(visit_frequency.replace('月', ''))
                return months * 30
            except ValueError:
                pass
    
    return frequency_map.get(visit_frequency, 30)  # 默认30天

def get_last_visit_date(customer_id, customer_type):
    """获取最后一次拜访日期"""
    last_visit = VisitRecord.query.filter(
        VisitRecord.customer_id == customer_id,
        VisitRecord.customer_type == customer_type
    ).order_by(VisitRecord.created_at.desc()).first()
    
    if last_visit:
        return last_visit.created_at.strftime('%Y-%m-%d')
    return '从未拜访'

# ========== 拜访记录 ==========
@bp.route('/record')
@login_required
def record_list():
    """拜访记录列表页面"""
    return render_template('visit/record.html')

@bp.route('/api/record/list')
@login_required
def get_record_list():
    """获取拜访记录列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    visitor_id = request.args.get('visitor_id', '')
    customer_name = request.args.get('customer_name', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    customer_type = request.args.get('customer_type', '')
    
    query = VisitRecord.query
    
    # 拜访人筛选
    if visitor_id:
        query = query.filter(VisitRecord.visitor_id == visitor_id)
    
    # 客户名称筛选
    if customer_name:
        query = query.filter(VisitRecord.customer_name.like(f'%{customer_name}%'))
    
    # 客户类型筛选
    if customer_type:
        query = query.filter(VisitRecord.customer_type == customer_type)
    
    # 时间范围筛选
    if start_date:
        query = query.filter(VisitRecord.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(VisitRecord.created_at <= datetime.fromisoformat(end_date))
    
    pagination = query.order_by(VisitRecord.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in pagination.items],
        'total': pagination.total
    })

@bp.route('/api/record/create', methods=['POST'])
@login_required
def create_record():
    """创建拜访记录"""
    data = request.get_json()
    
    import json
    
    # 处理JSON字段
    product_distribution_list = data.get('product_distribution_list', [])
    distribution_photos = data.get('distribution_photos', [])
    inventory_list = data.get('inventory_list', [])
    inventory_photos = data.get('inventory_photos', [])
    competitor_list = data.get('competitor_list', [])
    competitor_photos = data.get('competitor_photos', [])
    photos = data.get('photos', [])
    
    record = VisitRecord(
        plan_id=data.get('plan_id'),
        visitor_id=data.get('visitor_id', current_user.id),
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name'),
        customer_address=data.get('customer_address'),
        visit_frequency=data.get('visit_frequency'),
        visit_type=data.get('visit_type'),
        visit_content=data.get('visit_content'),
        checkin_time=datetime.fromisoformat(data.get('checkin_time')) if data.get('checkin_time') else None,
        checkin_latitude=data.get('checkin_latitude'),
        checkin_longitude=data.get('checkin_longitude'),
        checkin_address=data.get('checkin_address'),
        checkout_time=datetime.fromisoformat(data.get('checkout_time')) if data.get('checkout_time') else None,
        checkout_latitude=data.get('checkout_latitude'),
        checkout_longitude=data.get('checkout_longitude'),
        checkout_address=data.get('checkout_address'),
        product_distribution_list=json.dumps(product_distribution_list, ensure_ascii=False),
        distribution_photos=json.dumps(distribution_photos, ensure_ascii=False),
        distribution_remark=data.get('distribution_remark'),
        inventory_list=json.dumps(inventory_list, ensure_ascii=False),
        inventory_photos=json.dumps(inventory_photos, ensure_ascii=False),
        inventory_remark=data.get('inventory_remark'),
        competitor_list=json.dumps(competitor_list, ensure_ascii=False),
        competitor_photos=json.dumps(competitor_photos, ensure_ascii=False),
        competitor_remark=data.get('competitor_remark'),
        photos=json.dumps(photos, ensure_ascii=False)
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': record.to_dict()})

@bp.route('/api/record/<int:record_id>')
@login_required
def get_record_detail(record_id):
    """获取拜访记录详情"""
    record = VisitRecord.query.get_or_404(record_id)
    return jsonify({
        'success': True,
        'data': record.to_dict()
    })

