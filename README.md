# URL管理系统

一个功能完整的网站收藏和书签管理系统，基于React前端和Django后端开发，支持SQLite和PostgreSQL数据库。

## 项目特点

- 🎨 现代化响应式UI设计（基于Ant Design）
- 📱 移动端友好的自适应布局
- 🔐 完整的用户认证系统（注册/登录/JWT认证）
- 📂 多级分类和标签管理
- 🔍 智能搜索功能
- 📊 数据统计仪表盘
- 🌐 网站和书签双重管理
- 📝 网站笔记和评分功能
- 🎯 用户个人资料管理
- 🔒 数据安全和权限控制

## 技术栈

### 前端
- React 18 + TypeScript
- Ant Design 5.x
- React Router 6
- Axios HTTP客户端
- Context API状态管理

### 后端
- Django 5.2
- Django REST Framework
- JWT认证 (djangorestframework-simplejwt)
- SQLite/PostgreSQL数据库
- CORS支持

## 项目结构

```
URL_MANAGE_SYSTEM_WEB/
├── backend/                # Django后端
│   ├── config/             # 项目配置
│   │   ├── settings.py     # Django设置
│   │   ├── urls.py         # URL路由配置
│   │   └── wsgi.py         # WSGI配置
│   ├── users/              # 用户管理应用
│   │   ├── models.py       # 用户模型
│   │   ├── views.py        # 用户视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # 用户路由
│   ├── websites/           # 网站管理应用
│   │   ├── models.py       # 网站、分类、标签模型
│   │   ├── views.py        # 网站管理视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # 网站路由
│   ├── bookmarks/          # 书签管理应用
│   │   ├── models.py       # 书签模型
│   │   ├── views.py        # 书签视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # 书签路由
│   ├── dashboard/          # 仪表盘应用
│   │   ├── views.py        # 统计数据视图
│   │   └── urls.py         # 仪表盘路由
│   ├── analytics/          # 数据分析应用
│   ├── db.sqlite3          # SQLite数据库文件
│   ├── requirements.txt    # Python依赖
│   └── manage.py           # Django管理脚本
│
├── frontend/               # React前端
│   ├── public/             # 静态资源
│   │   ├── index.html      # HTML模板
│   │   └── favicon.ico     # 网站图标
│   ├── src/                # 源代码
│   │   ├── components/     # 可复用组件
│   │   │   ├── Layout/     # 布局组件
│   │   │   └── ErrorBoundary/ # 错误边界
│   │   ├── contexts/       # React上下文
│   │   │   └── AuthContext.tsx # 认证上下文
│   │   ├── pages/          # 页面组件
│   │   │   ├── Auth/       # 认证页面
│   │   │   ├── Dashboard/  # 仪表盘
│   │   │   ├── Websites/   # 网站管理
│   │   │   ├── Bookmarks/  # 书签管理
│   │   │   ├── Categories/ # 分类管理
│   │   │   └── Profile/    # 个人资料
│   │   ├── services/       # API服务
│   │   │   ├── httpClient.ts # HTTP客户端
│   │   │   └── authService.ts # 认证服务
│   │   ├── utils/          # 工具函数
│   │   │   └── renderSafe.ts # 安全渲染工具
│   │   ├── config/         # 配置文件
│   │   │   └── constants.ts # 常量配置
│   │   ├── App.tsx         # 主应用组件
│   │   └── index.tsx       # 应用入口
│   ├── package.json        # Node.js依赖
│   └── tsconfig.json       # TypeScript配置
│
├── config.ini.example      # 配置文件示例
└── README.md              # 项目说明文档
```

## 快速开始

### 前提条件
- Python 3.8+
- Node.js 16+
- Git

### 1. 克隆项目
```bash
git clone git@github.com:Dajucoder/URL_MANAGE_SYSTEM_WEB.git
cd URL_MANAGE_SYSTEM_WEB
```

### 2. 后端设置

#### 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 配置环境变量（可选）
项目默认使用SQLite数据库，无需额外配置。如需使用PostgreSQL，请设置以下环境变量：

```bash
# Linux/Mac
export DB_ENGINE=django.db.backends.postgresql
export DB_NAME=url_manage_db
export DB_USER=postgres
export DB_PASSWORD=your_password_here
export DB_HOST=localhost
export DB_PORT=5432
export DJANGO_SECRET_KEY=your_secret_key

# Windows PowerShell
$env:DB_ENGINE="django.db.backends.postgresql"
$env:DB_NAME="url_manage_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password_here"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DJANGO_SECRET_KEY="your_secret_key"
```

#### 初始化数据库
```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动后端服务器
python manage.py runserver
```

