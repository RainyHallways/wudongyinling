from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import json
import os
from datetime import datetime

from ..core.config import settings
from ..core import ai as ai_core
from .health_service import HealthService
from .prescription_service import PrescriptionService
from ..schemas.prescription import PrescriptionCreate, PrescriptionExerciseCreate
from ..repositories import health_repository, prescription_repository

class AIService:
    """
    AI服务，处理AI相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化AI服务
        """
        self.health_service = HealthService()
        self.prescription_service = PrescriptionService()
        
    async def analyze_health_data(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        分析用户健康数据
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            days: 分析天数
            
        Returns:
            分析结果
        """
        # 获取用户健康数据
        health_records = await health_repository.get_by_user_id(db, user_id=user_id)
        if not health_records:
            return {
                "status": "error",
                "message": "没有健康记录数据",
                "data": None
            }
        
        # 获取健康统计数据
        health_stats = await health_repository.get_statistics(db, user_id=user_id, days=days)
        
        # 使用健康服务分析趋势
        trend_analysis = self.health_service.analyze_health_trend(health_records)
        
        # 构建分析结果
        analysis_result = {
            "status": "success",
            "message": "健康数据分析完成",
            "data": {
                "statistics": health_stats,
                "trends": trend_analysis,
                "recommendations": await self._generate_health_recommendations(trend_analysis)
            }
        }
        
        return analysis_result
    
    async def _generate_health_recommendations(
        self, 
        trend_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        根据健康趋势生成建议
        
        Args:
            trend_analysis: 健康趋势分析结果
            
        Returns:
            建议列表
        """
        recommendations = []
        
        # 体重趋势建议
        weight_trend = trend_analysis.get("weight_trend")
        if weight_trend:
            if weight_trend["trend"] == "increasing" and weight_trend["change_percent"] > 5:
                recommendations.append({
                    "type": "weight",
                    "level": "warning",
                    "content": "您的体重在过去一段时间增长较快，建议控制饮食并增加运动量。"
                })
            elif weight_trend["trend"] == "decreasing" and weight_trend["change_percent"] < -5:
                recommendations.append({
                    "type": "weight",
                    "level": "info",
                    "content": "您的体重在下降，如果是有意减重，请确保健康减重，保持足够的营养摄入。"
                })
        
        # BMI趋势建议
        bmi_trend = trend_analysis.get("bmi_trend")
        if bmi_trend and bmi_trend.get("last_value"):
            bmi = bmi_trend["last_value"]
            if bmi < 18.5:
                recommendations.append({
                    "type": "bmi",
                    "level": "warning",
                    "content": "您的BMI值偏低，可能处于体重不足状态，建议适当增加营养摄入。"
                })
            elif 18.5 <= bmi < 24:
                recommendations.append({
                    "type": "bmi",
                    "level": "success",
                    "content": "您的BMI值在正常范围内，请继续保持健康的生活方式。"
                })
            elif 24 <= bmi < 28:
                recommendations.append({
                    "type": "bmi",
                    "level": "warning",
                    "content": "您的BMI值处于超重范围，建议适当控制饮食并增加运动量。"
                })
            elif bmi >= 28:
                recommendations.append({
                    "type": "bmi",
                    "level": "danger",
                    "content": "您的BMI值处于肥胖范围，建议咨询专业医生或营养师制定减重计划。"
                })
        
        # 心率趋势建议
        heart_rate_trend = trend_analysis.get("heart_rate_trend")
        if heart_rate_trend and heart_rate_trend.get("last_value"):
            heart_rate = heart_rate_trend["last_value"]
            if heart_rate < 60:
                recommendations.append({
                    "type": "heart_rate",
                    "level": "info",
                    "content": "您的静息心率较低，如果没有不适感，可能表明您的心肺功能良好。"
                })
            elif 60 <= heart_rate <= 100:
                recommendations.append({
                    "type": "heart_rate",
                    "level": "success",
                    "content": "您的心率在正常范围内，继续保持健康的生活习惯。"
                })
            elif heart_rate > 100:
                recommendations.append({
                    "type": "heart_rate",
                    "level": "warning",
                    "content": "您的静息心率偏高，建议注意休息，避免咖啡因等刺激性物质，必要时咨询医生。"
                })
        
        # 血糖趋势建议
        blood_sugar_trend = trend_analysis.get("blood_sugar_trend")
        if blood_sugar_trend and blood_sugar_trend.get("last_value"):
            blood_sugar = blood_sugar_trend["last_value"]
            if blood_sugar < 3.9:
                recommendations.append({
                    "type": "blood_sugar",
                    "level": "warning",
                    "content": "您的血糖水平偏低，请及时补充碳水化合物，必要时咨询医生。"
                })
            elif 3.9 <= blood_sugar <= 6.1:
                recommendations.append({
                    "type": "blood_sugar",
                    "level": "success",
                    "content": "您的空腹血糖水平在正常范围内，继续保持健康的生活习惯。"
                })
            elif blood_sugar > 6.1:
                recommendations.append({
                    "type": "blood_sugar",
                    "level": "warning",
                    "content": "您的血糖水平偏高，建议控制碳水化合物摄入，增加运动，必要时咨询医生。"
                })
        
        # 如果没有具体建议，添加一条通用建议
        if not recommendations:
            recommendations.append({
                "type": "general",
                "level": "info",
                "content": "建议保持规律的运动习惯，均衡饮食，充足睡眠，定期进行健康检查。"
            })
            
        return recommendations
    
    async def generate_prescription(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        disease_type: str
    ) -> Dict[str, Any]:
        """
        生成健身处方
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            disease_type: 疾病类型
            
        Returns:
            生成结果
        """
        try:
            # 获取最新的健康记录
            latest_record = await health_repository.get_latest_record(db, user_id=user_id)
            
            # 获取处方模板
            schedule_template = self.prescription_service.generate_schedule_template(disease_type)
            
            # 根据模板生成训练计划
            exercises = await self._generate_exercises_for_disease(disease_type)
            
            # 创建处方
            start_date = datetime.now()
            end_date = start_date.replace(month=start_date.month + 1)  # 默认一个月的处方
            
            prescription_data = {
                "user_id": user_id,
                "disease_type": disease_type,
                "training_plan": f"针对{disease_type}的康复训练计划",
                "schedule": schedule_template,
                "start_date": start_date,
                "end_date": end_date,
                "status": "active",
                "comments": f"根据您的健康数据自动生成的处方，针对{disease_type}定制。",
                "exercises": exercises
            }
            
            # 创建处方
            prescription = await prescription_repository.create_with_exercises(
                db, 
                obj_in=PrescriptionCreate(**prescription_data)
            )
            
            return {
                "status": "success",
                "message": "处方生成成功",
                "data": {
                    "prescription_id": prescription.id,
                    "disease_type": disease_type,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"处方生成失败: {str(e)}",
                "data": None
            }
    
    async def _generate_exercises_for_disease(
        self, 
        disease_type: str
    ) -> List[Dict[str, Any]]:
        """
        根据疾病类型生成训练项目
        
        Args:
            disease_type: 疾病类型
            
        Returns:
            训练项目列表
        """
        # 针对不同的疾病类型生成不同的训练项目
        exercise_templates = {
            "腰椎间盘突出": [
                {
                    "name": "腰椎牵引",
                    "description": "帮助减轻腰椎间盘压力，缓解神经根刺激症状",
                    "duration": 15,
                    "frequency": "每日一次",
                    "sets": None,
                    "reps": None
                },
                {
                    "name": "核心肌群训练",
                    "description": "增强腰部和腹部肌肉，提供脊柱支持",
                    "duration": 10,
                    "frequency": "每日两次",
                    "sets": 3,
                    "reps": 10
                },
                {
                    "name": "腰部伸展运动",
                    "description": "缓解腰部紧张，增加脊柱灵活性",
                    "duration": 10,
                    "frequency": "每日两次",
                    "sets": 2,
                    "reps": 5
                }
            ],
            "膝关节炎": [
                {
                    "name": "水中行走",
                    "description": "减轻关节负担的有氧运动，同时锻炼肌肉力量",
                    "duration": 20,
                    "frequency": "每周三次",
                    "sets": None,
                    "reps": None
                },
                {
                    "name": "直腿抬高",
                    "description": "增强股四头肌力量，稳定膝关节",
                    "duration": 10,
                    "frequency": "每日一次",
                    "sets": 3,
                    "reps": 10
                },
                {
                    "name": "膝关节活动度训练",
                    "description": "增加膝关节活动范围，预防僵硬",
                    "duration": 10,
                    "frequency": "每日两次",
                    "sets": 2,
                    "reps": 15
                }
            ],
            "肩周炎": [
                {
                    "name": "肩部摆动运动",
                    "description": "增加肩关节活动度，缓解肩部紧张",
                    "duration": 10,
                    "frequency": "每日三次",
                    "sets": 3,
                    "reps": 10
                },
                {
                    "name": "肩胛骨稳定训练",
                    "description": "增强肩胛骨周围肌肉力量，改善姿势",
                    "duration": 15,
                    "frequency": "每日两次",
                    "sets": 2,
                    "reps": 12
                },
                {
                    "name": "肩部拉伸",
                    "description": "缓解肌肉紧张，增加关节活动度",
                    "duration": 10,
                    "frequency": "每日两次",
                    "sets": 2,
                    "reps": 5
                }
            ]
        }
        
        # 获取疾病对应的训练项目，如果没有则使用通用训练项目
        exercises_data = exercise_templates.get(disease_type, [
            {
                "name": "有氧训练",
                "description": "提高心肺功能，增强整体耐力",
                "duration": 30,
                "frequency": "每周三次",
                "sets": None,
                "reps": None
            },
            {
                "name": "肌肉力量训练",
                "description": "增强肌肉力量，提高日常活动能力",
                "duration": 20,
                "frequency": "每周两次",
                "sets": 3,
                "reps": 12
            },
            {
                "name": "平衡训练",
                "description": "改善身体平衡能力，预防跌倒",
                "duration": 15,
                "frequency": "每周两次",
                "sets": 2,
                "reps": 10
            }
        ])
        
        # 转换为PrescriptionExerciseCreate对象
        exercises = [PrescriptionExerciseCreate(**data) for data in exercises_data]
        
        return exercises
    
    async def get_ai_coach_advice(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        question: str
    ) -> Dict[str, Any]:
        """
        获取AI教练建议
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            question: 用户问题
            
        Returns:
            AI建议
        """
        try:
            # 获取用户健康数据和处方信息
            health_records = await health_repository.get_by_user_id(
                db, 
                user_id=user_id,
                skip=0,
                limit=10
            )
            
            prescriptions = await prescription_repository.get_by_user_id(
                db,
                user_id=user_id,
                skip=0,
                limit=5
            )
            
            # 准备用户背景信息
            user_context = {
                "has_health_records": len(health_records) > 0,
                "latest_health": health_records[0].model_dump() if health_records else None,
                "has_prescription": len(prescriptions) > 0,
                "latest_prescription": {
                    "id": prescriptions[0].id,
                    "disease_type": prescriptions[0].disease_type,
                    "training_plan": prescriptions[0].training_plan
                } if prescriptions else None
            }
            
            # 使用AI核心模块生成回答
            response = await ai_core.get_coach_response(question, user_context)
            
            return {
                "status": "success",
                "message": "AI回答生成成功",
                "data": {
                    "question": question,
                    "answer": response["answer"],
                    "references": response.get("references", []),
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"AI回答生成失败: {str(e)}",
                "data": {
                    "question": question,
                    "answer": "抱歉，我现在无法回答您的问题。请稍后再试或联系客服。",
                    "generated_at": datetime.now().isoformat()
                }
            } 