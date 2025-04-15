from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.models.course import Course
from app.core.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
import os
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
def get_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    db.delete(db_course)
    db.commit()
    return {"message": "课程已删除"}

@router.post("/upload/{file_type}")
async def upload_file(file_type: str, file: UploadFile = File(...)):
    if file_type not in ["video", "image"]:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 检查文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")
    
    # 创建上传目录
    upload_dir = os.path.join(settings.UPLOAD_DIR, file_type)
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 返回文件URL
    return {"url": f"/uploads/{file_type}/{file.filename}"} 