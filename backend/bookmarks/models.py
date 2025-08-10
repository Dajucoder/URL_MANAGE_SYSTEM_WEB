from django.db import models
from django.conf import settings
from django.utils import timezone


class Collection(models.Model):
    """收藏夹模型"""
    name = models.CharField(max_length=100, verbose_name='收藏夹名称')
    description = models.TextField(blank=True, verbose_name='描述')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='颜色')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='用户'
    )
    is_default = models.BooleanField(default=False, verbose_name='默认收藏夹')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '收藏夹'
        verbose_name_plural = '收藏夹'
        db_table = 'collections'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    """书签模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    url = models.URLField(verbose_name='网址')
    description = models.TextField(blank=True, verbose_name='描述')
    notes = models.TextField(blank=True, verbose_name='笔记')
    thumbnail = models.URLField(blank=True, verbose_name='缩略图')
    
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='收藏夹'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name='用户'
    )
    
    is_favorite = models.BooleanField(default=False, verbose_name='收藏')
    is_archived = models.BooleanField(default=False, verbose_name='归档')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='访问次数')
    last_visited = models.DateTimeField(null=True, blank=True, verbose_name='最后访问时间')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '书签'
        verbose_name_plural = '书签'
        db_table = 'bookmarks'
        ordering = ['-created_at']
        unique_together = ['user', 'url']

    def __str__(self):
        return self.title

    def increment_visit_count(self):
        """增加访问次数"""
        self.visit_count += 1
        self.last_visited = timezone.now()
        self.save(update_fields=['visit_count', 'last_visited'])