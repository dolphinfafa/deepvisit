#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据上报模块数据库迁移脚本

此脚本用于创建数据上报模块的数据库表：
- display_reports: 铺货上报表
- inventory_reports: 库存上报表
- competitor_reports: 竞品上报表
"""

import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.data_report import DisplayReport, InventoryReport, CompetitorReport

def migrate():
    """执行迁移"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("数据上报模块数据库迁移")
        print("=" * 60)
        
        # 检查表是否已存在
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        tables_to_create = []
        
        if 'display_reports' not in existing_tables:
            tables_to_create.append('display_reports (铺货上报)')
        
        if 'inventory_reports' not in existing_tables:
            tables_to_create.append('inventory_reports (库存上报)')
        
        if 'competitor_reports' not in existing_tables:
            tables_to_create.append('competitor_reports (竞品上报)')
        
        if not tables_to_create:
            print("\n[OK] 所有数据上报表已存在，无需迁移")
            return
        
        print("\n准备创建以下数据表：")
        for table in tables_to_create:
            print(f"  - {table}")
        
        try:
            # 创建数据表
            print("\n开始创建数据表...")
            db.create_all()
            print("[OK] 数据表创建成功！")
            
            # 显示表结构
            print("\n" + "=" * 60)
            print("数据表结构")
            print("=" * 60)
            
            if 'display_reports' in [t for t in tables_to_create]:
                print("\n1. 铺货上报表 (display_reports)：")
                print("   - id: 主键")
                print("   - report_code: 上报编码")
                print("   - report_date: 上报日期")
                print("   - customer_name: 客户名称")
                print("   - customer_type: 客户类型")
                print("   - customer_level: 客户等级")
                print("   - customer_manager: 客户经理")
                print("   - product_code: 商品编码")
                print("   - product_name: 商品名称")
                print("   - specification: 规格")
                print("   - product_type: 商品类型")
                print("   - brand: 品牌")
                print("   - reported_by: 上报人ID")
                print("   - remark: 备注")
                print("   - created_at: 创建时间")
                print("   - updated_at: 更新时间")
            
            if 'inventory_reports' in [t for t in tables_to_create]:
                print("\n2. 库存上报表 (inventory_reports)：")
                print("   - id: 主键")
                print("   - report_code: 上报编码")
                print("   - customer_name: 客户名称")
                print("   - product_name: 商品名称")
                print("   - specification: 规格")
                print("   - product_code: 商品编码")
                print("   - quantity: 库存数量")
                print("   - remark: 备注")
                print("   - reported_by: 上报人ID")
                print("   - report_time: 上报时间")
                print("   - created_at: 创建时间")
                print("   - updated_at: 更新时间")
            
            if 'competitor_reports' in [t for t in tables_to_create]:
                print("\n3. 竞品上报表 (competitor_reports)：")
                print("   - id: 主键")
                print("   - report_code: 上报编码")
                print("   - competitor_name: 竞品名称")
                print("   - product_name: 商品名称（我方商品）")
                print("   - remark: 备注")
                print("   - reported_by: 上报人ID")
                print("   - report_time: 上报时间")
                print("   - created_at: 创建时间")
                print("   - updated_at: 更新时间")
            
            print("\n" + "=" * 60)
            print("[SUCCESS] 数据上报模块迁移完成！")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[ERROR] 迁移失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    migrate()

