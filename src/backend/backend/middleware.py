"""
Django中间件模块
包含日志记录、错误处理和CORS相关中间件
"""

import logging
import time
import json
import traceback
from typing import Dict, Any, Optional
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """
    日志记录中间件
    功能：记录所有API请求的详细信息，便于调试和监控

    Attributes:
        get_response: Django请求处理函数
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """处理请求并记录日志"""
        start_time = time.time()

        try:
            # 处理请求前记录
            self.log_request(request)

            # 获取响应
            response = self.get_response(request)

            # 处理响应后记录
            self.log_response(request, response, start_time)

            return response

        except Exception as e:
            # 记录异常
            self.log_exception(request, e, start_time)
            raise

    def log_request(self, request: HttpRequest) -> None:
        """记录请求信息"""
        log_data = {
            'type': 'request',
            'method': request.method,
            'path': request.path,
            'ip': self.get_client_ip(request),
            'user': str(request.user) if request.user.is_authenticated else 'anonymous',
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
        }

        # 记录请求体（过滤敏感信息）
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.body.decode('utf-8', errors='ignore')
                if body:
                    data = json.loads(body) if body.strip().startswith('{') else body
                    if isinstance(data, dict) and 'password' in data:
                        data['password'] = '***'
                    log_data['body'] = data[:500] if isinstance(data, str) else data
            except:
                log_data['body'] = 'parse_error'

        logger.info(f"API Request: {log_data}")

    def log_response(self, request: HttpRequest, response: HttpResponse, start_time: float) -> None:
        """记录响应信息"""
        duration = time.time() - start_time

        log_data = {
            'type': 'response',
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration': round(duration * 1000, 2),  # 毫秒
        }

        # 只记录错误响应的内容
        if response.status_code >= 400:
            try:
                content = json.loads(response.content) if hasattr(response, 'content') else str(response)
                log_data['error'] = content[:500]
            except:
                log_data['error'] = 'parse_error'

        level = logging.ERROR if response.status_code >= 400 else logging.INFO
        logger.log(level, f"API Response: {log_data}")

    def log_exception(self, request: HttpRequest, exception: Exception, start_time: float) -> None:
        """记录异常信息"""
        duration = time.time() - start_time

        log_data = {
            'type': 'exception',
            'method': request.method,
            'path': request.path,
            'exception': str(exception),
            'duration': round(duration * 1000, 2),
            'traceback': traceback.format_exc(),
        }

        logger.error(f"API Exception: {log_data}")

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip


class ErrorHandlingMiddleware:
    """
    错误处理中间件
    功能：统一处理API异常，返回标准化的错误响应
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.handle_exception(request, e)

    def handle_exception(self, request: HttpRequest, exception: Exception) -> JsonResponse:
        """处理异常并返回标准化错误响应"""

        # 记录异常详情
        logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)

        # 根据异常类型返回不同的状态码
        error_data = {
            'error': True,
            'message': str(exception),
            'code': 'server_error',
            'timestamp': time.time(),
        }

        # 添加调试信息（仅在开发环境）
        from django.conf import settings
        if settings.DEBUG:
            error_data['debug'] = {
                'exception_type': type(exception).__name__,
                'traceback': traceback.format_exc().split('\n'),
            }

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # 处理特定异常类型
        if hasattr(exception, 'status_code'):
            status_code = exception.status_code
        elif 'not found' in str(exception).lower():
            status_code = status.HTTP_404_NOT_FOUND
        elif 'permission' in str(exception).lower() or 'auth' in str(exception).lower():
            status_code = status.HTTP_403_FORBIDDEN

        return JsonResponse(error_data, status=status_code)


class RequestValidationMiddleware:
    """
    请求验证中间件
    功能：验证请求的Content-Type和基本格式
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # 验证JSON请求的Content-Type
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.content_type
            if 'application/json' in content_type and request.body:
                try:
                    json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({
                        'error': True,
                        'message': 'Invalid JSON format in request body',
                        'code': 'invalid_json',
                    }, status=status.HTTP_400_BAD_REQUEST)

        return self.get_response(request)