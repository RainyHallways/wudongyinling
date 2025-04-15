from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, courses, health, prescriptions, challenges

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["认证"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["用户管理"])
app.include_router(courses.router, prefix=f"{settings.API_V1_STR}/courses", tags=["舞蹈课程"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["健康记录"])
app.include_router(prescriptions.router, prefix=f"{settings.API_V1_STR}/prescriptions", tags=["运动处方"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["打卡挑战"])

@app.get("/")
async def root():
    return {"message": "欢迎使用AI舞蹈教练系统API"}