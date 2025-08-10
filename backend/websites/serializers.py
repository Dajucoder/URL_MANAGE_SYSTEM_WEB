from rest_framework import serializers
from .models import Category, Tag, Website, WebsiteNote


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    children = serializers.SerializerMethodField()
    full_path = serializers.CharField(source='get_full_path', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'color', 'icon', 'parent',
            'sort_order', 'website_count', 'children', 'full_path',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['website_count', 'created_at', 'updated_at']
    
    def get_children(self, obj):
        """获取子分类"""
        if hasattr(obj, 'children'):
            return CategorySerializer(obj.children.all(), many=True).data
        return []
    
    def validate_parent(self, value):
        """验证父分类"""
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("只能选择自己的分类作为父分类")
        return value


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    
    class Meta:
        model = Tag
        fields = [
            'id', 'name', 'color', 'usage_count', 'created_at'
        ]
        read_only_fields = ['usage_count', 'created_at']


class WebsiteNoteSerializer(serializers.ModelSerializer):
    """网站笔记序列化器"""
    
    class Meta:
        model = WebsiteNote
        fields = [
            'id', 'title', 'content', 'is_private', 'note_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WebsiteSerializer(serializers.ModelSerializer):
    """网站序列化器"""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    notes = WebsiteNoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Website
        fields = [
            'id', 'title', 'url', 'description', 'favicon', 'screenshot',
            'category', 'category_name', 'tags', 'tag_ids', 'notes',
            'meta_keywords', 'meta_author', 'meta_language',
            'is_active', 'is_public', 'visit_count', 'last_visited',
            'quality_score', 'loading_speed', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'visit_count', 'last_visited', 'quality_score', 'loading_speed',
            'created_at', 'updated_at'
        ]
    
    def validate_category(self, value):
        """验证分类"""
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("只能选择自己的分类")
        return value
    
    def validate_url(self, value):
        """验证URL"""
        user = self.context['request'].user
        if self.instance:
            # 更新时排除自己
            existing = Website.objects.filter(
                url=value, user=user
            ).exclude(id=self.instance.id)
        else:
            # 创建时检查重复
            existing = Website.objects.filter(url=value, user=user)
        
        if existing.exists():
            raise serializers.ValidationError("该网站已存在")
        return value
    
    def create(self, validated_data):
        """创建网站"""
        tag_ids = validated_data.pop('tag_ids', [])
        validated_data['user'] = self.context['request'].user
        
        website = Website.objects.create(**validated_data)
        
        # 设置标签
        if tag_ids:
            tags = Tag.objects.filter(
                id__in=tag_ids,
                user=self.context['request'].user
            )
            website.tags.set(tags)
        
        return website
    
    def update(self, instance, validated_data):
        """更新网站"""
        tag_ids = validated_data.pop('tag_ids', None)
        
        # 更新基本字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新标签
        if tag_ids is not None:
            tags = Tag.objects.filter(
                id__in=tag_ids,
                user=self.context['request'].user
            )
            instance.tags.set(tags)
        
        return instance


class WebsiteListSerializer(serializers.ModelSerializer):
    """网站列表序列化器（简化版）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Website
        fields = [
            'id', 'title', 'url', 'description', 'favicon',
            'category_name', 'tags_count', 'is_active', 'is_public',
            'visit_count', 'last_visited', 'quality_score', 'created_at'
        ]
    
    def get_tags_count(self, obj):
        return obj.tags.count()


class WebsiteStatsSerializer(serializers.Serializer):
    """网站统计序列化器"""
    total_websites = serializers.IntegerField()
    active_websites = serializers.IntegerField()
    public_websites = serializers.IntegerField()
    total_visits = serializers.IntegerField()
    categories_count = serializers.IntegerField()
    tags_count = serializers.IntegerField()
    avg_quality_score = serializers.FloatField()