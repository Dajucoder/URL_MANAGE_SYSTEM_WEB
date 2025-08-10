from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
import logging

from .models import Collection, Bookmark
from .serializers import (
    CollectionSerializer, BookmarkSerializer, BookmarkListSerializer,
    BookmarkStatsSerializer
)

logger = logging.getLogger(__name__)


class CollectionListCreateView(generics.ListCreateAPIView):
    """收藏夹列表和创建视图"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """收藏夹详情视图"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """删除收藏夹时检查是否为默认收藏夹"""
        instance = self.get_object()
        if instance.is_default:
            return Response(
                {'error': '不能删除默认收藏夹'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class BookmarkListCreateView(generics.ListCreateAPIView):
    """书签列表和创建视图"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collection', 'is_favorite', 'is_archived']
    search_fields = ['title', 'description', 'url', 'notes']
    ordering_fields = ['created_at', 'visit_count', 'last_visited', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('collection')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookmarkListSerializer
        return BookmarkSerializer
    
    def perform_create(self, serializer):
        # 如果没有指定收藏夹，使用默认收藏夹
        if not serializer.validated_data.get('collection'):
            default_collection, created = Collection.objects.get_or_create(
                user=self.request.user,
                is_default=True,
                defaults={'name': '默认收藏夹', 'description': '系统默认收藏夹'}
            )
            serializer.validated_data['collection'] = default_collection
        
        serializer.save(user=self.request.user)


class BookmarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """书签详情视图"""
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('collection')
    
    def retrieve(self, request, *args, **kwargs):
        """获取书签详情时增加访问次数"""
        instance = self.get_object()
        instance.increment_visit_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BookmarkStatsView(APIView):
    """书签统计视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            bookmarks = Bookmark.objects.filter(user=user)
            
            # 最近7天的书签
            recent_date = timezone.now() - timedelta(days=7)
            
            stats = {
                'total_bookmarks': bookmarks.count(),
                'favorite_bookmarks': bookmarks.filter(is_favorite=True).count(),
                'archived_bookmarks': bookmarks.filter(is_archived=True).count(),
                'total_visits': bookmarks.aggregate(Sum('visit_count'))['visit_count__sum'] or 0,
                'collections_count': Collection.objects.filter(user=user).count(),
                'recent_bookmarks': bookmarks.filter(created_at__gte=recent_date).count(),
            }
            
            serializer = BookmarkStatsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"获取书签统计失败: {str(e)}")
            return Response(
                {'error': '获取统计数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request, pk):
    """切换书签收藏状态"""
    try:
        bookmark = Bookmark.objects.get(id=pk, user=request.user)
        bookmark.is_favorite = not bookmark.is_favorite
        bookmark.save(update_fields=['is_favorite'])
        
        return Response({
            'message': '收藏状态已更新',
            'is_favorite': bookmark.is_favorite
        })
        
    except Bookmark.DoesNotExist:
        return Response(
            {'error': '书签不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"切换收藏状态失败: {str(e)}")
        return Response(
            {'error': '操作失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_archive(request, pk):
    """切换书签归档状态"""
    try:
        bookmark = Bookmark.objects.get(id=pk, user=request.user)
        bookmark.is_archived = not bookmark.is_archived
        bookmark.save(update_fields=['is_archived'])
        
        return Response({
            'message': '归档状态已更新',
            'is_archived': bookmark.is_archived
        })
        
    except Bookmark.DoesNotExist:
        return Response(
            {'error': '书签不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"切换归档状态失败: {str(e)}")
        return Response(
            {'error': '操作失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_bookmarks(request):
    """搜索书签"""
    try:
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'results': []})
        
        bookmarks = Bookmark.objects.filter(
            user=request.user,
            is_archived=False
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(url__icontains=query) |
            Q(notes__icontains=query)
        ).select_related('collection')[:20]
        
        serializer = BookmarkListSerializer(bookmarks, many=True)
        return Response({'results': serializer.data})
        
    except Exception as e:
        logger.error(f"搜索书签失败: {str(e)}")
        return Response(
            {'error': '搜索失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_operations(request):
    """批量操作书签"""
    try:
        action = request.data.get('action')
        bookmark_ids = request.data.get('bookmark_ids', [])
        
        if not action or not bookmark_ids:
            return Response(
                {'error': '请提供操作类型和书签ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bookmarks = Bookmark.objects.filter(
            id__in=bookmark_ids,
            user=request.user
        )
        
        if action == 'delete':
            count = bookmarks.count()
            bookmarks.delete()
            return Response({'message': f'已删除 {count} 个书签'})
        
        elif action == 'archive':
            count = bookmarks.update(is_archived=True)
            return Response({'message': f'已归档 {count} 个书签'})
        
        elif action == 'unarchive':
            count = bookmarks.update(is_archived=False)
            return Response({'message': f'已取消归档 {count} 个书签'})
        
        elif action == 'favorite':
            count = bookmarks.update(is_favorite=True)
            return Response({'message': f'已收藏 {count} 个书签'})
        
        elif action == 'unfavorite':
            count = bookmarks.update(is_favorite=False)
            return Response({'message': f'已取消收藏 {count} 个书签'})
        
        elif action == 'move':
            collection_id = request.data.get('collection_id')
            if not collection_id:
                return Response(
                    {'error': '请提供目标收藏夹ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            collection = Collection.objects.get(id=collection_id, user=request.user)
            count = bookmarks.update(collection=collection)
            return Response({'message': f'已移动 {count} 个书签到 {collection.name}'})
        
        else:
            return Response(
                {'error': '不支持的操作类型'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Collection.DoesNotExist:
        return Response(
            {'error': '收藏夹不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"批量操作失败: {str(e)}")
        return Response(
            {'error': '操作失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )