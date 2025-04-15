import httpx
from typing import Dict, Any
from .config import settings

class AIAnalyzer:
    def __init__(self):
        self.api_url = settings.MINICPM_V_API_URL
        self.api_key = settings.MINICPM_V_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def analyze_dance_video(self, video_data: bytes) -> Dict[str, Any]:
        """分析舞蹈视频并返回评分和建议"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/analyze",
                    headers=self.headers,
                    files={"video": video_data}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"AI分析服务请求失败: {str(e)}")

    async def get_dance_feedback(self, video_url: str) -> Dict[str, Any]:
        """获取舞蹈反馈"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/feedback",
                    headers=self.headers,
                    json={"video_url": video_url}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"获取反馈失败: {str(e)}")

    async def compare_with_standard(self, user_video: bytes, standard_video: bytes) -> Dict[str, Any]:
        """将用户视频与标准动作进行对比"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/compare",
                    headers=self.headers,
                    files={
                        "user_video": user_video,
                        "standard_video": standard_video
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"视频对比失败: {str(e)}")

ai_analyzer = AIAnalyzer() 