### 3. 前端设置

#### 安装Node.js依赖
```bash
cd frontend
npm install
```

#### 启动前端开发服务器
```bash
npm start
```

### 4. 访问系统
- 🌐 前端应用: http://localhost:3000
- 🔧 后端API: http://127.0.0.1:8000/api/
- ⚙️ Django管理后台: http://127.0.0.1:8000/admin/

## 功能特性

### 🔐 用户认证
- 用户注册和登录
- JWT令牌认证
- 密码安全存储
- 自动令牌刷新

### 📊 仪表盘
- 数据统计概览
- 最近活动展示
- 快速操作入口
- 可视化图表

### 🌐 网站管理
- 网站信息录入
- 分类和标签管理
- 网站质量评分
- 访问统计记录

### 📖 书签管理
- 书签收藏功能
- 批量操作支持
- 搜索和筛选
- 导入导出功能

### 👤 个人资料
- 用户信息管理
- 主题设置
- 语言偏好
- 密码修改

## API文档

### 认证相关
- `POST /api/users/register/` - 用户注册
- `POST /api/users/login/` - 用户登录
- `POST /api/users/logout/` - 用户登出
- `GET /api/users/info/` - 获取用户信息
- `PATCH /api/users/profile/` - 更新用户资料

### 网站管理
- `GET /api/websites/` - 获取网站列表
- `POST /api/websites/` - 创建新网站
- `GET /api/websites/{id}/` - 获取网站详情
- `PUT /api/websites/{id}/` - 更新网站信息
- `DELETE /api/websites/{id}/` - 删除网站

### 书签管理
- `GET /api/bookmarks/` - 获取书签列表
- `POST /api/bookmarks/` - 创建新书签
- `GET /api/bookmarks/{id}/` - 获取书签详情
- `PUT /api/bookmarks/{id}/` - 更新书签信息
- `DELETE /api/bookmarks/{id}/` - 删除书签

### 分类管理
- `GET /api/websites/categories/` - 获取分类列表
- `POST /api/websites/categories/` - 创建新分类
- `GET /api/websites/categories/{id}/` - 获取分类详情
- `PUT /api/websites/categories/{id}/` - 更新分类信息
- `DELETE /api/websites/categories/{id}/` - 删除分类

### 统计数据
- `GET /api/analytics/dashboard/` - 获取仪表盘统计数据
- `GET /api/analytics/activity/` - 获取活动时间线

## 开发说明

### 代码规范
- 前端使用TypeScript严格模式
- 后端遵循Django最佳实践
- 使用ESLint和Prettier格式化代码
- 遵循RESTful API设计原则

### 安全特性
- 🔒 JWT令牌认证机制
- 🛡️ CORS跨域请求保护
- 🔐 密码哈希存储
- 🚫 SQL注入防护
- 🔑 环境变量配置隔离
- 🛡️ 前端路由权限控制

### 数据库设计
- 用户表：存储用户基本信息和偏好设置
- 网站表：存储网站详细信息和元数据
- 书签表：存储用户收藏的书签
- 分类表：支持多级分类结构
- 标签表：灵活的标签系统

## 部署说明

### 生产环境部署
1. 设置环境变量
2. 配置PostgreSQL数据库
3. 收集静态文件：`python manage.py collectstatic`
4. 使用Gunicorn或uWSGI部署Django
5. 使用Nginx作为反向代理
6. 构建前端：`npm run build`

### Docker部署（推荐）

#### 快速启动
```bash
# Linux/Mac
chmod +x docker-start.sh
./docker-start.sh

# Windows
docker-start.bat
```

#### 手动启动

**开发环境**
```bash
# 启动开发环境（包含热重载）
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up --build -d
```

**生产环境**
```bash
# 启动生产环境
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### Docker服务说明
- **frontend**: React前端应用 (端口: 80)
- **backend**: Django后端API (端口: 8000)
- **db**: PostgreSQL数据库 (端口: 5432)
- **redis**: Redis缓存 (端口: 6379)
- **nginx**: 反向代理 (生产环境，端口: 443)

#### 环境变量配置
生产环境请修改 `docker-compose.yml` 中的以下变量：
- `DJANGO_SECRET_KEY`: Django密钥
- `POSTGRES_PASSWORD`: 数据库密码
- `DB_PASSWORD`: 后端数据库连接密码

#### 数据持久化
- PostgreSQL数据: `postgres_data` volume
- 静态文件: `static_volume` volume  
- 媒体文件: `media_volume` volume

## 贡献指南

1. Fork本项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目地址：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB
- 问题反馈：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/issues

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！
