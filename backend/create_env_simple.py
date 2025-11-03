"""
간단한 .env 파일 생성 스크립트
"""
import os

# .env 파일 내용
env_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql

# JWT Configuration
SECRET_KEY=your-secret-key-here-please-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=8000
"""

# .env 파일 생성
env_path = ".env"

if os.path.exists(env_path):
    print("⚠️  .env 파일이 이미 존재합니다.")
    response = input("덮어쓰시겠습니까? (y/n): ")
    if response.lower() != 'y':
        print("❌ 취소되었습니다.")
        exit()

with open(env_path, "w", encoding="utf-8") as f:
    f.write(env_content)

print("✅ .env 파일이 생성되었습니다!")
print()
print("📝 다음 단계:")
print("1. .env 파일을 열어서 DB_PASSWORD를 실제 비밀번호로 변경하세요")
print("2. PostgreSQL 서비스가 실행 중인지 확인하세요")
print("3. orderbean_db 데이터베이스를 생성하세요:")
print("   psql -U postgres")
print("   CREATE DATABASE orderbean_db;")
print("4. python seed_sample_data.py 를 실행하세요")

