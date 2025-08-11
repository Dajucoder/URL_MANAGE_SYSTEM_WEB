# URL管理系统

一个功能完整的网站收藏和书签管理系统，基于React前端和Django后端开发，支持SQLite和PostgreSQL数据库。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> 🚀 一个现代化的网站收藏和书签管理解决方案，提供完整的用户认证、分类管理、数据统计等功能。

## 项目特点

- 🎨 现代化响应式UI设计（基于Ant Design 5.x）
- 📱 移动端友好的自适应布局
- 🔐 完整的用户认证系统（注册/登录/JWT认证）
- 📂 多级分类和标签管理
- 🔍 智能搜索功能
- 📊 数据统计仪表盘
- 🌐 网站和书签双重管理
- 📝 网站笔记和评分功能
- 🎯 用户个人资料管理
- 🔒 数据安全和权限控制
- 🐳 Docker容器化部署支持
- 🚀 生产环境优化配置

## 技术栈

### 前端
- **React 19.1** + TypeScript 4.9
- **Ant Design 5.26** - 企业级UI组件库
- **React Router 7.8** - 路由管理
- **Axios 1.11** - HTTP客户端
- **Ant Design Plots 2.6** - 数据可视化
- Context API状态管理

### 后端
- **Django 4.2** - Web框架
- **Django REST Framework 3.14** - API框架
- **JWT认证** (djangorestframework-simplejwt 5.3)
- **PostgreSQL/SQLite** - 数据库支持
- **Redis 5.0** - 缓存和会话存储
- **Celery 5.3** - 异步任务队列
- **BeautifulSoup4** - 网页内容解析
- **Gunicorn** - WSGI服务器

### 部署
- **Docker & Docker Compose** - 容器化部署
- **Nginx** - 反向代理和静态文件服务
- **WhiteNoise** - 静态文件处理
- **PostgreSQL** - 生产环境数据库

## 项目结构

```
URL_MANAGE_SYSTEM_WEB/
├── backend/                    # Django后端
│   ├── config/                 # 项目配置
│   │   ├── settings.py         # Django设置
│   │   ├── urls.py             # URL路由配置
│   │   └── wsgi.py             # WSGI配置
│   ├── users/                  # 用户管理应用
│   │   ├── management/         # 管理命令
│   │   │   └── commands/
│   │   │       └── create_admin.py  # 创建管理员命令
│   │   ├── models.py           # 用户模型
│   │   ├── views.py            # 用户视图
│   │   ├── serializers.py      # 序列化器
│   │   └── urls.py             # 用户路由
│   ├── websites/               # 网站管理应用
│   │   ├── management/         # 管理命令
│   │   │   └── commands/
│   │   │       └── init_default_data.py  # 初始化数据
│   │   ├── models.py           # 网站、分类、标签模型
│   │   ├── views.py            # 网站管理视图
│   │   ├── serializers.py      # 序列化器
│   │   └── urls.py             # 网站路由
│   ├── bookmarks/              # 书签管理应用
│   ├── dashboard/              # 仪表盘应用
│   ├── analytics/              # 数据分析应用
│   ├── entrypoint.sh           # Docker入口脚本
│   ├── Dockerfile              # Docker镜像构建文件
│   ├── requirements.txt        # Python依赖
│   └── manage.py               # Django管理脚本
│
├── frontend/                   # React前端
│   ├── public/                 # 静态资源
│   │   ├── index.html          # HTML模板
│   │   └── favicon.ico         # 网站图标
│   ├── src/                    # 源代码
│   │   ├── components/         # 可复用组件
│   │   │   ├── Layout/         # 布局组件
│   │   │   └── ErrorBoundary/  # 错误边界
│   │   ├── contexts/           # React上下文
│   │   │   └── AuthContext.tsx # 认证上下文
│   │   ├── pages/              # 页面组件
│   │   │   ├── Auth/           # 认证页面
│   │   │   ├── Dashboard/      # 仪表盘
│   │   │   ├── Websites/       # 网站管理
│   │   │   ├── Bookmarks/      # 书签管理
│   │   │   ├── Categories/     # 分类管理
│   │   │   └── Profile/        # 个人资料
│   │   ├── services/           # API服务
│   │   │   ├── httpClient.ts   # HTTP客户端
│   │   │   └── authService.ts  # 认证服务
│   │   ├── utils/              # 工具函数
│   │   │   └── renderSafe.ts   # 安全渲染工具
│   │   ├── config/             # 配置文件
│   │   │   └── constants.ts    # 常量配置
│   │   ├── App.tsx             # 主应用组件
│   │   └── index.tsx           # 应用入口
│   ├── Dockerfile.dev          # 开发环境Docker文件
│   ├── package.json            # Node.js依赖
│   └── tsconfig.json           # TypeScript配置
│
├── docs/                       # 项目文档
│   ├── API.md                  # API接口文档
│   ├── DEPLOYMENT.md           # 部署指南
│   ├── development-plan.md     # 开发规划文档
│   ├── SECURITY_CHECK.md       # 安全检查清单
│   └── SECURITY_NOTES.md       # 安全部署说明
├── config.ini.example          # 配置文件示例
├── docker-compose.yml          # Docker生产环境配置
├── docker-compose.dev.yml      # Docker开发环境配置
├── LICENSE                     # MIT许可证
└── README.md                   # 项目说明文档
```

