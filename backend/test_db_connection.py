"""
데이터베이스 연결 테스트 스크립트
"""
import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import engine, AsyncSessionLocal
from app.core.config import settings
from app.models import Menu, MenuOption, Order


async def test_connection():
    """데이터베이스 연결 테스트"""
    print("\n" + "="*60)
    print("OrderBean 데이터베이스 연결 테스트")
    print("="*60)
    print()
    
    # 설정 정보 출력
    print("📊 데이터베이스 설정:")
    print(f"   Host: {settings.DB_HOST}")
    print(f"   Port: {settings.DB_PORT}")
    print(f"   Database: {settings.DB_NAME}")
    print(f"   User: {settings.DB_USER}")
    print(f"   URL: {settings.database_url}")
    print()
    
    tests_passed = 0
    tests_total = 5
    
    try:
        # 테스트 1: 기본 연결
        print("🔍 테스트 1/5: 데이터베이스 연결...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("   ✅ 연결 성공!")
        tests_passed += 1
        
        # 테스트 2: PostgreSQL 버전 확인
        print("\n🔍 테스트 2/5: PostgreSQL 버전 확인...")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"   ✅ {version.split(',')[0]}")
        tests_passed += 1
        
        # 테스트 3: 데이터베이스 존재 확인
        print("\n🔍 테스트 3/5: 데이터베이스 존재 확인...")
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT current_database()")
            )
            db_name = result.scalar()
            print(f"   ✅ 현재 데이터베이스: {db_name}")
            assert db_name == settings.DB_NAME
        tests_passed += 1
        
        # 테스트 4: 테이블 존재 확인
        print("\n🔍 테스트 4/5: 테이블 존재 확인...")
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
            )
            tables = [row[0] for row in result]
            
            if tables:
                print("   ✅ 발견된 테이블:")
                for table in tables:
                    print(f"      - {table}")
            else:
                print("   ⚠️  테이블이 없습니다. init_db.py를 실행하세요.")
        tests_passed += 1
        
        # 테스트 5: 세션 테스트
        print("\n🔍 테스트 5/5: 세션 및 쿼리 테스트...")
        async with AsyncSessionLocal() as session:
            # 메뉴 개수 확인
            result = await session.execute(text("SELECT COUNT(*) FROM menus"))
            menu_count = result.scalar()
            print(f"   ✅ 메뉴 개수: {menu_count}")
            
            # 옵션 개수 확인
            result = await session.execute(text("SELECT COUNT(*) FROM menu_options"))
            option_count = result.scalar()
            print(f"   ✅ 옵션 개수: {option_count}")
            
            # 주문 개수 확인
            result = await session.execute(text("SELECT COUNT(*) FROM orders"))
            order_count = result.scalar()
            print(f"   ✅ 주문 개수: {order_count}")
            
            if menu_count == 0:
                print("\n   💡 팁: 샘플 데이터를 생성하려면 'python seed_db.py'를 실행하세요.")
        tests_passed += 1
        
        # 결과 요약
        print("\n" + "="*60)
        print("테스트 결과")
        print("="*60)
        print(f"통과: {tests_passed}/{tests_total}")
        
        if tests_passed == tests_total:
            print("\n✅ 모든 테스트 통과! 데이터베이스가 정상적으로 작동합니다.")
            print("\n다음 단계:")
            print("  1. 샘플 데이터 생성: python seed_db.py")
            print("  2. 서버 시작: python -m uvicorn app.main:app --reload")
        else:
            print("\n⚠️  일부 테스트 실패. 위의 오류를 확인하세요.")
        
        print("="*60 + "\n")
        
        return tests_passed == tests_total
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ 오류 발생!")
        print("="*60)
        print(f"오류 메시지: {e}")
        print()
        print("해결 방법:")
        print("  1. PostgreSQL이 실행 중인지 확인:")
        print("     - Windows: 서비스에서 PostgreSQL 확인")
        print("     - 명령어: pg_ctl status")
        print()
        print("  2. .env 파일의 데이터베이스 설정 확인:")
        print(f"     - DB_HOST={settings.DB_HOST}")
        print(f"     - DB_PORT={settings.DB_PORT}")
        print(f"     - DB_NAME={settings.DB_NAME}")
        print(f"     - DB_USER={settings.DB_USER}")
        print(f"     - DB_PASSWORD=******")
        print()
        print("  3. 데이터베이스가 존재하는지 확인:")
        print(f"     psql -U {settings.DB_USER} -c \"CREATE DATABASE {settings.DB_NAME};\"")
        print()
        print("  4. 테이블 생성:")
        print("     python init_db.py")
        print()
        print("="*60 + "\n")
        
        return False
    
    finally:
        await engine.dispose()


def main():
    """메인 함수"""
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
