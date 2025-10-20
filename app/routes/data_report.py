from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.models.data_report import DisplayReport, InventoryReport, CompetitorReport
from app.models.customer import Terminal, DirectDistributor, KOL
from app.models.product import Product
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

bp = Blueprint('data_report', __name__, url_prefix='/data_report')

# ==================== 文件上传辅助函数 ====================

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, prefix=''):
    """保存上传的文件并返回文件路径"""
    if file and allowed_file(file.filename):
        # 生成唯一的文件名
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{prefix}_{uuid.uuid4().hex[:8]}.{ext}"
        
        # 确保uploads目录存在
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'data_reports')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 保存文件
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        # 返回相对路径（用于数据库存储）
        return f"uploads/data_reports/{unique_filename}"
    return None

def delete_uploaded_file(filepath):
    """删除已上传的文件"""
    if filepath:
        try:
            full_path = os.path.join(current_app.root_path, 'static', filepath)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            print(f"删除文件失败: {str(e)}")

# ==================== 铺货上报 ====================

@bp.route('/display')
@login_required
def display_list():
    """铺货上报列表"""
    reports = DisplayReport.query.order_by(DisplayReport.created_at.desc()).all()
    return render_template('data_report/display_list.html', reports=reports)

@bp.route('/display/create', methods=['GET', 'POST'])
@login_required
def create_display():
    """创建铺货上报"""
    if request.method == 'POST':
        try:
            report_date = request.form.get('report_date')
            customer_name = request.form.get('customer_name')
            customer_type = request.form.get('customer_type')
            customer_level = request.form.get('customer_level')
            customer_manager = request.form.get('customer_manager')
            product_code = request.form.get('product_code')
            product_name = request.form.get('product_name')
            specification = request.form.get('specification')
            product_type = request.form.get('product_type')
            brand = request.form.get('brand')
            remark = request.form.get('remark')
            
            if not report_date or not customer_name or not product_code or not product_name:
                flash('上报日期、客户名称、商品编码和商品名称不能为空', 'error')
                return render_template('data_report/create_display.html')
            
            # 处理照片上传
            photo_path = None
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    photo_path = save_uploaded_file(photo, prefix='display')
            
            report = DisplayReport(
                report_date=datetime.strptime(report_date, '%Y-%m-%d').date(),
                customer_name=customer_name,
                customer_type=customer_type,
                customer_level=customer_level,
                customer_manager=customer_manager,
                product_code=product_code,
                product_name=product_name,
                specification=specification,
                product_type=product_type,
                brand=brand,
                photo=photo_path,
                remark=remark,
                reported_by=current_user.id
            )
            
            db.session.add(report)
            db.session.commit()
            
            flash('铺货上报创建成功', 'success')
            return redirect(url_for('data_report.display_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建铺货上报失败: {str(e)}', 'error')
    
    return render_template('data_report/create_display.html')

@bp.route('/display/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_display(report_id):
    """编辑铺货上报"""
    report = DisplayReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        try:
            report_date = request.form.get('report_date')
            report.report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
            report.customer_name = request.form.get('customer_name')
            report.customer_type = request.form.get('customer_type')
            report.customer_level = request.form.get('customer_level')
            report.customer_manager = request.form.get('customer_manager')
            report.product_code = request.form.get('product_code')
            report.product_name = request.form.get('product_name')
            report.specification = request.form.get('specification')
            report.product_type = request.form.get('product_type')
            report.brand = request.form.get('brand')
            report.remark = request.form.get('remark')
            
            # 处理照片上传
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    # 删除旧照片
                    if report.photo:
                        delete_uploaded_file(report.photo)
                    # 保存新照片
                    report.photo = save_uploaded_file(photo, prefix='display')
            
            db.session.commit()
            flash('铺货上报更新成功', 'success')
            return redirect(url_for('data_report.display_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新铺货上报失败: {str(e)}', 'error')
    
    return render_template('data_report/edit_display.html', report=report)

@bp.route('/display/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_display(report_id):
    """删除铺货上报"""
    try:
        report = DisplayReport.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        flash('铺货上报删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除铺货上报失败: {str(e)}', 'error')
    
    return redirect(url_for('data_report.display_list'))

# ==================== 库存上报 ====================

@bp.route('/inventory')
@login_required
def inventory_list():
    """库存上报列表"""
    reports = InventoryReport.query.order_by(InventoryReport.created_at.desc()).all()
    return render_template('data_report/inventory_list.html', reports=reports)

@bp.route('/inventory/create', methods=['GET', 'POST'])
@login_required
def create_inventory():
    """创建库存上报"""
    if request.method == 'POST':
        try:
            customer_name = request.form.get('customer_name')
            product_name = request.form.get('product_name')
            specification = request.form.get('specification')
            product_code = request.form.get('product_code')
            quantity = request.form.get('quantity')
            remark = request.form.get('remark')
            
            if not customer_name or not product_name or not quantity:
                flash('客户名称、商品名称和库存数量不能为空', 'error')
                return render_template('data_report/create_inventory.html')
            
            # 处理照片上传
            photo_path = None
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    photo_path = save_uploaded_file(photo, prefix='inventory')
            
            report = InventoryReport(
                customer_name=customer_name,
                product_name=product_name,
                specification=specification,
                product_code=product_code,
                quantity=int(quantity),
                photo=photo_path,
                remark=remark,
                reported_by=current_user.id
            )
            
            db.session.add(report)
            db.session.commit()
            
            flash('库存上报创建成功', 'success')
            return redirect(url_for('data_report.inventory_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建库存上报失败: {str(e)}', 'error')
    
    return render_template('data_report/create_inventory.html')

@bp.route('/inventory/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_inventory(report_id):
    """编辑库存上报"""
    report = InventoryReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        try:
            report.customer_name = request.form.get('customer_name')
            report.product_name = request.form.get('product_name')
            report.specification = request.form.get('specification')
            report.product_code = request.form.get('product_code')
            report.quantity = int(request.form.get('quantity'))
            report.remark = request.form.get('remark')
            
            # 处理照片上传
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    # 删除旧照片
                    if report.photo:
                        delete_uploaded_file(report.photo)
                    # 保存新照片
                    report.photo = save_uploaded_file(photo, prefix='inventory')
            
            db.session.commit()
            flash('库存上报更新成功', 'success')
            return redirect(url_for('data_report.inventory_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新库存上报失败: {str(e)}', 'error')
    
    return render_template('data_report/edit_inventory.html', report=report)

@bp.route('/inventory/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_inventory(report_id):
    """删除库存上报"""
    try:
        report = InventoryReport.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        flash('库存上报删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除库存上报失败: {str(e)}', 'error')
    
    return redirect(url_for('data_report.inventory_list'))

# ==================== 竞品上报 ====================

@bp.route('/competitor')
@login_required
def competitor_list():
    """竞品上报列表"""
    reports = CompetitorReport.query.order_by(CompetitorReport.created_at.desc()).all()
    return render_template('data_report/competitor_list.html', reports=reports)

@bp.route('/competitor/create', methods=['GET', 'POST'])
@login_required
def create_competitor():
    """创建竞品上报"""
    if request.method == 'POST':
        try:
            competitor_name = request.form.get('competitor_name')
            product_name = request.form.get('product_name')
            remark = request.form.get('remark')
            
            if not competitor_name:
                flash('竞品名称不能为空', 'error')
                return render_template('data_report/create_competitor.html')
            
            # 处理照片上传
            photo_path = None
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    photo_path = save_uploaded_file(photo, prefix='competitor')
            
            report = CompetitorReport(
                competitor_name=competitor_name,
                product_name=product_name,
                photo=photo_path,
                remark=remark,
                reported_by=current_user.id
            )
            
            db.session.add(report)
            db.session.commit()
            
            flash('竞品上报创建成功', 'success')
            return redirect(url_for('data_report.competitor_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建竞品上报失败: {str(e)}', 'error')
    
    return render_template('data_report/create_competitor.html')

@bp.route('/competitor/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_competitor(report_id):
    """编辑竞品上报"""
    report = CompetitorReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        try:
            report.competitor_name = request.form.get('competitor_name')
            report.product_name = request.form.get('product_name')
            report.remark = request.form.get('remark')
            
            # 处理照片上传
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo and photo.filename != '':
                    # 删除旧照片
                    if report.photo:
                        delete_uploaded_file(report.photo)
                    # 保存新照片
                    report.photo = save_uploaded_file(photo, prefix='competitor')
            
            db.session.commit()
            flash('竞品上报更新成功', 'success')
            return redirect(url_for('data_report.competitor_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新竞品上报失败: {str(e)}', 'error')
    
    return render_template('data_report/edit_competitor.html', report=report)

@bp.route('/competitor/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_competitor(report_id):
    """删除竞品上报"""
    try:
        report = CompetitorReport.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        flash('竞品上报删除成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除竞品上报失败: {str(e)}', 'error')
    
    return redirect(url_for('data_report.competitor_list'))

# ==================== API接口 ====================

@bp.route('/api/products')
@login_required
def get_products():
    """获取商品列表API"""
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': p.id,
        'code': p.code,
        'name': p.name,
        'specification': p.specification,
        'brand': p.brand,
        'type': p.type
    } for p in products])

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
    else:
        # 获取所有客户
        terminals = [{'id': t.id, 'name': t.name, 'type': 'terminal', 'level': t.level, 'manager': t.manager.name if t.manager else None} for t in Terminal.query.all()]
        distributors = [{'id': d.id, 'name': d.name, 'type': 'distributor', 'level': d.level, 'manager': d.manager.name if d.manager else None} for d in DirectDistributor.query.all()]
        kols = [{'id': k.id, 'name': k.name, 'type': 'kol', 'level': None, 'manager': k.manager.name if k.manager else None} for k in KOL.query.all()]
        return jsonify(terminals + distributors + kols)
    
    return jsonify([{
        'id': customer.id,
        'name': customer.name,
        'type': customer_type,
        'level': getattr(customer, 'level', None),
        'manager': customer.manager.name if customer.manager else None
    } for customer in customers])

