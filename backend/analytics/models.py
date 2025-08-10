from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()

class UserActivity(models.Model):
    """用户活动记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', verbose_name='用户')
    
    ACTIVITY_TYPES = [
        ('login', '登录'),
        ('logout', '登出'),
        ('bookmark_add', '添加书签'),
        ('bookmark_delete', '删除书签'),
        ('bookmark_visit', '访问书签'),
        ('category_create', '创建分类'),
        ('category_update', '更新分类'),
        ('search', '搜索'),
        ('export', '导出数据'),
        ('import', '导入数据'),
    ]
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name='活动类型')
    
    # 活动详情
    description = models.TextField(blank=True, verbose_name='活动描述')
    metadata = models.JSONField(default=dict, verbose_name='元数据')
    
    # 请求信息
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, verbose_name='用户代理')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '用户活动'
        verbose_name_plural = '用户活动'
        db_table = 'user_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"

class WebsiteStatistics(models.Model):
    """网站统计"""
    website = models.OneToOneField('websites.Website', on_delete=models.CASCADE, 
                                  related_name='statistics', verbose_name='网站')
    
    # 访问统计
    total_visits = models.PositiveIntegerField(default=0, verbose_name='总访问次数')
    unique_visitors = models.PositiveIntegerField(default=0, verbose_name='独立访客数')
    avg_visit_duration = models.FloatField(default=0.0, verbose_name='平均访问时长')
    
    # 时间统计
    daily_visits = models.JSONField(default=dict, verbose_name='每日访问')
    weekly_visits = models.JSONField(default=dict, verbose_name='每周访问')
    monthly_visits = models.JSONField(default=dict, verbose_name='每月访问')
    
    # 用户行为
    bookmark_count = models.PositiveIntegerField(default=0, verbose_name='收藏次数')
    share_count = models.PositiveIntegerField(default=0, verbose_name='分享次数')
    rating_avg = models.FloatField(default=0.0, verbose_name='平均评分')
    rating_count = models.PositiveIntegerField(default=0, verbose_name='评分次数')
    
    # 推荐相关
    recommendation_score = models.FloatField(default=0.0, verbose_name='推荐分数')
    similarity_scores = models.JSONField(default=dict, verbose_name='相似度分数')
    
    last_updated = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    
    class Meta:
        verbose_name = '网站统计'
        verbose_name_plural = '网站统计'
        db_table = 'website_statistics'
    
    def __str__(self):
        return f"{self.website.title} - 统计"
    
    def update_daily_visits(self, date=None):
        """更新每日访问统计"""
        if date is None:
            date = timezone.now().date()
        
        date_str = date.strftime('%Y-%m-%d')
        if date_str in self.daily_visits:
            self.daily_visits[date_str] += 1
        else:
            self.daily_visits[date_str] = 1
        
        self.save(update_fields=['daily_visits'])

class UserStatistics(models.Model):
    """用户统计"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics', verbose_name='用户')
    
    # 基础统计
    total_bookmarks = models.PositiveIntegerField(default=0, verbose_name='总书签数')
    total_categories = models.PositiveIntegerField(default=0, verbose_name='总分类数')
    total_tags = models.PositiveIntegerField(default=0, verbose_name='总标签数')
    total_visits = models.PositiveIntegerField(default=0, verbose_name='总访问次数')
    
    # 活跃度统计
    login_count = models.PositiveIntegerField(default=0, verbose_name='登录次数')
    active_days = models.PositiveIntegerField(default=0, verbose_name='活跃天数')
    avg_daily_visits = models.FloatField(default=0.0, verbose_name='日均访问')
    
    # 时间分布
    activity_by_hour = models.JSONField(default=dict, verbose_name='按小时活动分布')
    activity_by_day = models.JSONField(default=dict, verbose_name='按天活动分布')
    activity_by_month = models.JSONField(default=dict, verbose_name='按月活动分布')
    
    # 偏好分析
    favorite_categories = models.JSONField(default=list, verbose_name='偏好分类')
    favorite_tags = models.JSONField(default=list, verbose_name='偏好标签')
    browsing_patterns = models.JSONField(default=dict, verbose_name='浏览模式')
    
    last_updated = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    
    class Meta:
        verbose_name = '用户统计'
        verbose_name_plural = '用户统计'
        db_table = 'user_statistics'
    
    def __str__(self):
        return f"{self.user.username} - 统计"

class SearchLog(models.Model):
    """搜索日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='search_logs', verbose_name='用户')
    
    query = models.CharField(max_length=200, verbose_name='搜索词')
    results_count = models.PositiveIntegerField(default=0, verbose_name='结果数量')
    
    # 搜索类型
    SEARCH_TYPES = [
        ('general', '全文搜索'),
        ('title', '标题搜索'),
        ('tag', '标签搜索'),
        ('category', '分类搜索'),
        ('url', 'URL搜索'),
    ]
    search_type = models.CharField(max_length=20, choices=SEARCH_TYPES, default='general', verbose_name='搜索类型')
    
    # 搜索结果
    clicked_results = models.JSONField(default=list, verbose_name='点击结果')
    search_duration = models.FloatField(default=0.0, verbose_name='搜索耗时')
    
    # 请求信息
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    user_agent = models.TextField(blank=True, verbose_name='用户代理')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '搜索日志'
        verbose_name_plural = '搜索日志'
        db_table = 'search_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['query']),
        ]
    
    def __str__(self):
        return f"搜索: {self.query}"

class RecommendationLog(models.Model):
    """推荐日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_logs', verbose_name='用户')
    recommended_website = models.ForeignKey('websites.Website', on_delete=models.CASCADE,
                                          related_name='recommendation_logs', verbose_name='推荐网站')
    
    # 推荐算法
    ALGORITHM_TYPES = [
        ('collaborative', '协同过滤'),
        ('content_based', '基于内容'),
        ('hybrid', '混合推荐'),
        ('popularity', '热门推荐'),
    ]
    algorithm_type = models.CharField(max_length=20, choices=ALGORITHM_TYPES, verbose_name='算法类型')
    
    # 推荐分数和原因
    recommendation_score = models.FloatField(verbose_name='推荐分数')
    recommendation_reason = models.TextField(blank=True, verbose_name='推荐原因')
    
    # 用户反馈
    is_clicked = models.BooleanField(default=False, verbose_name='是否点击')
    is_bookmarked = models.BooleanField(default=False, verbose_name='是否收藏')
    user_rating = models.IntegerField(null=True, blank=True, verbose_name='用户评分')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    clicked_at = models.DateTimeField(null=True, blank=True, verbose_name='点击时间')
    
    class Meta:
        verbose_name = '推荐日志'
        verbose_name_plural = '推荐日志'
        db_table = 'recommendation_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['algorithm_type']),
        ]
    
    def __str__(self):
        return f"推荐给 {self.user.username}: {self.recommended_website.title}"