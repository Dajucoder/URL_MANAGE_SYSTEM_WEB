from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户信息
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('info/', views.user_info_view, name='user_info'),
    path('stats/', views.UserStatsView.as_view(), name='user_stats'),
    
    # 密码管理
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]