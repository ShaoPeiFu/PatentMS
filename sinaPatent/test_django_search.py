#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Django项目中的搜索功能
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sinaPatent.settings")

try:
    django.setup()
    print("✅ Django环境设置成功")
except Exception as e:
    print(f"❌ Django环境设置失败: {e}")
    sys.exit(1)

from PatentMS.search_service import SearchService, BaiduSearchService


def test_search_service():
    """测试搜索服务"""
    print("\n🔍 测试搜索服务...")

    # 创建搜索服务实例
    search_service = SearchService(use_mock=False, use_simple_search=False)
    print(
        f"✅ 搜索服务创建成功，使用引擎: {type(search_service.search_engine).__name__}"
    )

    # 测试搜索
    test_queries = ["Python教程", "Django框架", "机器学习"]

    for query in test_queries:
        print(f"\n📝 搜索: {query}")
        print("-" * 50)

        try:
            # 执行搜索
            results = search_service.search_pages(query, num_results=3)

            if results:
                print(f"✅ 找到 {len(results)} 个搜索结果:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.get('title', '无标题')}")
                    print(f"     链接: {result.get('url', '无链接')}")
                    print(f"     描述: {result.get('snippet', '无描述')[:100]}...")
                    print()
            else:
                print("❌ 没有找到搜索结果")

        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            import traceback

            traceback.print_exc()


def test_baidu_service_direct():
    """直接测试百度搜索服务"""
    print("\n🔍 直接测试百度搜索服务...")

    try:
        baidu_service = BaiduSearchService()
        print("✅ 百度搜索服务创建成功")

        results = baidu_service.search("Python教程", 2)
        print(f"✅ 直接百度搜索成功，找到 {len(results)} 个结果")

        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.get('title', '无标题')}")
            print(f"     链接: {result.get('url', '无链接')}")
            print()

    except Exception as e:
        print(f"❌ 直接百度搜索失败: {e}")
        import traceback

        traceback.print_exc()


def test_suggestions():
    """测试搜索建议功能"""
    print("\n💡 测试搜索建议功能...")

    try:
        search_service = SearchService(use_mock=False, use_simple_search=False)
        suggestions = search_service.get_suggestions("Python")

        if suggestions:
            print(f"✅ 找到 {len(suggestions)} 个搜索建议:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("❌ 没有找到搜索建议")

    except Exception as e:
        print(f"❌ 搜索建议失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 开始测试Django项目中的搜索功能...")

    test_search_service()
    test_baidu_service_direct()
    test_suggestions()

    print("\n🎯 测试完成!")