## 快速开始

### 前提条件
- Python 3.8+
- Node.js 16+
- Git
- Docker & Docker Compose（可选）

### 方式一：本地开发环境

#### 1. 克隆项目
```bash
git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB.git
cd URL_MANAGE_SYSTEM_WEB
```

#### 2. 后端设置
```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp ../config.ini.example ../config.ini
# 编辑 config.ini 文件，设置数据库和其他配置

# 初始化数据库
python manage.py makemigrations
python manage.py migrate

# 创建管理员账户
python manage.py create_admin --username admin --password your_password --email admin@example.com

# 初始化默认数据（可选）
python manage.py init_default_data

# 启动后端服务器
python manage.py runserver
```

#### 3. 前端设置
```bash
cd frontend

# 安装Node.js依赖
npm install

# 配置环境变量
# 创建 .env 文件并设置 REACT_APP_API_URL=http://localhost:8000/api

# 启动前端开发服务器
npm start
```

### 方式二：Docker部署

#### 开发环境
```bash
# 启动开发环境（包含热重载）
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up --build -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 停止服务
docker-compose -f docker-compose.dev.yml down
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
- 🌐 **前端应用**: http://localhost:3000
- 🔧 **后端API**: http://localhost:8000/api/
- ⚙️ **Django管理后台**: http://localhost:8000/admin/
- 📊 **API文档**: http://localhost:8000/api/docs/

## 配置说明

### 环境变量配置

#### 后端配置 (config.ini)
```ini
[database]
ENGINE = django.db.backends.sqlite3
NAME = db.sqlite3
# 生产环境使用PostgreSQL
# ENGINE = django.db.backends.postgresql
# NAME = url_manage_db
# USER = your_db_user
# PASSWORD = your_db_password
# HOST = localhost
# PORT = 5432

[secret]
SECRET_KEY = your-secret-key-here

[debug]
DEBUG = True
ALLOWED_HOSTS = localhost,127.0.0.1

