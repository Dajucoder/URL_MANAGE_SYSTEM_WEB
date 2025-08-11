# 安全部署说明

## 🚨 重要安全提醒

部署到生产环境前，请务必完成以下安全配置：

### 1. 修改默认管理员账户
```bash
# 创建新的管理员账户
docker-compose exec backend python manage.py create_admin \
  --username your_admin_username \
  --password your_secure_password \
  --email your_email@domain.com
```

**默认账户信息（仅用于开发环境）**：
- 默认用户名：admin
- 默认密码：admin123
- 默认邮箱：admin@example.com

⚠️ **生产环境必须立即修改这些默认值！**

### 2. 环境变量安全配置

#### 后端配置 (config.ini)
```ini
[database]
# 生产环境使用PostgreSQL
ENGINE = django.db.backends.postgresql
NAME = url_manage_db
USER = your_secure_db_user
PASSWORD = your_very_secure_db_password
HOST = db
PORT = 5432

[secret]
# 生成强密钥：python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = your-very-long-and-secure-secret-key-at-least-50-characters

[debug]
DEBUG = False
ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com,your-server-ip

[cors]
ALLOWED_ORIGINS = https://yourdomain.com,https://www.yourdomain.com
```

#### Docker环境变量
编辑 `docker-compose.yml` 中的环境变量：
```yaml
environment:
  - DJANGO_SECRET_KEY=your-production-secret-key
  - DJANGO_DEBUG=False
  - DB_PASSWORD=your-secure-database-password
  - POSTGRES_PASSWORD=your-secure-database-password
```

### 3. 生产环境安全设置

#### SSL/HTTPS配置
```bash
# 使用Let's Encrypt获取免费SSL证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

#### 防火墙配置
```bash
# 启用UFW防火墙
sudo ufw enable

# 允许必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# 拒绝其他端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

#### Nginx安全配置
```nginx
server {
    # 安全头设置
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # 隐藏Nginx版本
    server_tokens off;
    
    # 限制请求大小
    client_max_body_size 10M;
    
    # 其他配置...
}
```

## 🔒 已保护的敏感文件

以下文件已通过 `.gitignore` 保护，不会被提交到版本控制：

### 配置文件
- `config.ini` - 主配置文件
- `.env` - 环境变量文件
- `.env.local` - 本地环境变量
- `.env.production` - 生产环境变量

### 数据库文件
- `*.sqlite3` - SQLite数据库文件
- `db.sqlite3` - 默认数据库文件

### 日志文件
- `*.log` - 所有日志文件
- `logs/` - 日志目录

### 缓存和临时文件
- `__pycache__/` - Python缓存
- `*.pyc` - Python编译文件
- `node_modules/` - Node.js依赖
- `build/` - 前端构建文件
- `.DS_Store` - macOS系统文件

### 媒体文件
- `media/` - 用户上传文件
- `staticfiles/` - 收集的静态文件

## 🛡️ 安全最佳实践

### 1. 密码安全
- 使用至少12位的强密码
- 包含大小写字母、数字和特殊字符
- 定期更换密码
- 不要在多个服务中重复使用密码

### 2. 数据库安全
```sql
-- 创建专用数据库用户
CREATE USER url_manage_user WITH PASSWORD 'your_secure_password';
GRANT CONNECT ON DATABASE url_manage_db TO url_manage_user;
GRANT USAGE ON SCHEMA public TO url_manage_user;
GRANT CREATE ON SCHEMA public TO url_manage_user;

-- 限制权限
REVOKE ALL ON DATABASE url_manage_db FROM PUBLIC;
```

### 3. 系统安全
```bash
# 定期更新系统
sudo apt update && sudo apt upgrade -y

# 配置自动安全更新
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 配置SSH安全
sudo nano /etc/ssh/sshd_config
# 设置：
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes
```

### 4. 应用安全
- 启用CSRF保护
- 使用HTTPS传输
- 实施输入验证
- 定期更新依赖包
- 监控异常访问

## 🔍 安全检查清单

部署前请确认以下项目：

### 基础安全
- [ ] 修改了默认管理员账户
- [ ] 设置了强密码和密钥
- [ ] 配置了正确的ALLOWED_HOSTS
- [ ] 关闭了DEBUG模式
- [ ] 启用了HTTPS

### 服务器安全
- [ ] 配置了防火墙
- [ ] 禁用了root登录
- [ ] 使用了SSH密钥认证
- [ ] 定期更新系统
- [ ] 配置了日志监控

### 应用安全
- [ ] 使用了环境变量存储敏感信息
- [ ] 配置了安全HTTP头
- [ ] 限制了文件上传大小
- [ ] 启用了请求频率限制
- [ ] 配置了错误页面

### 数据安全
- [ ] 使用了强数据库密码
- [ ] 限制了数据库访问权限
- [ ] 配置了数据备份
- [ ] 启用了数据库连接加密
- [ ] 定期清理敏感日志

## 🚨 紧急响应

### 发现安全问题时
1. **立即隔离**：断开网络连接或停止服务
2. **评估影响**：确定受影响的数据和系统范围
3. **修复漏洞**：应用安全补丁或配置修复
4. **恢复服务**：在确认安全后重新启动服务
5. **事后分析**：分析原因并改进安全措施

### 常见安全事件处理
```bash
# 发现异常登录
# 1. 查看登录日志
sudo tail -f /var/log/auth.log

# 2. 封禁可疑IP
sudo ufw deny from suspicious_ip

# 3. 强制用户重新登录
docker-compose exec backend python manage.py clearsessions

# 发现异常文件访问
# 1. 检查文件完整性
find /opt/url-manage-system -type f -name "*.py" -exec md5sum {} \;

# 2. 恢复备份文件
sudo cp /backup/clean_files/* /opt/url-manage-system/
```

## 📞 安全联系方式

如发现安全漏洞，请通过以下方式联系：
- 📧 安全邮箱：security@yourdomain.com
- 🐛 GitHub Issues：https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB/issues
- 📋 安全检查清单：[docs/SECURITY_CHECK.md](SECURITY_CHECK.md)

## 📚 相关文档

- [部署指南](DEPLOYMENT.md) - 完整的部署流程
- [API文档](API.md) - API接口说明
- [安全检查清单](SECURITY_CHECK.md) - 详细的安全验证步骤

---

⚠️ **安全是一个持续的过程，请定期检查和更新安全配置！**

🔒 **记住：安全配置不是一次性的，需要持续维护和监控！**
