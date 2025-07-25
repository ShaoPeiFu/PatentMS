"""
数据清理管理命令
用于清理无效数据、重复数据等
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from PatentMS.models import Page, Category, UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "清理数据库中的无效和重复数据"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="只显示将要删除的数据，不实际删除",
        )
        parser.add_argument(
            "--duplicates",
            action="store_true",
            help="清理重复数据",
        )
        parser.add_argument(
            "--orphans",
            action="store_true",
            help="清理孤立数据",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        clean_duplicates = options["duplicates"]
        clean_orphans = options["orphans"]

        if not clean_duplicates and not clean_orphans:
            clean_duplicates = True
            clean_orphans = True

        self.stdout.write(self.style.SUCCESS("开始数据清理..."))

        if clean_duplicates:
            self.clean_duplicates(dry_run)

        if clean_orphans:
            self.clean_orphans(dry_run)

        self.stdout.write(self.style.SUCCESS("数据清理完成！"))

    def clean_duplicates(self, dry_run):
        """清理重复数据"""
        self.stdout.write("检查重复的页面数据...")

        # 查找重复的页面
        duplicates = (
            Page.objects.values("category", "title")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
        )

        if duplicates.exists():
            self.stdout.write(f"发现 {duplicates.count()} 组重复数据:")

            for dup in duplicates:
                category_id = dup["category"]
                title = dup["title"]
                count = dup["count"]

                self.stdout.write(
                    f"  分类ID: {category_id}, 标题: {title}, 数量: {count}"
                )

                if not dry_run:
                    # 保留第一个，删除其他的
                    pages = Page.objects.filter(
                        category_id=category_id, title=title
                    ).order_by("id")
                    first_page = pages.first()
                    other_pages = pages.exclude(id=first_page.id)

                    deleted_count = other_pages.count()
                    other_pages.delete()

                    self.stdout.write(
                        f"    保留页面 ID {first_page.id}，删除 {deleted_count} 个重复页面"
                    )
        else:
            self.stdout.write("没有发现重复数据")

    def clean_orphans(self, dry_run):
        """清理孤立数据"""
        self.stdout.write("检查孤立数据...")

        # 检查没有分类的页面
        orphan_pages = Page.objects.filter(category__isnull=True)
        if orphan_pages.exists():
            self.stdout.write(f"发现 {orphan_pages.count()} 个没有分类的页面")
            if not dry_run:
                orphan_pages.delete()
                self.stdout.write("已删除孤立页面")

        # 检查没有用户的档案
        orphan_profiles = UserProfile.objects.filter(user__isnull=True)
        if orphan_profiles.exists():
            self.stdout.write(f"发现 {orphan_profiles.count()} 个没有用户的档案")
            if not dry_run:
                orphan_profiles.delete()
                self.stdout.write("已删除孤立档案")

        # 检查没有页面的分类
        empty_categories = Category.objects.annotate(page_count=Count("page")).filter(
            page_count=0
        )

        if empty_categories.exists():
            self.stdout.write(f"发现 {empty_categories.count()} 个没有页面的分类")
            if not dry_run:
                empty_categories.delete()
                self.stdout.write("已删除空分类")
