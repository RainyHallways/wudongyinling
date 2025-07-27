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

## 完整部署指南

### 1. 准备MySQL数据库

首先需要创建MySQL用户和数据库：

```bash
# 登录MySQL（如果没有安装MySQL，需要先安装）
mysql -u root -p

# 在MySQL命令行中执行以下命令
CREATE DATABASE dance_coach;
CREATE USER 'dance_admin'@'localhost' IDENTIFIED BY 'dance123456';
GRANT ALL PRIVILEGES ON dance_coach.* TO 'dance_admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. 创建Python虚拟环境

选择以下任一方法创建虚拟环境：

```bash
# 方法1：使用conda
conda create -n dance python=3.9
conda activate dance

# 方法2：使用venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. 安装后端依赖

```bash
cd websites/backend  # 如果在项目根目录，需要进入backend目录
pip install -r requirements.txt
```

如果安装过程中遇到问题：

```bash
# 如果mysqlclient安装失败，需安装系统依赖(Ubuntu/Debian)
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

# 安装异步MySQL驱动(可能需要单独安装)
pip install aiomysql==0.2.0
```

### 4. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，设置数据库连接等配置
```

环境变量示例：

```env
# 数据库连接
DATABASE_URL=mysql+pymysql://dance_admin:dance123456@localhost/dance_coach
ASYNC_DATABASE_URL=mysql+aiomysql://dance_admin:dance123456@localhost/dance_coach
SQL_ECHO=false  # 是否打印SQL语句，开发环境设为true

# 安全配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS配置
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# 上传文件配置
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=5242880  # 5MB
```

### 5. 初始化数据库

有两种方式初始化数据库：

```bash
# 方式1：使用初始化脚本(推荐)
python init.py  # 会创建表结构并添加管理员账号

# 方式2：使用Alembic迁移
alembic upgrade head

# 重置数据库(仅开发环境使用)
python reset_db.py
```

### 6. 启动后端服务

```bash
# 开发模式启动
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产模式启动
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. 前端部署

```bash
cd ../  # 返回到websites目录
npm install
npm run dev  # 开发模式启动前端
```

生产环境构建：

```bash
npm run build
```

### 8. 常见问题解决

#### MySQL连接错误

如果出现 `Access denied for user 'dance_admin'@'localhost'` 错误：

1. 确认用户名和密码是否正确
2. 确认用户是否有正确的权限
3. 尝试使用root账户登录MySQL并重新创建用户：
   ```sql
   DROP USER 'dance_admin'@'localhost';
   CREATE USER 'dance_admin'@'localhost' IDENTIFIED BY 'dance123456';
   GRANT ALL PRIVILEGES ON dance_coach.* TO 'dance_admin'@'localhost';
   FLUSH PRIVILEGES;
   ```

#### 依赖安装问题

对于Windows WSL用户，如果安装mysqlclient遇到问题：
```bash
sudo apt-get update
sudo apt-get install gcc python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysqlclient
```

如果仍然失败，可以继续使用pymysql，它是纯Python实现无需编译。

#### aiomysql安装问题

如果安装aiomysql失败，可尝试：
```bash
pip install --upgrade pip
pip install aiomysql==0.2.0 --no-cache-dir
```

### 9. Docker部署（可选）

项目提供了docker-compose.yml，可以一键启动整个系统：

```bash
docker-compose up -d
```

这将启动前端、后端和MySQL数据库服务，无需手动安装各种依赖。

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