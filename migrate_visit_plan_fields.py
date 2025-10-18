"""
迁移脚本：为 visit_plans 表添加缺失的字段
"""
import sqlite3
import os

def migrate_database():
    """添加缺失的字段到 visit_plans 表"""
    db_path = 'instance/deepvisit.db'
    
    if not os.path.exists(db_path):
        print(f"[ERROR] 数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='visit_plans'")
        if not cursor.fetchone():
            print("[ERROR] visit_plans 表不存在")
            return False
        
        # 获取当前表结构
        cursor.execute("PRAGMA table_info(visit_plans)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"[INFO] 当前表字段: {', '.join(columns)}")
        
        # 需要添加的字段
        fields_to_add = []
        
        if 'customer_code' not in columns:
            fields_to_add.append(('customer_code', "ALTER TABLE visit_plans ADD COLUMN customer_code VARCHAR(64)"))
        
        if 'route_name' not in columns:
            fields_to_add.append(('route_name', "ALTER TABLE visit_plans ADD COLUMN route_name VARCHAR(128)"))
        
        if not fields_to_add:
            print("[INFO] 所有字段已存在，无需迁移")
            return True
        
        # 执行迁移
        for field_name, sql in fields_to_add:
            print(f"[INFO] 添加字段: {field_name}")
            cursor.execute(sql)
            print(f"[OK] 字段 {field_name} 添加成功")
        
        conn.commit()
        
        # 验证迁移
        cursor.execute("PRAGMA table_info(visit_plans)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"[INFO] 更新后表字段: {', '.join(new_columns)}")
        
        cursor.close()
        conn.close()
        
        print("[OK] 数据库迁移完成")
        return True
        
    except Exception as e:
        print(f"[ERROR] 迁移失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("visit_plans 表字段迁移")
    print("=" * 60)
    
    success = migrate_database()
    
    print("=" * 60)
    if success:
        print("[PASS] 迁移成功")
    else:
        print("[FAIL] 迁移失败")

