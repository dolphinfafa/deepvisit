"""
数据库迁移脚本：为数据上报模块添加照片字段
为铺货上报、库存上报、竞品上报三个表添加photo字段
"""
import sqlite3
import os

def migrate():
    """执行数据库迁移"""
    db_path = os.path.join('instance', 'deepvisit.db')
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 为display_reports表添加photo字段
        try:
            cursor.execute("ALTER TABLE display_reports ADD COLUMN photo VARCHAR(255)")
            print("[OK] 成功为display_reports表添加photo字段")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("[OK] display_reports表已存在photo字段，跳过")
            else:
                raise
        
        # 为inventory_reports表添加photo字段
        try:
            cursor.execute("ALTER TABLE inventory_reports ADD COLUMN photo VARCHAR(255)")
            print("[OK] 成功为inventory_reports表添加photo字段")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("[OK] inventory_reports表已存在photo字段，跳过")
            else:
                raise
        
        # 为competitor_reports表添加photo字段
        try:
            cursor.execute("ALTER TABLE competitor_reports ADD COLUMN photo VARCHAR(255)")
            print("[OK] 成功为competitor_reports表添加photo字段")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("[OK] competitor_reports表已存在photo字段，跳过")
            else:
                raise
        
        conn.commit()
        print("\n数据库迁移完成！")
        
    except Exception as e:
        print(f"迁移失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("开始数据库迁移...")
    print("=" * 50)
    migrate()
    print("=" * 50)

