# 舞动银龄 - 后端服务

<p align="center">
  <b>基于FastAPI的现代化后端服务，支持舞蹈教学与健康管理平台</b>
</p>

## 项目介绍

"舞动银龄"后端服务，基于FastAPI框架构建，采用现代化的分层架构设计，提供用户管理、舞蹈课程、健康管理、AI教练、社交平台等功能的API接口。本项目经过全面重构，采用SQLAlchemy 2.0 ORM、Pydantic V2和异步编程模式，提供高性能、类型安全的后端服务。

## 技术栈

- **核心框架**: FastAPI
- **开发语言**: Python 3.8+
- **ORM**: SQLAlchemy 2.0 (声明式模型)
- **数据验证**: Pydantic V2
- **数据库迁移**: Alembic
- **异步支持**: asyncio, asyncpg
- **依赖注入**: FastAPI Depends
- **认证授权**: JWT, OAuth2
- **文档生成**: Swagger/OpenAPI, ReDoc
- **测试框架**: pytest, pytest-asyncio

## 项目架构

本项目采用清晰的分层架构设计:

- **API层**: 处理HTTP请求和响应，参数验证，调用Service层
- **Service层**: 实现业务逻辑，调用Repository层
- **Repository层**: 负责数据访问，与数据库交互
- **Model层**: 定义数据库模型和表结构
- **Schema层**: 定义数据验证和序列化模型

## 项目结构

```
backend/
├── alembic/                # 数据库迁移相关
│   └── versions/           # 迁移版本文件
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   └── v1/            # API v1版本
│   │       ├── auth.py    # 认证相关API
│   │       ├── users.py   # 用户管理API
│   │       ├── courses.py # 课程管理API
│   │       └── ...        # 其他API模块
│   ├── core/              # 核心配置
│   │   ├── config.py      # 应用配置
│   │   ├── database.py    # 数据库连接
│   │   ├── security.py    # 安全相关
│   │   └── ...            # 其他核心模块
│   ├── dependencies.py    # 依赖注入定义
│   ├── models/            # SQLAlchemy ORM模型
│   │   ├── base.py        # 基础模型类
│   │   ├── user.py        # 用户模型
│   │   ├── course.py      # 课程模型
│   │   └── ...            # 其他模型
│   ├── repositories/      # 数据访问层
│   │   ├── base.py        # 通用Repository基类
│   │   ├── user.py        # 用户数据访问
│   │   ├── course.py      # 课程数据访问
│   │   └── ...            # 其他数据访问
│   ├── schemas/           # Pydantic模型
│   │   ├── base.py        # 基础Schema类
│   │   ├── user.py        # 用户相关Schema
│   │   ├── course.py      # 课程相关Schema
│   │   └── ...            # 其他Schema
│   └── services/          # 业务逻辑层
│       ├── base_service.py # 基础Service类
│       ├── auth_service.py # 认证服务
│       ├── user_service.py # 用户服务
│       └── ...             # 其他服务
├── uploads/                # 文件上传目录
├── .env                    # 环境变量
├── .env.example            # 环境变量示例
├── alembic.ini             # Alembic配置
├── main.py                 # 应用入口
└── requirements.txt        # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，设置数据库连接等配置
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

### 3. 初始化数据库

```bash
# 应用数据库迁移
alembic upgrade head

# 如需重置数据库（开发环境）
python reset_db.py
```

### 4. 启动服务

```bash
# 开发模式启动
uvicorn main:app --reload

# 生产模式启动
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API文档

启动服务后，可通过以下地址访问API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 开发指南

### 添加新功能的工作流

1. **创建数据库模型**:
   - 在 `app/models/` 目录下创建或修改模型类
   - 使用SQLAlchemy 2.0语法，包含 `Mapped` 和 `mapped_column`

2. **创建数据库迁移**:
   ```bash
   alembic revision --autogenerate -m "添加新功能"
   alembic upgrade head
   ```

3. **定义Pydantic Schema**:
   - 在 `app/schemas/` 目录下创建或修改Schema类
   - 创建 `Base`, `Create`, `Update`, `InDB`, `Public` 等不同用途的Schema

4. **实现Repository层**:
   - 在 `app/repositories/` 目录下创建Repository类
   - 继承 `RepositoryBase`，实现数据访问方法

5. **实现Service层**:
   - 在 `app/services/` 目录下创建Service类
   - 注入对应的Repository，实现业务逻辑

6. **实现API路由**:
   - 在 `app/api/v1/` 目录下创建或修改路由文件
   - 通过依赖注入使用Service层

7. **注册路由**:
   - 在 `main.py` 中注册新的路由

### 异步编程注意事项

- 所有数据库操作都应该是异步的，使用 `async/await` 语法
- Repository层方法应接收 `AsyncSession` 参数
- API路由函数应使用 `async def` 定义

## 环境变量说明

```env
# 数据库连接
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
ASYNC_DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SQL_ECHO=True  # 是否打印SQL语句，开发环境设为True

# 安全配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS配置
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# 上传文件配置
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=5242880  # 5MB
```