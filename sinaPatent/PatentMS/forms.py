from django import forms
from PatentMS.models import Page, Category,UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="请输入名称")
    # views = forms.IntegerField(help_text="请输入views", initial=0)
    # likes = forms.IntegerField(help_text="请输入likes", initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(),initial = 0)
    # views = forms.IntegerField(widget=forms.HiddenInput(),initial = 0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        # fields = ("name", "views", "likes", "slug")
        fields = ("name",)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="请输入标题")
    url = forms.URLField(max_length=200, help_text="请输入URL")
    views = forms.IntegerField(help_text="请输入", initial=0)

    class Meta:
        model = Page
        exclude = ("category",)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())



    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website','picture')
        