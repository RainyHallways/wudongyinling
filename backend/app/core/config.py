from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI舞蹈教练系统"
    API_V1_STR: str = "/api/v1"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"  # 在生产环境中应该使用环境变量
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 数据库配置
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "your-password"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str = "dance_coach"
    
    # MiniCPM-V API配置
    MINICPM_V_API_URL: Optional[str] = None
    MINICPM_V_API_KEY: Optional[str] = None
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    class Config:
        env_file = ".env"

settings = Settings() 