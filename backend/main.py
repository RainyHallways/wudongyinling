from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.core.config import settings
from app.core.database import initialize_db, close_db_connection
from app.api.v1 import (
    courses, auth, stats, users, 
    health, prescriptions, challenges, 
    chat, ai_analysis
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建上传目录
def create_upload_dirs():
    for dir_name in ["video", "image"]:
        upload_path = os.path.join(settings.UPLOAD_DIR, dir_name)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            logger.info(f"Created upload directory: {upload_path}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序生命周期管理
    """
    # 启动前的操作
    logger.info("Starting application...")
    
    # 创建上传目录
    create_upload_dirs()
    
    # 初始化数据库
    await initialize_db()
    
    # 初始化WebSocket连接管理器
    from app.core.chat import chat_manager
    app.state.chat_manager = chat_manager
    
    # 提供应用实例
    yield
    
    # 应用关闭时的操作
    logger.info("Shutting down application...")
    
    # 关闭数据库连接
    await close_db_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    description="AI舞蹈教练系统API - 提供舞蹈课程、健康管理、社交功能",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["认证"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["用户管理"])
app.include_router(courses.router, prefix=f"{settings.API_V1_STR}/courses", tags=["舞蹈课程"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["健康记录"])
app.include_router(prescriptions.router, prefix=f"{settings.API_V1_STR}/prescriptions", tags=["健身处方"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["挑战"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["聊天"])
app.include_router(ai_analysis.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI分析"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["统计数据"])

@app.get("/")
async def root():
    return {"message": "欢迎使用AI舞蹈教练系统API"}