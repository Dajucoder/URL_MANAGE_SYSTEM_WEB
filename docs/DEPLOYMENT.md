# 部署指南

## 概述

本文档详细介绍了URL管理系统在不同环境下的部署方法，包括开发环境、测试环境和生产环境。

## 环境要求

### 最低要求
- **操作系统**: Ubuntu 18.04+, CentOS 7+, Debian 10+
- **内存**: 2GB RAM
- **CPU**: 2核心
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **操作系统**: Ubuntu 20.04 LTS
- **内存**: 4GB RAM
- **CPU**: 4核心
- **存储**: 50GB SSD
- **网络**: 100Mbps带宽

### 软件依赖
- Docker 20.10+
- Docker Compose 2.0+
- Git 2.0+
- Nginx 1.18+ (可选)

## 开发环境部署

### 1. 克隆项目
```bash
git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB.git
cd URL_MANAGE_SYSTEM_WEB
```

### 2. 配置环境
```bash
# 复制配置文件
cp config.ini.example config.ini

# 编辑配置文件
nano config.ini
```

### 3. 启动开发环境
```bash
# 使用Docker Compose启动
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up --build -d
```

### 4. 初始化数据
```bash
# 等待服务启动完成后执行
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
docker-compose -f docker-compose.dev.yml exec backend python manage.py create_admin
```

## 生产环境部署

### 方式一：Docker部署（推荐）

#### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
sudo systemctl enable docker
sudo systemctl start docker
```

#### 2. 项目部署
```bash
# 克隆项目到生产目录
sudo mkdir -p /opt/url-manage-system
cd /opt/url-manage-system
sudo git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB.git .

# 设置权限
sudo chown -R $USER:$USER /opt/url-manage-system
```

#### 3. 配置生产环境
```bash
# 复制并编辑配置文件
cp config.ini.example config.ini
nano config.ini
```

**生产环境配置示例**:
```ini
[database]
ENGINE = django.db.backends.postgresql
NAME = url_manage_db
USER = url_manage_user
PASSWORD = your_secure_password
HOST = db
PORT = 5432

[secret]
SECRET_KEY = your-very-long-and-secure-secret-key

[debug]
DEBUG = False
ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com

[cors]
ALLOWED_ORIGINS = https://yourdomain.com,https://www.yourdomain.com
```

#### 4. 配置Docker环境变量
```bash
# 编辑docker-compose.yml
nano docker-compose.yml
```

**重要环境变量**:
```yaml
environment:
  - DJANGO_SECRET_KEY=your-secret-key
  - DJANGO_DEBUG=False
  - DB_PASSWORD=your-db-password
  - POSTGRES_PASSWORD=your-db-password
```

#### 5. 启动生产服务
```bash
# 构建并启动服务
docker-compose up --build -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 6. 初始化生产数据
```bash
# 等待数据库启动完成
sleep 30

# 运行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建管理员账户
docker-compose exec backend python manage.py create_admin \
  --username admin \
  --password your_secure_admin_password \
  --email admin@yourdomain.com

# 收集静态文件
docker-compose exec backend python manage.py collectstatic --noinput
```

### 方式二：传统部署

#### 1. 安装系统依赖
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib nginx redis-server

# CentOS/RHEL
sudo yum update
sudo yum install -y python3 python3-pip nodejs npm postgresql postgresql-server postgresql-contrib nginx redis
```

#### 2. 配置数据库
```bash
# 启动PostgreSQL
sudo systemctl enable postgresql
sudo systemctl start postgresql

# 创建数据库和用户
sudo -u postgres psql
CREATE DATABASE url_manage_db;
CREATE USER url_manage_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE url_manage_db TO url_manage_user;
\q
```

#### 3. 部署后端
```bash
# 创建项目目录
sudo mkdir -p /opt/url-manage-system
cd /opt/url-manage-system

# 克隆项目
sudo git clone https://github.com/Dajucoder/URL_MANAGE_SYSTEM_WEB.git .
sudo chown -R $USER:$USER /opt/url-manage-system

# 创建虚拟环境
cd backend
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp ../config.ini.example ../config.ini
nano ../config.ini

