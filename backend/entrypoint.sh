#!/bin/bash

# 等待数据库启动
echo "等待数据库启动..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "数据库已启动"

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 创建管理员账号
echo "创建管理员账号..."
python manage.py create_admin --username admin --password admin123 --email admin@example.com

# 初始化默认数据
echo "初始化默认数据..."
python manage.py init_default_data

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动Django服务器
echo "启动Django服务器..."
exec "$@"