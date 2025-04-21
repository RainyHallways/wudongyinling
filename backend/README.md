# AI舞蹈教练系统后端

## 项目介绍
AI舞蹈教练系统后端服务，提供API接口支持用户管理、舞蹈课程、健康管理、社交平台等功能。

## 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis (可选，用于缓存)

## 项目结构
```
backend/
├── alembic/            # 数据库迁移相关
├── app/                # 应用主目录
│   ├── api/           # API路由
│   ├── core/          # 核心配置
│   ├── models/        # 数据模型
│   └── schemas/       # 数据验证
├── uploads/           # 文件上传目录
├── .env               # 环境变量
├── .env.example       # 环境变量示例
├── main.py            # 应用入口
└── requirements.txt   # 依赖包
```

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
- 复制 `.env.example` 为 `.env`
- 修改数据库连接等配置

3. 初始化数据库：
```bash
python reset_db.py      # 重置数据库
alembic upgrade head    # 应用迁移
```

4. 启动服务：
```bash
uvicorn main:app --reload
```

## API文档
启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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

## 环境变量说明
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```