#!/usr/bin/env python3
"""
测试搜索功能
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sinaPatent.settings")
django.setup()

from PatentMS.search_service import search_service


def test_search():
    """测试搜索功能"""
    print("=== 测试搜索功能 ===")

    # 测试搜索
    query = "Python教程"
    print(f"搜索关键词: {query}")

    try:
        results = search_service.search_pages(query, "Python", 5)
        print(f"找到 {len(results)} 个结果:")

        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('title', 'N/A')}")
            print(f"   URL: {result.get('url', 'N/A')}")
            print(f"   摘要: {result.get('abstract', 'N/A')[:100]}...")
            print()

    except Exception as e:
        print(f"搜索失败: {e}")
        import traceback

        traceback.print_exc()


def test_suggestions():
    """测试搜索建议功能"""
    print("=== 测试搜索建议功能 ===")

    query = "Python"
    print(f"获取建议关键词: {query}")

    try:
        suggestions = search_service.get_suggestions(query)
        print(f"找到 {len(suggestions)} 个建议:")

        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

    except Exception as e:
        print(f"获取建议失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_search()
    print("\n" + "=" * 50 + "\n")
    test_suggestions()
