"""
用户序列化器
处理用户数据的序列化和反序列化
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器（只读）"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar', 'bio', 'website',
            'credits', 'materials_count', 'downloads_count', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器

    Attributes:
        password: 密码字段（写操作）
        password_confirm: 确认密码字段
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        help_text='密码至少8位'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text='确认密码'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 30},
            'email': {'required': True}
        }

    def validate_username(self, value: str) -> str:
        """验证用户名"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value.lower()

    def validate_email(self, value: str) -> str:
        """验证邮箱"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value.lower()

    def validate(self, attrs: dict) -> dict:
        """验证注册数据"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data: dict) -> User:
        """创建用户"""
        validated_data.pop('password_confirm')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器

    Attributes:
        username: 用户名
        password: 密码
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs: dict) -> dict:
        """验证登录凭证"""
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('必须提供用户名和密码')

        # 尝试认证用户
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('用户名或密码错误')

        if not user.is_active:
            raise serializers.ValidationError('用户账户已被禁用')

        attrs['user'] = user
        return attrs


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""

    class Meta:
        model = User
        fields = ['email', 'avatar', 'bio', 'website']
        extra_kwargs = {
            'email': {'required': False}
        }


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value: str) -> str:
        """验证旧密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码错误")
        return value

    def validate(self, attrs: dict) -> dict:
        """验证密码数据"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "两次输入的密码不一致"})

        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({"new_password": "新密码不能与旧密码相同"})

        return attrs