[cors]
ALLOWED_ORIGINS = http://localhost:3000,http://127.0.0.1:3000
```

#### 前端配置 (.env)
```env
PORT=3000
REACT_APP_API_URL=http://localhost:8000/api
GENERATE_SOURCEMAP=false
```

### Docker环境变量
生产环境请修改 `docker-compose.yml` 中的以下变量：
- `DJANGO_SECRET_KEY`: Django密钥
- `POSTGRES_PASSWORD`: 数据库密码
- `DB_PASSWORD`: 后端数据库连接密码

## 功能特性

### 🔐 用户认证系统
- 用户注册和登录
- JWT令牌认证
- 密码安全存储和验证
- 自动令牌刷新
- 密码修改功能

### 📊 数据统计仪表盘
- 网站和书签数量统计
- 分类分布图表
- 最近活动时间线
- 访问统计分析
- 可视化数据展示

### 🌐 网站管理
- 网站信息自动抓取
- 分类和标签管理
- 网站质量评分
- 访问统计记录
- 网站截图功能
- 批量操作支持

### 📖 书签管理
- 书签收藏功能
- 收藏夹分组管理
- 批量操作支持
- 搜索和筛选
- 导入导出功能

### 👤 个人资料管理
- 用户信息编辑
- 主题设置
- 语言偏好
- 隐私设置
- 账户安全管理

### 🔍 搜索功能
- 全文搜索
- 分类筛选
- 标签过滤
- 高级搜索选项

## API文档

### 认证相关
```
POST /api/users/register/     # 用户注册
POST /api/users/login/        # 用户登录
POST /api/users/logout/       # 用户登出
GET  /api/users/info/         # 获取用户信息
PATCH /api/users/profile/     # 更新用户资料
POST /api/users/change-password/  # 修改密码
```

### 网站管理
```
GET    /api/websites/         # 获取网站列表
POST   /api/websites/         # 创建新网站
GET    /api/websites/{id}/    # 获取网站详情
PUT    /api/websites/{id}/    # 更新网站信息
DELETE /api/websites/{id}/    # 删除网站
GET    /api/websites/search/  # 搜索网站
```

### 书签管理
```
GET    /api/bookmarks/        # 获取书签列表
POST   /api/bookmarks/        # 创建新书签
GET    /api/bookmarks/{id}/   # 获取书签详情
PUT    /api/bookmarks/{id}/   # 更新书签信息
DELETE /api/bookmarks/{id}/   # 删除书签
```

### 分类管理
```
GET    /api/websites/categories/     # 获取分类列表
POST   /api/websites/categories/     # 创建新分类
GET    /api/websites/categories/{id}/ # 获取分类详情
PUT    /api/websites/categories/{id}/ # 更新分类信息
DELETE /api/websites/categories/{id}/ # 删除分类
```

### 统计数据
```
GET /api/dashboard/stats/     # 获取仪表盘统计数据
GET /api/dashboard/activity/  # 获取活动时间线
GET /api/analytics/reports/   # 获取分析报告
```

## Docker服务说明

### 服务组件
- **frontend**: React前端应用 (端口: 3000/80)
- **backend**: Django后端API (端口: 8000)
- **db**: PostgreSQL数据库 (端口: 5432)
- **redis**: Redis缓存 (端口: 6379)
- **nginx**: 反向代理 (生产环境，端口: 80/443)

### 数据持久化
- PostgreSQL数据: `postgres_data` volume
- 静态文件: `static_volume` volume  
- 媒体文件: `media_volume` volume
- Redis数据: `redis_data` volume

### 健康检查
所有服务都配置了健康检查，确保服务正常运行：
- 前端：HTTP GET /
- 后端：HTTP GET /api/health/
- 数据库：pg_isready命令
- Redis：redis-cli ping

## 安全特性

### 🔒 认证与授权
- JWT令牌认证机制
- 令牌自动刷新
- 密码哈希存储（bcrypt）
- 用户权限控制

### 🛡️ 安全防护
- CORS跨域请求保护
- SQL注入防护
- XSS攻击防护
- CSRF令牌验证
- 环境变量配置隔离

### 🔐 数据保护
- 敏感文件通过.gitignore保护
- 生产环境配置分离
- 数据库连接加密
- 静态文件安全访问

**重要提醒**：部署前请阅读 [docs/SECURITY_NOTES.md](docs/SECURITY_NOTES.md) 了解安全配置要求。

## 开发说明

### 代码规范
- 前端使用TypeScript严格模式
- 后端遵循Django最佳实践
- 使用ESLint和Prettier格式化代码
- 遵循RESTful API设计原则
- Git提交信息规范

### 数据库设计
- **用户表**：存储用户基本信息和偏好设置
- **网站表**：存储网站详细信息和元数据
- **书签表**：存储用户收藏的书签
- **分类表**：支持多级分类结构
- **标签表**：灵活的标签系统
- **收藏夹表**：书签分组管理

### 测试
```bash
# 后端测试
cd backend
python manage.py test

# 前端测试
cd frontend
npm test
```

## 部署指南

### 生产环境部署

1. **服务器要求**
   - Ubuntu 20.04+ / CentOS 8+ / Debian 11+
   - Docker 20.10+ 和 Docker Compose 2.0+
   - 最低配置：2GB RAM, 2 CPU核心, 20GB存储
   - 推荐配置：4GB RAM, 4 CPU核心, 50GB存储
   - 开放端口：80, 443, 22

2. **部署步骤**
```bash
# 1. 克隆项目
git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB.git
cd URL_MANAGE_SYSTEM_WEB

# 2. 配置环境变量
cp config.ini.example config.ini
# 编辑 config.ini 设置生产环境配置
nano config.ini

