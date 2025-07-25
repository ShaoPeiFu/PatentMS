from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from PatentMS.models import Category, Page, UserProfile
from PatentMS.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from PatentMS.search_service import search_service
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import json

# 设置日志
logger = logging.getLogger(__name__)


# 工具函数
def get_server_side_cookie(request, cookie, default_val=None):
    """获取服务器端cookie"""
    return request.session.get(cookie, default_val)


def visitor_cookie_handler(request):
    """处理访问者cookie"""
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(
        request, "last_visit", str(datetime.now())
    )
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie

    request.session["visits"] = visits


# 基础视图类
class BaseView(View):
    """基础视图类，提供通用功能"""

    def get_context_data(self, **kwargs):
        """获取上下文数据"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def handle_error(self, error, message="操作失败"):
        """统一错误处理"""
        logger.error(f"{message}: {error}")
        return JsonResponse({"error": message}, status=500)


# 主要视图函数
def index(request):
    """首页视图"""
    try:
        context = {
            "categories": Category.objects.exclude(slug="").order_by("-likes")[:5],
            "pages": Page.objects.order_by("-views")[:5],
        }
        visitor_cookie_handler(request)
        context["visits"] = request.session["visits"]
        return render(request, "PatentMS/index.html", context)
    except Exception as e:
        logger.error(f"首页加载失败: {e}")
        messages.error(request, "页面加载失败")
        return render(request, "PatentMS/index.html", {"categories": [], "pages": []})


def show_category(request, category_name_slug):
    """显示分类页面"""
    try:
        # 增加调试信息
        logger.info(f"尝试访问分类: {category_name_slug}")

        # 检查分类是否存在
        try:
            category = Category.objects.get(slug=category_name_slug)
            logger.info(f"找到分类: {category.name} (ID: {category.id})")
        except Category.DoesNotExist:
            logger.error(f"分类不存在: {category_name_slug}")
            messages.error(request, f"分类 '{category_name_slug}' 不存在")
            return redirect("index")

        # 获取页面
        pages = Page.objects.filter(category=category).order_by("-views")
        logger.info(f"分类 {category.name} 有 {pages.count()} 个页面")

        return render(
            request, "PatentMS/category.html", {"category": category, "pages": pages}
        )
    except Exception as e:
        logger.error(f"分类页面加载失败: {e}")
        messages.error(request, f"加载分类页面时发生错误: {str(e)}")
        return redirect("index")


@login_required
def add_category(request):
    """添加分类（函数视图）"""
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "分类添加成功！")
            return redirect("index")
        else:
            messages.error(request, "表单验证失败")
    else:
        form = CategoryForm()

    return render(request, "PatentMS/add_category.html", {"form": form})


@login_required
def add_page(request, category_name_slug):
    """添加页面"""
    try:
        category = get_object_or_404(Category, slug=category_name_slug)

        if request.method == "POST":
            form = PageForm(request.POST)
            if form.is_valid():
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                messages.success(request, "页面添加成功！")
                return redirect("show_category", category_name_slug=category_name_slug)
            else:
                messages.error(request, "表单验证失败")
        else:
            form = PageForm()

        return render(
            request, "PatentMS/add_page.html", {"form": form, "category": category}
        )
    except Exception as e:
        logger.error(f"添加页面失败: {e}")
        messages.error(request, "添加页面失败")
        return redirect("index")


def register(request):
    """用户注册"""
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                registered = True
                messages.success(request, "注册成功！")
            except Exception as e:
                logger.error(f"用户注册失败: {e}")
                messages.error(request, "注册失败，请重试")
        else:
            messages.error(request, "表单验证失败")
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "PatentMS/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request):
    """用户登录"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "用户名和密码不能为空")
            return render(request, "PatentMS/login.html")

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            messages.success(request, f"欢迎回来，{username}！")
            return redirect("index")
        else:
            logger.warning(f"登录失败: {username}")
            messages.error(request, "用户名或密码错误")

    return render(request, "PatentMS/login.html")


@login_required
def user_logout(request):
    """用户登出"""
    logout(request)
    messages.success(request, "您已成功登出")
    return redirect("index")


@login_required
def restricted(request):
    """受限页面"""
    return HttpResponse("由于你登录了，所以你可以看到这条信息，太棒了！")


def goto_url(request):
    """跳转到页面URL"""
    page_id = request.GET.get("page_id")
    if not page_id:
        messages.error(request, "页面ID不能为空")
        return redirect("index")

    try:
        page = get_object_or_404(Page, id=page_id)
        page.views += 1
        page.save()
        return redirect(page.url)
    except Exception as e:
        logger.error(f"页面跳转失败: {e}")
        messages.error(request, "页面不存在")
        return redirect("index")


@login_required
def register_profile(request):
    """注册用户档案"""
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                messages.success(request, "档案创建成功！")
                return redirect("index")
            except Exception as e:
                logger.error(f"档案创建失败: {e}")
                messages.error(request, "档案创建失败")
        else:
            messages.error(request, "表单验证失败")
    else:
        form = UserProfileForm()

    return render(request, "profile_registration.html", {"form": form})


# 类视图
class AddCategoryView(BaseView):
    """添加分类（类视图）"""

    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, "PatentMS/add_category.html", {"form": form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "分类添加成功！")
                return redirect("index")
            except Exception as e:
                logger.error(f"分类添加失败: {e}")
                messages.error(request, "分类添加失败")
        else:
            messages.error(request, "表单验证失败")

        return render(request, "PatentMS/add_category.html", {"form": form})


class ProfileView(BaseView):
    """用户档案视图"""

    def get_user_details(self, username):
        """获取用户详情"""
        try:
            user = get_object_or_404(User, username=username)
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            form = UserProfileForm(instance=user_profile)
            return user, user_profile, form
        except Exception as e:
            logger.error(f"获取用户详情失败: {e}")
            return None, None, None

    @method_decorator(login_required)
    def get(self, request, username):
        user, user_profile, form = self.get_user_details(username)
        if not user:
            messages.error(request, "用户不存在")
            return redirect("index")

        return render(
            request,
            "PatentMS/profile.html",
            {
                "user_profile": user_profile,
                "selected_user": user,
                "form": form,
            },
        )

    @method_decorator(login_required)
    def post(self, request, username):
        user, user_profile, form = self.get_user_details(username)
        if not user:
            messages.error(request, "用户不存在")
            return redirect("index")

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "档案更新成功！")
                return redirect("profile", username=user.username)
            except Exception as e:
                logger.error(f"档案更新失败: {e}")
                messages.error(request, "档案更新失败")
        else:
            messages.error(request, "表单验证失败")

        return render(
            request,
            "PatentMS/profile.html",
            {
                "user_profile": user_profile,
                "selected_user": user,
                "form": form,
            },
        )


class ListProfileView(BaseView):
    """用户档案列表"""

    @method_decorator(login_required)
    def get(self, request):
        try:
            profiles = UserProfile.objects.all()
            return render(
                request, "PatentMS/list_profiles.html", {"user_profile_list": profiles}
            )
        except Exception as e:
            logger.error(f"获取用户档案列表失败: {e}")
            messages.error(request, "获取用户列表失败")
            return redirect("index")


class LikeCategoryView(BaseView):
    """点赞分类视图"""

    @method_decorator(login_required)
    def post(self, request):
        logger.info(f"点赞请求收到，用户: {request.user.username}")
        category_id = request.POST.get("category_id")
        logger.info(f"分类ID参数: {category_id}")

        if not category_id:
            logger.error("没有提供分类ID")
            return self.handle_error("没有提供分类ID", "参数错误")

        try:
            category = get_object_or_404(Category, id=int(category_id))
            logger.info(f"找到分类: {category.name}, 当前点赞数: {category.likes}")
            category.likes += 1
            category.save()
            logger.info(f"更新后点赞数: {category.likes}")

            logger.info(f"用户 {request.user.username} 点赞了分类 {category.name}")
            return JsonResponse(category.likes, safe=False)

        except ValueError:
            return self.handle_error("无效的分类ID", "参数错误")
        except Exception as e:
            return self.handle_error(e, "点赞失败")

    def get(self, request):
        """GET请求也支持，保持向后兼容"""
        return self.post(request)


