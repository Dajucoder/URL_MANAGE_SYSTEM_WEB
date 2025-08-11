from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = '创建管理员账号'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='管理员用户名 (默认: admin)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='管理员密码 (默认: admin123)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='管理员邮箱 (默认: admin@example.com)'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        try:
            # 检查管理员是否已存在
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'管理员用户 "{username}" 已存在，跳过创建')
                )
                return

            # 创建管理员用户
            admin_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'成功创建管理员用户: {username}')
            )
            self.stdout.write(f'用户名: {username}')
            self.stdout.write(f'密码: {password}')
            self.stdout.write(f'邮箱: {email}')
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'创建管理员失败: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'创建管理员时发生错误: {str(e)}')
            )