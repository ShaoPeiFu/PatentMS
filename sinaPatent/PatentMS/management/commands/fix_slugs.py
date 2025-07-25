from django.core.management.base import BaseCommand
from PatentMS.models import Category, chinese_slugify


class Command(BaseCommand):
    help = "修复所有分类的slug字段"

    def handle(self, *args, **options):
        categories = Category.objects.filter(slug="")
        count = 0

        for category in categories:
            old_slug = category.slug
            category.slug = chinese_slugify(category.name)

            # 确保slug唯一性
            if category.slug == "category":
                # 如果是默认值，使用ID生成唯一slug
                counter = 1
                while Category.objects.filter(slug=f"category-{counter}").exists():
                    counter += 1
                category.slug = f"category-{counter}"
            else:
                # 检查slug唯一性
                counter = 1
                original_slug = category.slug
                while (
                    Category.objects.filter(slug=category.slug)
                    .exclude(id=category.id)
                    .exists()
                ):
                    category.slug = f"{original_slug}-{counter}"
                    counter += 1

            category.save(update_fields=["slug"])
            count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'修复分类 "{category.name}" 的slug: {old_slug} -> {category.slug}'
                )
            )

        if count == 0:
            self.stdout.write(self.style.WARNING("没有找到需要修复slug的分类"))
        else:
            self.stdout.write(self.style.SUCCESS(f"成功修复了 {count} 个分类的slug"))
 