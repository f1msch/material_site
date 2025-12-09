"""
用户视图模块
处理用户认证、注册、资料管理等API
"""

import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.db import transaction

from .models import User
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer,
    UserProfileUpdateSerializer, ChangePasswordSerializer, UserSerializer
)
from src.backend.exceptions import ValidationError, AuthenticationError

logger = logging.getLogger(__name__)


class UserRegisterView(generics.CreateAPIView):
    """
    用户注册视图

    POST /api/auth/register/
    创建新用户账户
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """创建用户"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                user = serializer.save()

            logger.info(f"User registered: {user.username}")

            return Response({
                'user': UserSerializer(user).data,
                'message': '注册成功'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            raise ValidationError(f"注册失败: {str(e)}")


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    用户资料视图

    GET /api/auth/profile/ - 获取用户资料
    PUT /api/auth/profile/ - 更新用户资料
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get_object(self):
        """获取当前登录用户"""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """更新用户资料"""
        try:
            user = self.get_object()
            serializer = UserProfileUpdateSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                self.perform_update(serializer)

            logger.info(f"User profile updated: {user.username}")

            return Response({
                'user': UserSerializer(user).data,
                'message': '资料更新成功'
            })

        except Exception as e:
            logger.error(f"Profile update failed: {str(e)}")
            raise ValidationError(f"资料更新失败: {str(e)}")


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    用户登录

    POST /api/auth/login/
    用户登录，返回JWT token
    """
    try:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # 生成JWT token
        refresh = RefreshToken.for_user(user)

        # 创建session（可选）
        login(request, user)

        logger.info(f"User logged in: {user.username}")

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise AuthenticationError("登录失败，请检查用户名和密码")


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    用户登出

    POST /api/auth/logout/
    登出用户，清除session
    """
    try:
        # JWT token由客户端管理，这里只清除session
        logout(request)

        logger.info(f"User logged out: {request.user.username}")

        return Response({
            'message': '成功退出登录'
        })

    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        raise ValidationError("退出登录失败")


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    修改密码

    POST /api/auth/change-password/
    修改当前用户密码
    """
    try:
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        with transaction.atomic():
            user.set_password(new_password)
            user.save()

        # 使旧token失效（客户端需要重新登录）
        logout(request)

        logger.info(f"Password changed: {user.username}")

        return Response({
            'message': '密码修改成功，请重新登录'
        })

    except Exception as e:
        logger.error(f"Password change failed: {str(e)}")
        raise ValidationError(f"密码修改失败: {str(e)}")