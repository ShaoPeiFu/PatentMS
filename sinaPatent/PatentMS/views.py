from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from PatentMS.models import Category, Page, UserProfile
from PatentMS.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(
        request, "last_visit", str(datetime.now())
    )
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie
    request.session["visits"] = visits


def index(request):

    category_list = Category.objects.exclude(slug="").order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = {}
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list
    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]
    response = render(request, "PatentMS/index.html", context=context_dict)
    return response


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by("-views")
        context_dict["pages"] = pages
        context_dict["category"] = category
    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "PatentMS/category.html", context_dict)


def add_category(request):
    form = Category()

    if request.method == "POST":

        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return redirect("/index/")
        else:
            print(form.errors)
    return render(request, "PatentMS/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)

            else:
                print(form.errors)
    context_dict = {"form": form, "category": category}
    return render(request, "PatentMS/add_page.html", context_dict)


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("index"))
            else:
                return HttpResponse("您的账号已经被禁用")
        else:
            print(f"无效登录信息:{username},{password}")
            return HttpResponse("提供的登录信息无效")
    else:
        return render(request, "PatentMS/login.html")


@login_required
def restricted(request):
    return HttpResponse("由于你登录了，所以你可以看到这条信息，太棒了！")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("index"))


def goto_url(request):
    page_id = request.GET.get("page_id")
    try:
        if page_id:
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)
    except Page.DoesNotExist:
        pass
    return redirect(reverse("index"))


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse("index"))
    else:
        print(form.errors)

    context_dict = {"form": form}
    return render(request, "profile_registration.html", context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, "PatentMS/add_category.html", {"form": form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("index"))
        else:
            print(form.errors)

        return render(request, "PatentMS/add_category.html", {"form": form})


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm(
            {"website": user_profile.website, "picture": user_profile.picture}
        )
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse("index"))

        context_dict = {
            "user_profile": user_profile,
            "selected_user": user,
            "form": form,
        }
        return render(request, "PatentMS/profile.html", context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse("index"))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect("profile", user.username)
        else:
            print(form.errors)

        context_dict = {
            "user_profile": user_profile,
            "selected_user": user,
            "form": form,
        }
        return render(request, "PatentMS/profile.html", context_dict)


class ListProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(
            request, "PatentMS/list_profiles.html", {"user_profile_list": profiles}
        )


class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        print("点赞请求收到")
        category_id = request.GET.get("category_id")
        print(f"分类ID: {category_id}")

        if not category_id:
            print("没有提供category_id")
            return HttpResponse("错误：没有提供分类ID", status=400)

        try:
            category = Category.objects.get(id=int(category_id))
            print(f"找到分类: {category.name}, 当前点赞数: {category.likes}")
        except Category.DoesNotExist:
            print(f"分类不存在: {category_id}")
            return HttpResponse("错误：分类不存在", status=404)
        except ValueError:
            print(f"无效的分类ID: {category_id}")
            return HttpResponse("错误：无效的分类ID", status=400)

        category.likes = category.likes + 1
        category.save()
        print(f"点赞成功，新的点赞数: {category.likes}")
        return HttpResponse(category.likes)


def jquery_test(request):
    """jQuery功能测试页面"""
    return render(request, "PatentMS/jquery_test.html")


def get_category_list(max_results=0, starts_with=""):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    return category_list


class CategorySuggestionView(View):
    def get(self, request):
        if "suggestion" in request.GET:
            suggestion = request.GET["suggestion"]
        else:
            suggestion = ""

        print(f"收到搜索建议请求: '{suggestion}'")

        category_list = get_category_list(max_results=8, starts_with=suggestion)
        if len(category_list) == 0:
            category_list = Category.objects.order_by("-likes")[:8]

        print(f"找到 {len(category_list)} 个分类")

        # 返回分类列表的HTML片段
        html = '<ul class="list-unstyled">'
        for category in category_list:
            html += f'<li><a href="/category/{category.slug}/">{category.name}</a></li>'
        html += "</ul>"

        return HttpResponse(html)


class SearchAddPageView(View):
    @method_decorator(login_required)
    def get(self, request):
        title = request.GET.get("title")
        url = request.GET.get("url")
        category_id = request.GET.get("category_id")

        print(f"添加页面请求: 标题={title}, URL={url}, 分类ID={category_id}")

        try:
            category = Category.objects.get(id=int(category_id))
            page = Page.objects.get_or_create(category=category, title=title, url=url)[
                0
            ]
            page.save()

            print(f"页面添加成功: {page.title}")

            # 返回更新后的页面列表HTML
            pages = Page.objects.filter(category=category).order_by("-views")
            html = "<ul><h2>页面列表</h2>"
            for p in pages:
                html += f'<li><a href="/goto/?page_id={p.id}">{p.title}</a> - {p.views} view{"s" if p.views != 1 else ""}</li>'
            html += "</ul>"

            return HttpResponse(html)

        except Category.DoesNotExist:
            return HttpResponse("分类不存在", status=404)
        except Exception as e:
            print(f"添加页面失败: {e}")
            return HttpResponse("添加页面失败", status=500)
