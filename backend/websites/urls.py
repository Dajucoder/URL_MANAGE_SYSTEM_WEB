from django.urls import path
from . import views

urlpatterns = [
    # 网站管理
    path('', views.WebsiteListCreateView.as_view(), name='website-list'),
    path('<int:pk>/', views.WebsiteDetailView.as_view(), name='website-detail'),
    
    # 分类管理
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # 标签管理
    path('tags/', views.TagListCreateView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
]