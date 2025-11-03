"""
데이터베이스 초기화 스크립트
"""
import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import init_db, engine, Base
from app.core.config import settings
from app.models import Menu, MenuOption, Order, OrderItem, OrderItemOption


async def create_database():
    """데이터베이스 생성"""
    print("="*60)
    print("OrderBean 데이터베이스 초기화")
    print("="*60)
    print()
    
    print(f"📊 데이터베이스 정보:")
    print(f"   - Host: {settings.DB_HOST}")
    print(f"   - Port: {settings.DB_PORT}")
    print(f"   - Database: {settings.DB_NAME}")
    print(f"   - User: {settings.DB_USER}")
    print(f"   - URL: {settings.database_url}")
    print()
    
    try:
        print("🔄 데이터베이스 연결 테스트 중...")
        
        # 연결 테스트
        async with engine.connect() as conn:
            print("✅ 데이터베이스 연결 성공!")
        
        print()
        print("🔄 테이블 생성 중...")
        
        # 테이블 생성
        await init_db()
        
        print("✅ 다음 테이블이 생성되었습니다:")
        print("   - menus (메뉴)")
        print("   - menu_options (메뉴 옵션)")
        print("   - orders (주문)")
        print("   - order_items (주문 항목)")
        print("   - order_item_options (주문 항목 옵션)")
        print()
        
        print("="*60)
        print("✅ 데이터베이스 초기화 완료!")
        print("="*60)
        print()
        print("다음 단계:")
        print("  1. 샘플 데이터 입력: python seed_db.py")
        print("  2. 서버 시작: python -m uvicorn app.main:app --reload")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("="*60)
        print("❌ 오류 발생!")
        print("="*60)
        print(f"오류 메시지: {e}")
        print()
        print("해결 방법:")
        print("  1. PostgreSQL이 실행 중인지 확인하세요")
        print("  2. .env 파일의 데이터베이스 설정을 확인하세요")
        print("  3. 데이터베이스가 존재하는지 확인하세요:")
        print(f"     psql -U {settings.DB_USER} -c \"CREATE DATABASE {settings.DB_NAME};\"")
        print()
        
        return False
    
    finally:
        await engine.dispose()


async def drop_tables():
    """모든 테이블 삭제 (주의!)"""
    print("="*60)
    print("⚠️  경고: 모든 테이블을 삭제합니다!")
    print("="*60)
    print()
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        
        print("✅ 모든 테이블이 삭제되었습니다.")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    finally:
        await engine.dispose()


async def reset_database():
    """데이터베이스 초기화 (삭제 + 생성)"""
    print("="*60)
    print("데이터베이스 초기화 (리셋)")
    print("="*60)
    print()
    
    # 테이블 삭제
    await drop_tables()
    print()
    
    # 테이블 생성
    await create_database()


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "reset":
            asyncio.run(reset_database())
        elif command == "drop":
            asyncio.run(drop_tables())
        else:
            print(f"알 수 없는 명령: {command}")
            print("사용법:")
            print("  python init_db.py        - 테이블 생성")
            print("  python init_db.py reset  - 데이터베이스 초기화 (삭제 + 생성)")
            print("  python init_db.py drop   - 모든 테이블 삭제")
    else:
        asyncio.run(create_database())


if __name__ == "__main__":
    main()

