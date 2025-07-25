# 点赞功能修复方案

## 🔍 问题分析

经过检查，发现点赞功能失效的主要原因：

1. **CSRF Token 缺失**：category.html 模板中没有 CSRF token
2. **HTTP 方法不匹配**：JavaScript 使用 POST 请求，但视图只支持 GET
3. **事件绑定冲突**：可能存在重复的事件绑定

## 🛠️ 修复方案

### 1. 添加 CSRF Token

在 `templates/PatentMS/category.html` 中添加 CSRF token：

```html
{% if category %}
<!-- 添加CSRF Token -->
{% csrf_token %}

<div data-category-id="{{ category.id }}"></div>
```

### 2. 修改视图支持 POST 请求

在 `PatentMS/views.py` 中修改 `LikeCategoryView`：

```python
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
```

### 3. 修改 JavaScript 代码

在 `templates/PatentMS/category.html` 中修改 Ajax 请求：

```javascript
$.ajax({
  url: "/like_category/",
  method: "POST",
  data: {
    category_id: categoryIdVar,
    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
  },
  success: function (data) {
    console.log("点赞成功，返回数据:", data);
    $("#like_count").html(data);

    // 更新按钮状态
    $("#like_btn")
      .removeClass("btn-primary")
      .addClass("btn-success")
      .html('<i class="fas fa-check me-2"></i>已点赞')
      .prop("disabled", true);

    showToast("success", "点赞成功！", "感谢您的支持！");
  },
  error: function (xhr, status, error) {
    console.error("点赞失败:", error);
    likeButtonClicked = false;

    $("#like_btn")
      .removeClass("btn-loading")
      .html('<i class="fas fa-thumbs-up me-2"></i>点赞');
    showToast("error", "点赞失败", "请稍后重试");
  },
});
```

### 4. 确保事件绑定不重复

在 `static/js/PatentMS-jquery.js` 中保持点赞事件被注释：

```javascript
$(document).ready(function () {
    // 移除重复的点赞按钮事件绑定，避免与category.html中的事件冲突
    // $("#like_btn").click(function () {
    //   var categoryIdVar;
    //   categoryIdVar = $(this).attr("data-categoryid");
    //   $.get("/like_category/", { category_id: categoryIdVar }, function (data) {
    //     $("#like_count").html(data);
    //     $("#like_btn").hide();
    //   });
    // });
```

## 🧪 测试步骤

1. **重启 Django 服务器**
2. **访问任意分类页面**
3. **检查浏览器控制台是否有错误**
4. **点击点赞按钮测试功能**
5. **检查点赞数是否更新**

## 🔧 调试信息

如果问题仍然存在，请检查：

1. **浏览器控制台错误信息**
2. **Django 日志文件** (`logs/django.log`)
3. **网络请求** (F12 -> Network 标签)
4. **CSRF token 是否正确传递**

## 📝 注意事项

- 确保用户已登录
- 确保分类存在且有效
- 检查数据库连接
- 验证 URL 配置正确

## ✅ 预期结果

修复后，点赞功能应该：

1. ✅ 点击按钮后显示加载状态
2. ✅ 成功更新点赞数
3. ✅ 按钮变为"已点赞"状态
4. ✅ 显示成功提示消息
5. ✅ 防止重复点击
