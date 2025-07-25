"""
URL configuration for sinaPatent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from PatentMS import views
from PatentMS.views import (
    AddCategoryView,
    ProfileView,
    ListProfileView,
    LikeCategoryView,
    CategorySuggestionView,
    SearchAddPageView,
    RealSearchView,
    SearchSuggestionsView,
)

urlpatterns = [
    # 管理后台
    path("admin/", admin.site.urls),
    # 主页
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    # 分类相关
    path(
        "category/<slug:category_name_slug>/", views.show_category, name="show_category"
    ),
    path("add_category/", views.add_category, name="add_category"),
    path("add_page/<slug:category_name_slug>/", views.add_page, name="add_page"),
    # 用户认证
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    # 用户档案
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("list_profiles/", ListProfileView.as_view(), name="list_profiles"),
    path("register_profile/", views.register_profile, name="register_profile"),
    # 功能页面
    path("restricted/", views.restricted, name="restricted"),
    path("goto/", views.goto_url, name="goto"),
    # 交互功能
    path("like_category/", LikeCategoryView.as_view(), name="like_category"),
    path("suggest/", CategorySuggestionView.as_view(), name="suggest"),
    path("search_add_page/", SearchAddPageView.as_view(), name="search_add_page"),
    # 新的搜索功能
    path("api/search/", RealSearchView.as_view(), name="real_search"),
    path(
        "api/search_suggestions/",
        SearchSuggestionsView.as_view(),
        name="search_suggestions",
    ),
    # 注册应用URLs
    path("accounts/", include("registration.backends.default.urls")),
]

# 开发环境静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
