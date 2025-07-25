from django.test import TestCase, Client
from django.urls import reverse
from PatentMS.models import Category, Page, UserProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """测试浏览次数不能为负数"""
        category = Category(name="test", views=-1, likes=0)
        category.save()
        self.assertEqual((category.views >= 0), True)

    def test_slug_line_creation(self):
        """测试slug自动生成"""
        category = Category(name="Random Category String")
        category.save()
        self.assertEqual(category.slug, "random-category-string")

    def test_category_str_method(self):
        """测试Category的__str__方法"""
        category = Category(name="Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_category_get_absolute_url(self):
        """测试Category的get_absolute_url方法"""
        category = Category(name="Test Category")
        category.save()
        expected_url = reverse("show_category", args=[category.slug])
        self.assertEqual(category.get_absolute_url(), expected_url)

    def test_category_increment_methods(self):
        """测试Category的increment方法"""
        category = Category(name="Test Category", views=5, likes=3)
        category.save()

        category.increment_views()
        self.assertEqual(category.views, 6)

        category.increment_likes()
        self.assertEqual(category.likes, 4)


class PageMethodTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name="Test Category")

    def test_page_str_method(self):
        """测试Page的__str__方法"""
        page = Page.objects.create(
            category=self.category, title="Test Page", url="https://example.com"
        )
        self.assertEqual(str(page), "Test Page")

    def test_page_get_absolute_url(self):
        """测试Page的get_absolute_url方法"""
        page = Page.objects.create(
            category=self.category, title="Test Page", url="https://example.com"
        )
        expected_url = reverse("goto") + f"?page_id={page.id}"
        self.assertEqual(page.get_absolute_url(), expected_url)

    def test_page_increment_views(self):
        """测试Page的increment_views方法"""
        page = Page.objects.create(
            category=self.category,
            title="Test Page",
            url="https://example.com",
            views=10,
        )
        page.increment_views()
        self.assertEqual(page.views, 11)

    def test_page_is_popular_property(self):
        """测试Page的is_popular属性"""
        page1 = Page.objects.create(
            category=self.category,
            title="Popular Page",
            url="https://example.com",
            views=15,
        )
        page2 = Page.objects.create(
            category=self.category,
            title="Not Popular Page",
            url="https://example.com",
            views=5,
        )

        self.assertTrue(page1.is_popular)
        self.assertFalse(page2.is_popular)


class UserProfileMethodTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_userprofile_str_method(self):
        """测试UserProfile的__str__方法"""
        profile = UserProfile.objects.create(
            user=self.user, website="https://example.com"
        )
        self.assertEqual(str(profile), "testuser的档案")

    def test_userprofile_get_absolute_url(self):
        """测试UserProfile的get_absolute_url方法"""
        profile = UserProfile.objects.create(user=self.user)
        expected_url = reverse("profile", args=[self.user.username])
        self.assertEqual(profile.get_absolute_url(), expected_url)

    def test_userprofile_get_full_name(self):
        """测试UserProfile的get_full_name方法"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.get_full_name(), "testuser")


class ViewTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category")
        self.page = Page.objects.create(
            category=self.category, title="Test Page", url="https://example.com"
        )

    def test_index_view(self):
        """测试首页视图"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "PatentMS/index.html")

    def test_show_category_view(self):
        """测试分类页面视图"""
        response = self.client.get(reverse("show_category", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "PatentMS/category.html")
        self.assertContains(response, self.category.name)

    def test_show_category_view_invalid_slug(self):
        """测试无效slug的分类页面"""
        response = self.client.get(reverse("show_category", args=["invalid-slug"]))
        self.assertEqual(response.status_code, 302)  # 重定向到首页

    def test_add_category_view_authenticated(self):
        """测试已认证用户添加分类"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("add_category"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "PatentMS/add_category.html")

    def test_add_category_view_unauthenticated(self):
        """测试未认证用户添加分类"""
        response = self.client.get(reverse("add_category"))
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面

    def test_like_category_view(self):
        """测试点赞功能"""
        self.client.login(username="testuser", password="testpass123")
        initial_likes = self.category.likes
        response = self.client.get(
            reverse("like_category"), {"category_id": self.category.id}
        )
        self.assertEqual(response.status_code, 200)

        # 刷新数据库中的对象
        self.category.refresh_from_db()
        self.assertEqual(self.category.likes, initial_likes + 1)

    def test_goto_url_view(self):
        """测试页面跳转功能"""
        initial_views = self.page.views
        response = self.client.get(reverse("goto"), {"page_id": self.page.id})
        self.assertEqual(response.status_code, 302)  # 重定向到外部URL

        # 刷新数据库中的对象
        self.page.refresh_from_db()
        self.assertEqual(self.page.views, initial_views + 1)


class FormTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.category = Category.objects.create(name="Test Category")

    def test_category_form_valid(self):
        """测试有效的分类表单"""
        from PatentMS.forms import CategoryForm

        form_data = {"name": "New Category"}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        """测试无效的分类表单"""
        from PatentMS.forms import CategoryForm

        # 空名称
        form_data = {"name": ""}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

        # 名称太短
        form_data = {"name": "A"}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_page_form_valid(self):
        """测试有效的页面表单"""
        from PatentMS.forms import PageForm

        form_data = {"title": "New Page", "url": "https://example.com"}
        form = PageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_page_form_invalid(self):
        """测试无效的页面表单"""
        from PatentMS.forms import PageForm

        # 无效URL
        form_data = {"title": "New Page", "url": "invalid-url"}
        form = PageForm(data=form_data)
        self.assertFalse(form.is_valid())


class URLTests(TestCase):
    def test_index_url(self):
        """测试首页URL"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """测试分类URL"""
        category = Category.objects.create(name="Test Category")
        response = self.client.get(f"/category/{category.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        """测试管理后台URL"""
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面
