"""
Django settings for URL管理系统项目.
"""

import os
import configparser
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# 构建路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(BASE_DIR.parent, 'config.ini')

# 如果配置文件不存在，使用示例配置
if not os.path.exists(config_path):
    config_path = os.path.join(BASE_DIR.parent, 'config.ini.example')

config.read(config_path)

# 从环境变量获取敏感信息
def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = f"必须设置环境变量 {var_name}"
        raise ImproperlyConfigured(error_msg)

# 安全设置
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY', 
                             config.get('secret', 'SECRET_KEY', fallback='django-insecure-default-key-change-this'))
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']

# 应用定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方应用
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    
    # 自定义应用
    'users',
    'websites',
    'bookmarks',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE', config.get('database', 'ENGINE', fallback='django.db.backends.sqlite3')),
        'NAME': get_env_variable('DB_NAME', config.get('database', 'NAME', fallback=os.path.join(BASE_DIR, 'db.sqlite3'))),
        'USER': get_env_variable('DB_USER', config.get('database', 'USER', fallback='')),
        'PASSWORD': get_env_variable('DB_PASSWORD', config.get('database', 'PASSWORD', fallback='')),
        'HOST': get_env_variable('DB_HOST', config.get('database', 'HOST', fallback='')),
        'PORT': get_env_variable('DB_PORT', config.get('database', 'PORT', fallback='')),
    }
}

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静态文件设置
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# REST Framework 设置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# drf-spectacular 设置
SPECTACULAR_SETTINGS = {
    'TITLE': 'URL管理系统 API',
    'DESCRIPTION': '''
    ## 🌐 URL管理系统 API 文档
    
    一个功能完整的网站收藏和书签管理系统的RESTful API接口文档。
    
    ### 🚀 主要功能
    - **用户认证**: JWT令牌认证，支持注册、登录、登出
    - **网站管理**: 网站信息的增删改查，支持分类、标签、搜索
    - **书签管理**: 个人书签收藏，支持收藏夹分组和批量操作
    - **数据统计**: 用户数据统计分析，提供仪表盘和活动时间线
    
    ### 🔐 认证说明
    大部分API需要JWT令牌认证，请先调用登录接口获取令牌，然后点击右上角的 **Authorize** 按钮输入令牌。
    
    令牌格式：`Bearer your-jwt-token-here`
    
    ### 📝 使用说明
    1. 首先调用 `/api/users/login/` 接口登录获取JWT令牌
    2. 点击页面右上角的 **Authorize** 按钮
    3. 在弹出框中输入 `Bearer ` + 你的令牌
    4. 现在可以测试需要认证的API接口了
    
    ### 🌟 技术栈
    - **后端**: Django 4.2 + Django REST Framework 3.14
    - **认证**: JWT (djangorestframework-simplejwt)
    - **数据库**: PostgreSQL / SQLite
    - **文档**: drf-spectacular (OpenAPI 3.0)
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'ENUM_NAME_OVERRIDES': {
        'ValidationErrorEnum': 'drf_spectacular.plumbing.ValidationErrorEnum.choices',
    },
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums'
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        'defaultModelRendering': 'example',
        'displayRequestDuration': True,
        'docExpansion': 'none',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
        'tryItOutEnabled': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
        'validatorUrl': None,
    },
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
        'expandResponses': '200,201',
        'pathInMiddlePanel': True,
        'theme': {
            'colors': {
                'primary': {
                    'main': '#1890ff'
                }
            },
            'typography': {
                'fontSize': '14px',
                'lineHeight': '1.5em',
                'code': {
                    'fontSize': '13px',
                    'fontFamily': 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace'
                },
                'headings': {
                    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                    'fontWeight': '600'
                }
            }
        }
    },
    'AUTHENTICATION_WHITELIST': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'TAGS': [
        {'name': '用户认证', 'description': '用户注册、登录、登出等认证相关接口'},
        {'name': '用户管理', 'description': '用户信息管理、个人资料设置等接口'},
        {'name': '网站管理', 'description': '网站信息的增删改查、搜索等接口'},
        {'name': '分类管理', 'description': '网站分类的管理接口'},
        {'name': '标签管理', 'description': '标签的管理接口'},
        {'name': '书签管理', 'description': '书签收藏、收藏夹管理等接口'},
        {'name': '数据统计', 'description': '仪表盘数据、统计分析等接口'},
    ],
}

# JWT设置
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# CORS设置
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST', config.get('email', 'EMAIL_HOST', fallback=''))
EMAIL_PORT = int(get_env_variable('EMAIL_PORT', config.get('email', 'EMAIL_PORT', fallback='587')))
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', config.get('email', 'EMAIL_USE_TLS', fallback='True')).lower() == 'true'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', config.get('email', 'EMAIL_HOST_USER', fallback=''))
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', config.get('email', 'EMAIL_HOST_PASSWORD', fallback=''))
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}