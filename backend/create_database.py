"""
PostgreSQL 데이터베이스 생성 스크립트
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

def create_database():
    """orderbean_db 데이터베이스 생성"""
    
    # 환경 변수에서 설정 가져오기
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'orderbean_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgresql')
    
    print("\n" + "="*60)
    print("PostgreSQL 데이터베이스 생성")
    print("="*60)
    print()
    print("📊 데이터베이스 설정:")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print()
    
    try:
        # postgres 데이터베이스에 연결 (기본 데이터베이스)
        print("🔌 PostgreSQL 서버에 연결 중...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database='postgres',  # 기본 postgres DB에 연결
            user=db_user,
            password=db_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("   ✅ 연결 성공!")
        print()
        
        # 데이터베이스 존재 여부 확인
        print(f"🔍 '{db_name}' 데이터베이스 존재 여부 확인...")
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"   ⚠️  '{db_name}' 데이터베이스가 이미 존재합니다.")
            print()
            
            response = input("   기존 데이터베이스를 삭제하고 새로 만들까요? (y/N): ")
            if response.lower() == 'y':
                print(f"\n🗑️  '{db_name}' 데이터베이스 삭제 중...")
                # 활성 연결 종료
                cursor.execute(f"""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{db_name}'
                    AND pid <> pg_backend_pid()
                """)
                # 데이터베이스 삭제
                cursor.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
                print("   ✅ 삭제 완료!")
                
                # 새 데이터베이스 생성
                print(f"\n📦 '{db_name}' 데이터베이스 생성 중...")
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                print("   ✅ 생성 완료!")
            else:
                print("\n   ℹ️  기존 데이터베이스를 사용합니다.")
        else:
            # 데이터베이스 생성
            print(f"📦 '{db_name}' 데이터베이스 생성 중...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print("   ✅ 생성 완료!")
        
        cursor.close()
        conn.close()
        
        print()
        print("="*60)
        print("✅ 데이터베이스 준비 완료!")
        print("="*60)
        print()
        print("다음 단계:")
        print("  1. 테이블 생성: python init_database.py")
        print("  2. 연결 테스트: python test_db_connection.py")
        print("  3. 서버 시작: python -m uvicorn app.main:app --reload")
        print()
        
        return True
        
    except psycopg2.OperationalError as e:
        print("\n" + "="*60)
        print("❌ PostgreSQL 연결 실패!")
        print("="*60)
        print(f"오류: {e}")
        print()
        print("해결 방법:")
        print("  1. PostgreSQL 서비스가 실행 중인지 확인하세요.")
        print("     - Windows: 서비스 앱에서 'postgresql' 검색")
        print("     - 서비스 이름: 'postgresql-x64-[버전]'")
        print()
        print("  2. .env 파일의 데이터베이스 설정을 확인하세요.")
        print(f"     DB_HOST={db_host}")
        print(f"     DB_PORT={db_port}")
        print(f"     DB_USER={db_user}")
        print(f"     DB_PASSWORD=******")
        print()
        print("  3. PostgreSQL 설치 확인:")
        print("     - 시작 메뉴에서 'pgAdmin' 실행")
        print("     - 또는 명령 프롬프트에서: psql --version")
        print()
        
        return False
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ 오류 발생!")
        print("="*60)
        print(f"오류: {e}")
        print()
        import traceback
        traceback.print_exc()
        
        return False


if __name__ == "__main__":
    success = create_database()
    exit(0 if success else 1)

