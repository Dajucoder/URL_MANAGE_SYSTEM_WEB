from django.urls import path
from . import views

urlpatterns = [
    # 暂时注释掉，等视图实现后再启用
    # path('dashboard/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
]
