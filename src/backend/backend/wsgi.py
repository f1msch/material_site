import os
import sys
import traceback

# 添加调试信息
print("🚀 WSGI 开始加载...")

# 添加项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

print("🔧 设置DJANGO_SETTINGS_MODULE: backend.settings")

try:
    from django.core.wsgi import get_wsgi_application
    print("✅ 导入get_wsgi_application成功")
    
    application = get_wsgi_application()
    print("🎉 Django应用启动成功！")
    
except Exception as e:
    print(f"💥 Django应用启动失败: {e}")
    print("🔍 详细错误信息:")
    traceback.print_exc()
    
    # 让进程崩溃，这样错误会显示在日志中
    sys.exit(1)