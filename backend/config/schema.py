"""
API文档配置和自定义Schema
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme


class JWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'rest_framework_simplejwt.authentication.JWTAuthentication'
    name = 'jwtAuth'

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme()


# API响应示例
API_EXAMPLES = {
    'user_login_success': {
        'summary': '登录成功',
        'value': {
            'user': {
                'id': 1,
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': '管理员',
                'last_name': '',
                'is_active': True,
                'date_joined': '2024-01-01T00:00:00Z'
            },
            'tokens': {
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        }
    },
    'user_login_error': {
        'summary': '登录失败',
        'value': {
            'detail': '用户名或密码错误'
        }
    },
    'website_list_success': {
        'summary': '网站列表',
        'value': {
            'count': 25,
            'next': 'http://localhost:8000/api/websites/?page=2',
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'title': 'GitHub',
                    'url': 'https://github.com',
                    'description': '全球最大的代码托管平台',
                    'category': {
                        'id': 1,
                        'name': '开发工具'
                    },
                    'tags': [
                        {'id': 1, 'name': 'Git'},
                        {'id': 2, 'name': '代码托管'}
                    ],
                    'quality_score': 5,
                    'visit_count': 100,
                    'is_active': True,
                    'created_at': '2024-01-01T00:00:00Z'
                }
            ]
        }
    },
    'validation_error': {
        'summary': '验证错误',
        'value': {
            'field_name': ['此字段是必需的。'],
            'email': ['请输入有效的电子邮件地址。']
        }
    },
    'permission_denied': {
        'summary': '权限不足',
        'value': {
            'detail': '您没有执行该操作的权限。'
        }
    },
    'not_found': {
        'summary': '资源未找到',
        'value': {
            'detail': '未找到。'
        }
    }
}

# 常用的OpenAPI标签
API_TAGS = [
    {
        'name': '用户认证',
        'description': '用户注册、登录、登出等认证相关接口'
    },
    {
        'name': '用户管理',
        'description': '用户信息管理、个人资料设置等接口'
    },
    {
        'name': '网站管理',
        'description': '网站信息的增删改查、搜索等接口'
    },
    {
        'name': '分类管理',
        'description': '网站分类的管理接口'
    },
    {
        'name': '标签管理',
        'description': '标签的管理接口'
    },
    {
        'name': '书签管理',
        'description': '书签收藏、收藏夹管理等接口'
    },
    {
        'name': '数据统计',
        'description': '仪表盘数据、统计分析等接口'
    }
]