# 3. 配置Docker环境变量
# 编辑 docker-compose.yml 中的环境变量
nano docker-compose.yml

# 4. 启动服务
docker-compose up -d

# 5. 等待服务启动完成
docker-compose logs -f

# 6. 初始化数据库
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py create_admin --username admin --password your_secure_password --email admin@yourdomain.com

# 7. 初始化默认数据（可选）
docker-compose exec backend python manage.py init_default_data

# 8. 验证部署
curl http://localhost/api/health/
```

3. **SSL证书配置**
```bash
# 使用Certbot获取Let's Encrypt证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

4. **Nginx配置示例**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 监控和维护

#### 健康检查
```bash
# 检查服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f [service_name]

# 检查系统资源使用
docker stats

# 检查磁盘空间
df -h
```

#### 数据备份
```bash
# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/backup/url_manage_system"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T db pg_dump -U postgres url_manage_db > $BACKUP_DIR/db_backup_$DATE.sql

# 备份媒体文件
docker cp $(docker-compose ps -q backend):/app/media $BACKUP_DIR/media_$DATE

# 清理7天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "media_*" -mtime +7 -exec rm -rf {} \;
```

#### 日志管理
```bash
# 配置日志轮转
sudo nano /etc/logrotate.d/docker-compose

# 内容：
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
```

#### 性能优化
- 启用Redis缓存提升响应速度
- 配置数据库连接池
- 使用CDN加速静态资源
- 启用Gzip压缩
- 定期清理无用的Docker镜像和容器

## 📚 项目文档

本项目提供完整的文档体系，所有文档统一存放在 `docs/` 目录中：

- **[API.md](docs/API.md)** - 详细的API接口文档，包含所有端点说明和示例
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - 完整的部署指南，包含生产环境配置
- **[development-plan.md](docs/development-plan.md)** - 项目开发规划和路线图
- **[SECURITY_CHECK.md](docs/SECURITY_CHECK.md)** - 安全检查清单和配置验证
- **[SECURITY_NOTES.md](docs/SECURITY_NOTES.md)** - 安全部署说明和最佳实践

## 开发规划

详细的开发规划和路线图请查看：[开发规划文档](docs/development-plan.md)

### 已完成功能 ✅
- 用户认证系统
- 网站和书签管理
- 分类标签系统
- 数据统计仪表盘
- Docker容器化部署
- 安全配置优化

### 短期目标 (v1.1) 🚀
- [ ] 搜索功能优化
- [ ] 用户体验提升
- [ ] 移动端适配优化
- [ ] 数据导入/导出功能
- [ ] 浏览器书签导入

### 中期目标 (v1.2-1.5) 🎯
- [ ] AI推荐系统
- [ ] 浏览器插件开发
- [ ] 第三方服务集成
- [ ] 性能优化
- [ ] 多语言支持

### 长期目标 (v2.0+) 🌟
- [ ] 多用户协作功能
- [ ] 企业级功能
- [ ] 微服务架构重构
- [ ] 插件系统
- [ ] 移动端APP

## 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork本项目
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'feat: add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交Pull Request

### 提交规范
使用约定式提交格式：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 开发流程
1. 查看[开发规划文档](docs/development-plan.md)了解项目方向
2. 在Issues中讨论新功能或bug修复
3. 遵循代码规范和测试要求
4. 提交前确保所有测试通过
5. 更新相关文档

## 常见问题

### Q: 如何重置管理员密码？
A: 使用管理命令：
```bash
python manage.py create_admin --username admin --password new_password --email admin@example.com
```

### Q: 如何备份和恢复数据？
A: 
```bash
# 备份数据
python manage.py dumpdata > backup.json

# 恢复数据
python manage.py loaddata backup.json
```

### Q: 如何切换到PostgreSQL？
A: 
1. 修改 `config.ini` 中的数据库配置：
```ini
[database]
ENGINE = django.db.backends.postgresql
NAME = url_manage_db
USER = your_db_user
PASSWORD = your_db_password
HOST = localhost
PORT = 5432
```
2. 安装PostgreSQL依赖：`pip install psycopg2-binary`
3. 重新运行迁移：`python manage.py migrate`

