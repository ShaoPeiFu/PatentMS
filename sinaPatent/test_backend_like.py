#!/usr/bin/env python3
"""
简单的后端点赞功能测试
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sinaPatent.settings")
django.setup()

from PatentMS.models import Category, User
from django.test import RequestFactory
from PatentMS.views import LikeCategoryView


def test_backend_like():
    """测试后端点赞功能"""
    print("=== 后端点赞功能测试 ===")

    # 检查分类是否存在
    try:
        category = Category.objects.get(id=5)
        print(f"✓ 找到分类: {category.name} (ID: {category.id})")
        print(f"  当前点赞数: {category.likes}")
    except Category.DoesNotExist:
        print("✗ 分类ID=5不存在")
        return

    # 检查用户是否存在
    try:
        user = User.objects.get(username="123")
        print(f"✓ 找到用户: {user.username}")
    except User.DoesNotExist:
        print("✗ 用户'123'不存在")
        return

    # 创建测试请求
    factory = RequestFactory()
    request = factory.post("/like_category/", {"category_id": "5"})
    request.user = user

    # 测试视图
    view = LikeCategoryView()

    try:
        print("\n--- 发送点赞请求 ---")
        response = view.post(request)

        print(f"✓ 请求处理成功")
        print(f"  响应状态码: {response.status_code}")
        print(f"  响应内容: {response.content.decode()}")

        # 检查数据库更新
        category.refresh_from_db()
        print(f"  更新后点赞数: {category.likes}")

        if category.likes > 0:
            print("✓ 点赞功能正常工作")
        else:
            print("✗ 点赞数未增加")

    except Exception as e:
        print(f"✗ 请求处理失败: {e}")
        import traceback

        traceback.print_exc()


def check_database():
    """检查数据库状态"""
    print("\n=== 数据库状态检查 ===")

    # 检查所有分类
    categories = Category.objects.all()
    print(f"分类总数: {categories.count()}")

    for cat in categories[:5]:  # 显示前5个分类
        print(f"  - {cat.name} (ID: {cat.id}, 点赞: {cat.likes}, 浏览: {cat.views})")

    # 检查所有用户
    users = User.objects.all()
    print(f"用户总数: {users.count()}")

    for user in users[:3]:  # 显示前3个用户
        print(f"  - {user.username} (ID: {user.id}, 激活: {user.is_active})")


if __name__ == "__main__":
    print("开始测试后端点赞功能...")
    print("=" * 50)

    check_database()
    test_backend_like()

    print("\n" + "=" * 50)
    print("测试完成")
