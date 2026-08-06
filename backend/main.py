import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers import convert

app = FastAPI(
    title="BizTalk Antigravity API",
    description="업무 말투 변환기 API 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 필요하면 허용할 Origin 제안
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check 엔드포인트
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}

# API 라우터 등록
app.include_router(convert.router, prefix="/api", tags=["Conversion"])

# 프론트엔드 정적 파일 서빙 설정
# main.py 위치를 기준으로 루트 아래의 frontend 폴더 참조
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"[Warning] Frontend directory not found at: {FRONTEND_DIR}")
