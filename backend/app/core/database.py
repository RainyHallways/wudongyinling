from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings

logger = logging.getLogger(__name__)

# 同步引擎和会话
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    echo=settings.SQL_ECHO
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步引擎和会话
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL or settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.SQL_ECHO,
    pool_pre_ping=True
)
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# 依赖注入 - 同步
def get_db():
    """
    获取同步数据库会话
    
    已弃用：请使用get_async_db或get_db_session
    """
    logger.warning("Using deprecated synchronous database session. Consider using get_async_db instead.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# 依赖注入 - 异步
async def get_async_db():
    """
    获取异步数据库会话
    
    异步应用程序中推荐的数据库会话获取方式
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

# 用于测试的异步会话创建工厂
async def get_test_async_session():
    """
    创建用于测试的异步会话
    """
    async with AsyncSessionLocal() as session:
        yield session
        
# 初始化数据库
async def initialize_db():
    """
    异步初始化数据库
    创建所有表
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
    
# 关闭数据库连接
async def close_db_connection():
    """
    关闭数据库连接池
    """
    await async_engine.dispose()
    logger.info("Database connections closed") 