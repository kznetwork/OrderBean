"""
FastAPI Main Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import init_db, close_db, get_db, engine
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행"""
    # 시작 시
    print("🚀 OrderBean API 서버 시작 중...")
    print(f"📊 데이터베이스: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # 데이터베이스 연결 테스트
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ 데이터베이스 연결 성공!")
    except Exception as e:
        print(f"⚠️  데이터베이스 연결 실패: {e}")
        print("   서버는 실행되지만 데이터베이스 기능은 사용할 수 없습니다.")
    
    yield
    
    # 종료 시
    print("🛑 OrderBean API 서버 종료 중...")
    await close_db()
    print("✅ 데이터베이스 연결 종료 완료")


app = FastAPI(
    title=settings.APP_NAME,
    description="커피 주문 관리 시스템 백엔드 API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router)


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
async def health_check(db: AsyncSession = Depends(get_db)):
    """헬스 체크 엔드포인트 (데이터베이스 연결 포함)"""
    db_status = "disconnected"
    
    try:
        # 데이터베이스 연결 확인
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/test")
async def test_endpoint(db: AsyncSession = Depends(get_db)):
    """테스트 엔드포인트 (데이터베이스 포함)"""
    
    # 데이터베이스에서 메뉴 개수 조회
    try:
        result = await db.execute(text("SELECT COUNT(*) FROM menus"))
        menu_count = result.scalar()
    except Exception:
        menu_count = "N/A (테이블이 없거나 연결 오류)"
    
    return {
        "success": True,
        "message": "FastAPI 서버가 정상적으로 작동 중입니다!",
        "data": {
            "framework": "FastAPI",
            "python": "3.11+",
            "features": ["비동기 처리", "자동 API 문서", "타입 검증"],
            "database": {
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "database": settings.DB_NAME,
                "menu_count": menu_count,
            },
        },
    }


@app.get("/api/v1/db-test")
async def database_test(db: AsyncSession = Depends(get_db)):
    """데이터베이스 연결 테스트 전용 엔드포인트"""
    try:
        # PostgreSQL 버전 확인
        result = await db.execute(text("SELECT version()"))
        version = result.scalar()
        
        # 현재 데이터베이스 확인
        result = await db.execute(text("SELECT current_database()"))
        current_db = result.scalar()
        
        # 테이블 목록 확인
        result = await db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        
        # 메뉴 개수 확인
        if "menus" in tables:
            result = await db.execute(text("SELECT COUNT(*) FROM menus"))
            menu_count = result.scalar()
        else:
            menu_count = 0
        
        return {
            "success": True,
            "message": "데이터베이스 연결 성공!",
            "database": {
                "version": version.split(",")[0],
                "current_database": current_db,
                "tables": tables,
                "menu_count": menu_count,
            },
        }
    except Exception as e:
        return {
            "success": False,
            "message": "데이터베이스 연결 실패",
            "error": str(e),
        }

