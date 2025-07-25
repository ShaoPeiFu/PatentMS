from django import forms
from PatentMS.models import Page, Category, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    """分类表单"""

    name = forms.CharField(
        max_length=128,
        help_text="请输入分类名称（至少2个字符）",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入分类名称",
                "minlength": "2",
            }
        ),
        error_messages={
            "required": "分类名称不能为空",
            "max_length": "分类名称不能超过128个字符",
        },
    )
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name",)

    def clean_name(self):
        """清理分类名称"""
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip()
            if len(name) < 2:
                raise ValidationError("分类名称至少需要2个字符")

            # 检查是否已存在相同名称的分类
            if Category.objects.filter(name__iexact=name).exists():
                raise ValidationError("该分类名称已存在")

        return name

    def save(self, commit=True):
        """保存分类"""
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class PageForm(forms.ModelForm):
    """页面表单"""

    title = forms.CharField(
        max_length=128,
        help_text="请输入页面标题（至少2个字符）",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入页面标题",
                "minlength": "2",
            }
        ),
        error_messages={
            "required": "页面标题不能为空",
            "max_length": "页面标题不能超过128个字符",
        },
    )
    url = forms.URLField(
        max_length=200,
        help_text="请输入有效的URL地址",
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://example.com",
                "pattern": "https?://.+",
            }
        ),
        error_messages={
            "required": "URL地址不能为空",
            "invalid": "请输入有效的URL地址",
        },
    )
    views = forms.IntegerField(
        help_text="初始浏览次数",
        initial=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": "0", "readonly": "readonly"}
        ),
        required=False,
    )

    class Meta:
        model = Page
        exclude = ("category",)

    def clean_title(self):
        """清理页面标题"""
        title = self.cleaned_data.get("title")
        if title:
            title = title.strip()
            if len(title) < 2:
                raise ValidationError("页面标题至少需要2个字符")
        return title

    def clean_url(self):
        """清理URL"""
        url = self.cleaned_data.get("url")
        if url:
            url = url.strip()
            if not url.startswith(("http://", "https://")):
                raise ValidationError("URL必须以http://或https://开头")
        return url

    def clean(self):
        """表单整体验证"""
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        url = cleaned_data.get("url")

        # 检查标题和URL是否都已提供
        if title and url:
            # 可以在这里添加更多的业务逻辑验证
            pass

        return cleaned_data


class UserForm(forms.ModelForm):
    """用户表单"""

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码",
                "minlength": "6",
            }
        ),
        help_text="密码至少6个字符",
        error_messages={
            "required": "密码不能为空",
        },
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请确认密码",
                "minlength": "6",
            }
        ),
        help_text="请再次输入密码",
        error_messages={
            "required": "请确认密码",
        },
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "请输入用户名",
                    "minlength": "3",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "请输入邮箱地址"}
            ),
        }
        error_messages = {
            "username": {
                "required": "用户名不能为空",
                "unique": "该用户名已被使用",
            },
            "email": {
                "required": "邮箱地址不能为空",
                "invalid": "请输入有效的邮箱地址",
            },
        }

    def clean_username(self):
        """清理用户名"""
        username = self.cleaned_data.get("username")
        if username:
            username = username.strip()
            if len(username) < 3:
                raise ValidationError("用户名至少需要3个字符")

            # 检查用户名是否已存在
            if User.objects.filter(username__iexact=username).exists():
                raise ValidationError("该用户名已被使用")

        return username

    def clean_email(self):
        """清理邮箱"""
        email = self.cleaned_data.get("email")
        if email:
            email = email.strip().lower()
            # 检查邮箱是否已存在
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError("该邮箱地址已被使用")
        return email

    def clean_confirm_password(self):
        """清理确认密码"""
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("两次输入的密码不一致")

        return confirm_password

    def clean(self):
        """表单整体验证"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if password and len(password) < 6:
            raise ValidationError("密码至少需要6个字符")

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """用户档案表单"""

    class Meta:
        model = UserProfile
        fields = ("website", "picture")
        widgets = {
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://your-website.com",
                }
            ),
            "picture": forms.FileInput(
                attrs={"class": "form-control-file", "accept": "image/*"}
            ),
        }
        error_messages = {
            "website": {
                "invalid": "请输入有效的网站地址",
            },
        }

    def clean_website(self):
        """清理网站地址"""
        website = self.cleaned_data.get("website")
        if website:
            website = website.strip()
            if not website.startswith(("http://", "https://")):
                raise ValidationError("网站地址必须以http://或https://开头")
        return website

    def clean_picture(self):
        """清理头像文件"""
        picture = self.cleaned_data.get("picture")
        if picture:
            # 检查文件大小（限制为5MB）
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("头像文件大小不能超过5MB")

            # 检查文件类型
            allowed_types = ["image/jpeg", "image/png", "image/gif"]
            if picture.content_type not in allowed_types:
                raise ValidationError("只支持JPEG、PNG和GIF格式的图片")

        return picture
