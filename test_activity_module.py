#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试活动模块功能
"""

from app import create_app, db
from app.models.activity import Activity, ActivityApplication, ActivityReport
from app.models.user import User
from datetime import datetime, date

def test_activity_module():
    """测试活动模块"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("活动模块功能测试")
        print("=" * 60)
        
        # 1. 测试查询现有活动
        print("\n1. 查询现有活动:")
        activities = Activity.query.all()
        print(f"   找到 {len(activities)} 个活动")
        for activity in activities:
            print(f"   - ID: {activity.id}, 编码: {activity.activity_code}, 名称: {activity.name}")
        
        # 2. 测试创建新活动
        print("\n2. 测试创建新活动:")
        try:
            # 获取第一个用户
            user = User.query.first()
            if not user:
                print("   警告：没有找到用户，跳过创建测试")
            else:
                new_activity = Activity(
                    name="测试活动 - 付费陈列",
                    activity_type="付费陈列",
                    execution_start_date=date(2025, 11, 1),
                    execution_end_date=date(2025, 12, 31),
                    description="这是一个测试活动",
                    require_application="需要",
                    customer_scope="终端客户",
                    product_scope="全部商品",
                    payment_method="仅现金",
                    settlement_method="月度结案",
                    application_start_date=date(2025, 10, 20),
                    application_end_date=date(2025, 10, 31),
                    cost_share_ratio=50.0,
                    customer_signature="手写签收",
                    created_by=user.id
                )
                db.session.add(new_activity)
                db.session.commit()
                
                print(f"   ✓ 创建成功！")
                print(f"   - 活动编码: {new_activity.activity_code}")
                print(f"   - 活动名称: {new_activity.name}")
                print(f"   - 活动类型: {new_activity.activity_type}")
                print(f"   - 执行周期: {new_activity.execution_start_date} 至 {new_activity.execution_end_date}")
                print(f"   - 参与客户范围: {new_activity.customer_scope}")
                print(f"   - 结案方式: {new_activity.settlement_method}")
                
                # 3. 测试活动的to_dict方法
                print("\n3. 测试活动to_dict方法:")
                activity_dict = new_activity.to_dict()
                print(f"   ✓ 转换成功！字典包含 {len(activity_dict)} 个字段")
                print(f"   - activity_code: {activity_dict.get('activity_code')}")
                print(f"   - activity_type: {activity_dict.get('activity_type')}")
                print(f"   - customer_scope: {activity_dict.get('customer_scope')}")
                print(f"   - application_count: {activity_dict.get('application_count')}")
                print(f"   - participant_count: {activity_dict.get('participant_count')}")
                
                # 4. 测试更新活动
                print("\n4. 测试更新活动:")
                new_activity.cost_share_ratio = 60.0
                new_activity.status = 'active'
                db.session.commit()
                print(f"   ✓ 更新成功！")
                print(f"   - 费用分摊比例: {new_activity.cost_share_ratio}%")
                print(f"   - 活动状态: {new_activity.status}")
                
                # 5. 测试活动关联
                print("\n5. 测试活动关联:")
                print(f"   - 创建人: {new_activity.creator.name if new_activity.creator else 'None'}")
                print(f"   - 申请数: {new_activity.applications.count()}")
                print(f"   - 参与数: {new_activity.reports.count()}")
                
        except Exception as e:
            db.session.rollback()
            print(f"   ✗ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)

if __name__ == '__main__':
    test_activity_module()

