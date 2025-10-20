"""
照片上传功能测试脚本
用于验证三个数据上报模块的照片字段是否正确添加
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.data_report import DisplayReport, InventoryReport, CompetitorReport

def test_photo_fields():
    """测试照片字段是否存在"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("照片上传功能测试")
        print("=" * 60)
        print()
        
        # 测试DisplayReport模型
        print("1. 测试铺货上报模型 (DisplayReport)")
        display = DisplayReport()
        if hasattr(display, 'photo'):
            print("   [OK] photo字段存在")
        else:
            print("   [FAIL] photo字段不存在")
        print()
        
        # 测试InventoryReport模型
        print("2. 测试库存上报模型 (InventoryReport)")
        inventory = InventoryReport()
        if hasattr(inventory, 'photo'):
            print("   [OK] photo字段存在")
        else:
            print("   [FAIL] photo字段不存在")
        print()
        
        # 测试CompetitorReport模型
        print("3. 测试竞品上报模型 (CompetitorReport)")
        competitor = CompetitorReport()
        if hasattr(competitor, 'photo'):
            print("   [OK] photo字段存在")
        else:
            print("   [FAIL] photo字段不存在")
        print()
        
        # 检查数据库表结构
        print("4. 检查数据库表结构")
        try:
            # 检查display_reports表
            result = db.session.execute(db.text("PRAGMA table_info(display_reports)"))
            columns = [row[1] for row in result]
            if 'photo' in columns:
                print("   [OK] display_reports表有photo字段")
            else:
                print("   [FAIL] display_reports表缺少photo字段")
            
            # 检查inventory_reports表
            result = db.session.execute(db.text("PRAGMA table_info(inventory_reports)"))
            columns = [row[1] for row in result]
            if 'photo' in columns:
                print("   [OK] inventory_reports表有photo字段")
            else:
                print("   [FAIL] inventory_reports表缺少photo字段")
            
            # 检查competitor_reports表
            result = db.session.execute(db.text("PRAGMA table_info(competitor_reports)"))
            columns = [row[1] for row in result]
            if 'photo' in columns:
                print("   [OK] competitor_reports表有photo字段")
            else:
                print("   [FAIL] competitor_reports表缺少photo字段")
        except Exception as e:
            print(f"   [FAIL] 检查数据库表结构失败: {str(e)}")
        print()
        
        # 检查uploads目录
        print("5. 检查上传目录")
        upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'data_reports')
        if os.path.exists(upload_dir):
            print(f"   [OK] 上传目录存在: {upload_dir}")
            if os.access(upload_dir, os.W_OK):
                print("   [OK] 上传目录可写")
            else:
                print("   [FAIL] 上传目录不可写")
        else:
            print(f"   [FAIL] 上传目录不存在: {upload_dir}")
        print()
        
        print("=" * 60)
        print("测试完成！")
        print("=" * 60)

if __name__ == '__main__':
    test_photo_fields()

