# API 接口文档

## 概述

URL管理系统提供完整的RESTful API接口，支持用户认证、网站管理、书签管理、分类标签管理、数据统计等功能。基于Django REST Framework构建，遵循RESTful设计原则。

## 基础信息

- **Base URL**: `http://localhost:8000/api/` (开发环境)
- **生产环境**: `https://yourdomain.com/api/`
- **认证方式**: JWT Token (djangorestframework-simplejwt)
- **数据格式**: JSON
- **字符编码**: UTF-8
- **API版本**: v1.0
- **文档更新**: 2025-01-11

## 认证

### 获取Token
```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应示例**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

### 使用Token
在请求头中添加：
```http
Authorization: Bearer <access_token>
```

## 用户管理

### 用户注册
```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secure_password",
  "password_confirm": "secure_password"
}
```

### 获取用户信息
```http
GET /api/users/info/
Authorization: Bearer <token>
```

### 更新用户资料
```http
PATCH /api/users/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 修改密码
```http
POST /api/users/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "old_password",
  "new_password": "new_password"
}
```

## 网站管理

### 获取网站列表
```http
GET /api/websites/
Authorization: Bearer <token>

# 查询参数
?page=1&page_size=20&category=1&search=github
```

**响应示例**:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/websites/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "GitHub",
      "url": "https://github.com",
      "description": "代码托管平台",
      "category": {
        "id": 1,
        "name": "开发工具"
      },
      "tags": [
        {"id": 1, "name": "git"},
        {"id": 2, "name": "代码"}
      ],
      "rating": 5,
      "visit_count": 10,
      "created_at": "2025-01-11T10:00:00Z",
      "updated_at": "2025-01-11T10:00:00Z"
    }
  ]
}
```

### 创建网站
```http
POST /api/websites/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "新网站",
  "url": "https://example.com",
  "description": "网站描述",
  "category": 1,
  "tags": [1, 2],
  "rating": 4
}
```

### 获取网站详情
```http
GET /api/websites/{id}/
Authorization: Bearer <token>
```

### 更新网站
```http
PUT /api/websites/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "更新的标题",
  "description": "更新的描述",
  "rating": 5
}
```

### 删除网站
```http
DELETE /api/websites/{id}/
Authorization: Bearer <token>
```

### 搜索网站
```http
GET /api/websites/search/
Authorization: Bearer <token>

# 查询参数
?q=github&category=1&tags=1,2
```

## 书签管理

### 获取书签列表
```http
GET /api/bookmarks/
Authorization: Bearer <token>

# 查询参数
?folder=1&page=1&page_size=20
```

### 创建书签
```http
POST /api/bookmarks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "书签标题",
  "url": "https://example.com",
  "folder": 1,
  "description": "书签描述"
}
```

### 更新书签
```http
PUT /api/bookmarks/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "新标题",
  "folder": 2
}
```

### 删除书签
```http
DELETE /api/bookmarks/{id}/
Authorization: Bearer <token>
```

## 分类管理

### 获取分类列表
```http
GET /api/websites/categories/
Authorization: Bearer <token>
```

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "开发工具",
    "description": "编程开发相关工具",
    "parent": null,
    "children": [
      {
        "id": 2,
        "name": "版本控制",
        "parent": 1
      }
    ],
    "website_count": 15
  }
]
```

### 创建分类
```http
POST /api/websites/categories/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "新分类",
  "description": "分类描述",
  "parent": 1
}
```

### 更新分类
```http
PUT /api/websites/categories/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "更新的分类名",
  "description": "更新的描述"
}
```

### 删除分类
```http
DELETE /api/websites/categories/{id}/
Authorization: Bearer <token>
```

## 标签管理

### 获取标签列表
```http
GET /api/websites/tags/
Authorization: Bearer <token>
```

### 创建标签
```http
POST /api/websites/tags/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "新标签",
  "color": "#ff0000"
}
```

## 统计数据

### 获取仪表盘统计
```http
GET /api/dashboard/stats/
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "total_websites": 150,
  "total_bookmarks": 89,
  "total_categories": 12,
  "total_tags": 25,
  "recent_websites": 5,
  "popular_categories": [
    {"name": "开发工具", "count": 45},
    {"name": "学习资源", "count": 32}
  ],
  "monthly_stats": {
    "websites_added": 12,
    "bookmarks_added": 8
  }
}
```

### 获取活动时间线
```http
GET /api/dashboard/activity/
Authorization: Bearer <token>

# 查询参数
?limit=10&days=7
```

## 数据导入导出

### 导出数据
```http
GET /api/export/
Authorization: Bearer <token>

# 查询参数
?format=json&type=websites,bookmarks
```

### 导入数据
```http
POST /api/import/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <选择文件>
format: json
```

## 错误处理

### 错误响应格式
```json
{
  "error": "错误类型",
  "message": "详细错误信息",
  "code": "ERROR_CODE",
  "details": {
    "field": ["字段错误信息"]
  }
}
```

### 常见错误码
- `400` - 请求参数错误
- `401` - 未认证或Token过期
- `403` - 权限不足
- `404` - 资源不存在
- `429` - 请求频率限制
- `500` - 服务器内部错误

## 请求限制

- **频率限制**: 每分钟最多100次请求
- **文件上传**: 最大10MB
- **批量操作**: 单次最多100条记录

## SDK和工具

### JavaScript SDK
```javascript
import { URLManageAPI } from 'url-manage-sdk';

const api = new URLManageAPI({
  baseURL: 'http://localhost:8000/api',
  token: 'your_jwt_token'
});

// 获取网站列表
const websites = await api.websites.list();

// 创建网站
const newWebsite = await api.websites.create({
  title: 'GitHub',
  url: 'https://github.com'
});
```

