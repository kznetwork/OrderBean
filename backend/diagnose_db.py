"""
데이터베이스 연결 문제 진단 스크립트
"""
import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

print("\n" + "="*60)
print("🔍 데이터베이스 연결 문제 진단")
print("="*60)
print()

# 1. 환경 변수 확인
print("📋 [1/5] 환경 변수 확인...")
db_host = os.getenv('DB_HOST', 'NOT_SET')
db_port = os.getenv('DB_PORT', 'NOT_SET')
db_name = os.getenv('DB_NAME', 'NOT_SET')
db_user = os.getenv('DB_USER', 'NOT_SET')
db_password = os.getenv('DB_PASSWORD', 'NOT_SET')

print(f"   DB_HOST: {db_host}")
print(f"   DB_PORT: {db_port}")
print(f"   DB_NAME: {db_name}")
print(f"   DB_USER: {db_user}")
print(f"   DB_PASSWORD: {'*' * len(db_password) if db_password != 'NOT_SET' else 'NOT_SET'}")
print()

if 'NOT_SET' in [db_host, db_port, db_name, db_user, db_password]:
    print("❌ .env 파일 설정이 올바르지 않습니다!")
    print("   .env 파일을 확인하세요.")
    sys.exit(1)

print("✅ 환경 변수 설정 확인 완료")
print()

# 2. PostgreSQL 기본 연결 테스트 (동기)
print("🔌 [2/5] PostgreSQL 서버 연결 테스트...")
try:
    import psycopg2
    
    # postgres 데이터베이스에 연결 시도
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database='postgres',  # 기본 데이터베이스
        user=db_user,
        password=db_password,
        connect_timeout=5
    )
    print("✅ PostgreSQL 서버 연결 성공!")
    
    # PostgreSQL 버전 확인
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()[0]
    print(f"   버전: {version.split(',')[0]}")
    
    cursor.close()
    conn.close()
    print()
    
except psycopg2.OperationalError as e:
    print(f"❌ PostgreSQL 서버 연결 실패!")
    print(f"   오류: {e}")
    print()
    print("해결 방법:")
    print("  1. PostgreSQL 서비스 실행 확인")
    print("     Windows + R → services.msc → postgresql 검색")
    print("  2. 비밀번호 확인")
    print("  3. 포트 번호 확인 (기본: 5432)")
    print()
    sys.exit(1)
except ImportError:
    print("⚠️  psycopg2가 설치되지 않았습니다.")
    print("   pip install psycopg2-binary")
    print()
    sys.exit(1)

# 3. 데이터베이스 존재 확인
print("🗄️  [3/5] orderbean_db 데이터베이스 존재 확인...")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database='postgres',
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (db_name,)
    )
    exists = cursor.fetchone()
    
    if exists:
        print(f"✅ '{db_name}' 데이터베이스가 존재합니다.")
    else:
        print(f"❌ '{db_name}' 데이터베이스가 없습니다!")
        print()
        print("해결 방법:")
        print("  python create_database.py")
        print()
        cursor.close()
        conn.close()
        sys.exit(1)
    
    cursor.close()
    conn.close()
    print()
    
except Exception as e:
    print(f"❌ 확인 실패: {e}")
    sys.exit(1)

# 4. 데이터베이스 직접 연결 테스트
print("🔗 [4/5] orderbean_db 데이터베이스 직접 연결 테스트...")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print(f"✅ '{db_name}' 데이터베이스 연결 성공!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_database()")
    current_db = cursor.fetchone()[0]
    print(f"   현재 데이터베이스: {current_db}")
    
    # 테이블 확인
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"   테이블 개수: {len(tables)}")
        print("   테이블 목록:")
        for table in tables:
            print(f"      - {table[0]}")
    else:
        print("   ⚠️  테이블이 없습니다.")
        print("      python init_database.py 를 실행하세요.")
    
    cursor.close()
    conn.close()
    print()
    
except Exception as e:
    print(f"❌ 연결 실패: {e}")
    sys.exit(1)

# 5. asyncpg 연결 테스트
print("🚀 [5/5] asyncpg (비동기) 연결 테스트...")
try:
    import asyncio
    import asyncpg
    
    async def test_asyncpg():
        try:
            conn = await asyncpg.connect(
                host=db_host,
                port=int(db_port),
                database=db_name,
                user=db_user,
                password=db_password,
                timeout=5
            )
            
            # 버전 확인
            version = await conn.fetchval('SELECT version()')
            print(f"✅ asyncpg 연결 성공!")
            print(f"   {version.split(',')[0]}")
            
            await conn.close()
            return True
            
        except Exception as e:
            print(f"❌ asyncpg 연결 실패!")
            print(f"   오류: {e}")
            print()
            print("이것은 FastAPI 서버에서 사용하는 드라이버입니다.")
            print("이 연결이 실패하면 API 서버도 작동하지 않습니다.")
            return False
    
    success = asyncio.run(test_asyncpg())
    print()
    
    if not success:
        sys.exit(1)
        
except ImportError:
    print("⚠️  asyncpg가 설치되지 않았습니다.")
    print("   pip install asyncpg")
    print()
    sys.exit(1)

# 최종 결과
print("="*60)
print("✅ 모든 진단 통과!")
print("="*60)
print()
print("데이터베이스 연결이 정상입니다.")
print("FastAPI 서버를 다시 시작해보세요:")
print("  uvicorn app.main:app --reload")
print()

