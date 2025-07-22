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
from django.urls import include, path
from PatentMS import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.urls import reverse


# app_name = 'PatentMS'


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse("register_profile")


urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("admin/", admin.site.urls),
    path(
        "category/<slug:category_name_slug>/", views.show_category, name="show_category"
    ),
    path("register/", views.register, name="register"),
    path("add_category/", views.add_category, name="add_category"),
    path("add_page/<slug:category_name_slug>/", views.add_page, name="add_page"),
    path("login/", views.user_login, name="login"),
    path("restricted/", views.restricted, name="restricted"),
    path("logout/", views.user_logout, name="logout"),
    path(
        "accounts/register", MyRegistrationView.as_view(), name="registration_register"
    ),
    path("accounts/", include("registration.backends.simple.urls")),
    path("goto/", views.goto_url, name="goto"),
    path("register_profile/", views.register_profile, name="register_profile"),
    path("add_category/", views.AddCategoryView.as_view(), name="add_category"),
    path("profile/<username>", views.ProfileView.as_view(), name="profile"),
    path("profiles/", views.ListProfileView.as_view(), name="list_profiles"),
    path("like_category/", views.LikeCategoryView.as_view(), name="like_category"),
    path("jquery-test/", views.jquery_test, name="jquery_test"),
    path("suggest/", views.CategorySuggestionView.as_view(), name="suggest"),
    path("search_add_page/", views.SearchAddPageView.as_view(), name="search_add_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
