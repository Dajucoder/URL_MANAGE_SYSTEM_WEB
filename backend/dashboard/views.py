from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import logging

from users.models import User
from websites.models import Website, Category, Tag
from bookmarks.models import Bookmark

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """获取仪表板统计数据"""
    try:
        user = request.user
        
        # 基础统计
        stats = {
            'websites_count': Website.objects.filter(user=user).count(),
            'bookmarks_count': Bookmark.objects.filter(user=user).count(),
            'categories_count': Category.objects.filter(user=user).count(),
            'tags_count': Tag.objects.filter(user=user).count(),
            'total_visits': user.total_visits,
        }
        
        # 最近7天的统计
        seven_days_ago = timezone.now() - timedelta(days=7)
        stats.update({
            'recent_websites': Website.objects.filter(
                user=user, 
                created_at__gte=seven_days_ago
            ).count(),
            'recent_bookmarks': Bookmark.objects.filter(
                user=user, 
                created_at__gte=seven_days_ago
            ).count(),
        })
        
        # 分类统计
        category_stats = Category.objects.filter(user=user).annotate(
            sites_count=Count('websites')
        ).values('name', 'sites_count', 'color')[:5]
        
        # 标签统计
        tag_stats = Tag.objects.filter(user=user).annotate(
            sites_count=Count('websites')
        ).values('name', 'sites_count', 'color')[:5]
        
        # 最近访问的网站
        recent_websites = Website.objects.filter(user=user).order_by('-last_visited')[:5].values(
            'id', 'title', 'url', 'favicon', 'last_visited', 'visit_count'
        )
        
        # 最近添加的书签
        recent_bookmarks = Bookmark.objects.filter(user=user).order_by('-created_at')[:5].values(
            'id', 'title', 'url', 'description', 'created_at'
        )
        
        stats.update({
            'category_stats': list(category_stats),
            'tag_stats': list(tag_stats),
            'recent_websites': list(recent_websites),
            'recent_bookmarks': list(recent_bookmarks),
        })
        
        return Response(stats)
        
    except Exception as e:
        logger.error(f"获取仪表板统计失败: {str(e)}")
        return Response(
            {'error': '获取统计数据失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_timeline(request):
    """获取用户活动时间线"""
    try:
        user = request.user
        days = int(request.GET.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # 网站添加活动
        website_activities = Website.objects.filter(
            user=user,
            created_at__gte=start_date
        ).values('created_at', 'title').order_by('-created_at')
        
        # 书签添加活动
        bookmark_activities = Bookmark.objects.filter(
            user=user,
            created_at__gte=start_date
        ).values('created_at', 'title').order_by('-created_at')
        
        # 合并活动并排序
        activities = []
        
        for website in website_activities:
            activities.append({
                'type': 'website',
                'title': website['title'],
                'timestamp': website['created_at'],
                'action': '添加了网站'
            })
        
        for bookmark in bookmark_activities:
            activities.append({
                'type': 'bookmark',
                'title': bookmark['title'],
                'timestamp': bookmark['created_at'],
                'action': '添加了书签'
            })
        
        # 按时间排序
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return Response({
            'activities': activities[:20]  # 返回最近20条活动
        })
        
    except Exception as e:
        logger.error(f"获取活动时间线失败: {str(e)}")
        return Response(
            {'error': '获取活动数据失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )