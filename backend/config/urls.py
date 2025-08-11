from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import health_check, api_info

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 系统接口
    path('api/health/', health_check, name='health-check'),
    path('api/info/', api_info, name='api-info'),
    
    # API路由
    path('api/users/', include('users.urls')),
    path('api/websites/', include('websites.urls')),
    path('api/bookmarks/', include('bookmarks.urls')),
    path('api/analytics/', include('dashboard.urls')),
    
    # API文档路由
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
