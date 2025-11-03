# OrderBean 데이터베이스 설정 가이드

## 📋 목차

1. [개요](#개요)
2. [데이터베이스 설정](#데이터베이스-설정)
3. [빠른 시작](#빠른-시작)
4. [단계별 설정](#단계별-설정)
5. [데이터베이스 스키마](#데이터베이스-스키마)
6. [테스트 및 검증](#테스트-및-검증)
7. [문제 해결](#문제-해결)

---

## 개요

OrderBean은 PostgreSQL 데이터베이스를 사용합니다. 이 가이드는 데이터베이스 설정부터 테스트까지 전체 과정을 안내합니다.

### 데이터베이스 정보

- **DBMS**: PostgreSQL 15+
- **데이터베이스 이름**: `orderbean_db`
- **기본 포트**: 5432
- **사용자**: postgres

---

## 데이터베이스 설정

### 환경 변수

프로젝트는 다음 데이터베이스 설정을 사용합니다:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql
```

---

## 빠른 시작

### 자동 설정 (권장)

```bash
# 1. 환경 변수 파일 생성
create_env.bat

# 2. 데이터베이스 초기화
python init_db.py

# 3. 샘플 데이터 생성
python seed_db.py

# 4. 연결 테스트
python test_db_connection.py
```

### 통합 설정 스크립트

모든 단계를 한 번에 실행:

```bash
setup_database.bat
```

---

## 단계별 설정

### 1단계: 환경 변수 설정

#### 방법 1: 배치 파일 사용
```bash
create_env.bat
```

#### 방법 2: 수동 설정
`.env` 파일을 생성하고 다음 내용을 입력:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=your_password_here

# Database URL
DATABASE_URL=postgresql+asyncpg://postgres:your_password_here@localhost:5432/orderbean_db

# Application Settings
APP_NAME=OrderBean API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Server Settings
HOST=0.0.0.0
PORT=8000
```

### 2단계: PostgreSQL 데이터베이스 생성

#### Windows (PowerShell 또는 CMD)

```bash
# PostgreSQL에 연결
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE orderbean_db;

# 확인
\l

# 종료
\q
```

#### 명령어 한 줄로 실행

```bash
psql -U postgres -c "CREATE DATABASE orderbean_db;"
```

### 3단계: 테이블 생성

```bash
python init_db.py
```

**실행 결과**:
```
====================================
OrderBean 데이터베이스 초기화
====================================

📊 데이터베이스 정보:
   - Host: localhost
   - Port: 5432
   - Database: orderbean_db
   - User: postgres

🔄 데이터베이스 연결 테스트 중...
✅ 데이터베이스 연결 성공!

🔄 테이블 생성 중...
✅ 다음 테이블이 생성되었습니다:
   - menus (메뉴)
   - menu_options (메뉴 옵션)
   - orders (주문)
   - order_items (주문 항목)
   - order_item_options (주문 항목 옵션)

====================================
✅ 데이터베이스 초기화 완료!
====================================
```

### 4단계: 샘플 데이터 생성 (선택사항)

```bash
python seed_db.py
```

**생성되는 샘플 메뉴**:
- 아메리카노 (4,500원)
- 카페라떼 (5,000원)
- 카푸치노 (5,000원)
- 바닐라라떼 (5,500원)
- 카라멜 마끼아또 (6,000원)
- 카페모카 (5,500원)
- 그린티 라떼 (5,500원)
- 자몽에이드 (6,000원)

각 메뉴에는 다양한 옵션(샷 추가, 휘핑크림 등)이 포함됩니다.

---

## 데이터베이스 스키마

### ERD (Entity Relationship Diagram)

```
┌─────────────────┐
│     Menu        │
├─────────────────┤
│ id              │──┐
│ name            │  │
│ description     │  │
│ price           │  │
│ image_url       │  │
│ stock           │  │
│ is_available    │  │
│ created_at      │  │
│ updated_at      │  │
└─────────────────┘  │
                     │
                     │ 1:N
                     │
                ┌────▼─────────────┐
                │  MenuOption      │
                ├──────────────────┤
                │ id               │
                │ menu_id (FK)     │
                │ name             │
                │ additional_price │
                │ created_at       │
                │ updated_at       │
                └──────────────────┘

┌─────────────────┐
│     Order       │
├─────────────────┤
│ id              │──┐
│ order_number    │  │
│ total_amount    │  │
│ status          │  │
│ created_at      │  │
│ updated_at      │  │
│ completed_at    │  │
└─────────────────┘  │
                     │ 1:N
                     │
                ┌────▼─────────────┐
                │  OrderItem       │
                ├──────────────────┤
                │ id               │──┐
                │ order_id (FK)    │  │
                │ menu_id (FK)     │  │
                │ quantity         │  │
                │ unit_price       │  │
                │ subtotal         │  │
                │ created_at       │  │
                └──────────────────┘  │
                                      │ 1:N
                                      │
                           ┌──────────▼────────────┐
                           │ OrderItemOption       │
                           ├───────────────────────┤
                           │ id                    │
                           │ order_item_id (FK)    │
                           │ option_id (FK)        │
                           │ option_name           │
                           │ additional_price      │
                           │ created_at            │
                           └───────────────────────┘
```

### 테이블 상세 설명

#### 1. menus (메뉴)
```sql
CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    image_url VARCHAR(500),
    stock INTEGER DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 2. menu_options (메뉴 옵션)
```sql
CREATE TABLE menu_options (
    id SERIAL PRIMARY KEY,
    menu_id INTEGER REFERENCES menus(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    additional_price NUMERIC(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. orders (주문)
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'received',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

**주문 상태 (status)**:
- `received`: 주문 접수
- `preparing`: 제조 중
- `completed`: 완료
- `cancelled`: 취소

#### 4. order_items (주문 항목)
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    menu_id INTEGER REFERENCES menus(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    subtotal NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 5. order_item_options (주문 항목 옵션)
```sql
CREATE TABLE order_item_options (
    id SERIAL PRIMARY KEY,
    order_item_id INTEGER REFERENCES order_items(id) ON DELETE CASCADE,
    option_id INTEGER REFERENCES menu_options(id),
    option_name VARCHAR(100) NOT NULL,
    additional_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 테스트 및 검증

### 1. 연결 테스트 스크립트

```bash
python test_db_connection.py
```

**테스트 항목**:
- ✅ 데이터베이스 연결
- ✅ PostgreSQL 버전 확인
- ✅ 데이터베이스 존재 확인
- ✅ 테이블 존재 확인
- ✅ 세션 및 쿼리 테스트

### 2. API를 통한 테스트

서버를 실행한 후:

```bash
python -m uvicorn app.main:app --reload
```

다음 엔드포인트로 접속:

#### 헬스 체크 (데이터베이스 포함)
```
GET http://localhost:8000/health
```

**응답 예시**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-02T16:35:07.005658"
}
```

#### 데이터베이스 상세 테스트
```
GET http://localhost:8000/api/v1/db-test
```

**응답 예시**:
```json
{
  "success": true,
  "message": "데이터베이스 연결 성공!",
  "database": {
    "version": "PostgreSQL 15.3",
    "current_database": "orderbean_db",
    "tables": [
      "menu_options",
      "menus",
      "order_item_options",
      "order_items",
      "orders"
    ],
    "menu_count": 8
  }
}
```

#### 일반 테스트 엔드포인트
```
GET http://localhost:8000/api/v1/test
```

**응답 예시**:
```json
{
  "success": true,
  "message": "FastAPI 서버가 정상적으로 작동 중입니다!",
  "data": {
    "framework": "FastAPI",
    "python": "3.11+",
    "features": ["비동기 처리", "자동 API 문서", "타입 검증"],
    "database": {
      "host": "localhost",
      "port": 5432,
      "database": "orderbean_db",
      "menu_count": 8
    }
  }
}
```

### 3. psql을 통한 직접 확인

```bash
# 데이터베이스 연결
psql -U postgres -d orderbean_db

# 테이블 목록 확인
\dt

# 메뉴 데이터 확인
SELECT * FROM menus;

# 옵션 데이터 확인
SELECT * FROM menu_options;

# 메뉴와 옵션 조인
SELECT m.name, mo.name as option_name, mo.additional_price
FROM menus m
LEFT JOIN menu_options mo ON m.id = mo.menu_id
ORDER BY m.id, mo.id;
```

---

## 문제 해결

### ❌ "psql: error: connection to server failed"

**원인**: PostgreSQL 서비스가 실행되지 않음

**해결**:
```bash
# Windows: 서비스 시작
net start postgresql-x64-15

# 또는 서비스 관리자에서 PostgreSQL 서비스 시작
services.msc
```

### ❌ "database 'orderbean_db' does not exist"

**원인**: 데이터베이스가 생성되지 않음

**해결**:
```bash
psql -U postgres -c "CREATE DATABASE orderbean_db;"
```

### ❌ "password authentication failed for user 'postgres'"

**원인**: 비밀번호가 올바르지 않음

**해결**:
1. `.env` 파일의 `DB_PASSWORD` 확인
2. PostgreSQL 비밀번호 재설정:
```bash
# PostgreSQL에 연결 (Windows 인증 사용)
psql -U postgres

# 비밀번호 변경
ALTER USER postgres PASSWORD 'postgresql';
```

### ❌ "cannot import name 'asyncpg'"

**원인**: asyncpg 패키지가 설치되지 않음

**해결**:
```bash
pip install asyncpg
# 또는
pip install -r requirements.txt
```

### ❌ "relation 'menus' does not exist"

**원인**: 테이블이 생성되지 않음

**해결**:
```bash
python init_db.py
```

### ❌ 테이블 초기화 (모든 데이터 삭제 후 재생성)

```bash
# 모든 테이블 삭제 + 재생성
python init_db.py reset

# 샘플 데이터 재생성
python seed_db.py
```

---

## 유용한 스크립트

### 데이터베이스 리셋 (개발 중)

```bash
# 1. 테이블 삭제 및 재생성
python init_db.py reset

# 2. 샘플 데이터 생성
python seed_db.py
```

### 데이터만 삭제

```bash
python seed_db.py clear
```

### 특정 테이블만 삭제 (psql)

```sql
-- 주문 데이터만 삭제
TRUNCATE TABLE orders CASCADE;

-- 메뉴 데이터만 삭제
TRUNCATE TABLE menus CASCADE;
```

---

## 다음 단계

1. ✅ 데이터베이스 설정 완료
2. ✅ 샘플 데이터 생성
3. ⏳ API 엔드포인트 개발
   - GET /api/v1/menus - 메뉴 목록
   - POST /api/v1/orders - 주문 생성
   - GET /api/v1/orders/{id} - 주문 조회
4. ⏳ 프론트엔드 연동
5. ⏳ 배포 준비

---

## 참고 자료

- **PostgreSQL 공식 문서**: https://www.postgresql.org/docs/
- **SQLAlchemy 문서**: https://docs.sqlalchemy.org/
- **asyncpg 문서**: https://magicstack.github.io/asyncpg/
- **FastAPI 데이터베이스 가이드**: https://fastapi.tiangolo.com/tutorial/sql-databases/

---

**작성일**: 2025년 11월 2일  
**버전**: 1.0  
**상태**: ✅ 데이터베이스 설정 완료
