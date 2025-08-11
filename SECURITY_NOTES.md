# 安全部署说明

## 重要提醒
部署到生产环境前，请务必：

1. **修改默认管理员账户**
   - 默认用户名：admin
   - 默认密码：admin123
   - 默认邮箱：admin@example.com
   
   **请在首次部署后立即修改这些默认值！**

2. **环境变量配置**
   - 复制 `config.ini.example` 为 `config.ini` 并配置实际值
   - 设置强密码的 `DJANGO_SECRET_KEY`
   - 配置生产环境数据库连接

3. **生产环境设置**
   - 将 `DJANGO_DEBUG` 设为 `False`
   - 配置正确的 `ALLOWED_HOSTS`
   - 使用 HTTPS

## 已保护的敏感文件
- *.env 文件
- config.ini
- 数据库文件
- 缓存和临时文件