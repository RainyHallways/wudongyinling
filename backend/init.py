from app.core.database import SessionLocal
from app.core.init_db import init_db

def main() -> None:
    db = SessionLocal()
    init_db(db)

if __name__ == "__main__":
    main()
    print("初始化完成！") 