#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试数据填充脚本
为DeepVisit系统的所有模块创建测试数据
"""

import sys
import io

# 设置标准输出为UTF-8编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import create_app, db
from app.models.role import Role
from app.models.user import User
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier
from app.models.customer import Terminal, DirectDistributor, KOL, CustomerContact
from app.models.inventory import Inventory
from app.models.purchase_order import PurchaseOrder
from app.models.order import SalesOrder, DeliveryOrder, ReturnOrder
from app.models.visit import VisitPlan, VisitRoute, VisitRecord
from app.models.activity import Activity, ActivityReport
from datetime import datetime, date, time, timedelta
import json
import random


def clear_all_data():
    """清空所有表数据"""
    print("清空现有数据...")
    
    # 删除顺序要考虑外键依赖关系
    ActivityReport.query.delete()
    Activity.query.delete()
    VisitRecord.query.delete()
    VisitRoute.query.delete()
    VisitPlan.query.delete()
    DeliveryOrder.query.delete()
    ReturnOrder.query.delete()
    SalesOrder.query.delete()
    PurchaseOrder.query.delete()
    Inventory.query.delete()
    CustomerContact.query.delete()
    KOL.query.delete()
    DirectDistributor.query.delete()
    Terminal.query.delete()
    Supplier.query.delete()
    Product.query.delete()
    Warehouse.query.delete()
    User.query.delete()
    Role.query.delete()
    
    db.session.commit()
    print("[OK] 数据清空完成")


def create_roles():
    """创建角色"""
    print("\n创建角色...")
    
    roles_data = [
        {'name': '系统管理员', 'code': 'admin', 'description': '系统最高权限管理员'},
        {'name': '销售经理', 'code': 'sales_manager', 'description': '销售团队负责人'},
        {'name': '客户经理', 'code': 'account_manager', 'description': '客户关系维护人员'},
        {'name': '仓库管理员', 'code': 'warehouse_manager', 'description': '仓库库存管理人员'},
        {'name': '业务员', 'code': 'salesperson', 'description': '一线销售人员'},
        {'name': '市场专员', 'code': 'marketing', 'description': '市场活动执行人员'},
    ]
    
    roles = []
    for data in roles_data:
        role = Role(**data)
        db.session.add(role)
        roles.append(role)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(roles)} 个角色")
    return roles


def create_users(roles):
    """创建用户"""
    print("\n创建用户...")
    
    users_data = [
        {'username': 'admin', 'email': 'admin@deepvisit.com', 'name': '张管理', 
         'phone': '13800138000', 'department': '技术部', 'role_id': roles[0].id},
        {'username': 'manager1', 'email': 'manager1@deepvisit.com', 'name': '李经理', 
         'phone': '13800138001', 'department': '销售部', 'role_id': roles[1].id},
        {'username': 'account1', 'email': 'account1@deepvisit.com', 'name': '王客户', 
         'phone': '13800138002', 'department': '销售部', 'role_id': roles[2].id},
        {'username': 'account2', 'email': 'account2@deepvisit.com', 'name': '赵助理', 
         'phone': '13800138003', 'department': '销售部', 'role_id': roles[2].id},
        {'username': 'warehouse1', 'email': 'warehouse1@deepvisit.com', 'name': '刘仓管', 
         'phone': '13800138004', 'department': '仓储部', 'role_id': roles[3].id},
        {'username': 'sales1', 'email': 'sales1@deepvisit.com', 'name': '陈业务', 
         'phone': '13800138005', 'department': '销售部', 'role_id': roles[4].id},
        {'username': 'sales2', 'email': 'sales2@deepvisit.com', 'name': '杨业务', 
         'phone': '13800138006', 'department': '销售部', 'role_id': roles[4].id},
        {'username': 'market1', 'email': 'market1@deepvisit.com', 'name': '周市场', 
         'phone': '13800138007', 'department': '市场部', 'role_id': roles[5].id},
    ]
    
    users = []
    for data in users_data:
        user = User(**data)
        user.set_password('123456')  # 默认密码
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(users)} 个用户（默认密码: 123456）")
    return users


def create_products():
    """创建商品"""
    print("\n创建商品...")
    
    products_data = [
        # 自家商品
        {'code': 'P001', 'name': '茅台酒飞天53度', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '茅台', 'type': 'own', 'price': 2999, 'cost': 2000, 'is_display': True},
        {'code': 'P002', 'name': '茅台王子酒', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '茅台', 'type': 'own', 'price': 368, 'cost': 250, 'is_display': True},
        {'code': 'P003', 'name': '茅台迎宾酒', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '茅台', 'type': 'own', 'price': 138, 'cost': 90, 'is_display': True},
        {'code': 'P004', 'name': '茅台醇', 'specification': '500ml*6', 'unit': '箱',
         'category': '白酒', 'brand': '茅台', 'type': 'own', 'price': 588, 'cost': 400, 'is_display': True},
        {'code': 'P005', 'name': '茅台1935', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '茅台', 'type': 'own', 'price': 1680, 'cost': 1200, 'is_display': True},
        
        # 竞品
        {'code': 'C001', 'name': '五粮液52度', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '五粮液', 'type': 'competitor', 'price': 1299, 'cost': 0, 'is_display': True},
        {'code': 'C002', 'name': '国窖1573', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '泸州老窖', 'type': 'competitor', 'price': 1199, 'cost': 0, 'is_display': True},
        {'code': 'C003', 'name': '剑南春', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '剑南春', 'type': 'competitor', 'price': 499, 'cost': 0, 'is_display': True},
        {'code': 'C004', 'name': '洋河梦之蓝', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '洋河', 'type': 'competitor', 'price': 899, 'cost': 0, 'is_display': True},
        {'code': 'C005', 'name': '汾酒青花20', 'specification': '500ml', 'unit': '瓶',
         'category': '白酒', 'brand': '汾酒', 'type': 'competitor', 'price': 599, 'cost': 0, 'is_display': True},
    ]
    
    products = []
    for data in products_data:
        product = Product(**data)
        db.session.add(product)
        products.append(product)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(products)} 个商品")
    return products


def create_warehouses():
    """创建仓库"""
    print("\n创建仓库...")
    
    warehouses_data = [
        {'code': 'WH001', 'name': '北京启光总仓', 'warehouse_type': 'qiguang',
         'address': '北京市朝阳区XX路XX号', 'manager': '刘仓管', 'phone': '13800138004', 'capacity': 10000},
        {'code': 'WH002', 'name': '上海启光仓', 'warehouse_type': 'qiguang',
         'address': '上海市浦东新区XX路XX号', 'manager': '钱仓管', 'phone': '13900139001', 'capacity': 8000},
        {'code': 'WH003', 'name': '广州直营仓', 'warehouse_type': 'direct_sales',
         'address': '广州市天河区XX路XX号', 'manager': '孙仓管', 'phone': '13900139002', 'capacity': 5000},
        {'code': 'WH004', 'name': '深圳直营仓', 'warehouse_type': 'direct_sales',
         'address': '深圳市南山区XX路XX号', 'manager': '李仓管', 'phone': '13900139003', 'capacity': 6000},
    ]
    
    warehouses = []
    for data in warehouses_data:
        warehouse = Warehouse(**data)
        db.session.add(warehouse)
        warehouses.append(warehouse)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(warehouses)} 个仓库")
    return warehouses


def create_suppliers():
    """创建供应商"""
    print("\n创建供应商...")
    
    suppliers_data = [
        {'code': 'SUP001', 'name': '贵州茅台酒厂集团', 'contact_person': '张经理',
         'phone': '0851-12345678', 'email': 'contact@moutai.com', 
         'address': '贵州省仁怀市茅台镇', 'payment_terms': '款到发货', 'credit_limit': 10000000},
        {'code': 'SUP002', 'name': '四川茅台经销商', 'contact_person': '李经理',
         'phone': '028-87654321', 'email': 'contact@scmt.com',
         'address': '四川省成都市XX区XX路XX号', 'payment_terms': '月结30天', 'credit_limit': 5000000},
        {'code': 'SUP003', 'name': '华东茅台总代理', 'contact_person': '王经理',
         'phone': '021-12345678', 'email': 'contact@hdmt.com',
         'address': '上海市黄浦区XX路XX号', 'payment_terms': '月结45天', 'credit_limit': 8000000},
    ]
    
    suppliers = []
    for data in suppliers_data:
        supplier = Supplier(**data)
        db.session.add(supplier)
        suppliers.append(supplier)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(suppliers)} 个供应商")
    return suppliers


def create_terminals(users):
    """创建终端客户"""
    print("\n创建终端客户...")
    
    terminals_data = [
        {'name': '北京华联超市朝阳店', 'code': 'T001', 'type': '超市', 'level': 'A',
         'manager_id': users[2].id, 'assistant_id': users[3].id, 'sales_area': '华北',
         'tags': '连锁,高端', 'cooperation_status': '合作中', 'phone': '010-12345678',
         'visit_frequency': '每周', 'approval_status': 'approved',
         'license_name': '北京华联超市有限公司', 'operator': '张三',
         'receiver_name': '李四', 'receiver_phone': '13700137001', 
         'receiver_address': '北京市朝阳区建国路88号', 'detail_address': '华联超市收货部',
         'contact_name': '王五', 'contact_phone': '13700137002'},
        {'name': '上海家乐福徐家汇店', 'code': 'T002', 'type': '超市', 'level': 'A',
         'manager_id': users[2].id, 'sales_area': '华东',
         'tags': '连锁,大型', 'cooperation_status': '合作中', 'phone': '021-22345678',
         'visit_frequency': '每周', 'approval_status': 'approved',
         'license_name': '上海家乐福商业有限公司', 'operator': '赵六',
         'receiver_name': '孙七', 'receiver_phone': '13800138011',
         'receiver_address': '上海市徐汇区虹桥路1号', 'detail_address': '收货处'},
        {'name': '深圳万象城Ole超市', 'code': 'T003', 'type': '高端超市', 'level': 'S',
         'manager_id': users[3].id, 'sales_area': '华南',
         'tags': '高端,进口', 'cooperation_status': '合作中', 'phone': '0755-88888888',
         'visit_frequency': '每两周', 'approval_status': 'approved',
         'license_name': '深圳万象城商业管理有限公司', 'operator': '周八',
         'receiver_name': '吴九', 'receiver_phone': '13900139011',
         'receiver_address': '深圳市南山区深南大道9668号', 'detail_address': 'B1收货区'},
        {'name': '广州天河城百货', 'code': 'T004', 'type': '百货', 'level': 'A',
         'manager_id': users[2].id, 'sales_area': '华南',
         'tags': '百货,综合', 'cooperation_status': '合作中', 'phone': '020-38888888',
         'visit_frequency': '每周', 'approval_status': 'approved',
         'license_name': '广州天河城百货有限公司', 'operator': '郑十',
         'receiver_name': '钱十一', 'receiver_phone': '13900139012',
         'receiver_address': '广州市天河区天河路208号', 'detail_address': '收货部'},
        {'name': '成都伊藤洋华堂', 'code': 'T005', 'type': '超市', 'level': 'B',
         'manager_id': users[3].id, 'sales_area': '西南',
         'tags': '日系,品质', 'cooperation_status': '合作中', 'phone': '028-85888888',
         'visit_frequency': '每两周', 'approval_status': 'approved',
         'license_name': '成都伊藤洋华堂有限公司', 'operator': '孙十二',
         'receiver_name': '李十三', 'receiver_phone': '13600136001',
         'receiver_address': '成都市锦江区红星路三段1号', 'detail_address': '后门收货'},
    ]
    
    terminals = []
    for data in terminals_data:
        data['created_by'] = users[2].id
        terminal = Terminal(**data)
        db.session.add(terminal)
        terminals.append(terminal)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(terminals)} 个终端客户")
    return terminals


def create_distributors(users):
    """创建直营商客户"""
    print("\n创建直营商客户...")
    
    distributors_data = [
        {'name': '北京启光酒业', 'code': 'D001', 'type': '一级经销商', 'level': 'S',
         'manager_id': users[2].id, 'assistant_id': users[3].id, 'sales_area': '华北',
         'tags': '核心,战略', 'cooperation_status': '合作中', 'phone': '010-66666666',
         'visit_frequency': '每月', 'approval_status': 'approved',
         'license_name': '北京启光酒业有限公司', 'operator': '张总',
         'receiver_name': '李经理', 'receiver_phone': '13500135001',
         'receiver_address': '北京市朝阳区XX路XX号', 'detail_address': '仓库1号门',
         'contact_name': '王助理', 'contact_phone': '13500135002'},
        {'name': '上海浦东贸易公司', 'code': 'D002', 'type': '一级经销商', 'level': 'A',
         'manager_id': users[2].id, 'sales_area': '华东',
         'tags': '优质', 'cooperation_status': '合作中', 'phone': '021-55555555',
         'visit_frequency': '每月', 'approval_status': 'approved',
         'license_name': '上海浦东贸易有限公司', 'operator': '陈总',
         'receiver_name': '张经理', 'receiver_phone': '13500135003',
         'receiver_address': '上海市浦东新区XX路XX号', 'detail_address': '物流中心'},
        {'name': '广州粤商酒业', 'code': 'D003', 'type': '二级经销商', 'level': 'B',
         'manager_id': users[3].id, 'sales_area': '华南',
         'tags': '潜力', 'cooperation_status': '合作中', 'phone': '020-44444444',
         'visit_frequency': '每两月', 'approval_status': 'approved',
         'license_name': '广州粤商酒业有限公司', 'operator': '林总',
         'receiver_name': '黄经理', 'receiver_phone': '13500135004',
         'receiver_address': '广州市天河区XX路XX号', 'detail_address': '后门仓库'},
    ]
    
    distributors = []
    for data in distributors_data:
        data['created_by'] = users[2].id
        distributor = DirectDistributor(**data)
        db.session.add(distributor)
        distributors.append(distributor)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(distributors)} 个直营商客户")
    return distributors


def create_kols(users):
    """创建KOL客户"""
    print("\n创建KOL客户...")
    
    kols_data = [
        {'code': 'KOL001', 'name': '张大厨', 'consumer_type': '餐饮业主', 'gender': '男',
         'phone': '13311113333', 'age_group': '35-40', 'kol_tags': '餐饮,高端',
         'location': '北京', 'profession': '餐厅老板', 'drinking_frequency': '经常',
         'drinking_scene': '商务宴请', 'cooperation_status': '合作中', 'manager_id': users[2].id,
         'province': '北京市', 'city': '北京市', 'district': '朝阳区',
         'detail_address': '三里屯XX路XX号', 'receiver_name': '张大厨',
         'receiver_phone': '13311113333', 'receiver_address': '北京市朝阳区三里屯XX路XX号'},
        {'code': 'KOL002', 'name': '李美酒', 'consumer_type': '红酒爱好者', 'gender': '女',
         'phone': '13822228888', 'age_group': '30-35', 'kol_tags': '品酒师,社交',
         'location': '上海', 'profession': '品酒师', 'drinking_frequency': '经常',
         'drinking_scene': '品鉴会', 'cooperation_status': '合作中', 'manager_id': users[2].id,
         'province': '上海市', 'city': '上海市', 'district': '黄浦区',
         'detail_address': '南京西路XX号', 'receiver_name': '李美酒',
         'receiver_phone': '13822228888', 'receiver_address': '上海市黄浦区南京西路XX号'},
        {'code': 'KOL003', 'name': '王企业家', 'consumer_type': '企业家', 'gender': '男',
         'phone': '13933339999', 'age_group': '45-50', 'kol_tags': '高端,商务',
         'location': '深圳', 'profession': '企业家', 'drinking_frequency': '经常',
         'drinking_scene': '商务接待', 'cooperation_status': '合作中', 'manager_id': users[3].id,
         'province': '广东省', 'city': '深圳市', 'district': '福田区',
         'detail_address': '深南大道XX号', 'receiver_name': '王助理',
         'receiver_phone': '13933339998', 'receiver_address': '深圳市福田区深南大道XX号'},
        {'code': 'KOL004', 'name': '赵收藏家', 'consumer_type': '收藏家', 'gender': '男',
         'phone': '13644445555', 'age_group': '50-55', 'kol_tags': '收藏,高端',
         'location': '广州', 'profession': '收藏家', 'drinking_frequency': '偶尔',
         'drinking_scene': '收藏品鉴', 'cooperation_status': '合作中', 'manager_id': users[2].id,
         'province': '广东省', 'city': '广州市', 'district': '天河区',
         'detail_address': '珠江新城XX路XX号', 'receiver_name': '赵收藏家',
         'receiver_phone': '13644445555', 'receiver_address': '广州市天河区珠江新城XX路XX号'},
    ]
    
    kols = []
    for data in kols_data:
        data['created_by'] = users[2].id
        kol = KOL(**data)
        db.session.add(kol)
        kols.append(kol)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(kols)} 个KOL客户")
    return kols


def create_customer_contacts(terminals, distributors, kols):
    """创建客户联系人"""
    print("\n创建客户联系人...")
    
    contacts = []
    
    # 为终端创建联系人
    for i, terminal in enumerate(terminals[:3]):
        contact1 = CustomerContact(
            customer_type='terminal',
            customer_id=terminal.id,
            name=f'联系人{i*2+1}',
            phone=f'139{i:04d}0001',
            is_primary=True,
            position='采购经理'
        )
        contact2 = CustomerContact(
            customer_type='terminal',
            customer_id=terminal.id,
            name=f'联系人{i*2+2}',
            phone=f'139{i:04d}0002',
            is_primary=False,
            position='收货员'
        )
        db.session.add(contact1)
        db.session.add(contact2)
        contacts.extend([contact1, contact2])
    
    # 为直营商创建联系人
    for i, distributor in enumerate(distributors):
        contact = CustomerContact(
            customer_type='distributor',
            customer_id=distributor.id,
            name=f'经销商联系人{i+1}',
            phone=f'138{i:04d}0001',
            is_primary=True,
            position='业务经理'
        )
        db.session.add(contact)
        contacts.append(contact)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(contacts)} 个客户联系人")
    return contacts


def create_purchase_orders(suppliers, warehouses, products, users):
    """创建采购订单"""
    print("\n创建采购订单...")
    
    purchase_orders = []
    
    for i in range(5):
        supplier = suppliers[i % len(suppliers)]
        warehouse = warehouses[i % len(warehouses)]
        
        # 随机选择3-5个商品
        selected_products = random.sample([p for p in products if p.type == 'own'], random.randint(3, 5))
        items = []
        total_amount = 0
        
        for product in selected_products:
            quantity = random.randint(50, 200)
            price = product.cost
            subtotal = quantity * price
            total_amount += subtotal
            
            items.append({
                'product_id': product.id,
                'product_code': product.code,
                'product_name': product.name,
                'specification': product.specification,
                'unit': product.unit,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        
        order_date = date.today() - timedelta(days=random.randint(1, 60))
        
        purchase_order = PurchaseOrder(
            order_no=f'PO{datetime.now().strftime("%Y%m%d")}{i+1:04d}',
            supplier_id=supplier.id,
            supplier_name=supplier.name,
            document_date=order_date,
            warehouse_id=warehouse.id,
            warehouse_name=warehouse.name,
            handler=users[4].name,
            items=json.dumps(items),
            total_amount=total_amount,
            status='approved' if i < 4 else 'pending',
            approval_status='approved' if i < 4 else 'pending',
            approved_by=users[1].id if i < 4 else None,
            approved_at=datetime.now() - timedelta(days=random.randint(1, 30)) if i < 4 else None,
            created_by=users[4].id
        )
        
        db.session.add(purchase_order)
        purchase_orders.append(purchase_order)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(purchase_orders)} 个采购订单")
    return purchase_orders


def create_inventories(warehouses, products, purchase_orders):
    """创建库存记录"""
    print("\n创建库存记录...")
    
    inventories = []
    
    # 为每个仓库的自有商品创建库存
    for warehouse in warehouses:
        for product in products:
            if product.type == 'own':
                # 基础库存
                quantity = random.randint(100, 1000)
                
                inventory = Inventory(
                    warehouse_id=warehouse.id,
                    warehouse_name=warehouse.name,
                    warehouse_type=warehouse.warehouse_type,
                    product_id=product.id,
                    quantity=quantity,
                    cost=product.cost,
                    total_cost=product.cost * quantity,
                    min_stock=50,
                    max_stock=2000
                )
                
                db.session.add(inventory)
                inventories.append(inventory)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(inventories)} 条库存记录")
    return inventories


def create_sales_orders(terminals, distributors, kols, warehouses, products, users):
    """创建销售订单"""
    print("\n创建销售订单...")
    
    sales_orders = []
    
    # 创建终端客户订单
    for i, terminal in enumerate(terminals):
        selected_products = random.sample([p for p in products if p.type == 'own'], random.randint(2, 4))
        items = []
        total_amount = 0
        
        for product in selected_products:
            quantity = random.randint(10, 50)
            price = product.price
            subtotal = quantity * price
            total_amount += subtotal
            
            items.append({
                'product_id': product.id,
                'product_code': product.code,
                'product_name': product.name,
                'specification': product.specification,
                'unit': product.unit,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        
        discount = total_amount * random.uniform(0.05, 0.15)
        final_amount = total_amount - discount
        
        order_date = datetime.now() - timedelta(days=random.randint(1, 30))
        delivery_date = order_date.date() + timedelta(days=random.randint(3, 7))
        
        status_choice = ['approved', 'pending', 'delivered'][i % 3]
        
        order = SalesOrder(
            order_no=f'SO{datetime.now().strftime("%Y%m%d")}T{i+1:04d}',
            customer_type='terminal',
            customer_id=terminal.id,
            customer_name=terminal.name,
            receiver_address=terminal.receiver_address,
            warehouse=warehouses[i % len(warehouses)].name,
            total_amount=total_amount,
            discount_amount=discount,
            final_amount=final_amount,
            items=json.dumps(items),
            order_date=order_date,
            delivery_date=delivery_date,
            status=status_choice,
            approval_status='approved' if status_choice != 'pending' else 'pending',
            approved_by=users[1].id if status_choice != 'pending' else None,
            approved_at=order_date + timedelta(hours=2) if status_choice != 'pending' else None,
            salesman_id=users[5].id,
            created_by=users[5].id
        )
        
        db.session.add(order)
        sales_orders.append(order)
    
    # 创建直营商订单
    for i, distributor in enumerate(distributors):
        selected_products = random.sample([p for p in products if p.type == 'own'], random.randint(3, 5))
        items = []
        total_amount = 0
        
        for product in selected_products:
            quantity = random.randint(50, 200)
            price = product.price * 0.85  # 批发价
            subtotal = quantity * price
            total_amount += subtotal
            
            items.append({
                'product_id': product.id,
                'product_code': product.code,
                'product_name': product.name,
                'specification': product.specification,
                'unit': product.unit,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        
        discount = total_amount * 0.05
        final_amount = total_amount - discount
        
        order_date = datetime.now() - timedelta(days=random.randint(1, 20))
        delivery_date = order_date.date() + timedelta(days=random.randint(5, 10))
        
        order = SalesOrder(
            order_no=f'SO{datetime.now().strftime("%Y%m%d")}D{i+1:04d}',
            customer_type='distributor',
            customer_id=distributor.id,
            customer_name=distributor.name,
            receiver_address=distributor.receiver_address,
            warehouse=warehouses[0].name,
            total_amount=total_amount,
            discount_amount=discount,
            final_amount=final_amount,
            items=json.dumps(items),
            order_date=order_date,
            delivery_date=delivery_date,
            status='approved',
            approval_status='approved',
            approved_by=users[1].id,
            approved_at=order_date + timedelta(hours=1),
            salesman_id=users[5].id,
            created_by=users[5].id
        )
        
        db.session.add(order)
        sales_orders.append(order)
    
    # 创建KOL订单
    for i, kol in enumerate(kols):
        selected_products = random.sample([p for p in products if p.type == 'own'], random.randint(1, 3))
        items = []
        total_amount = 0
        
        for product in selected_products:
            quantity = random.randint(5, 20)
            price = product.price
            subtotal = quantity * price
            total_amount += subtotal
            
            items.append({
                'product_id': product.id,
                'product_code': product.code,
                'product_name': product.name,
                'specification': product.specification,
                'unit': product.unit,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        
        order_date = datetime.now() - timedelta(days=random.randint(1, 15))
        delivery_date = order_date.date() + timedelta(days=random.randint(2, 5))
        
        order = SalesOrder(
            order_no=f'SO{datetime.now().strftime("%Y%m%d")}K{i+1:04d}',
            customer_type='kol',
            customer_id=kol.id,
            customer_name=kol.name,
            receiver_address=kol.receiver_address,
            warehouse=warehouses[i % len(warehouses)].name,
            total_amount=total_amount,
            discount_amount=0,
            final_amount=total_amount,
            items=json.dumps(items),
            order_date=order_date,
            delivery_date=delivery_date,
            status='delivered',
            approval_status='approved',
            approved_by=users[1].id,
            approved_at=order_date + timedelta(hours=1),
            salesman_id=users[6].id,
            created_by=users[6].id
        )
        
        db.session.add(order)
        sales_orders.append(order)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(sales_orders)} 个销售订单")
    return sales_orders


def create_delivery_orders(sales_orders, users):
    """创建发货订单"""
    print("\n创建发货订单...")
    
    delivery_orders = []
    
    # 为已审批的销售订单创建发货单
    approved_orders = [o for o in sales_orders if o.approval_status == 'approved']
    
    for i, sales_order in enumerate(approved_orders[:8]):
        items_data = json.loads(sales_order.items)
        
        delivery_order = DeliveryOrder(
            order_no=f'DO{datetime.now().strftime("%Y%m%d")}{i+1:04d}',
            sales_order_id=sales_order.id,
            sales_order_no=sales_order.order_no,
            customer_name=sales_order.customer_name,
            receiver_address=sales_order.receiver_address,
            warehouse=sales_order.warehouse,
            total_amount=sales_order.final_amount,
            items=sales_order.items,
            order_date=sales_order.order_date,
            delivery_date=sales_order.delivery_date,
            status='shipped' if i < 5 else 'pending',
            shipped_by=users[4].id if i < 5 else None,
            shipped_at=sales_order.order_date + timedelta(days=1) if i < 5 else None,
            salesman_id=sales_order.salesman_id
        )
        
        db.session.add(delivery_order)
        delivery_orders.append(delivery_order)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(delivery_orders)} 个发货订单")
    return delivery_orders


def create_return_orders(sales_orders, users):
    """创建退货订单"""
    print("\n创建退货订单...")
    
    return_orders = []
    
    # 为部分已发货订单创建退货单
    delivered_orders = [o for o in sales_orders if o.status == 'delivered']
    
    for i, sales_order in enumerate(delivered_orders[:3]):
        items_data = json.loads(sales_order.items)
        
        # 退部分商品
        return_items = []
        total_amount = 0
        
        for item in items_data[:2]:  # 只退前2个商品
            return_quantity = random.randint(1, item['quantity'] // 2)
            subtotal = return_quantity * item['price']
            total_amount += subtotal
            
            return_items.append({
                **item,
                'quantity': return_quantity,
                'subtotal': subtotal
            })
        
        return_date = sales_order.order_date + timedelta(days=random.randint(10, 30))
        
        status = ['pending', 'approved', 'confirmed'][i % 3]
        
        return_order = ReturnOrder(
            order_no=f'RO{datetime.now().strftime("%Y%m%d")}{i+1:04d}',
            return_type='sales_order',
            sales_order_id=sales_order.id,
            customer_type=sales_order.customer_type,
            customer_id=sales_order.customer_id,
            customer_name=sales_order.customer_name,
            receiver_address=sales_order.receiver_address,
            warehouse=sales_order.warehouse,
            total_amount=total_amount,
            items=json.dumps(return_items),
            return_reason='商品质量问题',
            order_date=return_date,
            status=status,
            approval_status='approved' if status != 'pending' else 'pending',
            approved_by=users[1].id if status != 'pending' else None,
            approved_at=return_date + timedelta(hours=3) if status != 'pending' else None,
            received_by=users[4].id if status == 'confirmed' else None,
            received_at=return_date + timedelta(days=2) if status == 'confirmed' else None,
            salesman_id=sales_order.salesman_id,
            created_by=sales_order.salesman_id
        )
        
        db.session.add(return_order)
        return_orders.append(return_order)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(return_orders)} 个退货订单")
    return return_orders


def create_visit_plans(terminals, distributors, kols, users):
    """创建拜访计划"""
    print("\n创建拜访计划...")
    
    visit_plans = []
    
    # 创建未来的拜访计划
    customers = [
        ('terminal', t.id, t.name) for t in terminals[:3]
    ] + [
        ('distributor', d.id, d.name) for d in distributors[:2]
    ] + [
        ('kol', k.id, k.name) for k in kols[:2]
    ]
    
    for i, (customer_type, customer_id, customer_name) in enumerate(customers):
        visit_date = date.today() + timedelta(days=random.randint(1, 14))
        
        plan = VisitPlan(
            visitor_id=users[5].id if i < 4 else users[6].id,
            customer_type=customer_type,
            customer_id=customer_id,
            customer_name=customer_name,
            visit_date=visit_date,
            start_time=time(9, 0),
            end_time=time(11, 0),
            plan_content=f'拜访{customer_name}，了解近期销售情况和库存状态',
            status='approved' if i < 5 else 'pending',
            approval_status='approved' if i < 5 else 'pending',
            created_by=users[5].id if i < 4 else users[6].id
        )
        
        db.session.add(plan)
        visit_plans.append(plan)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(visit_plans)} 个拜访计划")
    return visit_plans


def create_visit_routes(terminals, users):
    """创建拜访路线"""
    print("\n创建拜访路线...")
    
    visit_routes = []
    
    # 创建2条拜访路线
    route1_customers = [
        {'customer_type': 'terminal', 'customer_id': terminals[0].id, 'customer_name': terminals[0].name, 'order': 1},
        {'customer_type': 'terminal', 'customer_id': terminals[1].id, 'customer_name': terminals[1].name, 'order': 2},
        {'customer_type': 'terminal', 'customer_id': terminals[2].id, 'customer_name': terminals[2].name, 'order': 3},
    ]
    
    route1 = VisitRoute(
        name='华北区域拜访路线',
        visitor_id=users[5].id,
        customer_list=json.dumps(route1_customers),
        route_details=json.dumps({'total_distance': '15.8km', 'estimated_time': '3小时'}),
        remark='周一固定路线',
        approval_status='approved',
        approved_by=users[1].id,
        approved_at=datetime.now() - timedelta(days=7),
        created_by=users[5].id
    )
    
    route2_customers = [
        {'customer_type': 'terminal', 'customer_id': terminals[3].id, 'customer_name': terminals[3].name, 'order': 1},
        {'customer_type': 'terminal', 'customer_id': terminals[4].id, 'customer_name': terminals[4].name, 'order': 2},
    ]
    
    route2 = VisitRoute(
        name='华南区域拜访路线',
        visitor_id=users[6].id,
        customer_list=json.dumps(route2_customers),
        route_details=json.dumps({'total_distance': '22.5km', 'estimated_time': '4小时'}),
        remark='周三固定路线',
        approval_status='pending',
        created_by=users[6].id
    )
    
    db.session.add(route1)
    db.session.add(route2)
    visit_routes.extend([route1, route2])
    
    db.session.commit()
    print(f"[OK] 创建了 {len(visit_routes)} 个拜访路线")
    return visit_routes


def create_visit_records(terminals, products, users):
    """创建拜访记录"""
    print("\n创建拜访记录...")
    
    visit_records = []
    
    # 创建历史拜访记录
    for i, terminal in enumerate(terminals[:4]):
        # 每个客户创建2-3条历史记录
        for j in range(random.randint(2, 3)):
            visit_date = datetime.now() - timedelta(days=random.randint(1, 30))
            
            # 铺货商品列表
            distribution_list = []
            for product in random.sample([p for p in products if p.is_display], 3):
                distribution_list.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'brand': product.brand,
                    'has_display': random.choice([True, False])
                })
            
            # 库存列表
            inventory_list = []
            for product in random.sample([p for p in products if p.type == 'own'], 3):
                inventory_list.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'quantity': random.randint(10, 100)
                })
            
            # 竞品列表
            competitor_list = []
            for product in random.sample([p for p in products if p.type == 'competitor'], 2):
                competitor_list.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'brand': product.brand,
                    'price': product.price
                })
            
            record = VisitRecord(
                visitor_id=users[5].id if i < 2 else users[6].id,
                customer_type='terminal',
                customer_id=terminal.id,
                customer_name=terminal.name,
                customer_address=terminal.receiver_address,
                visit_frequency=terminal.visit_frequency,
                visit_type='planned',
                visit_content=f'本次拜访主要了解了{terminal.name}的销售情况，现场检查了商品陈列。',
                checkin_time=visit_date,
                checkin_latitude=39.9 + random.random() * 0.1,
                checkin_longitude=116.3 + random.random() * 0.1,
                checkin_address=terminal.receiver_address,
                checkout_time=visit_date + timedelta(hours=1, minutes=random.randint(30, 90)),
                checkout_latitude=39.9 + random.random() * 0.1,
                checkout_longitude=116.3 + random.random() * 0.1,
                checkout_address=terminal.receiver_address,
                product_distribution_list=json.dumps(distribution_list),
                distribution_remark='陈列情况良好',
                inventory_list=json.dumps(inventory_list),
                inventory_remark='库存正常',
                competitor_list=json.dumps(competitor_list),
                competitor_remark='竞品价格略高于我司',
                created_at=visit_date
            )
            
            db.session.add(record)
            visit_records.append(record)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(visit_records)} 个拜访记录")
    return visit_records


def create_activities(users):
    """创建活动"""
    print("\n创建活动...")
    
    activities_data = [
        {'name': '春节促销活动', 'description': '春节期间针对茅台系列产品的促销活动', 'status': 'active'},
        {'name': '中秋品鉴会', 'description': '中秋节高端客户品鉴会活动', 'status': 'active'},
        {'name': '国庆特惠', 'description': '国庆期间特惠活动', 'status': 'active'},
        {'name': '双十一狂欢', 'description': '双十一线上线下同步促销', 'status': 'inactive'},
    ]
    
    activities = []
    for data in activities_data:
        activity = Activity(
            name=data['name'],
            description=data['description'],
            status=data['status'],
            created_by=users[7].id
        )
        db.session.add(activity)
        activities.append(activity)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(activities)} 个活动")
    return activities


def create_activity_reports(activities, terminals, distributors, users):
    """创建活动上报"""
    print("\n创建活动上报...")
    
    reports = []
    
    # 为前3个活动创建上报记录
    for activity in activities[:3]:
        # 终端客户参与
        for i, terminal in enumerate(terminals[:3]):
            report = ActivityReport(
                activity_id=activity.id,
                customer_name=terminal.name,
                customer_type='terminal',
                customer_id=terminal.id,
                report_status=['pending', 'approved', 'approved'][i % 3],
                remark=f'{terminal.name}参与{activity.name}',
                reported_by=users[5].id
            )
            db.session.add(report)
            reports.append(report)
        
        # 直营商参与
        for i, distributor in enumerate(distributors[:2]):
            report = ActivityReport(
                activity_id=activity.id,
                customer_name=distributor.name,
                customer_type='distributor',
                customer_id=distributor.id,
                report_status='approved',
                remark=f'{distributor.name}参与{activity.name}',
                reported_by=users[5].id
            )
            db.session.add(report)
            reports.append(report)
    
    db.session.commit()
    print(f"[OK] 创建了 {len(reports)} 条活动上报记录")
    return reports


def main():
    """主函数"""
    import sys
    
    print("=" * 60)
    print("DeepVisit 测试数据填充脚本")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # 检查是否有命令行参数跳过确认
        skip_confirm = '--yes' in sys.argv or '-y' in sys.argv
        
        if not skip_confirm:
            # 询问是否清空现有数据
            print("\n[警告] 此操作将清空数据库中的所有数据！")
            try:
                confirm = input("确认要继续吗？(输入 yes 确认): ")
            except EOFError:
                print("\n检测到非交互模式，使用 --yes 或 -y 参数来自动确认")
                return
            
            if confirm.lower() != 'yes':
                print("操作已取消")
                return
        else:
            print("\n[自动确认] 将清空并重新填充数据...")
        
        try:
            # 清空数据
            clear_all_data()
            
            # 按顺序创建数据
            roles = create_roles()
            users = create_users(roles)
            products = create_products()
            warehouses = create_warehouses()
            suppliers = create_suppliers()
            
            terminals = create_terminals(users)
            distributors = create_distributors(users)
            kols = create_kols(users)
            
            create_customer_contacts(terminals, distributors, kols)
            
            purchase_orders = create_purchase_orders(suppliers, warehouses, products, users)
            inventories = create_inventories(warehouses, products, purchase_orders)
            
            sales_orders = create_sales_orders(terminals, distributors, kols, warehouses, products, users)
            delivery_orders = create_delivery_orders(sales_orders, users)
            return_orders = create_return_orders(sales_orders, users)
            
            visit_plans = create_visit_plans(terminals, distributors, kols, users)
            visit_routes = create_visit_routes(terminals, users)
            visit_records = create_visit_records(terminals, products, users)
            
            activities = create_activities(users)
            activity_reports = create_activity_reports(activities, terminals, distributors, users)
            
            print("\n" + "=" * 60)
            print("[完成] 测试数据填充完成！")
            print("=" * 60)
            print("\n登录信息：")
            print("  用户名: admin")
            print("  密码: 123456")
            print("\n其他测试用户：")
            print("  manager1, account1, account2, warehouse1, sales1, sales2, market1")
            print("  密码都是: 123456")
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"\n[错误] {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == '__main__':
    main()

