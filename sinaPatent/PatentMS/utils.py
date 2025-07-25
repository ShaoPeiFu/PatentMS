"""
工具函数模块
包含项目中常用的辅助函数
"""

import logging
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def get_cache_key(prefix, *args):
    """
    生成缓存键

    Args:
        prefix: 缓存键前缀
        *args: 其他参数

    Returns:
        str: 缓存键
    """
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"


def cache_get_or_set(key, callback, timeout=300):
    """
    获取缓存或设置缓存

    Args:
        key: 缓存键
        callback: 获取数据的回调函数
        timeout: 缓存超时时间（秒）

    Returns:
        缓存的数据
    """
    result = cache.get(key)
    if result is None:
        try:
            result = callback()
            cache.set(key, result, timeout)
        except Exception as e:
            logger.error(f"缓存获取失败: {e}")
            result = callback()
    return result


def format_number(num):
    """
    格式化数字显示

    Args:
        num: 数字

    Returns:
        str: 格式化后的字符串
    """
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)


def get_time_ago(datetime_obj):
    """
    获取相对时间描述

    Args:
        datetime_obj: 时间对象

    Returns:
        str: 相对时间描述
    """
    now = timezone.now()
    diff = now - datetime_obj

    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}小时前"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}分钟前"
    else:
        return "刚刚"


def validate_url(url):
    """
    验证URL格式

    Args:
        url: URL字符串

    Returns:
        bool: 是否有效
    """
    if not url:
        return False

    url = url.strip()
    return url.startswith(("http://", "https://"))


def truncate_text(text, max_length=100, suffix="..."):
    """
    截断文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀

    Returns:
        str: 截断后的文本
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def get_popular_items(model, field="views", limit=10, days=None):
    """
    获取热门项目

    Args:
        model: 模型类
        field: 排序字段
        limit: 限制数量
        days: 天数限制

    Returns:
        QuerySet: 热门项目
    """
    queryset = model.objects.all()

    if days:
        start_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=start_date)

    return queryset.order_by(f"-{field}")[:limit]


def log_user_action(user, action, details=None):
    """
    记录用户操作

    Args:
        user: 用户对象
        action: 操作类型
        details: 详细信息
    """
    log_message = f"用户 {user.username} 执行了 {action}"
    if details:
        log_message += f": {details}"

    logger.info(log_message)


def get_client_ip(request):
    """
    获取客户端IP地址

    Args:
        request: 请求对象

    Returns:
        str: IP地址
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def is_mobile_device(request):
    """
    判断是否为移动设备

    Args:
        request: 请求对象

    Returns:
        bool: 是否为移动设备
    """
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    mobile_keywords = ["mobile", "android", "iphone", "ipad", "windows phone"]
    return any(keyword in user_agent for keyword in mobile_keywords)


def generate_slug(text):
    """
    生成slug

    Args:
        text: 原始文本

    Returns:
        str: slug
    """
    import re
    from django.utils.text import slugify

    # 移除特殊字符
    text = re.sub(r"[^\w\s-]", "", text)
    # 生成slug
    slug = slugify(text)
    return slug


def get_file_extension(filename):
    """
    获取文件扩展名

    Args:
        filename: 文件名

    Returns:
        str: 文件扩展名
    """
    return filename.split(".")[-1].lower() if "." in filename else ""


def is_valid_image_file(filename):
    """
    检查是否为有效的图片文件

    Args:
        filename: 文件名

    Returns:
        bool: 是否为有效图片
    """
    valid_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
    extension = get_file_extension(filename)
    return extension in valid_extensions


def calculate_reading_time(text, words_per_minute=200):
    """
    计算阅读时间

    Args:
        text: 文本内容
        words_per_minute: 每分钟阅读字数

    Returns:
        int: 阅读时间（分钟）
    """
    if not text:
        return 0

    word_count = len(text.split())
    reading_time = word_count / words_per_minute
    return max(1, int(reading_time))
