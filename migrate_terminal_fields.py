#!/usr/bin/env python3
"""
终端客户字段迁移脚本
在pyenv deepvisit虚拟环境下运行此脚本
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import Terminal

def migrate_terminal_fields():
    """迁移终端客户字段"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否需要添加新字段
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('terminals')]
            
            print("现有字段:", existing_columns)
            
            # 需要添加的新字段
            new_fields = [
                'receiver_name',      # 收货人姓名
                'receiver_phone',     # 收货人手机号
                'receiver_address',  # 收货地址
                'detail_address',     # 详细地址
                'contact_name',       # 联系人姓名
                'contact_phone',      # 联系人手机号
            ]
            
            # 检查并添加缺失的字段
            for field in new_fields:
                if field not in existing_columns:
                    print(f"添加字段: {field}")
                    if field in ['receiver_name', 'contact_name']:
                        db.engine.execute(f"ALTER TABLE terminals ADD COLUMN {field} VARCHAR(64)")
                    elif field in ['receiver_phone', 'contact_phone']:
                        db.engine.execute(f"ALTER TABLE terminals ADD COLUMN {field} VARCHAR(20)")
                    elif field in ['receiver_address', 'detail_address']:
                        db.engine.execute(f"ALTER TABLE terminals ADD COLUMN {field} VARCHAR(256)")
            
            # 检查字段顺序和注释
            print("字段迁移完成!")
            
            # 显示当前表结构
            print("\n当前终端客户表结构:")
            columns = inspector.get_columns('terminals')
            for col in columns:
                print(f"  {col['name']}: {col['type']}")
                
        except Exception as e:
            print(f"迁移过程中出现错误: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("开始迁移终端客户字段...")
    print("请确保在pyenv deepvisit虚拟环境下运行此脚本")
    
    success = migrate_terminal_fields()
    
    if success:
        print("\n✅ 字段迁移成功完成!")
        print("现在可以启动应用程序测试新字段功能")
    else:
        print("\n❌ 字段迁移失败，请检查错误信息")
        sys.exit(1)
