from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class Category(models.Model):
    """分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='分类颜色')
    icon = models.CharField(max_length=50, blank=True, verbose_name='图标')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='父分类')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', verbose_name='用户')
    
    # 排序和统计
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    website_count = models.PositiveIntegerField(default=0, verbose_name='网站数量')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        db_table = 'categories'
        unique_together = ['name', 'user', 'parent']
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_full_path(self):
        """获取完整路径"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name

class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, verbose_name='标签名称')
    color = models.CharField(max_length=7, default='#6c757d', verbose_name='标签颜色')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags', verbose_name='用户')
    
    # 统计
    usage_count = models.PositiveIntegerField(default=0, verbose_name='使用次数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'tags'
        unique_together = ['name', 'user']
        ordering = ['-usage_count', 'name']
    
    def __str__(self):
        return self.name

class Website(models.Model):
    """网站模型"""
    title = models.CharField(max_length=200, verbose_name='网站标题')
    url = models.URLField(verbose_name='网站链接')
    description = models.TextField(blank=True, verbose_name='网站描述')
    favicon = models.URLField(blank=True, verbose_name='网站图标')
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True, verbose_name='网站截图')
    
    # 关联
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websites', verbose_name='用户')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='websites', verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, related_name='websites', verbose_name='标签')
    
    # 元数据
    meta_keywords = models.TextField(blank=True, verbose_name='关键词')
    meta_author = models.CharField(max_length=100, blank=True, verbose_name='作者')
    meta_language = models.CharField(max_length=10, blank=True, verbose_name='语言')
    
    # 状态和统计
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='访问次数')
    last_visited = models.DateTimeField(null=True, blank=True, verbose_name='最后访问时间')
    
    # 质量评分
    quality_score = models.FloatField(default=0.0, verbose_name='质量评分')
    loading_speed = models.FloatField(null=True, blank=True, verbose_name='加载速度')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '网站'
        verbose_name_plural = '网站'
        db_table = 'websites'
        unique_together = ['url', 'user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['quality_score']),
        ]
    
    def __str__(self):
        return self.title or self.url
    
    def increment_visit_count(self):
        """增加访问次数"""
        self.visit_count += 1
        self.last_visited = timezone.now()
        self.save(update_fields=['visit_count', 'last_visited'])

class WebsiteNote(models.Model):
    """网站笔记模型"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='notes', verbose_name='网站')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='website_notes', verbose_name='用户')
    
    title = models.CharField(max_length=200, verbose_name='笔记标题')
    content = models.TextField(verbose_name='笔记内容')
    is_private = models.BooleanField(default=True, verbose_name='是否私有')
    
    # 笔记类型
    NOTE_TYPES = [
        ('general', '一般笔记'),
        ('highlight', '重点标记'),
        ('todo', '待办事项'),
        ('review', '评价反馈'),
    ]
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default='general', verbose_name='笔记类型')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '网站笔记'
        verbose_name_plural = '网站笔记'
        db_table = 'website_notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.website.title} - {self.title}"