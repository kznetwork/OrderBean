# 🔧 PostgreSQL 연결 문제 해결 가이드

## ❌ 발생한 오류
```
ConnectionRefusedError: [WinError 1225] 원격 컴퓨터가 네트워크 연결을 거부했습니다
```

이 오류는 PostgreSQL 서버에 연결할 수 없을 때 발생합니다.

---

## ✅ 해결 방법 (순서대로 진행)

### 1단계: PostgreSQL 서비스 확인 및 시작

#### Windows Services로 확인
1. `Win + R` 키 → `services.msc` 입력 → 엔터
2. "postgresql-x64-xx" 서비스 찾기
3. 서비스가 "실행 중"인지 확인
4. 실행 중이 아니면 → 마우스 오른쪽 클릭 → "시작"

#### 명령어로 확인 (관리자 권한 CMD)
```cmd
# PostgreSQL 서비스 상태 확인
sc query postgresql-x64-16

# PostgreSQL 서비스 시작
net start postgresql-x64-16
```

> **참고**: `postgresql-x64-16`은 PostgreSQL 버전에 따라 다를 수 있습니다.
> - PostgreSQL 15: `postgresql-x64-15`
> - PostgreSQL 14: `postgresql-x64-14`

---

### 2단계: .env 파일 생성

#### 방법 1: 자동 생성 스크립트 사용 (권장)
```cmd
cd C:\DEV\Cursor_pro\OrderBean\backend
python create_env_file.py
```

#### 방법 2: 수동 생성
`backend/.env` 파일을 생성하고 아래 내용을 입력:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=your_password_here

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
```

**⚠️ 중요**: `DB_PASSWORD`를 실제 PostgreSQL 비밀번호로 변경하세요!

---

### 3단계: 데이터베이스 생성

PostgreSQL에 연결하여 데이터베이스를 생성합니다.

#### pgAdmin 사용
1. pgAdmin 실행
2. 서버 연결 (localhost)
3. 데이터베이스 → 마우스 오른쪽 클릭 → "생성..."
4. 데이터베이스 이름: `orderbean_db`
5. 저장

#### psql 명령어 사용
```cmd
# PostgreSQL에 연결
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE orderbean_db;

# 데이터베이스 목록 확인
\l

# 종료
\q
```

---

### 4단계: 데이터베이스 연결 테스트

```cmd
cd C:\DEV\Cursor_pro\OrderBean\backend
python test_db_connection.py
```

성공하면 다음과 같은 메시지가 표시됩니다:
```
✅ 데이터베이스 연결 성공!
```

---

### 5단계: 샘플 데이터 생성

```cmd
python seed_sample_data.py
```

---

## 🔍 문제별 해결 방법

### 문제 1: PostgreSQL 서비스를 찾을 수 없음
**증상**: `services.msc`에서 PostgreSQL 서비스가 없음

**해결**:
- PostgreSQL이 설치되어 있지 않습니다
- PostgreSQL 다운로드: https://www.postgresql.org/download/windows/
- 설치 후 다시 시도

### 문제 2: 비밀번호가 맞지 않음
**증상**: `password authentication failed`

**해결**:
1. PostgreSQL 설치 시 설정한 비밀번호 확인
2. `backend/.env` 파일의 `DB_PASSWORD` 수정
3. 다시 시도

### 문제 3: 데이터베이스가 존재하지 않음
**증상**: `database "orderbean_db" does not exist`

**해결**:
- 3단계로 돌아가서 데이터베이스 생성

### 문제 4: 포트가 이미 사용 중
**증상**: `port 5432 is already in use`

**해결**:
1. PostgreSQL이 이미 실행 중인지 확인
2. 다른 프로그램이 5432 포트를 사용하는지 확인
```cmd
netstat -ano | findstr :5432
```

---

## 📋 빠른 해결 체크리스트

- [ ] PostgreSQL 서비스가 실행 중인가?
- [ ] `.env` 파일이 `backend/` 폴더에 있는가?
- [ ] `.env` 파일의 비밀번호가 올바른가?
- [ ] `orderbean_db` 데이터베이스가 생성되어 있는가?
- [ ] 방화벽이 5432 포트를 차단하지 않는가?

---

## 🚀 모든 것이 해결되면

```cmd
cd C:\DEV\Cursor_pro\OrderBean\backend

# 1. 샘플 데이터 생성
python seed_sample_data.py

# 2. 서버 시작
uvicorn app.main:app --reload
```

서버가 정상적으로 시작되면:
- http://localhost:8000 접속 가능
- http://localhost:8000/api/docs 에서 API 문서 확인

---

## 💡 추가 도움말

### PostgreSQL 설치 확인
```cmd
# PostgreSQL 버전 확인
psql --version

# PostgreSQL 설치 경로 확인
where psql
```

### 로그 확인
PostgreSQL 로그 위치:
```
C:\Program Files\PostgreSQL\16\data\log\
```

---

## 📞 여전히 문제가 있다면

1. PostgreSQL 서비스 로그 확인
2. Windows 이벤트 뷰어 확인
3. 방화벽 설정 확인
4. PostgreSQL을 완전히 재설치

---

**작성일**: 2025년 11월 2일  
**프로젝트**: OrderBean

