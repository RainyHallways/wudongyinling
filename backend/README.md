# AI舞蹈教练系统后端

## 项目说明
这是AI舞蹈教练系统的后端服务，使用FastAPI框架开发。

## 环境要求
- Python 3.8+
- MySQL 8.0+

## 安装步骤

1. 创建虚拟环境（推荐）
```bash
conda create -n dance python=3.9
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制`.env.example`文件为`.env`，并修改相应的配置：
```bash
cp .env.example .env
```

4. 初始化数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE dance_coach CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 运行数据库迁移
alembic upgrade head
```

5. 启动服务
```bash
uvicorn main:app --reload
```

## API文档
启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要功能
- 用户认证（登录/注册）
- 用户管理
- 舞蹈课程管理
- 健康数据记录
- 运动处方管理
- 社交功能
- 实时聊天

## 开发指南
1. 添加新的数据模型：
   - 在 `app/models/` 目录下创建新的模型文件
   - 使用 alembic 创建迁移文件：`alembic revision --autogenerate -m "描述"`
   - 应用迁移：`alembic upgrade head`

2. 添加新的API端点：
   - 在 `app/api/v1/` 目录下创建新的路由文件
   - 在 `main.py` 中注册路由

3. 添加新的依赖：
   - 安装新的包：`pip install package_name`
   - 更新 requirements.txt：`pip freeze > requirements.txt` 