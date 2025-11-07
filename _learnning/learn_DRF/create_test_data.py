# 使用requests库测试API
import requests
import json

# 获取文章列表
response = requests.get('http://localhost:8000/api/posts/')
print(response.json())

# 创建新文章（需要认证）
headers = {
    'Authorization': 'Token your-token-here',  # 或者使用Session认证
    'Content-Type': 'application/json'
}
data = {
    'title': '新的文章',
    'content': '这是新文章的内容...',
    'category': 1,
    'status': 'published'
}
response = requests.post(
    'http://localhost:8000/api/posts/',
    headers=headers,
    data=json.dumps(data)
)
print(response.json())