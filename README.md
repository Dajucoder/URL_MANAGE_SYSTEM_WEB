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
├── docs/                   # 项目文档
│   └── development-plan.md # 开发规划文档
├── config.ini.example      # 配置文件示例
├── docker-compose.yml      # Docker生产环境配置
├── docker-compose.dev.yml  # Docker开发环境配置
├── LICENSE                 # MIT许可证
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

### 2. 本地开发环境

#### 后端设置
```bash
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动后端服务器
python manage.py runserver
```

#### 前端设置
```bash
cd frontend

# 安装Node.js依赖
npm install

# 启动前端开发服务器
npm start
```

### 3. Docker部署

#### 开发环境
```bash
# 启动开发环境（包含热重载）
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up --build -d
```

#### 生产环境
```bash
# 启动生产环境
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
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

## Docker服务说明

### 服务组件
- **frontend**: React前端应用 (端口: 80)
- **backend**: Django后端API (端口: 8000)
- **db**: PostgreSQL数据库 (端口: 5432)
- **redis**: Redis缓存 (端口: 6379)
- **nginx**: 反向代理 (生产环境，端口: 443)

### 环境变量配置
生产环境请修改 `docker-compose.yml` 中的以下变量：
- `DJANGO_SECRET_KEY`: Django密钥
- `POSTGRES_PASSWORD`: 数据库密码
- `DB_PASSWORD`: 后端数据库连接密码

### 数据持久化
- PostgreSQL数据: `postgres_data` volume
- 静态文件: `static_volume` volume  
- 媒体文件: `media_volume` volume

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

## 开发规划

详细的开发规划和路线图请查看：[开发规划文档](docs/development-plan.md)

### 短期目标 (v1.1)
- 搜索功能优化
- 用户体验提升
- 移动端适配
- 数据导入/导出

### 中期目标 (v1.2-1.5)
- AI推荐系统
- 浏览器插件
- 第三方集成
- 性能优化

### 长期目标 (v2.0+)
- 多用户协作
- 企业级功能
- 微服务架构
- 插件系统

## 贡献指南

1. Fork本项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交Pull Request

### 开发流程
1. 查看[开发规划文档](docs/development-plan.md)了解项目方向
2. 在Issues中讨论新功能或bug修复
3. 遵循代码规范和测试要求
4. 提交前确保所有测试通过

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目地址：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB
- 问题反馈：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/issues
- 开发规划：[docs/development-plan.md](docs/development-plan.md)

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！