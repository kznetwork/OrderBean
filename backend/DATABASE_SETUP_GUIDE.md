# 🗄️ OrderBean 데이터베이스 설정 가이드

PostgreSQL 데이터베이스를 설정하고 OrderBean 프로젝트를 실행하기 위한 완전한 가이드입니다.

## ✅ 사전 요구 사항

- ✅ PostgreSQL 설치 완료
- ✅ Python 3.8 이상 설치

## 📋 설정 단계

### 1단계: .env 파일 확인

`backend/.env` 파일이 이미 생성되어 있습니다. 다음 내용을 확인하세요:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql
```

### 2단계: Python 가상환경 생성 (권장)

```powershell
# backend 폴더로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (PowerShell)
venv\Scripts\Activate.ps1

# 또는 CMD
venv\Scripts\activate.bat
```

**주의**: PowerShell에서 스크립트 실행 정책 오류가 발생하면:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3단계: 필요한 패키지 설치

```powershell
# requirements.txt의 모든 패키지 설치
pip install -r requirements.txt
```

설치되는 주요 패키지:
- FastAPI (웹 프레임워크)
- SQLAlchemy (ORM)
- asyncpg (PostgreSQL 비동기 드라이버)
- psycopg2-binary (PostgreSQL 동기 드라이버)
- uvicorn (ASGI 서버)
- python-dotenv (환경 변수)
- 기타 의존성

### 4단계: PostgreSQL 서비스 확인

PostgreSQL 서비스가 실행 중인지 확인:

**방법 1: 서비스 앱 사용**
1. `Windows + R` → `services.msc` 입력
2. `postgresql-x64-[버전]` 서비스 찾기
3. 상태가 "실행 중"인지 확인
4. 중지되어 있다면 우클릭 → "시작"

**방법 2: PowerShell 사용**
```powershell
Get-Service | Where-Object {$_.Name -like "postgresql*"}
```

### 5단계: 데이터베이스 생성

Python 스크립트를 사용하여 `orderbean_db` 데이터베이스를 생성:

```powershell
python create_database.py
```

이 스크립트는 자동으로:
- PostgreSQL 서버 연결
- `orderbean_db` 데이터베이스 존재 여부 확인
- 없으면 생성, 있으면 선택 옵션 제공

**수동으로 생성하려면** (pgAdmin 또는 psql 사용):
```sql
CREATE DATABASE orderbean_db;
```

### 6단계: 데이터베이스 테이블 생성 및 샘플 데이터

```powershell
# 테이블 생성 및 샘플 데이터 추가
python init_database.py
```

이 명령은:
- 모든 테이블 생성 (menus, menu_options, orders, order_items)
- 5개의 샘플 메뉴 추가
- 각 메뉴에 옵션 추가
- 테스트 주문 1개 생성

### 7단계: 데이터베이스 연결 테스트

```powershell
python test_db_connection.py
```

성공 시 다음과 같은 출력이 표시됩니다:
```
✅ 모든 테스트 통과! 데이터베이스가 정상적으로 작동합니다.
```

### 8단계: 백엔드 서버 시작

```powershell
uvicorn app.main:app --reload
```

또는 간단하게:
```powershell
start_dev.bat
```

서버가 시작되면:
- 서버 주소: http://localhost:8000
- API 문서: http://localhost:8000/api/docs
- 헬스 체크: http://localhost:8000/health

### 9단계: 프론트엔드 시작 (선택사항)

**새 터미널**을 열고:

```powershell
# frontend 폴더로 이동
cd frontend

# 패키지 설치 (처음 한 번만)
npm install

# 개발 서버 시작
npm run dev
```

브라우저에서 http://localhost:5173 접속

## 🔍 문제 해결

### ❌ PostgreSQL 연결 실패

**증상**: `could not connect to server` 또는 `Connection refused`

**해결 방법**:
1. PostgreSQL 서비스 실행 확인
2. `.env` 파일의 포트 번호 확인 (기본: 5432)
3. 방화벽 설정 확인
4. PostgreSQL 설치 경로 확인

### ❌ 패키지 설치 오류

**증상**: `ModuleNotFoundError: No module named 'fastapi'`

**해결 방법**:
```powershell
# 가상환경 활성화 확인
# 프롬프트 앞에 (venv)가 있어야 함

# 패키지 재설치
pip install -r requirements.txt --upgrade
```

### ❌ 데이터베이스 생성 실패

**증상**: `permission denied to create database`

**해결 방법**:
1. `.env` 파일의 `DB_USER`가 `postgres` (슈퍼유저)인지 확인
2. 비밀번호가 정확한지 확인
3. pgAdmin에서 수동으로 데이터베이스 생성:
   ```sql
   CREATE DATABASE orderbean_db;
   ```

### ❌ 테이블 생성 오류

**증상**: 마이그레이션 또는 테이블 생성 실패

**해결 방법**:
```powershell
# 데이터베이스 재초기화
python init_database.py
```

### ❌ 포트 충돌

**증상**: `Address already in use`

**해결 방법**:
```powershell
# 8000 포트 사용 중인 프로세스 찾기
netstat -ano | findstr :8000

# 프로세스 종료 (PID는 위 명령의 마지막 숫자)
taskkill /PID [PID번호] /F

# 또는 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

## 📊 데이터베이스 구조

생성되는 테이블:

### `menus` (메뉴)
- id (Primary Key)
- name (메뉴명)
- description (설명)
- price (가격)
- image_url (이미지 URL)
- stock_quantity (재고 수량)
- is_available (판매 가능 여부)
- created_at, updated_at

### `menu_options` (메뉴 옵션)
- id (Primary Key)
- menu_id (Foreign Key → menus)
- name (옵션명: 사이즈, 샷 추가 등)
- value (옵션 값: Large, 1샷 추가 등)
- price (추가 가격)
- created_at

### `orders` (주문)
- id (Primary Key)
- order_number (주문 번호)
- customer_name (고객명)
- total_price (총 금액)
- status (주문 상태)
- notes (메모)
- created_at, updated_at

### `order_items` (주문 항목)
- id (Primary Key)
- order_id (Foreign Key → orders)
- menu_id (Foreign Key → menus)
- quantity (수량)
- unit_price (단가)
- total_price (총 가격)
- options (선택한 옵션 JSON)
- created_at

## 🎯 다음 단계

1. ✅ 데이터베이스 설정 완료
2. ✅ 백엔드 서버 실행 확인
3. 🔄 프론트엔드 연동
4. 🔄 기능 테스트
5. 🔄 배포 준비

## 📚 참고 문서

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [PostgreSQL 문서](https://www.postgresql.org/docs/)

## 💡 유용한 명령어

```powershell
# 데이터베이스 재설정 (주의: 모든 데이터 삭제)
python init_database.py

# 샘플 데이터만 추가
python seed_sample_data.py

# 데이터베이스 연결 테스트
python test_db_connection.py

# 서버 시작 (개발 모드)
uvicorn app.main:app --reload

# 서버 시작 (프로덕션 모드)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🎉 완료!

모든 단계를 완료하셨다면, 이제 OrderBean 프로젝트를 사용할 준비가 되었습니다!

API 문서에서 엔드포인트를 테스트해보세요:
👉 http://localhost:8000/api/docs

---

**작성일**: 2025년 11월 3일  
**프로젝트**: OrderBean  
**버전**: 1.0.0

