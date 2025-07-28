from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI舞蹈教练系统"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://dance_admin:dance123456@localhost/dance_coach")
    ASYNC_DATABASE_URL: Optional[str] = os.getenv("ASYNC_DATABASE_URL")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() == "true"
    
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # 跨域配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:5174"]
    
    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "104857600"))  # 100MB in bytes

    # AI服务配置
    MINICPM_V_API_URL: str = os.getenv("MINICPM_V_API_URL", "http://localhost:9000/v1")
    MINICPM_V_API_KEY: str = os.getenv("MINICPM_V_API_KEY", "dummy_key_for_development")

    class Config:
        case_sensitive = True

settings = Settings() 