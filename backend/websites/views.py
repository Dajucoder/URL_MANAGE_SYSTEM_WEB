from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
import logging
import requests
from urllib.parse import urljoin, urlparse
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

from .models import Category, Tag, Website, WebsiteNote
from .serializers import (
    CategorySerializer, TagSerializer, WebsiteSerializer,
    WebsiteListSerializer, WebsiteNoteSerializer, WebsiteStatsSerializer
)

logger = logging.getLogger(__name__)


class CategoryListCreateView(generics.ListCreateAPIView):
    """分类列表和创建视图"""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent']
    search_fields = ['name', 'description']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['sort_order', 'name']
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """分类详情视图"""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TagListCreateView(generics.ListCreateAPIView):
    """标签列表和创建视图"""
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['usage_count', 'name', 'created_at']
    ordering = ['-usage_count', 'name']
    
    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """标签详情视图"""
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class WebsiteListCreateView(generics.ListCreateAPIView):
    """网站列表和创建视图"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'is_public']
    search_fields = ['title', 'description', 'url', 'meta_keywords']
    ordering_fields = ['created_at', 'visit_count', 'quality_score', 'last_visited']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).select_related('category').prefetch_related('tags')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WebsiteListSerializer
        return WebsiteSerializer
    
    def perform_create(self, serializer):
        website = serializer.save(user=self.request.user)
        # 异步获取网站元数据
        self.fetch_website_metadata.delay(website.id)


class WebsiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """网站详情视图"""
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).select_related('category').prefetch_related('tags', 'notes')
    
    def retrieve(self, request, *args, **kwargs):
        """获取网站详情时增加访问次数"""
        instance = self.get_object()
        instance.increment_visit_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class WebsiteNoteListCreateView(generics.ListCreateAPIView):
    """网站笔记列表和创建视图"""
    serializer_class = WebsiteNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        website_id = self.kwargs.get('website_id')
        return WebsiteNote.objects.filter(
            website_id=website_id,
            user=self.request.user
        )
    
    def perform_create(self, serializer):
        website_id = self.kwargs.get('website_id')
        website = Website.objects.get(id=website_id, user=self.request.user)
        serializer.save(user=self.request.user, website=website)


class WebsiteNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """网站笔记详情视图"""
    serializer_class = WebsiteNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WebsiteNote.objects.filter(user=self.request.user)


class WebsiteStatsView(APIView):
    """网站统计视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            websites = Website.objects.filter(user=user)
            
            stats = {
                'total_websites': websites.count(),
                'active_websites': websites.filter(is_active=True).count(),
                'public_websites': websites.filter(is_public=True).count(),
                'total_visits': websites.aggregate(Sum('visit_count'))['visit_count__sum'] or 0,
                'categories_count': Category.objects.filter(user=user).count(),
                'tags_count': Tag.objects.filter(user=user).count(),
                'avg_quality_score': websites.aggregate(Avg('quality_score'))['quality_score__avg'] or 0.0,
            }
            
            serializer = WebsiteStatsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"获取网站统计失败: {str(e)}")
            return Response(
                {'error': '获取统计数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def fetch_website_info(request):
    """获取网站信息"""
    try:
        url = request.data.get('url')
        if not url:
            return Response(
                {'error': '请提供网站URL'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取网站信息
        info = get_website_info(url)
        return Response(info)
        
    except Exception as e:
        logger.error(f"获取网站信息失败: {str(e)}")
        return Response(
            {'error': '获取网站信息失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_website_info(url):
    """获取网站基本信息"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 获取标题
        title = ''
        if soup.title:
            title = soup.title.string.strip()
        
        # 获取描述
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()
        
        # 获取关键词
        keywords = ''
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '').strip()
        
        # 获取favicon
        favicon = ''
        favicon_link = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon_link:
            favicon = urljoin(url, favicon_link.get('href', ''))
        else:
            # 尝试默认favicon路径
            parsed_url = urlparse(url)
            favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        
        return {
            'title': title,
            'description': description,
            'meta_keywords': keywords,
            'favicon': favicon,
        }
        
    except Exception as e:
        logger.error(f"获取网站信息失败: {str(e)}")
        return {
            'title': '',
            'description': '',
            'meta_keywords': '',
            'favicon': '',
        }


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_websites(request):
    """搜索网站"""
    try:
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'results': []})
        
        websites = Website.objects.filter(
            user=request.user,
            is_active=True
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(url__icontains=query) |
            Q(meta_keywords__icontains=query)
        ).select_related('category').prefetch_related('tags')[:20]
        
        serializer = WebsiteListSerializer(websites, many=True)
        return Response({'results': serializer.data})
        
    except Exception as e:
        logger.error(f"搜索网站失败: {str(e)}")
        return Response(
            {'error': '搜索失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )