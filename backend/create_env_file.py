"""
.env 파일 생성 스크립트
"""
import os

ENV_CONTENT = """# OrderBean Backend Environment Variables

# Application Settings
APP_NAME=OrderBean
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql

# Database URL (PostgreSQL with asyncpg)
DATABASE_URL=postgresql+asyncpg://postgres:postgresql@localhost:5432/orderbean_db

# Security (JWT)
SECRET_KEY=your-secret-key-change-this-in-production-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
"""

def create_env_file():
    """
    .env 파일 생성
    """
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        print("⚠️  .env 파일이 이미 존재합니다.")
        response = input("덮어쓰시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("❌ 취소되었습니다.")
            return
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(ENV_CONTENT)
    
    print("✅ .env 파일이 생성되었습니다!")
    print(f"📁 경로: {env_path}")
    print("\n다음 단계:")
    print("1. .env 파일에서 DATABASE_URL과 DB_PASSWORD를 확인하세요.")
    print("2. PostgreSQL 데이터베이스를 생성하세요:")
    print("   psql -U postgres")
    print("   CREATE DATABASE orderbean_db;")
    print("3. 데이터베이스 연결을 테스트하세요:")
    print("   python test_db_connection.py")

if __name__ == "__main__":
    create_env_file()

