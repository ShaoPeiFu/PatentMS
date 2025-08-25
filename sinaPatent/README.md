# 新浪专利管理系统

一个基于 Django 的专利分类和管理系统，提供用户注册、分类管理、页面添加等功能。

## 🚀 功能特性

- **用户管理**：用户注册、登录、档案管理
- **分类管理**：创建和管理专利分类
- **页面管理**：为分类添加相关页面
- **点赞功能**：用户可以为分类点赞
- **搜索功能**：实时搜索分类建议
- **响应式设计**：支持移动端和桌面端

## 🛠️ 技术栈

- **后端**：Django 4.0.5
- **前端**：Bootstrap 4.2, jQuery 3.7.1
- **数据库**：SQLite3
- **用户认证**：django-registration-redux
- **静态文件**：Django Static Files

## 📋 系统要求

- Python 3.8+
- Django 4.0.5
- 其他依赖见 `requirements.txt`

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd sinaPatent
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 运行开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 查看应用

## 📁 项目结构

```
sinaPatent/
├── PatentMS/                 # 主应用
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   ├── forms.py             # 表单
│   ├── utils.py             # 工具函数
│   ├── tests.py             # 测试文件
│   └── management/          # 管理命令
├── sinaPatent/              # 项目配置
│   ├── settings.py          # 设置文件
│   ├── urls.py              # URL配置
│   └── wsgi.py              # WSGI配置
├── templates/               # 模板文件
│   ├── PatentMS/           # 应用模板
│   └── registration/       # 注册模板
├── static/                  # 静态文件
│   ├── js/                 # JavaScript文件
│   └── images/             # 图片文件
├── media/                   # 用户上传文件
├── logs/                    # 日志文件
└── requirements.txt         # 依赖列表
```

## 🗄️ 数据模型

### Category（分类）

- `name`: 分类名称
- `views`: 浏览次数
- `likes`: 点赞次数
- `slug`: URL 别名

### Page（页面）

- `category`: 所属分类
- `title`: 页面标题
- `url`: 页面 URL
- `views`: 浏览次数

### UserProfile（用户档案）

- `user`: 关联用户
- `website`: 个人网站
- `picture`: 头像

## 🔧 管理命令

### 数据清理

```bash
# 查看将要删除的数据
python manage.py cleanup_data --dry-run

# 清理重复数据
python manage.py cleanup_data --duplicates

# 清理孤立数据
python manage.py cleanup_data --orphans

# 清理所有无效数据
python manage.py cleanup_data
```

## 🧪 运行测试

```bash
# 运行所有测试
python manage.py test

# 运行特定测试
python manage.py test PatentMS.tests.CategoryMethodTests

# 生成测试覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🔒 安全设置

项目包含以下安全特性：

- CSRF 保护
- XSS 过滤
- 内容类型嗅探保护
- 安全的会话设置
- 密码验证

## 📝 日志

日志文件位于 `logs/django.log`，包含：

- 应用错误
- 用户操作
- 系统事件

## 🚀 部署

### 生产环境设置

1. 修改 `settings.py`：

   - 设置 `DEBUG = False`
   - 配置生产数据库
   - 设置 `ALLOWED_HOSTS`
   - 配置静态文件

2. 收集静态文件：

   ```bash
   python manage.py collectstatic
   ```

3. 使用生产服务器（如 Gunicorn）：
   ```bash
   pip install gunicorn
   gunicorn sinaPatent.wsgi:application
   ```

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **开发团队** - 新浪专利管理系统开发组



---

**注意**：这是一个开发版本，请在生产环境中谨慎使用。