def get_category_list(max_results=0, starts_with=""):
    """获取分类列表"""
    try:
        if starts_with:
            category_list = Category.objects.filter(name__istartswith=starts_with)
        else:
            category_list = Category.objects.all()

        if max_results > 0:
            category_list = category_list[:max_results]

        return category_list
    except Exception as e:
        logger.error(f"获取分类列表失败: {e}")
        return []


class CategorySuggestionView(BaseView):
    """分类建议视图"""

    def get(self, request):
        suggestion = request.GET.get("suggestion", "")

        try:
            category_list = get_category_list(max_results=8, starts_with=suggestion)
            if not category_list:
                category_list = Category.objects.order_by("-likes")[:8]

            # 使用模板渲染HTML片段
            html = '<ul class="list-unstyled">'
            for category in category_list:
                if category.slug:
                    html += f'<li><a href="{reverse("show_category", args=[category.slug])}">{category.name}</a></li>'
                else:
                    html += f'<li><a href="#" onclick="alert(\'该分类暂时无法访问\')">{category.name}</a></li>'
            html += "</ul>"

            return HttpResponse(html)

        except Exception as e:
            logger.error(f"获取分类建议失败: {e}")
            return HttpResponse('<ul class="list-unstyled"><li>加载失败</li></ul>')


class SearchAddPageView(BaseView):
    """搜索添加页面视图"""

    @method_decorator(login_required)
    def get(self, request):
        title = request.GET.get("title")
        url = request.GET.get("url")
        category_id = request.GET.get("category_id")

        if not all([title, url, category_id]):
            return self.handle_error("缺少必要参数", "参数错误")

        try:
            category = get_object_or_404(Category, id=int(category_id))
            page, created = Page.objects.get_or_create(
                category=category, title=title, url=url
            )

            if created:
                logger.info(f"用户 {request.user.username} 添加了页面 {page.title}")

            # 返回更新后的页面列表HTML
            pages = Page.objects.filter(category=category).order_by("-views")
            html = "<ul><h2>页面列表</h2>"
            for p in pages:
                html += f'<li><a href="{reverse("goto")}?page_id={p.id}">{p.title}</a> - {p.views} view{"s" if p.views != 1 else ""}</li>'
            html += "</ul>"

            return HttpResponse(html)

        except ValueError:
            return self.handle_error("无效的分类ID", "参数错误")
        except Exception as e:
            return self.handle_error(e, "添加页面失败")


class RealSearchView(BaseView):
    """真正的搜索视图"""

    @method_decorator(login_required)
    def get(self, request):
        query = request.GET.get("query", "").strip()
        category_id = request.GET.get("category_id", "")

        if not query:
            return JsonResponse({"error": "搜索关键词不能为空"}, status=400)

        try:
            # 获取分类信息
            category = None
            if category_id:
                category = get_object_or_404(Category, id=int(category_id))

            # 执行搜索
            results = search_service.search_pages(
                query=query,
                category_name=category.name if category else "",
                num_results=10,
            )

            # 检查是否已存在相同页面
            if category:
                existing_pages = Page.objects.filter(category=category)
                for result in results:
                    result["exists"] = existing_pages.filter(
                        title=result["title"]
                    ).exists()

            logger.info(f"用户 {request.user.username} 搜索了关键词: {query}")

            return JsonResponse(
                {
                    "success": True,
                    "results": results,
                    "query": query,
                    "total": len(results),
                }
            )

        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return JsonResponse({"error": "搜索失败，请稍后重试"}, status=500)


class SearchSuggestionsView(BaseView):
    """搜索建议视图"""

    def get(self, request):
        query = request.GET.get("query", "").strip()

        if not query or len(query) < 2:
            return JsonResponse({"suggestions": []})

        try:
            suggestions = search_service.get_suggestions(query)
            return JsonResponse({"suggestions": suggestions[:5]})  # 限制建议数量
        except Exception as e:
            logger.error(f"获取搜索建议失败: {e}")
            return JsonResponse({"suggestions": []})
