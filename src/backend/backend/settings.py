import os
import sys
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-production')

# 调试模式
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 允许的主机
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# 数据库配置函数
def get_database_config():
    """
    根据环境变量选择数据库配置
    优先级：DATABASE_URL > DB_ENGINE > 默认SQLite
    """
    # 如果提供了 DATABASE_URL（Railway 会自动提供）
    if os.getenv('DATABASE_URL'):
        return dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
        )

    # 如果指定了数据库引擎
    db_engine = os.getenv('DB_ENGINE', 'sqlite').lower()

    if db_engine == 'postgresql':
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'mydatabase'),
            'USER': os.getenv('DB_USER', 'myuser'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    elif db_engine == 'mysql':
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'mydatabase'),
            'USER': os.getenv('DB_USER', 'myuser'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    else:  # 默认使用 SQLite
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }


# 应用数据库配置
DATABASES = {
    'default': get_database_config()
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',

    # Local apps
    'users.apps.UsersConfig',
    'material_site.apps.MaterialSiteConfig',
    'payments.apps.PaymentsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Whitenoise 配置
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # 安全设置
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# 支付宝配置
ALIPAY_APP_ID = '你的应用ID'
ALIPAY_APP_PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
你的应用私钥
-----END RSA PRIVATE KEY-----
'''
ALIPAY_PUBLIC_KEY = '''
-----BEGIN PUBLIC KEY-----
支付宝公钥
-----END PUBLIC KEY-----
'''
ALIPAY_RETURN_URL = 'http://yourdomain.com/payment/success/'
ALIPAY_NOTIFY_URL = 'http://yourdomain.com/api/payments/notify/alipay/'

# 微信支付配置
WECHAT_APP_ID = '你的公众号APPID'
WECHAT_MCH_ID = '你的商户号'
WECHAT_API_KEY = '你的API密钥'
WECHAT_NOTIFY_URL = 'http://yourdomain.com/api/payments/notify/wechat/'

# 1. 配置缓存后端为 django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 连接地址：如果你的Redis没有密码，可以省略 `:密码@` 部分
        # 如果你使用方案一（MSI安装），通常不需要密码，地址如下：
        "LOCATION": "redis://127.0.0.1:6379/0",
        # 如果你使用Docker，并且想连接其他机器上的Redis，请替换IP。
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 如果Redis设置了密码，取消注释并修改下面这行
            # "PASSWORD": "your_redis_password_here",
        },
        # 可选：为所有缓存键添加一个前缀，防止多个项目冲突
        "KEY_PREFIX": "myproject_"
    }
}

# 2. （可选但推荐）将Session存储后端也设置为Redis
# 这可以让用户的Session数据也存储在Redis中，速度比默认的数据库存储更快。
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://localhost:9200'  # 如果你使用 Docker 且 Django 运行在宿主机，请使用 'http://host.docker.internal:9200'
    },
}