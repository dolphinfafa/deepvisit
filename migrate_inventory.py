#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理模块数据库迁移脚本
创建新的数据表：suppliers, warehouses, purchase_orders
更新 inventories 表结构
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import *

def create_tables():
    """创建新的数据表"""
    print("创建新的数据表...")
    
    # 创建供应商表
    db.create_all()
    
    print("数据表创建完成！")

def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    # 创建示例供应商
    suppliers = [
        {
            'code': 'SUP001',
            'name': '启光供应商A',
            'contact_person': '张三',
            'phone': '13800138001',
            'email': 'zhangsan@example.com',
            'address': '北京市朝阳区xxx路xxx号',
            'credit_limit': 100000
        },
        {
            'code': 'SUP002', 
            'name': '启光供应商B',
            'contact_person': '李四',
            'phone': '13800138002',
            'email': 'lisi@example.com',
            'address': '上海市浦东新区xxx路xxx号',
            'credit_limit': 200000
        }
    ]
    
    for supplier_data in suppliers:
        supplier = Supplier(**supplier_data)
        db.session.add(supplier)
    
    # 创建示例仓库
    warehouses = [
        {
            'code': 'WH001',
            'name': '启光仓库A',
            'warehouse_type': 'qiguang',
            'address': '北京市朝阳区仓库区1号',
            'manager': '王五',
            'phone': '13800138003',
            'capacity': 1000
        },
        {
            'code': 'WH002',
            'name': '启光仓库B', 
            'warehouse_type': 'qiguang',
            'address': '北京市朝阳区仓库区2号',
            'manager': '赵六',
            'phone': '13800138004',
            'capacity': 1500
        },
        {
            'code': 'WH003',
            'name': '直营商仓库A',
            'warehouse_type': 'direct_sales',
            'address': '上海市浦东新区直营区1号',
            'manager': '孙七',
            'phone': '13800138005',
            'capacity': 800
        },
        {
            'code': 'WH004',
            'name': '直营商仓库B',
            'warehouse_type': 'direct_sales', 
            'address': '上海市浦东新区直营区2号',
            'manager': '周八',
            'phone': '13800138006',
            'capacity': 1200
        }
    ]
    
    for warehouse_data in warehouses:
        warehouse = Warehouse(**warehouse_data)
        db.session.add(warehouse)
    
    db.session.commit()
    print("示例数据创建完成！")

def main():
    """主函数"""
    app = create_app()
    
    with app.app_context():
        try:
            create_tables()
            create_sample_data()
            print("数据库迁移完成！")
        except Exception as e:
            print(f"数据库迁移失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    main()

