from django import template
from PatentMS.models import Category

register = template.Library()

@register.inclusion_tag('PatentMS/categories.html')
def get_category_list(current_category=None):
    return {'categories':Category.objects.all(),
            'current_category':current_category}

# 自定义数学运算过滤器
@register.filter
def multiply(value, arg):
    """将值乘以参数"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def add(value, arg):
    """将值加上参数"""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def subtract(value, arg):
    """将值减去参数"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def divide(value, arg):
    """将值除以参数"""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value










