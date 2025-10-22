# 前端构建阶段
FROM node:18-alpine AS frontend-build
WORKDIR /app

# 1. 先只复制 package.json 和 lock 文件
COPY package.json ./

# 2. 现在再安装依赖，这样能正确安装
RUN npm install

# 3. 最后复制你所有的源代码
COPY . .

# 4. 现在运行构建，此时 node_modules 已经准备好了
RUN npm run build

# Python后端构建阶段
FROM python:3.11-slim AS backend-build
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 最终运行阶段
FROM python:3.11-slim
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制前端构建产物
COPY --from=frontend-build /app/dist /app/frontend

# 复制后端
COPY --from=backend-build /app /app/backend
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# 配置Nginx
RUN echo 'server { \
    listen 80; \
    \
    # 前端路由 \
    location / { \
        root /app/frontend; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # 静态资源处理 \
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ { \
        root /app/frontend; \
        expires 1y; \
        add_header Cache-Control "public, max-age=31536000"; \
        access_log off; \
    } \
    \
    # 上传文件处理 \
    location /uploads { \
        alias /app/backend/uploads; \
        expires 30d; \
        add_header Cache-Control "public, max-age=2592000"; \
    } \
    \
    # API后端代理 \
    location /api { \
        proxy_pass http://localhost:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
        proxy_read_timeout 300; \
        proxy_connect_timeout 300; \
        proxy_send_timeout 300; \
    } \
    \
    # WebSocket支持 \
    location /ws { \
        proxy_pass http://localhost:8000; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 创建必要的目录
RUN mkdir -p /app/backend/uploads/image /app/backend/uploads/video

# 启动脚本
RUN echo '#!/bin/bash \n\
set -e \n\
\n\
# 等待数据库启动 \n\
echo "Waiting for database..." \n\
while ! nc -z db 3306; do \n\
  sleep 1 \n\
done \n\
echo "Database is ready!" \n\
\n\
# 启动Nginx \n\
echo "Starting Nginx..." \n\
nginx \n\
\n\
# 进入后端目录并运行数据库迁移 \n\
cd /app/backend \n\
echo "Running database migrations..." \n\
alembic upgrade head || echo "Migration failed, continuing..." \n\
\n\
# 启动后端服务 \n\
echo "Starting backend..." \n\
uvicorn main:app --host 0.0.0.0 --port 8000 --reload \n\
' > /app/start.sh

RUN chmod +x /app/start.sh

# 安装netcat for database health check
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

EXPOSE 80 8000

CMD ["/app/start.sh"] 