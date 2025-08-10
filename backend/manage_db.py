#!/usr/bin/env python
"""
数据库管理脚本
用于创建数据库、运行迁移等操作
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.conf import settings

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_superuser():
    """创建超级用户"""
    from django.contrib.auth import get_user_model
    import getpass
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        print("创建管理员账户...")
        username = input("请输入管理员用户名 (默认: admin): ") or 'admin'
        email = input("请输入管理员邮箱 (默认: admin@example.com): ") or 'admin@example.com'
        password = getpass.getpass("请输入管理员密码: ")
        
        if not password:
            print("密码不能为空！")
            return
            
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"超级用户创建成功: {username}")
    else:
        print("超级用户已存在")

def setup_database():
    """设置数据库"""
    print("正在创建数据库迁移...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("正在应用数据库迁移...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("正在创建超级用户...")
    create_superuser()
    
    print("数据库设置完成！")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'setup':
            setup_database()
        elif sys.argv[1] == 'reset':
            # 重置数据库
            if input("确定要重置数据库吗？(y/N): ").lower() == 'y':
                execute_from_command_line(['manage.py', 'flush', '--noinput'])
                setup_database()
        else:
            execute_from_command_line(sys.argv)
    else:
        print("使用方法:")
        print("  python manage_db.py setup    - 初始化数据库")
        print("  python manage_db.py reset    - 重置数据库")