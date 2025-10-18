#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库字段迁移脚本
添加表格字段精简后需要的新字段
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import KOL
from app.models.visit import VisitPlan, VisitRecord
from app.models.inventory import Inventory
from app.models.order import SalesOrder, ReturnOrder, DeliveryOrder
from sqlalchemy import text

def add_missing_fields():
    """添加缺失的数据库字段"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始添加缺失的数据库字段...")
            
            # 添加KOL表的缺失字段
            print("添加KOL表缺失字段...")
            try:
                # 添加街道字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE kols ADD COLUMN street VARCHAR(128)"))
                    conn.commit()
                print("✓ 添加KOL.street字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ KOL.street字段已存在")
                else:
                    print(f"✗ 添加KOL.street字段失败: {e}")
            
            try:
                # 添加个人爱好字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE kols ADD COLUMN hobbies VARCHAR(256)"))
                    conn.commit()
                print("✓ 添加KOL.hobbies字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ KOL.hobbies字段已存在")
                else:
                    print(f"✗ 添加KOL.hobbies字段失败: {e}")
            
            try:
                # 添加备注字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE kols ADD COLUMN remark TEXT"))
                    conn.commit()
                print("✓ 添加KOL.remark字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ KOL.remark字段已存在")
                else:
                    print(f"✗ 添加KOL.remark字段失败: {e}")
            
            # 添加VisitPlan表的缺失字段
            print("添加VisitPlan表缺失字段...")
            try:
                # 添加客户编码字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_plans ADD COLUMN customer_code VARCHAR(64)"))
                    conn.commit()
                print("✓ 添加VisitPlan.customer_code字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitPlan.customer_code字段已存在")
                else:
                    print(f"✗ 添加VisitPlan.customer_code字段失败: {e}")
            
            try:
                # 添加所属路线字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_plans ADD COLUMN route_name VARCHAR(128)"))
                    conn.commit()
                print("✓ 添加VisitPlan.route_name字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitPlan.route_name字段已存在")
                else:
                    print(f"✗ 添加VisitPlan.route_name字段失败: {e}")
            
            # 添加VisitRecord表的缺失字段
            print("添加VisitRecord表缺失字段...")
            try:
                # 添加客户经理字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_records ADD COLUMN customer_manager VARCHAR(64)"))
                    conn.commit()
                print("✓ 添加VisitRecord.customer_manager字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitRecord.customer_manager字段已存在")
                else:
                    print(f"✗ 添加VisitRecord.customer_manager字段失败: {e}")
            
            try:
                # 添加完成状态字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_records ADD COLUMN status VARCHAR(32) DEFAULT 'completed'"))
                    conn.commit()
                print("✓ 添加VisitRecord.status字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitRecord.status字段已存在")
                else:
                    print(f"✗ 添加VisitRecord.status字段失败: {e}")
            
            try:
                # 添加抵达距离偏差字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_records ADD COLUMN checkin_distance_deviation FLOAT"))
                    conn.commit()
                print("✓ 添加VisitRecord.checkin_distance_deviation字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitRecord.checkin_distance_deviation字段已存在")
                else:
                    print(f"✗ 添加VisitRecord.checkin_distance_deviation字段失败: {e}")
            
            try:
                # 添加离开距离偏差字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE visit_records ADD COLUMN checkout_distance_deviation FLOAT"))
                    conn.commit()
                print("✓ 添加VisitRecord.checkout_distance_deviation字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ VisitRecord.checkout_distance_deviation字段已存在")
                else:
                    print(f"✗ 添加VisitRecord.checkout_distance_deviation字段失败: {e}")
            
            # 添加Inventory表的缺失字段
            print("添加Inventory表缺失字段...")
            try:
                # 添加占用库存字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE inventories ADD COLUMN occupied_quantity INTEGER DEFAULT 0"))
                    conn.commit()
                print("✓ 添加Inventory.occupied_quantity字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ Inventory.occupied_quantity字段已存在")
                else:
                    print(f"✗ 添加Inventory.occupied_quantity字段失败: {e}")
            
            # 添加SalesOrder表的缺失字段
            print("添加SalesOrder表缺失字段...")
            try:
                # 添加原始金额字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE sales_orders ADD COLUMN original_amount FLOAT DEFAULT 0"))
                    conn.commit()
                print("✓ 添加SalesOrder.original_amount字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ SalesOrder.original_amount字段已存在")
                else:
                    print(f"✗ 添加SalesOrder.original_amount字段失败: {e}")
            
            # 添加ReturnOrder表的缺失字段
            print("添加ReturnOrder表缺失字段...")
            try:
                # 添加确认金额字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE return_orders ADD COLUMN confirmed_amount FLOAT DEFAULT 0"))
                    conn.commit()
                print("✓ 添加ReturnOrder.confirmed_amount字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ ReturnOrder.confirmed_amount字段已存在")
                else:
                    print(f"✗ 添加ReturnOrder.confirmed_amount字段失败: {e}")
            
            try:
                # 添加客户编码字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE return_orders ADD COLUMN customer_code VARCHAR(64)"))
                    conn.commit()
                print("✓ 添加ReturnOrder.customer_code字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ ReturnOrder.customer_code字段已存在")
                else:
                    print(f"✗ 添加ReturnOrder.customer_code字段失败: {e}")
            
            # 添加DeliveryOrder表的缺失字段
            print("添加DeliveryOrder表缺失字段...")
            try:
                # 添加备注字段
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE delivery_orders ADD COLUMN remark TEXT"))
                    conn.commit()
                print("✓ 添加DeliveryOrder.remark字段")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e) or "duplicate" in str(e).lower():
                    print("✓ DeliveryOrder.remark字段已存在")
                else:
                    print(f"✗ 添加DeliveryOrder.remark字段失败: {e}")
            
            # 提交所有更改
            db.session.commit()
            print("\n✓ 数据库字段迁移完成！")
            
        except Exception as e:
            print(f"\n✗ 数据库字段迁移失败: {e}")
            db.session.rollback()
            raise

def update_existing_data():
    """更新现有数据以适配新字段"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n开始更新现有数据...")
            
            # 更新VisitRecord的status字段
            print("更新VisitRecord状态...")
            with db.engine.connect() as conn:
                conn.execute(text("UPDATE visit_records SET status = 'completed' WHERE status IS NULL"))
                conn.commit()
            print("✓ 更新VisitRecord状态完成")
            
            # 更新Inventory的占用库存
            print("更新Inventory占用库存...")
            with db.engine.connect() as conn:
                conn.execute(text("UPDATE inventories SET occupied_quantity = 0 WHERE occupied_quantity IS NULL"))
                conn.commit()
            print("✓ 更新Inventory占用库存完成")
            
            # 更新SalesOrder的原始金额
            print("更新SalesOrder原始金额...")
            with db.engine.connect() as conn:
                conn.execute(text("UPDATE sales_orders SET original_amount = total_amount WHERE original_amount IS NULL"))
                conn.commit()
            print("✓ 更新SalesOrder原始金额完成")
            
            # 更新ReturnOrder的确认金额
            print("更新ReturnOrder确认金额...")
            with db.engine.connect() as conn:
                conn.execute(text("UPDATE return_orders SET confirmed_amount = total_amount WHERE confirmed_amount IS NULL"))
                conn.commit()
            print("✓ 更新ReturnOrder确认金额完成")
            
            print("\n✓ 现有数据更新完成！")
            
        except Exception as e:
            print(f"\n✗ 现有数据更新失败: {e}")
            raise

if __name__ == '__main__':
    print("=" * 50)
    print("数据库字段迁移脚本")
    print("=" * 50)
    
    # 添加缺失字段
    add_missing_fields()
    
    # 更新现有数据
    update_existing_data()
    
    print("\n" + "=" * 50)
    print("迁移完成！")
    print("=" * 50)
