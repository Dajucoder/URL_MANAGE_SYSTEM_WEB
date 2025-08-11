FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 安装netcat用于检查数据库连接
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# 复制并设置启动脚本权限
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 创建静态文件和媒体文件目录
RUN mkdir -p static media

# 暴露端口
EXPOSE 8000

# 设置入口点
ENTRYPOINT ["/entrypoint.sh"]

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
