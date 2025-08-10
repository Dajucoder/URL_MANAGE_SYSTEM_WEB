@echo off
chcp 65001 >nul
echo 🚀 启动 URL管理系统...

REM 检查Docker是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未运行，请先启动Docker
    pause
    exit /b 1
)

echo 请选择运行环境：
echo 1^) 开发环境 ^(dev^)
echo 2^) 生产环境 ^(prod^)
set /p choice=请输入选择 ^(1/2^): 

if "%choice%"=="1" (
    echo 🔧 启动开发环境...
    docker-compose -f docker-compose.dev.yml up --build
) else if "%choice%"=="2" (
    echo 🏭 启动生产环境...
    docker-compose up --build -d
    echo ✅ 生产环境已启动
    echo 🌐 前端访问地址: http://localhost
    echo 🔧 后端API地址: http://localhost:8000/api
    echo 📊 管理后台: http://localhost:8000/admin
    pause
) else (
    echo ❌ 无效选择
    pause
    exit /b 1
)