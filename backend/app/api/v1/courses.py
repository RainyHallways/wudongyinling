from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.course import Course
from pydantic import BaseModel
import shutil
import os
from datetime import datetime

router = APIRouter()

class CourseBase(BaseModel):
    title: str
    description: str
    duration: int
    difficulty: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    duration: int | None = None
    difficulty: str | None = None
    cover_url: str | None = None
    video_url: str | None = None

class CourseResponse(CourseBase):
    id: int
    cover_url: str
    video_url: str
    created_at: datetime
    class Config:
        from_attributes = True

@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0, 
    limit: int = 10, 
    difficulty: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    courses = query.offset(skip).limit(limit).all()
    return courses

@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    cover_file: UploadFile = File(None),
    video_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_course = Course(**course.model_dump())
    
    # 处理文件上传
    if cover_file:
        file_location = f"uploads/covers/{cover_file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(cover_file.file, file_object)
        db_course.cover_url = file_location

    if video_file:
        file_location = f"uploads/videos/{video_file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(video_file.file, file_object)
        db_course.video_url = file_location
    
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db)
):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    # 删除相关文件
    if course.cover_url and os.path.exists(course.cover_url):
        os.remove(course.cover_url)
    if course.video_url and os.path.exists(course.video_url):
        os.remove(course.video_url)
    
    db.delete(course)
    db.commit()
    return {"message": "课程已删除"} 