#!/usr/bin/env python3
"""
直营商字段迁移脚本
在pyenv deepvisit虚拟环境下运行此脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import DirectDistributor

def migrate_distributor_fields():
    """迁移直营商字段"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否需要添加新字段
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('direct_distributors')]
            
            print("现有字段:", existing_columns)
            
            # 需要添加的新字段
            new_fields = [
                'sales_area',         # 销售区域
                'tags',              # 直营商标签
                'supplier',          # 供货商
                'remark',            # 备注
                'visit_frequency',   # 拜访频率
                'approval_status',   # 审批状态
                'business_license',  # 营业执照
                'license_name',      # 营业执照名称
                'registration_no',   # 工商注册号
                'registration_date', # 注册日期
                'operator',          # 经营者
                'receiver_name',     # 收货人姓名
                'receiver_phone',    # 收货人手机号
                'receiver_address',  # 收货地址
                'detail_address',    # 详细地址
                'contact_name',       # 联系人姓名
                'contact_phone',     # 联系人手机号
            ]
            
            # 检查并添加缺失的字段
            for field in new_fields:
                if field not in existing_columns:
                    print(f"添加字段: {field}")
                    if field in ['sales_area', 'tags', 'supplier', 'remark', 'visit_frequency', 'approval_status', 'business_license', 'license_name', 'registration_no', 'operator', 'receiver_name', 'receiver_address', 'detail_address', 'contact_name']:
                        if field == 'remark':
                            db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} TEXT")
                        elif field in ['tags', 'business_license', 'receiver_address', 'detail_address']:
                            db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} VARCHAR(256)")
                        elif field in ['sales_area', 'visit_frequency', 'approval_status', 'license_name', 'operator', 'receiver_name', 'contact_name']:
                            db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} VARCHAR(64)")
                        elif field in ['supplier']:
                            db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} VARCHAR(128)")
                        elif field in ['registration_no']:
                            db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} VARCHAR(64)")
                    elif field in ['receiver_phone', 'contact_phone']:
                        db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} VARCHAR(20)")
                    elif field == 'registration_date':
                        db.engine.execute(f"ALTER TABLE direct_distributors ADD COLUMN {field} DATE")
            
            # 检查字段顺序和注释
            print("字段迁移完成!")
            
            # 显示当前表结构
            print("\n当前直营商表结构:")
            columns = inspector.get_columns('direct_distributors')
            for col in columns:
                print(f"  {col['name']}: {col['type']}")
                
        except Exception as e:
            print(f"迁移过程中出现错误: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("开始迁移直营商字段...")
    print("请确保在pyenv deepvisit虚拟环境下运行此脚本")
    
    success = migrate_distributor_fields()
    
    if success:
        print("\n✅ 字段迁移成功完成!")
        print("现在可以启动应用程序测试新字段功能")
    else:
        print("\n❌ 字段迁移失败，请检查错误信息")
        sys.exit(1)
