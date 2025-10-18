from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.activity import Activity, ActivityReport, ActivityApplication
from app.models.customer import Terminal, DirectDistributor, KOL
from werkzeug.utils import secure_filename
import os
import uuid

bp = Blueprint('activity', __name__, url_prefix='/activity')

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder):
    """保存上传的文件"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = os.path.join('static', 'uploads', folder)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        return f"uploads/{folder}/{unique_filename}"
    return None

@bp.route('/')
@login_required
def index():
    """活动管理首页"""
    return render_template('activity/index.html')

@bp.route('/center')
@login_required
def center():
    """活动中心"""
    # 显示所有活动（包括草稿、活跃、非活跃）
    activities = Activity.query.order_by(Activity.created_at.desc()).all()
    return render_template('activity/center.html', activities=activities)

@bp.route('/center/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    """创建活动"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            activity_type = request.form.get('activity_type')
            description = request.form.get('description')
            
            if not name or not activity_type:
                flash('活动名称和活动类型不能为空', 'error')
                return render_template('activity/create_activity.html')
            
            # 处理日期字段
            execution_start_date = request.form.get('execution_start_date')
            execution_end_date = request.form.get('execution_end_date')
            application_start_date = request.form.get('application_start_date')
            application_end_date = request.form.get('application_end_date')
            
            # 处理费用分摊比例
            cost_share_ratio = request.form.get('cost_share_ratio')
            cost_share_ratio = float(cost_share_ratio) if cost_share_ratio else None
            
            activity = Activity(
                name=name,
                activity_type=activity_type,
                execution_start_date=execution_start_date if execution_start_date else None,
                execution_end_date=execution_end_date if execution_end_date else None,
                description=description,
                require_application=request.form.get('require_application'),
                customer_scope=request.form.get('customer_scope'),
                product_scope=request.form.get('product_scope'),
                payment_method=request.form.get('payment_method'),
                settlement_method=request.form.get('settlement_method'),
                application_start_date=application_start_date if application_start_date else None,
                application_end_date=application_end_date if application_end_date else None,
                cost_share_ratio=cost_share_ratio,
                customer_signature=request.form.get('customer_signature'),
                created_by=current_user.id
            )
            
            db.session.add(activity)
            db.session.commit()
            
            flash('活动创建成功', 'success')
            return redirect(url_for('activity.center'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建活动失败: {str(e)}', 'error')
            return render_template('activity/create_activity.html')
    
    return render_template('activity/create_activity.html')

@bp.route('/center/<int:activity_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    """编辑活动"""
    activity = Activity.query.get_or_404(activity_id)
    
    if request.method == 'POST':
        try:
            activity.name = request.form.get('name')
            activity.activity_type = request.form.get('activity_type')
            activity.description = request.form.get('description')
            
            # 处理日期字段
            execution_start_date = request.form.get('execution_start_date')
            execution_end_date = request.form.get('execution_end_date')
            application_start_date = request.form.get('application_start_date')
            application_end_date = request.form.get('application_end_date')
            
            activity.execution_start_date = execution_start_date if execution_start_date else None
            activity.execution_end_date = execution_end_date if execution_end_date else None
            activity.application_start_date = application_start_date if application_start_date else None
            activity.application_end_date = application_end_date if application_end_date else None
            
            # 处理费用分摊比例
            cost_share_ratio = request.form.get('cost_share_ratio')
            activity.cost_share_ratio = float(cost_share_ratio) if cost_share_ratio else None
            
            # 更新其他字段
            activity.require_application = request.form.get('require_application')
            activity.customer_scope = request.form.get('customer_scope')
            activity.product_scope = request.form.get('product_scope')
            activity.payment_method = request.form.get('payment_method')
            activity.settlement_method = request.form.get('settlement_method')
            activity.customer_signature = request.form.get('customer_signature')
            activity.status = request.form.get('status', 'active')
            
            db.session.commit()
            flash('活动更新成功', 'success')
            return redirect(url_for('activity.center'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新活动失败: {str(e)}', 'error')
    
    return render_template('activity/edit_activity.html', activity=activity)

@bp.route('/center/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    """删除活动"""
    try:
        activity = Activity.query.get_or_404(activity_id)
        
        # 检查是否有上报记录
        if activity.reports.count() > 0:
            flash('该活动已有上报记录，无法删除', 'error')
            return redirect(url_for('activity.center'))
        
        db.session.delete(activity)
        db.session.commit()
        flash('活动删除成功', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'删除活动失败: {str(e)}', 'error')
    
    return redirect(url_for('activity.center'))

@bp.route('/reports')
@login_required
def reports():
    """活动上报记录"""
    reports = ActivityReport.query.order_by(ActivityReport.created_at.desc()).all()
    return render_template('activity/reports.html', reports=reports)

@bp.route('/reports/create', methods=['GET', 'POST'])
@login_required
def create_report():
    """创建活动上报"""
    if request.method == 'POST':
        try:
            activity_id = request.form.get('activity_id')
            application_no = request.form.get('application_no')
            customer_name = request.form.get('customer_name')
            customer_code = request.form.get('customer_code')
            customer_type = request.form.get('customer_type')
            customer_id = request.form.get('customer_id')
            address = request.form.get('address')
            account_manager = request.form.get('account_manager')
            signature_method = request.form.get('signature_method')
            remark = request.form.get('remark')
            
            if not activity_id or not customer_name:
                flash('活动和客户名称不能为空', 'error')
                return render_template('activity/create_report.html', activities=Activity.query.filter_by(status='active').all())
            
            # 处理文件上传
            display_photo = None
            location_photo = None
            payment_photo = None
            signature_photo = None
            
            if 'display_photo' in request.files:
                file = request.files['display_photo']
                display_photo = save_uploaded_file(file, 'activity_display')
            
            if 'location_photo' in request.files:
                file = request.files['location_photo']
                location_photo = save_uploaded_file(file, 'activity_location')
            
            if 'payment_photo' in request.files:
                file = request.files['payment_photo']
                payment_photo = save_uploaded_file(file, 'activity_payment')
            
            if 'signature_photo' in request.files:
                file = request.files['signature_photo']
                signature_photo = save_uploaded_file(file, 'activity_signature')
            
            report = ActivityReport(
                activity_id=activity_id,
                application_no=application_no,
                customer_name=customer_name,
                customer_code=customer_code,
                customer_type=customer_type,
                customer_id=customer_id,
                address=address,
                account_manager=account_manager,
                display_photo=display_photo,
                location_photo=location_photo,
                payment_photo=payment_photo,
                signature_method=signature_method,
                signature_photo=signature_photo,
                remark=remark,
                reported_by=current_user.id
            )
            
            db.session.add(report)
            db.session.commit()
            
            flash('活动上报成功', 'success')
            return redirect(url_for('activity.reports'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建上报失败: {str(e)}', 'error')
    
    activities = Activity.query.filter_by(status='active').all()
    return render_template('activity/create_report.html', activities=activities)

@bp.route('/reports/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    """编辑活动上报"""
    report = ActivityReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        try:
            report.application_no = request.form.get('application_no')
            report.customer_name = request.form.get('customer_name')
            report.customer_code = request.form.get('customer_code')
            report.customer_type = request.form.get('customer_type')
            report.customer_id = request.form.get('customer_id')
            report.address = request.form.get('address')
            report.account_manager = request.form.get('account_manager')
            report.signature_method = request.form.get('signature_method')
            report.remark = request.form.get('remark')
            report.report_status = request.form.get('report_status', 'pending')
            
            # 处理文件上传
            if 'display_photo' in request.files:
                file = request.files['display_photo']
                if file and file.filename:
                    display_photo = save_uploaded_file(file, 'activity_display')
                    if display_photo:
                        report.display_photo = display_photo
            
            if 'location_photo' in request.files:
                file = request.files['location_photo']
                if file and file.filename:
                    location_photo = save_uploaded_file(file, 'activity_location')
                    if location_photo:
                        report.location_photo = location_photo
            
            if 'payment_photo' in request.files:
                file = request.files['payment_photo']
                if file and file.filename:
                    payment_photo = save_uploaded_file(file, 'activity_payment')
                    if payment_photo:
                        report.payment_photo = payment_photo
            
            if 'signature_photo' in request.files:
                file = request.files['signature_photo']
                if file and file.filename:
                    signature_photo = save_uploaded_file(file, 'activity_signature')
                    if signature_photo:
                        report.signature_photo = signature_photo
            
            db.session.commit()
            flash('上报记录更新成功', 'success')
            return redirect(url_for('activity.reports'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新上报失败: {str(e)}', 'error')
    
    activities = Activity.query.filter_by(status='active').all()
    return render_template('activity/edit_report.html', report=report, activities=activities)

@bp.route('/reports/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    """删除活动上报"""
    try:
        report = ActivityReport.query.get_or_404(report_id)
        
        # 删除相关文件
        if report.display_photo:
            file_path = os.path.join('static', report.display_photo)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if report.location_photo:
            file_path = os.path.join('static', report.location_photo)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if report.payment_photo:
            file_path = os.path.join('static', report.payment_photo)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if report.signature_photo:
            file_path = os.path.join('static', report.signature_photo)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(report)
        db.session.commit()
        flash('上报记录删除成功', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'删除上报失败: {str(e)}', 'error')
    
    return redirect(url_for('activity.reports'))

@bp.route('/api/customers')
@login_required
def get_customers():
    """获取客户列表API"""
    customer_type = request.args.get('type', '')
    
    customers = []
    if customer_type == 'terminal':
        customers = Terminal.query.all()
    elif customer_type == 'distributor':
        customers = DirectDistributor.query.all()
    elif customer_type == 'kol':
        customers = KOL.query.all()
    
    return jsonify([{
        'id': customer.id,
        'name': customer.name,
        'type': customer_type
    } for customer in customers])
