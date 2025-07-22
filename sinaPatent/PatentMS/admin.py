from django.contrib import admin
from PatentMS.models import Category,Page
from PatentMS.models import UserProfile


admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)


