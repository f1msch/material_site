# minimal_test.py
import os
import sys

# 添加路径
sys.path.insert(0, os.getcwd())

def simple_app(environ, start_response):
    """最简单的 WSGI 应用"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b"Minimal test: Working!\n"]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 启动最小测试服务器在端口 {port}")
    with make_server('0.0.0.0', port, simple_app) as httpd:
        print(f"✅ 服务器运行在 http://0.0.0.0:{port}")
        httpd.serve_forever()