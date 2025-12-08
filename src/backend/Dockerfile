# 基础镜像
FROM python:3.10-slim

# 工作目录
WORKDIR /material-site

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DJANGO_SETTINGS_MODULE=backend.settings

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT}