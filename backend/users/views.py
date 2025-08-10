from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import logging

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义JWT登录视图"""
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                user = authenticate(
                    username=request.data.get('username'),
                    password=request.data.get('password')
                )
                if user:
                    # 更新最后活跃时间
                    user.last_active = timezone.now()
                    user.save(update_fields=['last_active'])
                    
                    # 添加用户信息到响应
                    user_serializer = UserSerializer(user)
                    response.data['user'] = user_serializer.data
                    logger.info(f"用户 {user.username} 登录成功")
            return response
        except Exception as e:
            logger.error(f"登录失败: {str(e)}")
            return Response(
                {'error': '登录失败，请检查用户名和密码'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationView(APIView):
    """用户注册视图"""
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                # 验证密码强度
                password = serializer.validated_data['password']
                try:
                    validate_password(password)
                except ValidationError as e:
                    return Response(
                        {'error': '密码不符合要求', 'details': e.messages},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # 创建用户
                validated_data = serializer.validated_data
                user = User.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=password,
                    first_name=validated_data.get('first_name', ''),
                    last_name=validated_data.get('last_name', '')
                )
                
                # 创建用户资料
                UserProfile.objects.create(user=user)
                
                # 生成JWT令牌
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"新用户注册成功: {user.username}")
                
                return Response({
                    'message': '注册成功',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"注册失败: {str(e)}")
            return Response(
                {'error': '注册失败，请稍后重试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """用户资料视图"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            if serializer.is_valid():
                self.perform_update(serializer)
                logger.info(f"用户 {instance.username} 更新资料")
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"更新用户资料失败: {str(e)}")
            return Response(
                {'error': '更新失败，请稍后重试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(APIView):
    """修改密码视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            if not old_password or not new_password:
                return Response(
                    {'error': '请提供旧密码和新密码'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 验证旧密码
            if not user.check_password(old_password):
                return Response(
                    {'error': '旧密码不正确'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 验证新密码强度
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response(
                    {'error': '新密码不符合要求', 'details': e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 更新密码
            user.set_password(new_password)
            user.save()
            
            logger.info(f"用户 {user.username} 修改密码成功")
            
            return Response({'message': '密码修改成功'})
            
        except Exception as e:
            logger.error(f"修改密码失败: {str(e)}")
            return Response(
                {'error': '修改密码失败，请稍后重试'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserStatsView(APIView):
    """用户统计视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            stats = {
                'total_bookmarks': user.total_bookmarks,
                'total_visits': user.total_visits,
                'categories_count': user.categories.count(),
                'tags_count': user.tags.count(),
                'websites_count': user.websites.count(),
                'collections_count': user.collections.count(),
                'last_active': user.last_active,
                'join_date': user.date_joined,
            }
            
            return Response(stats)
            
        except Exception as e:
            logger.error(f"获取用户统计失败: {str(e)}")
            return Response(
                {'error': '获取统计数据失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """登出视图"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logger.info(f"用户 {request.user.username} 登出")
        return Response({'message': '登出成功'})
        
    except Exception as e:
        logger.error(f"登出失败: {str(e)}")
        return Response(
            {'error': '登出失败'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info_view(request):
    """获取当前用户信息"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return Response(
            {'error': '获取用户信息失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )