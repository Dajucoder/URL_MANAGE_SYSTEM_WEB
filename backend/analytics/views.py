from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from users.models import User
from websites.models import Website, Category, Tag
from bookmarks.models import Bookmark, Collection

logger = logging.getLogger(__name__)


class DashboardStatsView(APIView):
    """仪表板统计视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # 基础统计
            stats = {
                'websites_count': Website.objects.filter(user=user).count(),
                'bookmarks_count': Bookmark.objects.filter(user=user).count(),
                'categories_count': Category.objects.filter(user=user).count(),
                'tags_count': Tag.objects.filter(user=user).count(),
                'collections_count': Collection.objects.filter(user=user).count(),
            }
            
            # 访问统计
            websites = Website.objects.filter(user=user)
            bookmarks = Bookmark.objects.filter(user=user)
            
            stats.update({
                'total_website_visits': websites.aggregate(Sum('visit_count'))['visit_count__sum'] or 0,
                'total_bookmark_visits': bookmarks.aggregate(Sum('visit_count'))['visit_count__sum'] or 0,
                'avg_website_quality': websites.aggregate(Avg('quality_score'))['quality_score__avg'] or 0.0,
            })
            
            # 最近活动统计
            recent_date = timezone.now() - timedelta(days=7)
            stats.update({
                'recent_websites': websites.filter(created_at__gte=recent_date).count(),
                'recent_bookmarks': bookmarks.filter(created_at__gte=recent_date).count(),
            })
            
            return Response(stats)
            
        except Exception as e:
            logger.error(f"获取仪表板统计失败: {str(e)}")
            return Response(
                {'error': '获取统计数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TrendAnalysisView(APIView):
    """趋势分析视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            days = int(request.GET.get('days', 30))
            
            # 计算日期范围
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)
            
            # 网站创建趋势
            website_trend = []
            bookmark_trend = []
            
            current_date = start_date
            while current_date <= end_date:
                next_date = current_date + timedelta(days=1)
                
                website_count = Website.objects.filter(
                    user=user,
                    created_at__date=current_date
                ).count()
                
                bookmark_count = Bookmark.objects.filter(
                    user=user,
                    created_at__date=current_date
                ).count()
                
                website_trend.append({
                    'date': current_date.isoformat(),
                    'count': website_count
                })
                
                bookmark_trend.append({
                    'date': current_date.isoformat(),
                    'count': bookmark_count
                })
                
                current_date = next_date
            
            return Response({
                'website_trend': website_trend,
                'bookmark_trend': bookmark_trend,
            })
            
        except Exception as e:
            logger.error(f"获取趋势分析失败: {str(e)}")
            return Response(
                {'error': '获取趋势分析失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryAnalysisView(APIView):
    """分类分析视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # 分类统计
            categories = Category.objects.filter(user=user).annotate(
                websites_count=Count('websites')
            ).order_by('-websites_count')[:10]
            
            category_stats = []
            for category in categories:
                category_stats.append({
                    'name': category.name,
                    'count': category.websites_count,
                    'color': category.color,
                })
            
            # 标签统计
            tags = Tag.objects.filter(user=user).annotate(
                websites_count=Count('websites')
            ).order_by('-websites_count')[:20]
            
            tag_stats = []
            for tag in tags:
                tag_stats.append({
                    'name': tag.name,
                    'count': tag.websites_count,
                    'color': tag.color,
                })
            
            return Response({
                'categories': category_stats,
                'tags': tag_stats,
            })
            
        except Exception as e:
            logger.error(f"获取分类分析失败: {str(e)}")
            return Response(
                {'error': '获取分类分析失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PopularContentView(APIView):
    """热门内容视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # 最受欢迎的网站
            popular_websites = Website.objects.filter(
                user=user,
                is_active=True
            ).order_by('-visit_count')[:10]
            
            website_stats = []
            for website in popular_websites:
                website_stats.append({
                    'id': website.id,
                    'title': website.title,
                    'url': website.url,
                    'visit_count': website.visit_count,
                    'quality_score': website.quality_score,
                    'last_visited': website.last_visited,
                })
            
            # 最受欢迎的书签
            popular_bookmarks = Bookmark.objects.filter(
                user=user,
                is_archived=False
            ).order_by('-visit_count')[:10]
            
            bookmark_stats = []
            for bookmark in popular_bookmarks:
                bookmark_stats.append({
                    'id': bookmark.id,
                    'title': bookmark.title,
                    'url': bookmark.url,
                    'visit_count': bookmark.visit_count,
                    'is_favorite': bookmark.is_favorite,
                    'last_visited': bookmark.last_visited,
                })
            
            return Response({
                'popular_websites': website_stats,
                'popular_bookmarks': bookmark_stats,
            })
            
        except Exception as e:
            logger.error(f"获取热门内容失败: {str(e)}")
            return Response(
                {'error': '获取热门内容失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_data(request):
    """导出数据"""
    try:
        user = request.user
        export_type = request.GET.get('type', 'all')
        
        data = {}
        
        if export_type in ['all', 'websites']:
            websites = Website.objects.filter(user=user).select_related('category').prefetch_related('tags')
            data['websites'] = []
            for website in websites:
                data['websites'].append({
                    'title': website.title,
                    'url': website.url,
                    'description': website.description,
                    'category': website.category.name if website.category else '',
                    'tags': [tag.name for tag in website.tags.all()],
                    'visit_count': website.visit_count,
                    'created_at': website.created_at.isoformat(),
                })
        
        if export_type in ['all', 'bookmarks']:
            bookmarks = Bookmark.objects.filter(user=user).select_related('collection')
            data['bookmarks'] = []
            for bookmark in bookmarks:
                data['bookmarks'].append({
                    'title': bookmark.title,
                    'url': bookmark.url,
                    'description': bookmark.description,
                    'notes': bookmark.notes,
                    'collection': bookmark.collection.name,
                    'is_favorite': bookmark.is_favorite,
                    'visit_count': bookmark.visit_count,
                    'created_at': bookmark.created_at.isoformat(),
                })
        
        return Response(data)
        
    except Exception as e:
        logger.error(f"导出数据失败: {str(e)}")
        return Response(
            {'error': '导出数据失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )