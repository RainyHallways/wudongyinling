#!/usr/bin/env python3
"""
数据库重置脚本
重新创建数据库并添加初始数据
"""

import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, Base, engine
from app.models import *
from app.core.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_tables():
    """创建所有数据表"""
    logger.info("开始创建数据表...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据表创建完成")

async def create_sample_users(db: AsyncSession):
    """创建示例用户"""
    logger.info("创建示例用户...")
    
    users_data = [
        {
            "username": "zhang_yumei",
            "email": "zhang.yumei@example.com",
            "password": hash_password("password123"),
            "nickname": "张玉梅",
            "is_active": True,
            "role": "ELDERLY",
            "unique_id": "E000001"
        },
        {
            "username": "wang_defu", 
            "email": "wang.defu@example.com",
            "password": hash_password("password123"),
            "nickname": "王德福",
            "is_active": True,
            "role": "ELDERLY",
            "unique_id": "E000002"
        },
        {
            "username": "chen_shufen",
            "email": "chen.shufen@example.com", 
            "password": hash_password("password123"),
            "nickname": "陈淑芬",
            "is_active": True,
            "role": "ELDERLY",
            "unique_id": "E000003"
        },
        {
            "username": "li_minghua",
            "email": "li.minghua@example.com",
            "password": hash_password("password123"),
            "nickname": "李明华",
            "is_active": True,
            "role": "TEACHER",
            "unique_id": "T000001"
        },
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": hash_password("admin123"),
            "nickname": "管理员",
            "is_active": True,
            "role": "ADMIN",
            "unique_id": "A000001"
        }
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
    
    await db.commit()
    logger.info(f"创建了 {len(users_data)} 个示例用户")

async def create_sample_posts(db: AsyncSession):
    """创建示例动态"""
    logger.info("创建示例动态...")
    
    # 获取用户
    users = await db.execute(select(User))
    users = users.scalars().all()
    user_dict = {user.username: user for user in users}
    
    posts_data = [
        {
            "user_id": user_dict["zhang_yumei"].id,
            "title": "今日广场舞练习",
            "content": "今天学习了新的广场舞动作，虽然还不熟练，但很开心！坚持打卡第15天~",
            "post_type": "dance",
            "media_url": "/images/zym-2.png",
            "likes_count": 24,
            "comments_count": 8,
            "shares_count": 2,
            "is_public": True,
            "is_featured": True,
            "created_at": datetime.now() - timedelta(hours=1)
        },
        {
            "user_id": user_dict["chen_shufen"].id,
            "title": "民族舞表演分享",
            "content": "参加了社区的民族舞表演，虽然紧张但顺利完成，感谢平台的教学视频！",
            "post_type": "dance",
            "media_url": "/images/csf-2.png",
            "likes_count": 36,
            "comments_count": 12,
            "shares_count": 5,
            "is_public": True,
            "is_featured": False,
            "created_at": datetime.now() - timedelta(hours=2)
        },
        {
            "user_id": user_dict["wang_defu"].id,
            "title": "健康锻炼心得",
            "content": "跟着平台学舞蹈三个月了，感觉身体越来越好，血压也稳定了。推荐给所有的老年朋友！",
            "post_type": "text",
            "likes_count": 45,
            "comments_count": 15,
            "shares_count": 8,
            "is_public": True,
            "is_featured": True,
            "created_at": datetime.now() - timedelta(hours=4)
        },
        {
            "user_id": user_dict["li_minghua"].id,
            "title": "太极拳教学分享",
            "content": "分享一套适合初学者的太极拳动作，动作缓慢，适合老年人练习。大家可以跟着视频一起学习。",
            "post_type": "video",
            "media_url": "/images/taiji-demo.mp4",
            "likes_count": 68,
            "comments_count": 20,
            "shares_count": 12,
            "is_public": True,
            "is_featured": True,
            "created_at": datetime.now() - timedelta(hours=6)
        }
    ]
    
    for post_data in posts_data:
        post = Post(**post_data)
        db.add(post)
    
    await db.commit()
    logger.info(f"创建了 {len(posts_data)} 条示例动态")

async def create_sample_heritage_data(db: AsyncSession):
    """创建示例非遗数据"""
    logger.info("创建示例非遗数据...")
    
    # 创建非遗项目
    projects_data = [
        {
            "name": "蒙古族安代舞",
            "category": "传统舞蹈",
            "level": "national",
            "description": "安代舞是蒙古族传统舞蹈，具有浓郁的民族特色",
            "history": "安代舞起源于明末清初，已有400多年历史",
            "techniques": "以踏步、摆臂、转身等动作为主，节奏明快",
            "current_status": "传承良好，在内蒙古地区广泛流传",
            "protection_measures": "建立传承基地，培养传承人",
            "image_url": "/images/安代舞图片.png",
            "status": "active"
        },
        {
            "name": "藏族锅庄舞",
            "category": "传统舞蹈", 
            "level": "national",
            "description": "锅庄舞是藏族传统集体舞蹈，寓意团结和谐",
            "history": "起源于古代祭祀活动，历史悠久",
            "techniques": "围圈而舞，手拉手，动作整齐划一",
            "current_status": "在藏区广泛传承，深受群众喜爱",
            "protection_measures": "录制教学视频，建立数字档案",
            "image_url": "/images/藏族锅庄舞图片.png",
            "status": "active"
        },
        {
            "name": "傣族孔雀舞",
            "category": "传统舞蹈",
            "level": "national", 
            "description": "孔雀舞是傣族具有代表性的传统舞蹈",
            "history": "模仿孔雀的优美姿态，表达对美好生活的向往",
            "techniques": "手臂动作柔美，模仿孔雀开屏、觅食等动作",
            "current_status": "传承活跃，有专业传承人",
            "protection_measures": "设立传承点，开展教学活动",
            "image_url": "/images/傣族孔雀舞图片.png",
            "status": "active"
        }
    ]
    
    for project_data in projects_data:
        project = HeritageProject(**project_data)
        db.add(project)
    
    # 创建非遗传承人
    inheritors_data = [
        {
            "name": "格日勒图",
            "gender": "male",
            "birth_year": 1955,
            "hometown": "内蒙古呼和浩特",
            "bio": "蒙古族安代舞国家级传承人，从事安代舞表演和教学40余年",
            "achievements": "获得国家级非遗传承人称号，培养学生200余人",
            "inheritance_years": 40,
            "teaching_experience": "在多所学校和社区开展安代舞教学",
            "representative_works": "《草原安代》、《欢乐安代》等经典作品",
            "contact_info": "电话：138****1234",
            "avatar_url": "/images/非遗传承人1.png",
            "status": "active"
        },
        {
            "name": "央金卓玛",
            "gender": "female", 
            "birth_year": 1960,
            "hometown": "西藏拉萨",
            "bio": "藏族锅庄舞省级传承人，致力于锅庄舞的传承和推广",
            "achievements": "省级非遗传承人，多次参加国际文化交流",
            "inheritance_years": 35,
            "teaching_experience": "在西藏多地开展锅庄舞培训",
            "representative_works": "《雪域锅庄》、《高原之舞》",
            "contact_info": "电话：139****5678",
            "avatar_url": "/images/非遗传承人2.png",
            "status": "active"
        }
    ]
    
    for inheritor_data in inheritors_data:
        inheritor = HeritageInheritor(**inheritor_data)
        db.add(inheritor)
    
    await db.commit()
    logger.info(f"创建了 {len(projects_data)} 个非遗项目和 {len(inheritors_data)} 个传承人")

async def create_sample_challenges(db: AsyncSession):
    """创建示例挑战"""
    logger.info("创建示例挑战...")
    
    challenges_data = [
        {
            "title": "30天广场舞打卡挑战",
            "description": "连续30天每天练习广场舞15分钟，养成运动好习惯",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=30),
            "target_days": 30,
            "reward_points": 300,
            "status": "active",
            "max_participants": 1000
        },
        {
            "title": "太极拳基础动作学习",
            "description": "21天学会太极拳24式基础动作",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=21),
            "target_days": 21,
            "reward_points": 210,
            "status": "active",
            "max_participants": 500
        }
    ]
    
    for challenge_data in challenges_data:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
    
    await db.commit()
    logger.info(f"创建了 {len(challenges_data)} 个示例挑战")

async def create_sample_courses(db: AsyncSession):
    """创建示例课程"""
    logger.info("创建示例课程...")
    
    # 获取教师用户
    teacher = await db.execute(select(User).where(User.role == "TEACHER"))
    teacher = teacher.scalar_first()
    
    if not teacher:
        logger.warning("没有找到教师用户，跳过课程创建")
        return
    
    courses_data = [
        {
            "title": "广场舞基础入门",
            "description": "适合初学者的广场舞课程，从基础动作开始学习",
            "instructor_id": teacher.id,
            "category": "广场舞",
            "difficulty": "初级",
            "duration": 720,  # 12分钟
            "price": 0.00,
            "is_featured": True,
            "cover_image": "/images/gcw.jpeg",
            "video_url": "/videos/guangchangwu-basic.mp4"
        },
        {
            "title": "民族舞精选",
            "description": "学习多种民族舞蹈的经典动作和文化内涵",
            "instructor_id": teacher.id,
            "category": "民族舞",
            "difficulty": "中级",
            "duration": 960,  # 16分钟
            "price": 29.90,
            "is_featured": True,
            "cover_image": "/images/mzw.jpg",
            "video_url": "/videos/minzuwu-collection.mp4"
        },
        {
            "title": "太极拳24式",
            "description": "传统太极拳24式完整教学，适合养生保健",
            "instructor_id": teacher.id,
            "category": "太极拳",
            "difficulty": "初级",
            "duration": 1800,  # 30分钟
            "price": 19.90,
            "is_featured": False,
            "cover_image": "/images/taiji.png",
            "video_url": "/videos/taiji-24.mp4"
        }
    ]
    
    for course_data in courses_data:
        course = Course(**course_data)
        db.add(course)
    
    await db.commit()
    logger.info(f"创建了 {len(courses_data)} 个示例课程")

async def main():
    """主函数"""
    try:
        logger.info("开始重置数据库...")
        
        # 创建数据表
        await create_tables()
        
        # 创建数据库会话
        async with AsyncSessionLocal() as db:
            # 导入必要的查询函数
            from sqlalchemy import select
            
            # 创建示例数据
            await create_sample_users(db)
            await create_sample_posts(db)
            await create_sample_heritage_data(db)
            await create_sample_challenges(db)
            await create_sample_courses(db)
        
        logger.info("数据库重置完成！")
        logger.info("默认用户账号：")
        logger.info("- 管理员: admin / admin123")
        logger.info("- 老人用户: zhang_yumei / password123")
        logger.info("- 教师用户: li_minghua / password123")
        
    except Exception as e:
        logger.error(f"数据库重置失败: {e}")
        raise

if __name__ == "__main__":
    # 在WSL环境中运行
    asyncio.run(main()) 