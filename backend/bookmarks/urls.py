from django.urls import path
from . import views

urlpatterns = [
    # 收藏夹相关
    path('collections/', views.CollectionListCreateView.as_view(), name='collection-list'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    
    # 书签相关
    path('', views.BookmarkListCreateView.as_view(), name='bookmark-list'),
    path('<int:pk>/', views.BookmarkDetailView.as_view(), name='bookmark-detail'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='bookmark-toggle-favorite'),
    path('<int:pk>/toggle-archive/', views.toggle_archive, name='bookmark-toggle-archive'),
    
    # 其他功能
    path('search/', views.search_bookmarks, name='bookmark-search'),
    path('stats/', views.BookmarkStatsView.as_view(), name='bookmark-stats'),
    path('bulk-operations/', views.bulk_operations, name='bookmark-bulk-operations'),
]
