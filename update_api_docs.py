#!/usr/bin/env python
"""
更新API文档依赖和配置的脚本
"""
import os
import subprocess
import sys

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def main():
    print("🚀 开始更新API文档配置...")
    
    # 切换到backend目录
    backend_dir = os.path.join(os.getcwd(), 'backend')
    if not os.path.exists(backend_dir):
        print("❌ backend目录不存在")
        return False
    
    os.chdir(backend_dir)
    print(f"📁 切换到目录: {backend_dir}")
    
    # 安装新依赖
    if not run_command("pip install drf-spectacular==0.27.0", "安装drf-spectacular"):
        return False
    
    # 运行数据库迁移
    if not run_command("python manage.py makemigrations", "创建数据库迁移"):
        return False
    
    if not run_command("python manage.py migrate", "应用数据库迁移"):
        return False
    
    # 收集静态文件
    if not run_command("python manage.py collectstatic --noinput", "收集静态文件"):
        print("⚠️ 收集静态文件失败，但可以继续")
    
    # 生成API Schema
    if not run_command("python manage.py spectacular --color --file schema.yml", "生成API Schema"):
        print("⚠️ 生成Schema失败，但可以继续")
    
    print("\n🎉 API文档配置更新完成！")
    print("\n📋 可用的API文档地址:")
    print("   • Swagger UI: http://localhost:8000/api/docs/")
    print("   • ReDoc: http://localhost:8000/api/redoc/")
    print("   • OpenAPI Schema: http://localhost:8000/api/schema/")
    print("   • 健康检查: http://localhost:8000/api/health/")
    print("   • API信息: http://localhost:8000/api/info/")
    
    print("\n🔧 启动开发服务器:")
    print("   python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)