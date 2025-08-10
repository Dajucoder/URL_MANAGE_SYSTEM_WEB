from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('activity/', views.activity_timeline, name='activity_timeline'),
]