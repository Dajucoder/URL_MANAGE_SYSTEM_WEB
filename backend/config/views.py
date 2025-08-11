"""
系统级视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from django.conf import settings
import django
import sys
from datetime import datetime


@extend_schema(
    tags=['系统信息'],
    summary='健康检查',
    description='检查API服务是否正常运行，返回系统基本信息',
    responses={
        200: OpenApiResponse(
            description='服务正常',
            examples=[
                OpenApiExample(
                    'Success',
                    summary='健康检查成功',
                    value={
                        'status': 'healthy',
                        'message': 'API服务运行正常',
                        'timestamp': '2024-01-01T12:00:00Z',
                        'version': '1.0.0',
                        'django_version': '4.2.7',
                        'python_version': '3.9.0',
                        'debug_mode': False
                    }
                )
            ]
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    健康检查接口
    
    用于检查API服务是否正常运行
    """
    try:
        return Response({
            'status': 'healthy',
            'message': 'API服务运行正常',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'django_version': django.get_version(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'debug_mode': settings.DEBUG
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'message': f'服务异常: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['系统信息'],
    summary='API信息',
    description='获取API的基本信息和可用端点概览',
    responses={
        200: OpenApiResponse(
            description='API信息',
            examples=[
                OpenApiExample(
                    'Success',
                    summary='API信息示例',
                    value={
                        'name': 'URL管理系统 API',
                        'version': '1.0.0',
                        'description': '功能完整的网站收藏和书签管理系统API',
                        'endpoints': {
                            'authentication': '/api/users/',
                            'websites': '/api/websites/',
                            'bookmarks': '/api/bookmarks/',
                            'analytics': '/api/analytics/',
                            'documentation': '/api/docs/',
                            'schema': '/api/schema/'
                        },
                        'features': [
                            'JWT认证',
                            '网站管理',
                            '书签收藏',
                            '数据统计',
                            '搜索功能',
                            '分类标签'
                        ]
                    }
                )
            ]
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    API信息接口
    
    返回API的基本信息和功能概览
    """
    return Response({
        'name': 'URL管理系统 API',
        'version': '1.0.0',
        'description': '功能完整的网站收藏和书签管理系统API',
        'endpoints': {
            'authentication': '/api/users/',
            'websites': '/api/websites/',
            'bookmarks': '/api/bookmarks/',
            'analytics': '/api/analytics/',
            'documentation': '/api/docs/',
            'schema': '/api/schema/'
        },
        'features': [
            'JWT认证',
            '网站管理',
            '书签收藏',
            '数据统计',
            '搜索功能',
            '分类标签'
        ],
        'documentation': {
            'swagger_ui': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'openapi_schema': request.build_absolute_uri('/api/schema/')
        }
    })