### Python SDK
```python
from url_manage_client import URLManageClient

client = URLManageClient(
    base_url='http://localhost:8000/api',
    token='your_jwt_token'
)

# 获取网站列表
websites = client.websites.list()

# 创建网站
new_website = client.websites.create({
    'title': 'GitHub',
    'url': 'https://github.com'
})
```

## 测试

### 使用curl测试
```bash
# 登录获取token
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 使用token访问API
curl -X GET http://localhost:8000/api/websites/ \
  -H "Authorization: Bearer <your_token>"
```

### 使用Postman
1. 导入API集合文件：`docs/postman_collection.json`
2. 设置环境变量：`base_url`, `token`
3. 运行测试用例

## 健康检查

### 系统健康状态
```http
GET /api/health/
```

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-11T14:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "storage": "available"
  },
  "uptime": "2 days, 14:30:25"
}
```

## 分页说明

所有列表接口都支持分页，使用以下参数：
- `page`: 页码（从1开始）
- `page_size`: 每页数量（默认20，最大100）

**分页响应格式**:
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/websites/?page=3",
  "previous": "http://localhost:8000/api/websites/?page=1",
  "results": [...]
}
```

## 搜索和过滤

### 全文搜索
```http
GET /api/websites/?search=github
GET /api/bookmarks/?search=开发工具
```

### 分类过滤
```http
GET /api/websites/?category=1
GET /api/websites/?category__name=开发工具
```

### 标签过滤
```http
GET /api/websites/?tags=1,2,3
GET /api/websites/?tags__name=git,代码
```

### 日期范围过滤
```http
GET /api/websites/?created_after=2025-01-01
GET /api/websites/?created_before=2025-12-31
GET /api/websites/?updated_since=2025-01-10
```

### 排序
```http
GET /api/websites/?ordering=-created_at
GET /api/websites/?ordering=title
GET /api/websites/?ordering=-rating,title
```

可用排序字段：
- `title`: 标题
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `rating`: 评分
- `visit_count`: 访问次数

## 批量操作

### 批量创建网站
```http
POST /api/websites/batch/
Authorization: Bearer <token>
Content-Type: application/json

{
  "websites": [
    {
      "title": "GitHub",
      "url": "https://github.com",
      "category": 1
    },
    {
      "title": "GitLab",
      "url": "https://gitlab.com",
      "category": 1
    }
  ]
}
```

### 批量删除
```http
DELETE /api/websites/batch/
Authorization: Bearer <token>
Content-Type: application/json

{
  "ids": [1, 2, 3, 4, 5]
}
```

### 批量更新分类
```http
PATCH /api/websites/batch/
Authorization: Bearer <token>
Content-Type: application/json

{
  "ids": [1, 2, 3],
  "data": {
    "category": 2
  }
}
```

## 文件上传

### 上传网站图标
```http
POST /api/websites/{id}/upload-icon/
Authorization: Bearer <token>
Content-Type: multipart/form-data

icon: <选择图片文件>
```

### 支持的文件格式
- 图片：PNG, JPG, JPEG, GIF, WebP
- 最大文件大小：5MB
- 推荐尺寸：32x32, 64x64, 128x128

## WebHooks

### 配置WebHook
```http
POST /api/webhooks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["website.created", "website.updated", "website.deleted"],
  "secret": "your_webhook_secret"
}
```

### 支持的事件
- `website.created`: 网站创建
- `website.updated`: 网站更新
- `website.deleted`: 网站删除
- `bookmark.created`: 书签创建
- `category.created`: 分类创建

## 更新日志

### v1.0.0 (2025-01-11)
- ✅ 完整的RESTful API架构
- ✅ JWT认证机制和令牌刷新
- ✅ 用户注册、登录、资料管理
- ✅ 网站CRUD操作和搜索功能
- ✅ 书签管理和收藏夹功能
- ✅ 分类和标签系统
- ✅ 数据统计和仪表盘接口
- ✅ 文件上传和媒体处理
- ✅ 分页、排序、过滤功能
- ✅ 错误处理和状态码规范
- ✅ API文档和健康检查

### 即将发布 (v1.1.0)
- 🔄 批量操作API优化
- 🔄 高级搜索功能
- 🔄 数据导入导出API
- 🔄 WebHook通知系统
- 🔄 API访问统计和限流
- 🔄 GraphQL支持

### 计划中的功能 (v1.2+)
- 📋 WebSocket实时通知
- 📋 API版本控制 (v2)
- 📋 第三方集成API
- 📋 移动端专用API
- 📋 AI推荐接口
- 📋 数据分析API

## 开发工具

### Postman集合
下载并导入Postman集合文件：
```bash
curl -O https://raw.githubusercontent.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/master/docs/postman_collection.json
```

### OpenAPI规范
访问交互式API文档：
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

### 开发环境测试
```bash
# 启动开发服务器
docker-compose -f docker-compose.dev.yml up

# 运行API测试
cd backend
python manage.py test api

# 生成测试覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 技术支持

- 📚 **完整文档**: [项目README](../README.md)
- 🚀 **部署指南**: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔒 **安全说明**: [SECURITY_NOTES.md](SECURITY_NOTES.md)
- ✅ **安全检查**: [SECURITY_CHECK.md](SECURITY_CHECK.md)
- 📋 **开发规划**: [development-plan.md](development-plan.md)
- 🐛 **问题反馈**: https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/issues

---

📝 **文档最后更新**: 2025年1月11日  
🔄 **API版本**: v1.0.0  
👨‍💻 **维护者**: Dajucoder  
📧 **联系方式**: 通过GitHub Issues反馈问题
