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
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes
import logging

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    用户登录接口
    
    使用用户名和密码获取JWT访问令牌和刷新令牌
    """
    
    @extend_schema(
        tags=['用户认证'],
        summary='用户登录',
        description='使用用户名和密码登录系统，成功后返回JWT令牌和用户信息',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': '用户名',
                        'example': 'admin'
                    },
                    'password': {
                        'type': 'string',
                        'description': '密码',
                        'example': 'admin123'
                    }
                },
                'required': ['username', 'password']
            }
        },
        responses={
            200: OpenApiResponse(
                description='登录成功',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='登录成功示例',
                        value={
                            'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                            'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                            'user': {
                                'id': 1,
                                'username': 'admin',
                                'email': 'admin@example.com',
                                'first_name': '管理员',
                                'last_name': '',
                                'is_active': True,
                                'date_joined': '2024-01-01T00:00:00Z'
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='登录失败',
                examples=[
                    OpenApiExample(
                        'Invalid credentials',
                        summary='用户名或密码错误',
                        value={'error': '登录失败，请检查用户名和密码'}
                    )
                ]
            )
        }
    )
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
    """
    用户注册接口
    
    创建新用户账户并返回JWT令牌
    """
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        tags=['用户认证'],
        summary='用户注册',
        description='创建新用户账户，注册成功后自动登录并返回JWT令牌',
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                description='注册成功',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='注册成功示例',
                        value={
                            'message': '注册成功',
                            'user': {
                                'id': 2,
                                'username': 'newuser',
                                'email': 'newuser@example.com',
                                'first_name': '新用户',
                                'last_name': '',
                                'is_active': True,
                                'date_joined': '2024-01-01T00:00:00Z'
                            },
                            'tokens': {
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='注册失败',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        summary='验证错误示例',
                        value={
                            'username': ['该用户名已存在'],
                            'email': ['请输入有效的电子邮件地址'],
                            'password': ['密码长度至少8位']
                        }
                    ),
                    OpenApiExample(
                        'Password Error',
                        summary='密码强度不足',
                        value={
                            'error': '密码不符合要求',
                            'details': ['密码太常见', '密码必须包含字母和数字']
                        }
                    )
                ]
            )
        }
    )
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
    """
    用户资料管理接口
    
    获取和更新当前用户的个人资料信息
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @extend_schema(
        tags=['用户管理'],
        summary='获取用户资料',
        description='获取当前登录用户的详细资料信息',
        responses={
            200: OpenApiResponse(
                description='获取成功',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='用户资料示例',
                        value={
                            'id': 1,
                            'username': 'admin',
                            'email': 'admin@example.com',
                            'first_name': '管理员',
                            'last_name': '',
                            'is_active': True,
                            'date_joined': '2024-01-01T00:00:00Z',
                            'last_active': '2024-01-01T12:00:00Z',
                            'profile': {
                                'avatar': None,
                                'bio': '这是我的个人简介',
                                'theme': 'light',
                                'language': 'zh-cn',
                                'is_public': True
                            }
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description='未认证')
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        tags=['用户管理'],
        summary='更新用户资料',
        description='更新当前登录用户的个人资料信息',
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                description='更新成功',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='更新成功示例',
                        value={
                            'id': 1,
                            'username': 'admin',
                            'email': 'newemail@example.com',
                            'first_name': '新名字',
                            'last_name': '新姓氏'
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='验证错误',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        summary='验证错误示例',
                        value={
                            'email': ['请输入有效的电子邮件地址']
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description='未认证')
        }
    )
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
    """
    修改密码接口
    
    允许用户修改登录密码
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=['用户管理'],
        summary='修改密码',
        description='修改当前用户的登录密码，需要提供旧密码进行验证',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'old_password': {
                        'type': 'string',
                        'description': '当前密码',
                        'example': 'oldpassword123'
                    },
                    'new_password': {
                        'type': 'string',
                        'description': '新密码（至少8位，包含字母和数字）',
                        'example': 'newpassword123'
                    }
                },
                'required': ['old_password', 'new_password']
            }
        },
        responses={
            200: OpenApiResponse(
                description='密码修改成功',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='修改成功示例',
                        value={'message': '密码修改成功'}
                    )
                ]
            ),
            400: OpenApiResponse(
                description='修改失败',
                examples=[
                    OpenApiExample(
                        'Wrong old password',
                        summary='旧密码错误',
                        value={'error': '旧密码不正确'}
                    ),
                    OpenApiExample(
                        'Weak password',
                        summary='新密码强度不足',
                        value={
                            'error': '新密码不符合要求',
                            'details': ['密码长度至少8位', '密码必须包含字母和数字']
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description='未认证')
        }
    )
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
    """
    用户统计数据接口
    
    获取当前用户的统计信息
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=['用户管理'],
        summary='获取用户统计',
        description='获取当前用户的书签、网站、分类等统计数据',
        responses={
            200: OpenApiResponse(
                description='统计数据',
                examples=[
                    OpenApiExample(
                        'Success',
                        summary='统计数据示例',
                        value={
                            'total_bookmarks': 150,
                            'total_visits': 2500,
                            'categories_count': 12,
                            'tags_count': 35,
                            'websites_count': 89,
                            'collections_count': 8,
                            'last_active': '2024-01-01T12:00:00Z',
                            'join_date': '2024-01-01T00:00:00Z'
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description='未认证')
        }
    )
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


@extend_schema(
    tags=['用户认证'],
    summary='用户登出',
    description='登出当前用户，将刷新令牌加入黑名单',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh_token': {
                    'type': 'string',
                    'description': '刷新令牌',
                    'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                }
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description='登出成功',
            examples=[
                OpenApiExample(
                    'Success',
                    summary='登出成功示例',
                    value={'message': '登出成功'}
                )
            ]
        ),
        400: OpenApiResponse(
            description='登出失败',
            examples=[
                OpenApiExample(
                    'Error',
                    summary='登出失败示例',
                    value={'error': '登出失败'}
                )
            ]
        ),
        401: OpenApiResponse(description='未认证')
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """用户登出接口"""
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


@extend_schema(
    tags=['用户管理'],
    summary='获取用户信息',
    description='获取当前登录用户的基本信息',
    responses={
        200: OpenApiResponse(
            description='用户信息',
            examples=[
                OpenApiExample(
                    'Success',
                    summary='用户信息示例',
                    value={
                        'id': 1,
                        'username': 'admin',
                        'email': 'admin@example.com',
                        'first_name': '管理员',
                        'last_name': '',
                        'is_active': True,
                        'date_joined': '2024-01-01T00:00:00Z'
                    }
                )
            ]
        ),
        401: OpenApiResponse(description='未认证')
    }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info_view(request):
    """获取当前用户信息接口"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return Response(
            {'error': '获取用户信息失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )