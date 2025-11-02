"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="OrderBean API",
    description="커피 주문 관리 시스템 백엔드 API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 개발 서버
        "http://localhost:3000",  # 대체 포트
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """루트 엔드포인트 - API 상태 확인"""
    return {
        "message": "OrderBean API Server",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/test")
async def test_endpoint():
    """테스트 엔드포인트"""
    return {
        "success": True,
        "message": "FastAPI 서버가 정상적으로 작동 중입니다!",
        "data": {
            "framework": "FastAPI",
            "python": "3.11+",
            "features": ["비동기 처리", "자동 API 문서", "타입 검증"],
        },
    }

