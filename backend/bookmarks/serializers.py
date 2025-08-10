from rest_framework import serializers
from .models import Collection, Bookmark


class CollectionSerializer(serializers.ModelSerializer):
    """收藏夹序列化器"""
    bookmarks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'description', 'color', 'is_default',
            'bookmarks_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()
    
    def validate_name(self, value):
        """验证收藏夹名称"""
        user = self.context['request'].user
        if self.instance:
            # 更新时排除自己
            existing = Collection.objects.filter(
                name=value, user=user
            ).exclude(id=self.instance.id)
        else:
            # 创建时检查重复
            existing = Collection.objects.filter(name=value, user=user)
        
        if existing.exists():
            raise serializers.ValidationError("收藏夹名称已存在")
        return value


class BookmarkSerializer(serializers.ModelSerializer):
    """书签序列化器"""
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    
    class Meta:
        model = Bookmark
        fields = [
            'id', 'title', 'url', 'description', 'notes', 'thumbnail',
            'collection', 'collection_name', 'is_favorite', 'is_archived',
            'visit_count', 'last_visited', 'created_at', 'updated_at'
        ]
        read_only_fields = ['visit_count', 'last_visited', 'created_at', 'updated_at']
    
    def validate_collection(self, value):
        """验证收藏夹"""
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("只能选择自己的收藏夹")
        return value
    
    def validate_url(self, value):
        """验证URL"""
        user = self.context['request'].user
        if self.instance:
            # 更新时排除自己
            existing = Bookmark.objects.filter(
                url=value, user=user
            ).exclude(id=self.instance.id)
        else:
            # 创建时检查重复
            existing = Bookmark.objects.filter(url=value, user=user)
        
        if existing.exists():
            raise serializers.ValidationError("该书签已存在")
        return value
    
    def create(self, validated_data):
        """创建书签"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookmarkListSerializer(serializers.ModelSerializer):
    """书签列表序列化器（简化版）"""
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    
    class Meta:
        model = Bookmark
        fields = [
            'id', 'title', 'url', 'description', 'thumbnail',
            'collection_name', 'is_favorite', 'is_archived',
            'visit_count', 'last_visited', 'created_at'
        ]


class BookmarkStatsSerializer(serializers.Serializer):
    """书签统计序列化器"""
    total_bookmarks = serializers.IntegerField()
    favorite_bookmarks = serializers.IntegerField()
    archived_bookmarks = serializers.IntegerField()
    total_visits = serializers.IntegerField()
    collections_count = serializers.IntegerField()
    recent_bookmarks = serializers.IntegerField()