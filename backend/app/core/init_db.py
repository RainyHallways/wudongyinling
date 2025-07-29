from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import get_password_hash
from app.models.user import User, UserRole

def init_db(db: Session) -> None:
    # 先执行SQL迁移
    try:
        # 添加role字段
        db.execute(text("ALTER TABLE users ADD COLUMN role ENUM('USER', 'ADMIN', 'TEACHER', 'DOCTOR') NOT NULL DEFAULT 'USER'"))
        # 添加unique_id字段
        db.execute(text("ALTER TABLE users ADD COLUMN unique_id VARCHAR(20) NOT NULL DEFAULT 'U000000' UNIQUE"))
        db.commit()
        print("数据库字段迁移成功！")
    except Exception as e:
        print(f"迁移字段时出错（如果字段已存在可以忽略）: {str(e)}")
        db.rollback()

    # 创建管理员用户
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            username="admin",
            email="admin@example.com",
            nickname="系统管理员",
            hashed_password=get_password_hash("123456"),
            is_admin=True,
            role=UserRole.ADMIN,
            unique_id="A000001",  # 管理员固定ID
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user) 