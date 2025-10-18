#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
活动表迁移脚本
用于在现有数据库上添加新的活动字段
"""

import os
import sys
from datetime import datetime
import uuid
from sqlalchemy import text
from app import create_app, db

def migrate_activity_table():
    """迁移活动表"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始迁移活动表...")
            
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'activities' not in tables:
                print("活动表不存在，创建新表...")
                db.create_all()
                print("迁移完成！")
                return
            
            # 检查是否已经有新字段
            columns = [col['name'] for col in inspector.get_columns('activities')]
            
            if 'activity_code' in columns:
                print("活动表已经包含新字段，无需迁移")
                # 检查是否强制重建
                force_rebuild = '--force' in sys.argv
                if not force_rebuild:
                    print("如需重建表，请使用 --force 参数（警告：将删除所有活动数据）")
                    return
                else:
                    print("强制重建模式：删除并重建活动表...")
                    db.session.execute(text('DROP TABLE IF EXISTS activity_applications'))
                    db.session.execute(text('DROP TABLE IF EXISTS activity_reports'))
                    db.session.execute(text('DROP TABLE IF EXISTS activities'))
                    db.session.commit()
                    db.create_all()
                    print("表重建完成！")
                    return
            
            print("备份现有活动数据...")
            # 获取现有数据
            result = db.session.execute(text('SELECT * FROM activities'))
            activities = result.fetchall()
            print(f"找到 {len(activities)} 条活动记录")
            
            print("删除旧表...")
            # 删除相关表（注意外键顺序）
            db.session.execute(text('DROP TABLE IF EXISTS activity_reports'))
            db.session.execute(text('DROP TABLE IF EXISTS activities'))
            db.session.commit()
            
            print("创建新表结构...")
            # 创建新表
            db.create_all()
            
            print("恢复数据并生成活动编码...")
            # 恢复数据
            for activity in activities:
                # 生成活动编码
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                random_suffix = str(uuid.uuid4().int)[:4]
                activity_code = f'ACT{timestamp}{random_suffix}'
                
                # 插入数据
                insert_sql = text("""
                    INSERT INTO activities (
                        id, activity_code, name, description, status, 
                        created_by, created_at, updated_at
                    ) VALUES (
                        :id, :activity_code, :name, :description, :status,
                        :created_by, :created_at, :updated_at
                    )
                """)
                
                db.session.execute(insert_sql, {
                    'id': activity[0],  # id
                    'activity_code': activity_code,
                    'name': activity[1],  # name
                    'description': activity[2],  # description
                    'status': activity[3] if len(activity) > 3 else 'active',  # status
                    'created_by': activity[4] if len(activity) > 4 else None,  # created_by
                    'created_at': activity[5] if len(activity) > 5 else datetime.utcnow(),  # created_at
                    'updated_at': activity[6] if len(activity) > 6 else datetime.utcnow()  # updated_at
                })
            
            db.session.commit()
            print(f"成功恢复 {len(activities)} 条活动记录")
            
            print("迁移完成！")
            print("\n注意：")
            print("1. 新增字段已添加到活动表")
            print("2. 已为所有现有活动生成活动编码")
            print("3. 新增字段（活动类型、执行周期等）需要手动填充")
            print("4. 新增了活动申请表(activity_applications)")
            
        except Exception as e:
            db.session.rollback()
            print(f"迁移失败: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("活动表迁移工具")
    print("=" * 60)
    print("\n警告：此操作将修改数据库结构！")
    print("建议在执行前备份数据库文件：instance/deepvisit.db\n")
    
    # 检查是否有 --auto-confirm 参数
    auto_confirm = '--auto-confirm' in sys.argv or '-y' in sys.argv
    
    if auto_confirm:
        print("自动确认模式，开始迁移...")
        migrate_activity_table()
    else:
        response = input("是否继续？(yes/no): ")
        if response.lower() == 'yes':
            migrate_activity_table()
        else:
            print("取消迁移")

