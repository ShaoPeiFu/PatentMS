#!/usr/bin/env python3
"""
点赞功能测试脚本
用于测试Django后端的点赞功能
"""

import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sinaPatent.settings")
django.setup()

from PatentMS.models import Category
from PatentMS.views import LikeCategoryView


def test_like_functionality():
    """测试点赞功能"""
    print("=== 点赞功能测试 ===")

    # 创建测试用户
    try:
        user = User.objects.get(username="123")
        print(f"✓ 找到测试用户: {user.username}")
    except User.DoesNotExist:
        print("✗ 测试用户不存在，请先创建用户 '123'")
        return

    # 获取测试分类
    try:
        category = Category.objects.get(id=2)
        print(f"✓ 找到测试分类: {category.name} (ID: {category.id})")
        print(f"  当前点赞数: {category.likes}")
    except Category.DoesNotExist:
        print("✗ 测试分类不存在，请先创建ID为2的分类")
        return

    # 创建请求工厂
    factory = RequestFactory()

    # 模拟POST请求
    print("\n--- 模拟点赞请求 ---")
    request = factory.post("/like_category/", {"category_id": category.id})
    request.user = user

    # 创建视图实例
    view = LikeCategoryView()

    try:
        # 调用视图方法
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


def test_category_model():
    """测试分类模型"""
    print("\n=== 分类模型测试 ===")

    try:
        category = Category.objects.get(id=2)
        print(f"分类名称: {category.name}")
        print(f"当前点赞数: {category.likes}")
        print(f"当前浏览数: {category.views}")

        # 测试increment_likes方法
        original_likes = category.likes
        category.increment_likes()
        print(f"调用increment_likes后点赞数: {category.likes}")

        if category.likes == original_likes + 1:
            print("✓ increment_likes方法正常工作")
        else:
            print("✗ increment_likes方法异常")

    except Category.DoesNotExist:
        print("✗ 分类不存在")
    except Exception as e:
        print(f"✗ 测试失败: {e}")


def test_user_authentication():
    """测试用户认证"""
    print("\n=== 用户认证测试 ===")

    try:
        user = User.objects.get(username="123")
        print(f"用户存在: {user.username}")
        print(f"用户ID: {user.id}")
        print(f"用户是否激活: {user.is_active}")
        print(f"用户是否认证: {user.is_authenticated}")

        # 测试认证
        authenticated_user = authenticate(username="123", password="123")
        if authenticated_user:
            print("✓ 用户认证成功")
        else:
            print("✗ 用户认证失败")

    except User.DoesNotExist:
        print("✗ 用户不存在")


if __name__ == "__main__":
    print("开始测试点赞功能...")
    print("=" * 50)

    test_user_authentication()
    test_category_model()
    test_like_functionality()

    print("\n" + "=" * 50)
    print("测试完成")
