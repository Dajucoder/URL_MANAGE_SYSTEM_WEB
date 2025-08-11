# API 接口文档

## 概述

URL管理系统提供完整的RESTful API接口，支持用户认证、网站管理、书签管理等功能。

## 基础信息

- **Base URL**: `http://localhost:8000/api/`
- **认证方式**: JWT Token
- **数据格式**: JSON
- **字符编码**: UTF-8

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

## 更新日志

### v1.0.0
- 完整的RESTful API
- JWT认证机制
- 用户、网站、书签管理
- 数据统计接口

### 计划中的功能
- GraphQL支持
- WebSocket实时通知
- 批量操作优化
- API版本控制