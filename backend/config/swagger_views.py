"""
自定义 Swagger UI 视图
"""
from django.shortcuts import render
from django.http import JsonResponse
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.plumbing import build_object_type
from drf_spectacular.openapi import AutoSchema
import json


class CustomSwaggerView(SpectacularSwaggerView):
    """
    自定义 Swagger UI 视图，修复布局问题
    """
    template_name = 'swagger-ui-fixed.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 修复 Swagger UI 配置
        context.update({
            'title': 'URL管理系统 API',
            'swagger_settings': {
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
            }
        })
        
        return context


def swagger_ui_fixed(request):
    """
    修复版本的 Swagger UI 页面
    """
    return render(request, 'swagger-ui-fixed.html', {
        'title': 'URL管理系统 API - 修复版',
        'schema_url': '/api/schema/',
        'swagger_css_url': '/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui.css',
        'swagger_js_url': '/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.js',
        'swagger_preset_js_url': '/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.js',
        'swagger_favicon_url': '/static/drf_spectacular_sidecar/swagger-ui-dist/favicon-32x32.png',
    })