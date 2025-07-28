from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.models.course import Course
from app.models.challenge import Challenge
from app.models.health import HealthRecord
from app.core.security import get_password_hash

def init_db():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("数据库表创建成功！")
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 检查是否已存在管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建管理员用户
            admin = User(
                username="admin",
                hashed_password=get_password_hash("123456"),  # 使用哈希密码
                email="admin@example.com",
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("管理员用户创建成功！")
        
        db.close()
        
    except Exception as e:
        print(f"初始化数据库时出错：{str(e)}")
        raise e

if __name__ == "__main__":
    init_db() 