from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from ...core.database import get_async_db
from ...schemas.course import CourseCreate, CourseUpdate, CoursePublic
from ...schemas.base import DataResponse, ListResponse, PaginatedResponse
from ...services.course_service import CourseService

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[CoursePublic])
async def get_courses(
    skip: int = 0, 
    limit: int = 10, 
    difficulty: Optional[str] = None,
    keyword: Optional[str] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
    instructor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    获取课程列表，支持筛选和搜索
    """
    # 根据提供的参数选择不同的查询方法
    if keyword:
        courses = await course_service.search(db, keyword=keyword, skip=skip, limit=limit)
    elif difficulty:
        courses = await course_service.get_by_difficulty(db, difficulty=difficulty, skip=skip, limit=limit)
    elif min_duration is not None and max_duration is not None:
        courses = await course_service.get_by_duration_range(
            db, 
            min_duration=min_duration, 
            max_duration=max_duration, 
            skip=skip, 
            limit=limit
        )
    elif instructor_id:
        courses = await course_service.get_by_instructor(
            db, 
            instructor_id=instructor_id, 
            skip=skip, 
            limit=limit
        )
    else:
        # 无特定筛选条件，获取所有课程
        courses = await course_service.get_multi(db, skip=skip, limit=limit)
    
    # 获取总数
    filters = {}
    if difficulty:
        filters["difficulty"] = difficulty
    if instructor_id:
        filters["instructor_id"] = instructor_id
    
    total = await course_service.repository.count(db, filters=filters)
    
    return PaginatedResponse(
        data=courses,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/", response_model=DataResponse[CoursePublic])
async def create_course(
    course: CourseCreate, 
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    创建新课程
    """
    # 检查课程名是否已存在
    existing_course = await course_service.get_by_title(db, title=course.title)
    if existing_course:
        raise HTTPException(status_code=400, detail="课程标题已存在")
    
    db_course = await course_service.create(db, obj_in=course)
    return DataResponse(data=db_course, message="课程创建成功")

@router.get("/categories", response_model=DataResponse[List[dict]])
async def get_course_categories():
    """
    获取课程分类列表
    """
    categories = [
        {"value": "square", "label": "广场舞"},
        {"value": "folk", "label": "民族舞"},
        {"value": "taichi", "label": "太极拳"},
        {"value": "social", "label": "交谊舞"},
        {"value": "fitness", "label": "健身操"}
    ]
    return DataResponse(data=categories, message="获取课程分类成功")

@router.get("/difficulties", response_model=DataResponse[List[dict]])
async def get_course_difficulties():
    """
    获取课程难度列表
    """
    difficulties = [
        {"value": "beginner", "label": "初级"},
        {"value": "intermediate", "label": "中级"},
        {"value": "advanced", "label": "高级"}
    ]
    return DataResponse(data=difficulties, message="获取课程难度成功")

@router.get("/durations", response_model=DataResponse[List[dict]])
async def get_course_durations():
    """
    获取课程时长选项
    """
    durations = [
        {"value": "short", "label": "短时（10分钟内）", "min": 0, "max": 10},
        {"value": "medium", "label": "中时（10-30分钟）", "min": 10, "max": 30},
        {"value": "long", "label": "长时（30分钟以上）", "min": 30, "max": 999}
    ]
    return DataResponse(data=durations, message="获取课程时长选项成功")

@router.get("/{course_id}", response_model=DataResponse[CoursePublic])
async def get_course(
    course_id: int, 
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    通过ID获取课程详情
    """
    course = await course_service.get(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return DataResponse(data=course)

@router.post("/", response_model=DataResponse[CoursePublic])
async def create_course(
    course: CourseCreate, 
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    创建新课程
    """
    # 检查课程标题是否已存在
    existing_course = await course_service.get_by_title(db, title=course.title)
    if existing_course:
        raise HTTPException(status_code=400, detail="课程标题已存在")
    
    new_course = await course_service.create(db, obj_in=course)
    return DataResponse(data=new_course, message="课程创建成功")

@router.put("/{course_id}", response_model=DataResponse[CoursePublic])
async def update_course(
    course_id: int, 
    course: CourseUpdate, 
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    更新课程信息
    """
    db_course = await course_service.get(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    # 如果修改了标题，检查新标题是否已被使用
    if course.title and course.title != db_course.title:
        existing_course = await course_service.get_by_title(db, title=course.title)
        if existing_course and existing_course.id != course_id:
            raise HTTPException(status_code=400, detail="课程标题已存在")
    
    updated_course = await course_service.update(db, db_obj=db_course, obj_in=course)
    return DataResponse(data=updated_course, message="课程更新成功")

@router.delete("/{course_id}", response_model=DataResponse)
async def delete_course(
    course_id: int, 
    db: AsyncSession = Depends(get_async_db),
    course_service: CourseService = Depends()
):
    """
    删除课程
    """
    db_course = await course_service.delete(db, id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return DataResponse(message="课程已删除")

@router.post("/upload/{file_type}", response_model=DataResponse)
async def upload_file(
    file_type: str, 
    file: UploadFile = File(...),
    course_service: CourseService = Depends()
):
    """
    上传课程相关文件（视频或图片）
    """
    try:
        content = await file.read()
        url = await course_service.handle_file_upload(
            file_type=file_type, 
            file_content=content, 
            filename=file.filename
        )
        return DataResponse(data={"url": url}, message="文件上传成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 