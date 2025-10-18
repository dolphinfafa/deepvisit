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
            (Terminal.phone.like(f'%{search}%')) |
            (Terminal.contact_phone.like(f'%{search}%')) |
            (Terminal.receiver_phone.like(f'%{search}%')) |
            (Terminal.license_name.like(f'%{search}%')) |
            (Terminal.registration_no.like(f'%{search}%'))
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
    # 处理文件上传
    business_license_path = None
    if 'business_license' in request.files:
        file = request.files['business_license']
        if file and file.filename:
            # 保存文件到uploads目录
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"license_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            business_license_path = f"uploads/{filename}"
    
    # 获取表单数据
    data = request.form.to_dict()
    
    terminal = Terminal(
        name=data.get('name'),
        code=data.get('code'),
        type=data.get('type'),
        level=data.get('level'),
        manager_id=data.get('manager_id') if data.get('manager_id') else None,
        assistant_id=data.get('assistant_id') if data.get('assistant_id') else None,
        sales_area=data.get('sales_area'),
        tags=data.get('tags'),
        supplier=data.get('supplier'),
        cooperation_status=data.get('cooperation_status', '合作中'),
        phone=data.get('phone'),
        remark=data.get('remark'),
        visit_frequency=data.get('visit_frequency'),
        approval_status=data.get('approval_status', 'pending'),
        business_license=business_license_path,
        license_name=data.get('license_name'),
        registration_no=data.get('registration_no'),
        registration_date=datetime.strptime(data.get('registration_date'), '%Y-%m-%d').date() if data.get('registration_date') else None,
        operator=data.get('operator'),
        receiver_name=data.get('receiver_name'),
        receiver_phone=data.get('receiver_phone'),
        receiver_address=data.get('receiver_address'),
        detail_address=data.get('detail_address'),
        contact_name=data.get('contact_name'),
        contact_phone=data.get('contact_phone'),
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

@bp.route('/terminal/<int:id>')
@login_required
def terminal_detail(id):
    """终端客户详情页面"""
    return render_template('customer/terminal_detail.html', id=id)

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
            (DirectDistributor.code.like(f'%{search}%')) |
            (DirectDistributor.phone.like(f'%{search}%')) |
            (DirectDistributor.contact_phone.like(f'%{search}%')) |
            (DirectDistributor.receiver_phone.like(f'%{search}%')) |
            (DirectDistributor.license_name.like(f'%{search}%')) |
            (DirectDistributor.registration_no.like(f'%{search}%'))
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
    # 处理文件上传
    business_license_path = None
    if 'business_license' in request.files:
        file = request.files['business_license']
        if file and file.filename:
            # 保存文件到uploads目录
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"license_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            business_license_path = f"uploads/{filename}"
    
    # 获取表单数据
    data = request.form.to_dict()
    
    distributor = DirectDistributor(
        name=data.get('name'),
        code=data.get('code'),
        type=data.get('type'),
        level=data.get('level'),
        manager_id=data.get('manager_id') if data.get('manager_id') else None,
        assistant_id=data.get('assistant_id') if data.get('assistant_id') else None,
        sales_area=data.get('sales_area'),
        tags=data.get('tags'),
        supplier=data.get('supplier'),
        cooperation_status=data.get('cooperation_status', '合作中'),
        phone=data.get('phone'),
        remark=data.get('remark'),
        visit_frequency=data.get('visit_frequency'),
        approval_status=data.get('approval_status', 'pending'),
        business_license=business_license_path,
        license_name=data.get('license_name'),
        registration_no=data.get('registration_no'),
        registration_date=datetime.strptime(data.get('registration_date'), '%Y-%m-%d').date() if data.get('registration_date') else None,
        operator=data.get('operator'),
        receiver_name=data.get('receiver_name'),
        receiver_phone=data.get('receiver_phone'),
        receiver_address=data.get('receiver_address'),
        detail_address=data.get('detail_address'),
        contact_name=data.get('contact_name'),
        contact_phone=data.get('contact_phone'),
        created_by=current_user.id
    )
    
    db.session.add(distributor)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': distributor.to_dict()})

@bp.route('/api/distributor/<int:id>', methods=['GET'])
@login_required
def get_distributor(id):
    """获取经销商详情"""
    distributor = DirectDistributor.query.get_or_404(id)
    return jsonify({'success': True, 'data': distributor.to_dict()})

@bp.route('/api/distributor/<int:id>', methods=['DELETE'])
@login_required
def delete_distributor(id):
    """删除经销商"""
    distributor = DirectDistributor.query.get_or_404(id)
    db.session.delete(distributor)
    db.session.commit()
    return jsonify({'success': True, 'message': '删除成功'})

@bp.route('/distributor/<int:id>')
@login_required
def distributor_detail(id):
    """经销商详情页面"""
    return render_template('customer/distributor_detail.html', id=id)

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
            (KOL.code.like(f'%{search}%')) |
            (KOL.phone.like(f'%{search}%')) |
            (KOL.profession.like(f'%{search}%')) |
            (KOL.location.like(f'%{search}%')) |
            (KOL.kol_tags.like(f'%{search}%'))
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
        consumer_type=data.get('consumer_type'),
        gender=data.get('gender'),
        phone=data.get('phone'),
        age_group=data.get('age_group'),
        kol_tags=data.get('kol_tags'),
        birthday=datetime.strptime(data.get('birthday'), '%Y-%m-%d').date() if data.get('birthday') else None,
        location=data.get('location'),
        profession=data.get('profession'),
        drinking_frequency=data.get('drinking_frequency'),
        drinking_scene=data.get('drinking_scene'),
        cooperation_status=data.get('cooperation_status', '合作中'),
        manager_id=data.get('manager_id'),
        position_note=data.get('position_note'),
        province=data.get('province'),
        city=data.get('city'),
        district=data.get('district'),
        street=data.get('street'),
        detail_address=data.get('detail_address'),
        hobbies=data.get('hobbies'),
        remark=data.get('remark'),
        receiver_name=data.get('receiver_name'),
        receiver_phone=data.get('receiver_phone'),
        receiver_address=data.get('receiver_address'),
        created_by=current_user.id
    )
    
    db.session.add(kol)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '创建成功', 'data': kol.to_dict()})

@bp.route('/api/kol/<int:id>', methods=['GET'])
@login_required
def get_kol(id):
    """获取KOL详情"""
    kol = KOL.query.get_or_404(id)
    return jsonify({'success': True, 'data': kol.to_dict()})

@bp.route('/api/kol/<int:id>', methods=['DELETE'])
@login_required
def delete_kol(id):
    """删除KOL"""
    kol = KOL.query.get_or_404(id)
    db.session.delete(kol)
    db.session.commit()
    return jsonify({'success': True, 'message': '删除成功'})

@bp.route('/kol/<int:id>')
@login_required
def kol_detail(id):
    """KOL详情页面"""
    return render_template('customer/kol_detail.html', id=id)

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

