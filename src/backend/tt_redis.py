# tt_redis.py
import os
import django
from django.conf import settings

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # 替换为你的实际settings路径

# 初始化Django
django.setup()

# 现在可以导入Django的组件了
from django.core.cache import cache


def test_redis_connection():
    try:
        # 测试Redis连接
        cache.set('django_test_key', 'This value came from Django!', 30)
        value = cache.get('django_test_key')

        if value == 'This value came from Django!':
            print("✅ Redis连接测试成功！")
            print(f"读取到的数据: {value}")
        else:
            print("❌ Redis连接测试失败")

    except Exception as e:
        print(f"❌ 连接Redis时出错: {e}")


if __name__ == "__main__":
    test_redis_connection()