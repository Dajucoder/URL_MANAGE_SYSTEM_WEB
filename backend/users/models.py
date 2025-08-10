from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """自定义用户模型"""
    email = models.EmailField(unique=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    website = models.URLField(blank=True, verbose_name='个人网站')
    location = models.CharField(max_length=100, blank=True, verbose_name='位置')
    birth_date = models.DateField(blank=True, null=True, verbose_name='生日')
    
    # 用户偏好设置
    theme = models.CharField(
        max_length=10,
        choices=[('light', '浅色'), ('dark', '深色')],
        default='light',
        verbose_name='主题'
    )
    language = models.CharField(
        max_length=10,
        choices=[('zh-cn', '中文'), ('en', 'English')],
        default='zh-cn',
        verbose_name='语言'
    )
    
    # 统计字段
    total_bookmarks = models.PositiveIntegerField(default=0, verbose_name='收藏总数')
    total_visits = models.PositiveIntegerField(default=0, verbose_name='访问总数')
    last_active = models.DateTimeField(default=timezone.now, verbose_name='最后活跃时间')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users'
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 隐私设置
    is_public = models.BooleanField(default=True, verbose_name='公开资料')
    show_email = models.BooleanField(default=False, verbose_name='显示邮箱')
    show_stats = models.BooleanField(default=True, verbose_name='显示统计')
    
    # 通知设置
    email_notifications = models.BooleanField(default=True, verbose_name='邮件通知')
    bookmark_notifications = models.BooleanField(default=True, verbose_name='收藏通知')
    
    # 推荐算法偏好
    enable_recommendations = models.BooleanField(default=True, verbose_name='启用推荐')
    recommendation_weight = models.JSONField(default=dict, verbose_name='推荐权重')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username}的资料"