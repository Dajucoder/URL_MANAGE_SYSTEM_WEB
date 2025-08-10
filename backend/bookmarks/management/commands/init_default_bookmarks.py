from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bookmarks.models import Collection, Bookmark

User = get_user_model()


class Command(BaseCommand):
    help = '初始化默认的书签收藏夹和网站'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='为指定用户创建默认书签（用户名），不指定则为所有用户创建'
        )

    def handle(self, *args, **options):
        # 默认收藏夹和书签配置
        default_data = {
            '开发工具': {
                'description': '编程开发相关的工具、平台和资源',
                'color': '#1890ff',
                'bookmarks': [
                    {'title': 'GitHub', 'url': 'https://github.com', 'description': '全球最大的代码托管平台'},
                    {'title': 'Stack Overflow', 'url': 'https://stackoverflow.com', 'description': '程序员问答社区'},
                    {'title': 'Visual Studio Code', 'url': 'https://code.visualstudio.com', 'description': '轻量级代码编辑器'},
                    {'title': 'MDN Web Docs', 'url': 'https://developer.mozilla.org', 'description': 'Web开发文档'},
                    {'title': 'Postman', 'url': 'https://www.postman.com', 'description': 'API测试工具'},
                ]
            },
            '学习教育': {
                'description': '在线学习平台、教育资源、课程网站',
                'color': '#52c41a',
                'bookmarks': [
                    {'title': '中国大学MOOC', 'url': 'https://www.icourse163.org', 'description': '国内优质课程平台'},
                    {'title': 'Coursera', 'url': 'https://www.coursera.org', 'description': '国际知名在线课程平台'},
                    {'title': 'LeetCode', 'url': 'https://leetcode.cn', 'description': '算法练习平台'},
                    {'title': '菜鸟教程', 'url': 'https://www.runoob.com', 'description': '编程入门教程'},
                    {'title': '知乎', 'url': 'https://www.zhihu.com', 'description': '知识问答社区'},
                ]
            },
            '设计创意': {
                'description': '设计工具、创意资源、素材网站',
                'color': '#722ed1',
                'bookmarks': [
                    {'title': 'Figma', 'url': 'https://www.figma.com', 'description': '协作设计工具'},
                    {'title': 'Dribbble', 'url': 'https://dribbble.com', 'description': '设计作品展示平台'},
                    {'title': 'Unsplash', 'url': 'https://unsplash.com', 'description': '高质量免费图片'},
                    {'title': 'Adobe Color', 'url': 'https://color.adobe.com', 'description': '配色方案工具'},
                    {'title': 'Iconfont', 'url': 'https://www.iconfont.cn', 'description': '阿里巴巴图标库'},
                ]
            },
            '生活服务': {
                'description': '日常生活相关的服务网站',
                'color': '#fa8c16',
                'bookmarks': [
                    {'title': '高德地图', 'url': 'https://www.amap.com', 'description': '地图导航服务'},
                    {'title': '美团', 'url': 'https://www.meituan.com', 'description': '本地生活服务'},
                    {'title': '12306', 'url': 'https://www.12306.cn', 'description': '火车票预订'},
                    {'title': '携程', 'url': 'https://www.ctrip.com', 'description': '旅游出行服务'},
                    {'title': '下厨房', 'url': 'https://www.xiachufang.com', 'description': '菜谱分享平台'},
                ]
            },
            '娱乐休闲': {
                'description': '娱乐和休闲相关的网站',
                'color': '#eb2f96',
                'bookmarks': [
                    {'title': '哔哩哔哩', 'url': 'https://www.bilibili.com', 'description': '年轻人的视频社区'},
                    {'title': '网易云音乐', 'url': 'https://music.163.com', 'description': '音乐社交平台'},
                    {'title': '豆瓣', 'url': 'https://www.douban.com', 'description': '文艺生活社区'},
                    {'title': '微信读书', 'url': 'https://weread.qq.com', 'description': '社交阅读应用'},
                    {'title': 'Steam', 'url': 'https://store.steampowered.com', 'description': 'PC游戏平台'},
                ]
            },
            '新闻资讯': {
                'description': '新闻媒体、资讯网站和信息获取平台',
                'color': '#fa541c',
                'bookmarks': [
                    {'title': '新华网', 'url': 'http://www.xinhuanet.com', 'description': '国家通讯社官网'},
                    {'title': '36氪', 'url': 'https://36kr.com', 'description': '创投媒体平台'},
                    {'title': 'IT之家', 'url': 'https://www.ithome.com', 'description': '科技新闻网站'},
                    {'title': '澎湃新闻', 'url': 'https://www.thepaper.cn', 'description': '时政新闻平台'},
                    {'title': '虎嗅网', 'url': 'https://www.huxiu.com', 'description': '商业科技资讯'},
                ]
            },
            '社交媒体': {
                'description': '社交网络、通讯平台和社区交流网站',
                'color': '#13c2c2',
                'bookmarks': [
                    {'title': '微博', 'url': 'https://weibo.com', 'description': '社交媒体平台'},
                    {'title': '小红书', 'url': 'https://www.xiaohongshu.com', 'description': '生活方式分享'},
                    {'title': '脉脉', 'url': 'https://maimai.cn', 'description': '职场社交平台'},
                    {'title': '即刻', 'url': 'https://web.okjike.com', 'description': '兴趣社交应用'},
                    {'title': 'LinkedIn', 'url': 'https://www.linkedin.com', 'description': '职业社交网络'},
                ]
            },
            '购物电商': {
                'description': '电商购物平台、比价网站和购物助手工具',
                'color': '#f759ab',
                'bookmarks': [
                    {'title': '淘宝', 'url': 'https://www.taobao.com', 'description': '综合购物平台'},
                    {'title': '京东', 'url': 'https://www.jd.com', 'description': '自营电商平台'},
                    {'title': '天猫', 'url': 'https://www.tmall.com', 'description': '品牌商城平台'},
                    {'title': '什么值得买', 'url': 'https://www.smzdm.com', 'description': '购物决策平台'},
                    {'title': '拼多多', 'url': 'https://www.pinduoduo.com', 'description': '社交电商平台'},
                ]
            },
            '金融理财': {
                'description': '金融服务、理财工具、投资平台',
                'color': '#389e0d',
                'bookmarks': [
                    {'title': '支付宝', 'url': 'https://www.alipay.com', 'description': '移动支付平台'},
                    {'title': '蚂蚁财富', 'url': 'https://www.antfortune.com', 'description': '理财服务平台'},
                    {'title': '雪球', 'url': 'https://xueqiu.com', 'description': '投资者社区'},
                    {'title': '天天基金', 'url': 'https://www.1234567.com.cn', 'description': '基金投资平台'},
                    {'title': '招商银行', 'url': 'https://www.cmbchina.com', 'description': '零售银行服务'},
                ]
            },
            '工具软件': {
                'description': '实用工具、在线服务和效率提升软件',
                'color': '#096dd9',
                'bookmarks': [
                    {'title': '腾讯文档', 'url': 'https://docs.qq.com', 'description': '在线协作文档'},
                    {'title': '有道云笔记', 'url': 'https://note.youdao.com', 'description': '云端笔记应用'},
                    {'title': '草料二维码', 'url': 'https://cli.im', 'description': '二维码生成器'},
                    {'title': 'Notion', 'url': 'https://www.notion.so', 'description': '全能工作空间'},
                    {'title': '石墨文档', 'url': 'https://shimo.im', 'description': '云端办公套件'},
                ]
            }
        }

        # 获取目标用户
        if options['user']:
            try:
                users = [User.objects.get(username=options['user'])]
                self.stdout.write(f"为用户 {options['user']} 创建默认书签...")
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"用户 {options['user']} 不存在")
                )
                return
        else:
            users = User.objects.all()
            self.stdout.write("为所有用户创建默认书签...")

        total_collections = 0
        total_bookmarks = 0

        for user in users:
            self.stdout.write(f"处理用户: {user.username}")
            
            for collection_name, collection_info in default_data.items():
                # 创建收藏夹
                collection, created = Collection.objects.get_or_create(
                    user=user,
                    name=collection_name,
                    defaults={
                        'description': collection_info['description'],
                        'color': collection_info['color'],
                        'is_default': False
                    }
                )
                
                if created:
                    total_collections += 1
                    self.stdout.write(f"  创建收藏夹: {collection_name}")
                else:
                    self.stdout.write(f"  收藏夹已存在: {collection_name}")
                
                # 创建书签
                for bookmark_data in collection_info['bookmarks']:
                    bookmark, created = Bookmark.objects.get_or_create(
                        user=user,
                        url=bookmark_data['url'],
                        defaults={
                            'title': bookmark_data['title'],
                            'description': bookmark_data['description'],
                            'collection': collection,
                        }
                    )
                    
                    if created:
                        total_bookmarks += 1
                        self.stdout.write(f"    添加书签: {bookmark_data['title']}")
                    else:
                        # 如果书签已存在但不在当前收藏夹，更新收藏夹
                        if bookmark.collection != collection:
                            bookmark.collection = collection
                            bookmark.save()
                            self.stdout.write(f"    更新书签收藏夹: {bookmark_data['title']}")
                        else:
                            self.stdout.write(f"    书签已存在: {bookmark_data['title']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n初始化完成！\n"
                f"创建收藏夹: {total_collections} 个\n"
                f"创建书签: {total_bookmarks} 个"
            )
        )