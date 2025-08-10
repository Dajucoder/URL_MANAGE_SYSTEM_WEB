#!/bin/bash

# URL管理系统 Docker 启动脚本

echo "🚀 启动 URL管理系统..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 选择环境
echo "请选择运行环境："
echo "1) 开发环境 (dev)"
echo "2) 生产环境 (prod)"
read -p "请输入选择 (1/2): " choice

case $choice in
    1)
        echo "🔧 启动开发环境..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    2)
        echo "🏭 启动生产环境..."
        docker-compose up --build -d
        echo "✅ 生产环境已启动"
        echo "🌐 前端访问地址: http://localhost"
        echo "🔧 后端API地址: http://localhost:8000/api"
        echo "📊 管理后台: http://localhost:8000/admin"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac