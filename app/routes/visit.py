from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.visit import VisitPlan, VisitRoute, VisitRecord
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
    
    query = VisitPlan.query
    
    if status:
        query = query.filter(VisitPlan.status == status)
    
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
    
    pagination = VisitRoute.query.order_by(VisitRoute.created_at.desc()).paginate(
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
    
    route = VisitRoute(
        name=data.get('name'),
        visitor_id=data.get('visitor_id', current_user.id),
        customer_list=data.get('customer_list'),
        remark=data.get('remark'),
        created_by=current_user.id
    )
    
    db.session.add(route)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': route.to_dict()})

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
    
    pagination = VisitRecord.query.order_by(VisitRecord.created_at.desc()).paginate(
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
    
    record = VisitRecord(
        visitor_id=current_user.id,
        customer_type=data.get('customer_type'),
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name'),
        visit_type=data.get('visit_type'),
        checkin_time=datetime.now(),
        visit_content=data.get('visit_content')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': record.to_dict()})