### Q: Docker容器启动失败怎么办？
A: 
1. 检查日志：`docker-compose logs -f`
2. 确保端口未被占用：`netstat -tulpn | grep :3000`
3. 检查Docker服务状态：`docker ps -a`
4. 重新构建镜像：`docker-compose up --build`

### Q: 如何启用HTTPS？
A: 
1. 获取SSL证书（推荐Let's Encrypt）
2. 配置Nginx反向代理
3. 修改前端API地址为HTTPS
4. 更新CORS设置

### Q: 如何导入浏览器书签？
A: 
1. 从浏览器导出书签为HTML格式
2. 使用管理后台的导入功能
3. 或通过API批量导入：`POST /api/bookmarks/import/`

### Q: 系统性能优化建议？
A: 
- 启用Redis缓存
- 配置数据库索引
- 使用CDN加速静态资源
- 启用Gzip压缩
- 定期清理日志文件

## 故障排除

### 🔧 常见问题解决

#### 前端问题
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install

# 检查端口占用
lsof -i :3000
```

#### 后端问题
```bash
# 检查Django配置
python manage.py check

# 查看详细错误信息
python manage.py runserver --verbosity=2

# 重置数据库
python manage.py flush
python manage.py migrate
```

#### Docker问题
```bash
# 清理Docker资源
docker system prune -a

# 重新构建镜像
docker-compose build --no-cache

# 查看容器资源使用
docker stats

# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend sh
```

#### 数据库问题
```bash
# 检查数据库连接
python manage.py dbshell

# 查看数据库状态
docker-compose exec db psql -U postgres -c "\l"

# 重建索引
python manage.py migrate --run-syncdb
```

### 🚨 紧急恢复

#### 服务无法启动
1. 检查日志：`docker-compose logs -f`
2. 验证配置文件：`config.ini`
3. 检查端口占用：`netstat -tulpn`
4. 重启服务：`docker-compose restart`

#### 数据丢失恢复
1. 停止服务：`docker-compose down`
2. 恢复数据库备份：`docker-compose exec db psql -U postgres url_manage_db < backup.sql`
3. 恢复媒体文件：`docker cp backup/media/. container:/app/media/`
4. 重启服务：`docker-compose up -d`

#### 性能问题诊断
```bash
# 查看系统资源
htop
iostat -x 1

# 查看数据库性能
docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_activity;"

# 查看应用日志
docker-compose logs backend | grep ERROR
```

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 📧 **项目地址**：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB
- 🐛 **问题反馈**：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/issues
- 📋 **开发规划**：[docs/development-plan.md](docs/development-plan.md)
- 🔒 **安全说明**：[docs/SECURITY_NOTES.md](docs/SECURITY_NOTES.md)
- 📚 **API文档**：[docs/API.md](docs/API.md)
- 🚀 **部署指南**：[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- ✅ **安全检查**：[docs/SECURITY_CHECK.md](docs/SECURITY_CHECK.md)

## 版本历史

### v1.0.0 (2025-01-11)
- ✅ 完整的用户认证系统
- ✅ 网站和书签管理功能
- ✅ 分类标签系统
- ✅ 数据统计仪表盘
- ✅ Docker容器化部署
- ✅ 响应式UI设计
- ✅ RESTful API架构
- ✅ 安全防护机制

### 即将发布 (v1.1.0)
- 🔄 搜索功能优化
- 🔄 用户体验提升
- 🔄 移动端适配优化
- 🔄 数据导入/导出功能
- 🔄 浏览器书签导入

## 项目统计

- 📊 **代码行数**: ~15,000+ 行
- 🏗️ **架构**: 前后端分离
- 🧪 **测试覆盖率**: 目标 80%+
- 📱 **支持平台**: Web, 移动端浏览器
- 🌍 **多语言**: 计划支持中英文
- 👥 **团队规模**: 1-5人小团队

## 致谢

感谢所有为这个项目做出贡献的开发者！

特别感谢以下开源项目：
- [React](https://reactjs.org/) - 前端框架
- [Django](https://www.djangoproject.com/) - 后端框架
- [Ant Design](https://ant.design/) - UI组件库
- [Docker](https://www.docker.com/) - 容器化技术

---

⭐ **如果这个项目对您有帮助，请给个Star支持一下！**

🚀 **欢迎提交Issue和Pull Request，让我们一起完善这个项目！**

📧 **有问题或建议？欢迎通过Issue或邮件联系我们！**
