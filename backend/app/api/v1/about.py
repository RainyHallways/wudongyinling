from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from ...core.database import get_async_db
from ...core.security import get_current_active_user
from ...schemas.base import DataResponse
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=DataResponse[Dict[str, Any]])
async def get_about_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取关于页面基本信息
    """
    about_info = {
        "title": "关于我们",
        "description": "AI舞蹈教练系统致力于通过人工智能技术为舞蹈爱好者提供专业的指导和训练方案。",
        "version": "1.0.0",
        "features": [
            "AI舞蹈动作分析",
            "个性化训练处方",
            "健康管理",
            "社交互动平台",
            "在线课程学习"
        ]
    }
    return DataResponse(data=about_info, message="获取关于信息成功")

@router.get("/team", response_model=DataResponse[List[Dict[str, Any]]])
async def get_team_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取团队成员信息
    """
    team_members = [
        {
            "id": 1,
            "name": "张明",
            "position": "创始人 & CEO",
            "description": "资深舞蹈教练，15年教学经验",
            "expertise": ["古典舞", "芭蕾舞", "现代舞"],
            "avatar": "/images/team/zhang-ming.jpg"
        },
        {
            "id": 2,
            "name": "李雪",
            "position": "技术总监",
            "description": "AI算法专家，专注于计算机视觉",
            "expertise": ["AI算法", "计算机视觉", "深度学习"],
            "avatar": "/images/team/li-xue.jpg"
        },
        {
            "id": 3,
            "name": "王强",
            "position": "产品设计",
            "description": "用户体验设计师，专注于健康科技",
            "expertise": ["UI/UX设计", "用户研究", "产品设计"],
            "avatar": "/images/team/wang-qiang.jpg"
        }
    ]
    
    return DataResponse(data=team_members, message="获取团队成员信息成功")

@router.get("/partners", response_model=DataResponse[List[Dict[str, Any]]])
async def get_partners_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取合作伙伴信息
    """
    partners = [
        {
            "id": 1,
            "name": "中国舞蹈家协会",
            "type": "行业协会",
            "description": "中国舞蹈领域的权威组织",
            "logo": "/images/partners/dance-association.jpg",
            "website": "https://www.dance.org.cn"
        },
        {
            "id": 2,
            "name": "健康科技研究院",
            "type": "科研机构",
            "description": "专注于健康科技研发",
            "logo": "/images/partners/health-research.jpg",
            "website": "https://health-tech.org"
        },
        {
            "id": 3,
            "name": "体育舞蹈培训中心",
            "type": "培训机构",
            "description": "专业舞蹈培训服务",
            "logo": "/images/partners/dance-center.jpg",
            "website": "https://dance-center.com"
        }
    ]
    
    return DataResponse(data=partners, message="获取合作伙伴信息成功")

@router.get("/awards", response_model=DataResponse[List[Dict[str, Any]]])
async def get_awards_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取获奖信息
    """
    awards = [
        {
            "id": 1,
            "year": 2023,
            "title": "最佳创新应用奖",
            "organization": "科技创新大赛",
            "description": "凭借AI舞蹈分析技术获得创新应用奖"
        },
        {
            "id": 2,
            "year": 2022,
            "title": "优秀用户体验奖",
            "organization": "设计大赛",
            "description": "在健康科技类别获得用户体验优秀奖"
        },
        {
            "id": 3,
            "year": 2021,
            "title": "最佳健康科技产品",
            "organization": "健康产业峰会",
            "description": "被评为年度最佳健康科技产品"
        }
    ]
    
    return DataResponse(data=awards, message="获取获奖信息成功")

@router.get("/milestones", response_model=DataResponse[List[Dict[str, Any]]])
async def get_milestones_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取发展里程碑
    """
    milestones = [
        {
            "id": 1,
            "date": "2024-01",
            "title": "正式发布1.0版本",
            "description": "AI舞蹈教练系统正式上线",
            "importance": "major"
        },
        {
            "id": 2,
            "date": "2023-08",
            "title": "获得天使轮融资",
            "description": "完成1000万元天使轮融资",
            "importance": "major"
        },
        {
            "id": 3,
            "date": "2023-06",
            "title": "与舞蹈协会达成合作",
            "description": "与中国舞蹈家协会达成战略合作",
            "importance": "medium"
        },
        {
            "id": 4,
            "date": "2023-03",
            "title": "技术团队组建完成",
            "description": "组建了15人的核心研发团队",
            "importance": "medium"
        },
        {
            "id": 5,
            "date": "2023-01",
            "title": "项目启动",
            "description": "AI舞蹈教练项目正式启动",
            "importance": "high"
        }
    ]
    
    return DataResponse(data=milestones, message="获取发展里程碑信息成功")

@router.post("/contact", response_model=DataResponse)
async def submit_contact_form(
    contact_data: Dict[str, Any],
    db: AsyncSession = Depends(get_async_db)
):
    """
    提交联系表单
    """
    # 这里需要实现联系表单的存储逻辑
    # 例如保存到数据库或发送邮件
    
    required_fields = ["name", "email", "subject", "message"]
    for field in required_fields:
        if field not in contact_data:
            raise HTTPException(status_code=400, detail=f"缺少必填字段: {field}")
    
    # 验证邮箱格式
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, contact_data["email"]):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")
    
    # 这里可以添加实际的存储或邮件发送逻辑
    # 暂时返回成功响应
    return DataResponse(message="联系表单提交成功，我们会尽快与您联系")