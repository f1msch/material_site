"""
自定义异常类
用于统一的错误处理和类型定义
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAPIError(APIException):
    """基础API异常类"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '服务器错误'
    default_code = 'server_error'

    def __init__(self, detail=None, code=None, extra=None):
        super().__init__(detail=detail, code=code)
        self.extra = extra or {}


class ValidationError(BaseAPIError):
    """验证错误"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '数据验证失败'
    default_code = 'validation_error'


class NotFoundError(BaseAPIError):
    """资源未找到"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '资源不存在'
    default_code = 'not_found'


class PermissionError(BaseAPIError):
    """权限错误"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '没有操作权限'
    default_code = 'permission_denied'


class AuthenticationError(BaseAPIError):
    """认证错误"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '认证失败'
    default_code = 'authentication_failed'


class MaterialUploadError(BaseAPIError):
    """素材上传错误"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '素材上传失败'
    default_code = 'material_upload_failed'