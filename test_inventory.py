#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存管理功能测试脚本
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_inventory_apis():
    """测试库存管理API"""
    print("测试库存管理功能...")
    
    # 测试供应商列表
    try:
        response = requests.get(f'{BASE_URL}/inventory/api/supplier/list')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 供应商列表API正常，共{data.get('total', 0)}个供应商")
        else:
            print(f"❌ 供应商列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 供应商列表API异常: {e}")
    
    # 测试仓库列表
    try:
        response = requests.get(f'{BASE_URL}/inventory/api/warehouse/list')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 仓库列表API正常，共{data.get('total', 0)}个仓库")
        else:
            print(f"❌ 仓库列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 仓库列表API异常: {e}")
    
    # 测试商品列表
    try:
        response = requests.get(f'{BASE_URL}/inventory/api/product/list')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 商品列表API正常，共{data.get('total', 0)}个商品")
        else:
            print(f"❌ 商品列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 商品列表API异常: {e}")
    
    # 测试库存列表
    try:
        response = requests.get(f'{BASE_URL}/inventory/api/stock/list')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 库存列表API正常，共{data.get('total', 0)}条库存记录")
        else:
            print(f"❌ 库存列表API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 库存列表API异常: {e}")
    
    # 测试库存汇总
    try:
        response = requests.get(f'{BASE_URL}/inventory/api/stock/summary')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 库存汇总API正常，共{len(data.get('data', []))}个仓库汇总")
        else:
            print(f"❌ 库存汇总API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 库存汇总API异常: {e}")

def test_pages():
    """测试页面访问"""
    print("\n测试页面访问...")
    
    pages = [
        '/inventory/supplier',
        '/inventory/warehouse', 
        '/inventory/purchase',
        '/inventory/product',
        '/inventory/stock'
    ]
    
    for page in pages:
        try:
            response = requests.get(f'{BASE_URL}{page}')
            if response.status_code == 200:
                print(f"✅ {page} 页面正常")
            else:
                print(f"❌ {page} 页面失败: {response.status_code}")
        except Exception as e:
            print(f"❌ {page} 页面异常: {e}")

if __name__ == '__main__':
    test_inventory_apis()
    test_pages()
    print("\n测试完成！")

