from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from websites.models import Category, Tag, Website
from bookmarks.models import Collection, Bookmark

User = get_user_model()

class Command(BaseCommand):
    help = '初始化默认的分类、网站和书签数据'

    def handle(self, *args, **options):
        try:
            # 获取管理员用户
            admin_user = User.objects.filter(username='admin').first()
            if not admin_user:
                self.stdout.write(
                    self.style.ERROR('管理员用户不存在，请先创建管理员用户')
                )
                return

            # 创建默认分类
            self.create_default_categories(admin_user)
            
            # 创建默认标签
            self.create_default_tags(admin_user)
            
            # 创建默认网站
            self.create_default_websites(admin_user)
            
            # 创建默认收藏夹
            self.create_default_collections(admin_user)
            
            # 创建默认书签
            self.create_default_bookmarks(admin_user)
            
            self.stdout.write(
                self.style.SUCCESS('成功初始化默认数据')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'初始化默认数据失败: {str(e)}')
            )

    def create_default_categories(self, user):
        """创建默认分类"""
        categories_data = [
            {'name': '开发工具', 'description': '编程开发相关工具和资源', 'color': '#007bff', 'icon': 'code'},
            {'name': '学习资源', 'description': '在线学习平台和教程', 'color': '#28a745', 'icon': 'book'},
            {'name': '设计素材', 'description': '设计工具和素材资源', 'color': '#dc3545', 'icon': 'palette'},
            {'name': '新闻资讯', 'description': '科技新闻和行业资讯', 'color': '#ffc107', 'icon': 'newspaper'},
            {'name': '社交媒体', 'description': '社交网络和交流平台', 'color': '#17a2b8', 'icon': 'users'},
            {'name': '娱乐休闲', 'description': '娱乐和休闲网站', 'color': '#6f42c1', 'icon': 'gamepad'},
            {'name': '工作效率', 'description': '提高工作效率的工具', 'color': '#fd7e14', 'icon': 'briefcase'},
            {'name': '购物网站', 'description': '电商和购物平台', 'color': '#20c997', 'icon': 'shopping-cart'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                user=user,
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                self.stdout.write(f'创建分类: {category.name}')

    def create_default_tags(self, user):
        """创建默认标签"""
        tags_data = [
            {'name': 'JavaScript', 'color': '#f7df1e'},
            {'name': 'Python', 'color': '#3776ab'},
            {'name': 'React', 'color': '#61dafb'},
            {'name': 'Vue', 'color': '#4fc08d'},
            {'name': 'Node.js', 'color': '#339933'},
            {'name': 'CSS', 'color': '#1572b6'},
            {'name': 'HTML', 'color': '#e34f26'},
            {'name': '免费', 'color': '#28a745'},
            {'name': '付费', 'color': '#dc3545'},
            {'name': '开源', 'color': '#6f42c1'},
            {'name': '教程', 'color': '#17a2b8'},
            {'name': '工具', 'color': '#fd7e14'},
        ]
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                user=user,
                defaults={'color': tag_data['color']}
            )
            if created:
                self.stdout.write(f'创建标签: {tag.name}')

    def create_default_websites(self, user):
        """创建默认网站"""
        # 获取分类
        dev_category = Category.objects.filter(name='开发工具', user=user).first()
        learn_category = Category.objects.filter(name='学习资源', user=user).first()
        design_category = Category.objects.filter(name='设计素材', user=user).first()
        news_category = Category.objects.filter(name='新闻资讯', user=user).first()
        
        websites_data = [
            {
                'title': 'GitHub',
                'url': 'https://github.com',
                'description': '全球最大的代码托管平台',
                'category': dev_category,
                'tags': ['开源', '工具']
            },
            {
                'title': 'Stack Overflow',
                'url': 'https://stackoverflow.com',
                'description': '程序员问答社区',
                'category': dev_category,
                'tags': ['工具']
            },
            {
                'title': 'MDN Web Docs',
                'url': 'https://developer.mozilla.org',
                'description': 'Web开发文档和教程',
                'category': learn_category,
                'tags': ['JavaScript', 'HTML', 'CSS', '教程', '免费']
            },
            {
                'title': 'Vue.js',
                'url': 'https://vuejs.org',
                'description': 'Vue.js官方文档',
                'category': learn_category,
                'tags': ['Vue', '教程', '免费']
            },
            {
                'title': 'React',
                'url': 'https://react.dev',
                'description': 'React官方文档',
                'category': learn_category,
                'tags': ['React', '教程', '免费']
            },
            {
                'title': 'Figma',
                'url': 'https://figma.com',
                'description': '在线UI设计工具',
                'category': design_category,
                'tags': ['工具']
            },
            {
                'title': 'Unsplash',
                'url': 'https://unsplash.com',
                'description': '免费高质量图片素材',
                'category': design_category,
                'tags': ['免费']
            },
            {
                'title': '掘金',
                'url': 'https://juejin.cn',
                'description': '技术社区和资讯平台',
                'category': news_category,
                'tags': []
            },
        ]
        
        for site_data in websites_data:
            website, created = Website.objects.get_or_create(
                url=site_data['url'],
                user=user,
                defaults={
                    'title': site_data['title'],
                    'description': site_data['description'],
                    'category': site_data['category'],
                    'is_public': True
                }
            )
            
            if created:
                # 添加标签
                for tag_name in site_data['tags']:
                    tag = Tag.objects.filter(name=tag_name, user=user).first()
                    if tag:
                        website.tags.add(tag)
                
                self.stdout.write(f'创建网站: {website.title}')

    def create_default_collections(self, user):
        """创建默认收藏夹"""
        collections_data = [
            {'name': '默认收藏夹', 'description': '默认的书签收藏夹', 'color': '#007bff', 'is_default': True},
            {'name': '开发资源', 'description': '开发相关的书签', 'color': '#28a745'},
            {'name': '学习笔记', 'description': '学习资料和笔记', 'color': '#17a2b8'},
            {'name': '设计灵感', 'description': '设计相关的收藏', 'color': '#dc3545'},
            {'name': '工具箱', 'description': '实用工具收藏', 'color': '#ffc107'},
        ]
        
        for coll_data in collections_data:
            collection, created = Collection.objects.get_or_create(
                name=coll_data['name'],
                user=user,
                defaults={
                    'description': coll_data['description'],
                    'color': coll_data['color'],
                    'is_default': coll_data.get('is_default', False)
                }
            )
            if created:
                self.stdout.write(f'创建收藏夹: {collection.name}')

    def create_default_bookmarks(self, user):
        """创建默认书签"""
        # 获取收藏夹
        default_collection = Collection.objects.filter(name='默认收藏夹', user=user).first()
        dev_collection = Collection.objects.filter(name='开发资源', user=user).first()
        learn_collection = Collection.objects.filter(name='学习笔记', user=user).first()
        design_collection = Collection.objects.filter(name='设计灵感', user=user).first()
        tool_collection = Collection.objects.filter(name='工具箱', user=user).first()
        
        bookmarks_data = [
            {
                'title': 'GitHub',
                'url': 'https://github.com',
                'description': '代码托管和版本控制',
                'collection': dev_collection,
                'is_favorite': True
            },
            {
                'title': 'VS Code',
                'url': 'https://code.visualstudio.com',
                'description': '微软开发的代码编辑器',
                'collection': dev_collection
            },
            {
                'title': 'Node.js',
                'url': 'https://nodejs.org',
                'description': 'JavaScript运行时环境',
                'collection': dev_collection
            },
            {
                'title': 'freeCodeCamp',
                'url': 'https://freecodecamp.org',
                'description': '免费编程学习平台',
                'collection': learn_collection,
                'is_favorite': True
            },
            {
                'title': 'Coursera',
                'url': 'https://coursera.org',
                'description': '在线课程平台',
                'collection': learn_collection
            },
            {
                'title': 'Dribbble',
                'url': 'https://dribbble.com',
                'description': '设计师作品展示平台',
                'collection': design_collection
            },
            {
                'title': 'Behance',
                'url': 'https://behance.net',
                'description': 'Adobe创意作品平台',
                'collection': design_collection
            },
            {
                'title': 'Can I Use',
                'url': 'https://caniuse.com',
                'description': '浏览器兼容性查询工具',
                'collection': tool_collection
            },
            {
                'title': 'JSON Formatter',
                'url': 'https://jsonformatter.curiousconcept.com',
                'description': 'JSON格式化工具',
                'collection': tool_collection
            },
            {
                'title': 'Google',
                'url': 'https://google.com',
                'description': '搜索引擎',
                'collection': default_collection,
                'is_favorite': True
            },
        ]
        
        for bookmark_data in bookmarks_data:
            bookmark, created = Bookmark.objects.get_or_create(
                url=bookmark_data['url'],
                user=user,
                defaults={
                    'title': bookmark_data['title'],
                    'description': bookmark_data['description'],
                    'collection': bookmark_data['collection'] or default_collection,
                    'is_favorite': bookmark_data.get('is_favorite', False)
                }
            )
            if created:
                self.stdout.write(f'创建书签: {bookmark.title}')