# 运行迁移
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --noinput
```

#### 4. 部署前端
```bash
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 复制构建文件到Nginx目录
sudo cp -r build/* /var/www/html/
```

#### 5. 配置Nginx
```bash
sudo nano /etc/nginx/sites-available/url-manage-system
```

**Nginx配置**:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # 前端静态文件
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 静态文件
    location /static/ {
        alias /opt/url-manage-system/backend/staticfiles/;
    }
    
    # 媒体文件
    location /media/ {
        alias /opt/url-manage-system/backend/media/;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/url-manage-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. 配置系统服务
```bash
# 创建systemd服务文件
sudo nano /etc/systemd/system/url-manage-backend.service
```

**服务配置**:
```ini
[Unit]
Description=URL Manage System Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/url-manage-system/backend
Environment=PATH=/opt/url-manage-system/backend/venv/bin
ExecStart=/opt/url-manage-system/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable url-manage-backend
sudo systemctl start url-manage-backend
```

## SSL证书配置

### 使用Let's Encrypt
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 手动SSL配置
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # 其他配置...
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## 监控和维护

### 健康检查脚本
```bash
#!/bin/bash
# health_check.sh

# 检查服务状态
check_service() {
    if systemctl is-active --quiet $1; then
        echo "✅ $1 is running"
    else
        echo "❌ $1 is not running"
        systemctl restart $1
    fi
}

# 检查各个服务
check_service nginx
check_service postgresql
check_service redis-server
check_service url-manage-backend

# 检查磁盘空间
df -h | awk '$5 > 80 {print "⚠️  Disk usage high: " $0}'

# 检查内存使用
free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
```

### 备份脚本
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/url-manage-system"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
pg_dump -h localhost -U url_manage_user url_manage_db > $BACKUP_DIR/db_backup_$DATE.sql

# 备份媒体文件
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /opt/url-manage-system/backend/media/

# 备份配置文件
cp /opt/url-manage-system/config.ini $BACKUP_DIR/config_backup_$DATE.ini

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.ini" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### 日志管理
```bash
# 配置logrotate
sudo nano /etc/logrotate.d/url-manage-system

# 内容:
/opt/url-manage-system/backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload url-manage-backend
    endscript
}
```

## 性能优化

### 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_websites_user_id ON websites_website(user_id);
CREATE INDEX idx_websites_category_id ON websites_website(category_id);
CREATE INDEX idx_websites_created_at ON websites_website(created_at);

-- 配置PostgreSQL
-- 编辑 /etc/postgresql/13/main/postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
```

### Redis缓存配置
```bash
# 编辑 /etc/redis/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Nginx优化
```nginx
# 启用Gzip压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# 启用缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# 连接优化
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
```

## 故障排除

### 常见问题

#### 服务无法启动
```bash
# 检查日志
sudo journalctl -u url-manage-backend -f
sudo tail -f /var/log/nginx/error.log

# 检查端口占用
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :80
```

#### 数据库连接问题
```bash
# 测试数据库连接
psql -h localhost -U url_manage_user -d url_manage_db

# 检查PostgreSQL状态
sudo systemctl status postgresql
```

#### 静态文件问题
```bash
# 重新收集静态文件
cd /opt/url-manage-system/backend
source venv/bin/activate
python manage.py collectstatic --noinput

# 检查文件权限
sudo chown -R www-data:www-data /opt/url-manage-system/backend/staticfiles/
```

## 安全建议

1. **定期更新系统和依赖包**
2. **使用强密码和密钥**
3. **启用防火墙**
4. **定期备份数据**
5. **监控系统日志**
6. **限制SSH访问**
7. **使用HTTPS**
8. **定期安全审计**

## 扩展部署

### 负载均衡
```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### 数据库主从复制
```bash
# 主数据库配置
# postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

# pg_hba.conf
host replication replica_user slave_ip/32 md5
```

### 容器编排（Kubernetes）
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-manage-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: url-manage-backend
  template:
    metadata:
      labels:
        app: url-manage-backend
    spec:
      containers:
      - name: backend
        image: url-manage-system:latest
        ports:
        - containerPort: 8000
```

这个部署指南涵盖了从开发环境到生产环境的完整部署流程，包括监控、维护和故障排除等方面的内容。