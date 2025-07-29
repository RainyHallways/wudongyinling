from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.user import User, UserRole
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
                nickname="系统管理员",
                is_admin=True,
                role=UserRole.ADMIN,
                unique_id="A000001",  # 管理员固定ID
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("管理员用户创建成功！")
        else:
            # 更新现有管理员用户的字段
            try:
                db.execute(text("UPDATE users SET role = 'ADMIN', unique_id = 'A000001' WHERE username = 'admin'"))
                db.commit()
                print("管理员用户字段更新成功！")
            except Exception as e:
                print(f"更新管理员用户字段时出错: {str(e)}")
                db.rollback()
        
        # 验证和修复用户数据
        print("验证用户数据完整性...")
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            needs_update = False
            
            # 检查并修复role字段
            if admin_user.role is None:
                admin_user.role = UserRole.ADMIN
                needs_update = True
                print("修复admin用户的role字段")
            
            # 检查并修复unique_id字段
            if admin_user.unique_id is None or admin_user.unique_id == '':
                admin_user.unique_id = 'A000001'
                needs_update = True
                print("修复admin用户的unique_id字段")
            
            if needs_update:
                db.commit()
                print("✅ admin用户数据修复完成")
            
            # 显示最终结果
            print(f"✅ 管理员用户验证完成:")
            print(f"   用户名: {admin_user.username}")
            print(f"   角色: {admin_user.role}")
            print(f"   唯一ID: {admin_user.unique_id}")
            print(f"   是否管理员: {admin_user.is_admin}")
        
        db.close()
        
    except Exception as e:
        print(f"初始化数据库时出错：{str(e)}")
        raise e

if __name__ == "__main__":
    init_db() 