# Backend 개발 환경 구축 보고서

**프로젝트**: OrderBean  
**작업일**: 2025년 11월 2일  
**작업자**: AI Assistant  
**작업 내용**: FastAPI + Python 백엔드 개발 환경 구축 및 PostgreSQL 데이터베이스 연결  
**업데이트**: 2025년 11월 2일 (서버 테스트 및 DB 연결 완료)

---

## 📋 목차

1. [작업 개요](#1-작업-개요)
2. [백엔드 PRD 작성](#2-백엔드-prd-작성)
3. [프로젝트 구조 생성](#3-프로젝트-구조-생성)
4. [주요 파일 설명](#4-주요-파일-설명)
5. [개발 환경 설정 가이드](#5-개발-환경-설정-가이드)
6. [서버 실행 테스트](#6-서버-실행-테스트)
7. [데이터베이스 연결 설정](#7-데이터베이스-연결-설정)
8. [다음 단계](#8-다음-단계)

---

## 1. 작업 개요

### 1.1 목적

OrderBean 프로젝트의 백엔드 서버를 FastAPI + Python 조합으로 개발하기 위한 기반 환경을 구축하고, 개발 가이드 문서를 작성합니다.

### 1.2 완료된 작업

✅ **백엔드 PRD 문서 작성**
- 데이터 모델 설계 (Menus, Options, Orders, OrderItems)
- API 설계 (RESTful API)
- 비즈니스 로직 정의
- 기술 스택 선정
- 개발 로드맵 수립

✅ **프로젝트 구조 생성**
- 표준 FastAPI 프로젝트 디렉토리 구조
- 모듈별 패키지 분리 (api, models, schemas, services, core, utils)
- 테스트 디렉토리 구성

✅ **핵심 설정 파일 작성**
- `requirements.txt`: Python 패키지 의존성 정의
- `app/main.py`: FastAPI 애플리케이션 진입점
- `README.md`: 개발 가이드 문서
- `env_example.txt`: 환경 변수 예시
- `.gitignore`: Git 버전 관리 제외 파일

✅ **서버 실행 및 접속 테스트**
- FastAPI 서버 정상 실행 확인
- 루트 엔드포인트 테스트 완료
- API 문서 (Swagger UI) 접근 확인

✅ **PostgreSQL 데이터베이스 연결**
- 데이터베이스 설정 파일 작성 (`app/core/config.py`, `app/core/database.py`)
- SQLAlchemy 모델 정의 (Menu, MenuOption, Order, OrderItem, OrderItemOption)
- 환경 변수 자동 생성 스크립트 (`create_env.bat`)
- 데이터베이스 초기화 스크립트 (`init_db.py`)
- 샘플 데이터 생성 스크립트 (`seed_db.py`)
- 연결 테스트 스크립트 (`test_db_connection.py`)
- FastAPI 애플리케이션에 데이터베이스 통합

### 1.3 기술 스택

| 구분 | 기술 | 버전 |
|------|------|------|
| **언어** | Python | 3.11+ |
| **프레임워크** | FastAPI | 0.109.0 |
| **서버** | Uvicorn | 0.27.0 |
| **데이터베이스** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.0.25 |
| **마이그레이션** | Alembic | 1.13.1 |
| **인증** | JWT (python-jose) | 3.3.0 |
| **테스트** | pytest | 7.4.4 |

---

## 2. 백엔드 PRD 작성

### 2.1 문서 위치

`Docs/Backend_PRD.md`

### 2.2 주요 내용

#### 데이터 모델

**Menus (메뉴)**
- 커피 이름, 설명, 가격, 이미지, 재고 수량
- 판매 가능 여부 관리
- 옵션과 1:N 관계

**Options (옵션)**
- 옵션 이름, 가격, 옵션 타입
- 메뉴에 종속적
- 사이즈, 샷, 시럽, 얼음 등 다양한 옵션 타입 지원

**Orders (주문)**
- 주문 번호 (ORD-YYYYMMDD-XXX 형식)
- 주문 상태 (pending → preparing → completed)
- 총 주문 금액, 특별 요청사항

**OrderItems (주문 상세)**
- 메뉴별 수량, 단가, 소계
- 선택된 옵션 정보 (JSON 형식)

#### API 설계

**메뉴 API**
- `GET /api/v1/menus`: 메뉴 목록 조회
- `GET /api/v1/menus/:id`: 메뉴 상세 조회
- `POST /api/v1/menus`: 메뉴 등록 (관리자)
- `PATCH /api/v1/menus/:id/stock`: 재고 수정 (관리자)

**주문 API**
- `POST /api/v1/orders`: 주문 생성
- `GET /api/v1/orders/:id`: 주문 상세 조회

**관리자 API**
- `GET /api/v1/admin/orders`: 전체 주문 조회
- `PATCH /api/v1/admin/orders/:id/status`: 주문 상태 변경
- `GET /api/v1/admin/menus/stock`: 재고 현황 조회

#### 비즈니스 로직

**주문 생성 프로세스**
1. 데이터 유효성 검증
2. 재고 확인
3. 가격 계산 (메뉴 가격 + 옵션 가격)
4. 트랜잭션 처리
   - 주문 생성
   - 주문 아이템 생성
   - 재고 감소
   - 재고 0이면 판매 중지
5. 주문 번호 생성

**재고 관리 로직**
- 주문 시 자동 재고 감소
- 재고 0이면 `is_available = FALSE`
- 관리자가 재고 추가 시 판매 재개

**주문 상태 전이**
- pending → preparing → completed
- pending → cancelled (취소는 접수 상태에서만 가능)

---

## 3. 프로젝트 구조 생성

### 3.1 디렉토리 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   │
│   ├── api/                    # API 엔드포인트
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── __init__.py
│   │
│   ├── models/                 # SQLAlchemy 모델
│   │   └── __init__.py
│   │
│   ├── schemas/                # Pydantic 스키마
│   │   └── __init__.py
│   │
│   ├── services/               # 비즈니스 로직
│   │   └── __init__.py
│   │
│   ├── core/                   # 설정 및 데이터베이스
│   │   └── __init__.py
│   │
│   └── utils/                  # 유틸리티 함수
│       └── __init__.py
│
├── tests/                      # 테스트 파일
│   └── __init__.py
│
├── alembic/                    # 데이터베이스 마이그레이션 (향후 추가)
│
├── requirements.txt            # Python 패키지 의존성
├── env_example.txt             # 환경 변수 예시
├── .gitignore                  # Git 제외 파일
└── README.md                   # 개발 가이드
```

### 3.2 설계 원칙

**모듈화**
- 각 기능을 독립적인 모듈로 분리
- api, models, schemas, services 계층 분리
- 재사용 가능한 유틸리티 함수 분리

**확장성**
- API 버전 관리 (v1, v2 등)
- 새로운 엔드포인트 추가 용이
- 테스트 가능한 구조

**유지보수성**
- 명확한 디렉토리 구조
- 표준 네이밍 컨벤션
- 문서화된 코드

---

## 4. 주요 파일 설명

### 4.1 requirements.txt

Python 패키지 의존성을 정의한 파일입니다.

**주요 패키지**
- `fastapi==0.109.0`: 웹 프레임워크
- `uvicorn[standard]==0.27.0`: ASGI 서버
- `sqlalchemy==2.0.25`: ORM
- `asyncpg==0.29.0`: 비동기 PostgreSQL 드라이버
- `alembic==1.13.1`: 데이터베이스 마이그레이션
- `pydantic==2.5.3`: 데이터 검증
- `python-jose[cryptography]==3.3.0`: JWT 인증
- `pytest==7.4.4`: 테스트 프레임워크

### 4.2 app/main.py

FastAPI 애플리케이션의 진입점입니다.

**주요 기능**
1. FastAPI 애플리케이션 생성
2. CORS 미들웨어 설정
3. 기본 엔드포인트 정의
   - `GET /`: API 상태 확인
   - `GET /health`: 헬스 체크
   - `GET /api/v1/test`: 테스트 엔드포인트

**코드 하이라이트**
```python
app = FastAPI(
    title="OrderBean API",
    description="커피 주문 관리 시스템 백엔드 API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.3 env_example.txt

환경 변수 예시 파일입니다. 실제 사용 시 `.env` 파일로 복사하여 사용합니다.

**주요 환경 변수**
- `DATABASE_URL`: PostgreSQL 데이터베이스 연결 URL
- `SECRET_KEY`: JWT 토큰 생성용 비밀키
- `ALLOWED_ORIGINS`: CORS 허용 도메인
- `ENVIRONMENT`: 개발/프로덕션 환경 구분

### 4.4 .gitignore

Git 버전 관리에서 제외할 파일/폴더를 정의합니다.

**주요 제외 항목**
- Python 캐시 파일 (`__pycache__/`, `*.pyc`)
- 가상환경 (`venv/`, `.venv/`)
- 환경 변수 파일 (`.env`)
- IDE 설정 (`.vscode/`, `.idea/`)
- 데이터베이스 파일 (`*.db`, `*.sqlite3`)
- 로그 파일 (`*.log`)

### 4.5 README.md

백엔드 개발 가이드 문서입니다.

**포함 내용**
- 기술 스택 소개
- 프로젝트 구조 설명
- 시작하기 가이드
  - 가상환경 설정
  - 패키지 설치
  - 서버 실행
- API 문서 링크
- 개발/테스트/배포 가이드

---

## 5. 개발 환경 설정 가이드

### 5.1 사전 요구사항

- Python 3.11 이상
- PostgreSQL 15 이상 (향후 데이터베이스 연동 시)
- Git

### 5.2 설치 및 실행 단계

#### Step 1: 가상환경 생성 및 활성화

```bash
# backend 디렉토리로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
```

#### Step 2: 패키지 설치

```bash
pip install -r requirements.txt
```

**예상 설치 시간**: 2-5분

#### Step 3: 환경 변수 설정 (선택사항)

```bash
# env_example.txt를 .env로 복사
copy env_example.txt .env    # Windows
cp env_example.txt .env      # macOS/Linux

# .env 파일 편집 (필요한 경우)
```

#### Step 4: 서버 실행

```bash
# 개발 서버 실행 (핫 리로드 활성화)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**서버 시작 확인**
```
INFO:     Will watch for changes in these directories: ['C:\\DEV\\Cursor_pro\\OrderBean\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Step 5: API 테스트

**브라우저에서 확인**
1. http://localhost:8000/ - 루트 엔드포인트
2. http://localhost:8000/health - 헬스 체크
3. http://localhost:8000/api/v1/test - 테스트 엔드포인트
4. http://localhost:8000/api/docs - Swagger UI (자동 API 문서)
5. http://localhost:8000/api/redoc - ReDoc (자동 API 문서)

**curl로 테스트**
```bash
# 루트 엔드포인트
curl http://localhost:8000/

# 헬스 체크
curl http://localhost:8000/health

# 테스트 엔드포인트
curl http://localhost:8000/api/v1/test
```

**예상 응답 (루트 엔드포인트)**
```json
{
  "message": "OrderBean API Server",
  "version": "1.0.0",
  "status": "running",
  "timestamp": "2025-11-02T10:30:00.123456",
  "docs": "/api/docs"
}
```

**예상 응답 (테스트 엔드포인트)**
```json
{
  "success": true,
  "message": "FastAPI 서버가 정상적으로 작동 중입니다!",
  "data": {
    "framework": "FastAPI",
    "python": "3.11+",
    "features": ["비동기 처리", "자동 API 문서", "타입 검증"]
  }
}
```

### 5.3 Swagger UI 사용법

1. 브라우저에서 http://localhost:8000/api/docs 접속
2. 각 API 엔드포인트 확인
3. "Try it out" 버튼 클릭하여 직접 테스트 가능
4. 파라미터 입력 후 "Execute" 클릭
5. 응답 확인

---

## 6. 서버 실행 테스트

### 6.1 서버 실행 결과

**실행 날짜**: 2025년 11월 2일  
**실행 환경**: Windows 10, Python 3.11+

#### 실행 명령어
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 서버 시작 로그
```
INFO:     Will watch for changes in these directories: ['C:\\DEV\\Cursor_pro\\OrderBean\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 6.2 엔드포인트 테스트 결과

#### ✅ 루트 엔드포인트 (/)
**URL**: http://localhost:8000/  
**Method**: GET  
**Status**: 200 OK

**응답 예시**:
```json
{
  "message": "OrderBean API Server",
  "version": "1.0.0",
  "status": "running",
  "timestamp": "2025-11-02T16:35:07.005658",
  "docs": "/api/docs"
}
```

#### ✅ 헬스 체크 (/health)
**URL**: http://localhost:8000/health  
**Method**: GET  
**Status**: 200 OK

**응답 예시**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-02T16:35:08.123456"
}
```

#### ✅ 테스트 엔드포인트 (/api/v1/test)
**URL**: http://localhost:8000/api/v1/test  
**Method**: GET  
**Status**: 200 OK

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

#### ✅ 데이터베이스 테스트 (/api/v1/db-test)
**URL**: http://localhost:8000/api/v1/db-test  
**Method**: GET  
**Status**: 200 OK

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

#### ✅ API 문서 (Swagger UI)
**URL**: http://localhost:8000/api/docs  
**Status**: 접근 가능

**기능 확인**:
- 모든 엔드포인트 목록 표시
- "Try it out" 기능으로 직접 API 테스트 가능
- 자동 생성된 스키마 문서

### 6.3 개발 편의 스크립트

프로젝트에 다음 스크립트들이 추가되었습니다:

#### start_server.bat
서버를 간편하게 시작하는 배치 파일
```bash
start_server.bat
```

#### test_server.py
자동화된 API 테스트 스크립트
```bash
python test_server.py
```

**테스트 항목**:
- ✅ 루트 엔드포인트
- ✅ 헬스 체크
- ✅ API 테스트 엔드포인트

---

## 7. 데이터베이스 연결 설정

### 7.1 데이터베이스 정보

**DBMS**: PostgreSQL 15+  
**데이터베이스명**: orderbean_db  
**호스트**: localhost  
**포트**: 5432  
**사용자**: postgres  
**비밀번호**: postgresql

### 7.2 생성된 설정 파일

#### app/core/config.py
애플리케이션 설정 관리 클래스

**주요 기능**:
- 환경 변수 로드 및 검증 (pydantic-settings 사용)
- 데이터베이스 URL 자동 생성
- CORS 설정 파싱

**주요 설정**:
```python
class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "orderbean_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgresql"
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```

#### app/core/database.py
데이터베이스 연결 및 세션 관리

**주요 기능**:
- 비동기 SQLAlchemy 엔진 생성
- 세션 팩토리 설정
- 데이터베이스 의존성 함수 (`get_db`)
- 테이블 초기화 함수 (`init_db`)

### 7.3 데이터베이스 모델

#### Menu (메뉴)
**파일**: `app/models/menu.py`

**필드**:
- id: 메뉴 ID (Primary Key)
- name: 커피 이름 (최대 100자)
- description: 설명 (Text)
- price: 가격 (Decimal 10,2)
- image_url: 이미지 URL (최대 500자)
- stock: 재고 수량 (Integer)
- is_available: 판매 가능 여부 (Boolean)
- created_at, updated_at: 타임스탬프

**관계**:
- options (1:N): 메뉴 옵션
- order_items (1:N): 주문 항목

#### MenuOption (메뉴 옵션)
**파일**: `app/models/option.py`

**필드**:
- id: 옵션 ID (Primary Key)
- menu_id: 메뉴 ID (Foreign Key)
- name: 옵션 이름 (최대 100자)
- additional_price: 추가 가격 (Decimal 10,2)
- created_at, updated_at: 타임스탬프

**관계**:
- menu (N:1): 메뉴
- order_item_options (1:N): 주문 항목 옵션

#### Order (주문)
**파일**: `app/models/order.py`

**필드**:
- id: 주문 ID (Primary Key)
- order_number: 주문 번호 (Unique, 최대 50자)
- total_amount: 총 금액 (Decimal 10,2)
- status: 주문 상태 (Enum: received, preparing, completed, cancelled)
- created_at, updated_at, completed_at: 타임스탬프

**관계**:
- items (1:N): 주문 항목

#### OrderItem (주문 항목)
**파일**: `app/models/order.py`

**필드**:
- id: 주문 항목 ID (Primary Key)
- order_id: 주문 ID (Foreign Key)
- menu_id: 메뉴 ID (Foreign Key)
- quantity: 수량 (Integer)
- unit_price: 단가 (Decimal 10,2)
- subtotal: 소계 (Decimal 10,2)
- created_at: 타임스탬프

**관계**:
- order (N:1): 주문
- menu (N:1): 메뉴
- options (1:N): 주문 항목 옵션

#### OrderItemOption (주문 항목 옵션)
**파일**: `app/models/order.py`

**필드**:
- id: 주문 항목 옵션 ID (Primary Key)
- order_item_id: 주문 항목 ID (Foreign Key)
- option_id: 옵션 ID (Foreign Key)
- option_name: 옵션 이름 스냅샷 (최대 100자)
- additional_price: 추가 가격 스냅샷 (Decimal 10,2)
- created_at: 타임스탬프

**관계**:
- order_item (N:1): 주문 항목
- option (N:1): 메뉴 옵션

### 7.4 ERD (Entity Relationship Diagram)

```
┌─────────────────┐       ┌──────────────────┐
│     Menu        │───┬───│  MenuOption      │
│                 │   │   │                  │
│ id (PK)         │   │   │ id (PK)          │
│ name            │   └───│ menu_id (FK)     │
│ description     │       │ name             │
│ price           │       │ additional_price │
│ image_url       │       └──────────────────┘
│ stock           │
│ is_available    │
└─────────────────┘

┌─────────────────┐       ┌──────────────────┐
│     Order       │───┬───│   OrderItem      │
│                 │   │   │                  │
│ id (PK)         │   │   │ id (PK)          │
│ order_number    │   └───│ order_id (FK)    │
│ total_amount    │       │ menu_id (FK)     │
│ status          │       │ quantity         │
│ created_at      │       │ unit_price       │
└─────────────────┘       │ subtotal         │
                          └──────────────────┘
                                    │
                                    │ 1:N
                                    │
                          ┌─────────▼──────────┐
                          │ OrderItemOption    │
                          │                    │
                          │ id (PK)            │
                          │ order_item_id (FK) │
                          │ option_id (FK)     │
                          │ option_name        │
                          │ additional_price   │
                          └────────────────────┘
```

### 7.5 유틸리티 스크립트

#### create_env.bat
환경 변수 파일 자동 생성

**실행**:
```bash
cd backend
create_env.bat
```

**생성 파일**: `.env` (데이터베이스 설정 포함)

#### init_db.py
데이터베이스 테이블 생성

**실행**:
```bash
python init_db.py
```

**기능**:
- 데이터베이스 연결 테스트
- 모든 테이블 생성 (menus, menu_options, orders, order_items, order_item_options)

**추가 명령**:
- `python init_db.py reset`: 모든 테이블 삭제 후 재생성
- `python init_db.py drop`: 모든 테이블 삭제

#### seed_db.py
샘플 데이터 생성

**실행**:
```bash
python seed_db.py
```

**생성 데이터**:
- 8개의 커피 메뉴 (아메리카노, 카페라떼, 카푸치노 등)
- 각 메뉴당 2-5개의 옵션 (샷 추가, 휘핑크림, ICE/HOT 등)

**추가 명령**:
- `python seed_db.py clear`: 모든 데이터 삭제

#### test_db_connection.py
데이터베이스 연결 테스트

**실행**:
```bash
python test_db_connection.py
```

**테스트 항목**:
1. ✅ 데이터베이스 기본 연결
2. ✅ PostgreSQL 버전 확인
3. ✅ 데이터베이스 존재 확인
4. ✅ 테이블 존재 확인
5. ✅ 세션 및 쿼리 테스트

#### setup_database.bat
통합 데이터베이스 설정

**실행**:
```bash
setup_database.bat
```

**수행 작업**:
1. 환경 변수 파일 생성
2. PostgreSQL 연결 확인
3. 데이터베이스 생성
4. 테이블 생성
5. 샘플 데이터 생성 (선택)

### 7.6 FastAPI 통합

#### 애플리케이션 Lifespan 이벤트
`app/main.py`에 데이터베이스 연결/종료 로직 추가

**시작 시**:
- 데이터베이스 연결 테스트
- 연결 상태 로그 출력

**종료 시**:
- 데이터베이스 연결 정리

#### 업데이트된 엔드포인트

**`/health` 엔드포인트**:
- 데이터베이스 연결 상태 포함
- `database: "connected"` 또는 에러 메시지

**`/api/v1/test` 엔드포인트**:
- 데이터베이스 정보 추가
- 메뉴 개수 표시

**`/api/v1/db-test` 엔드포인트 (신규)**:
- PostgreSQL 버전 확인
- 현재 데이터베이스 확인
- 테이블 목록 표시
- 메뉴 개수 표시

### 7.7 작성된 문서

#### DATABASE_SETUP.md
**위치**: `backend/DATABASE_SETUP.md`

**내용**:
- 데이터베이스 설정 전체 가이드
- ERD 및 스키마 상세 설명
- 테이블별 SQL 정의
- 테스트 방법
- 문제 해결 가이드

#### QUICK_START.md
**위치**: `backend/QUICK_START.md`

**내용**:
- 3단계 빠른 시작 가이드
- 주요 명령어 요약
- 문제 해결 팁

---

## 8. 다음 단계

### 8.1 완료된 작업 ✅

✅ **가상환경 설정 및 패키지 설치**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

✅ **서버 실행 및 접속 테스트**
```bash
uvicorn app.main:app --reload
```

✅ **PostgreSQL 데이터베이스 설정**
```bash
create_env.bat          # 환경 변수 생성
python init_db.py       # 테이블 생성
python seed_db.py       # 샘플 데이터 생성
```

### 8.2 즉시 진행 가능한 작업

### 8.3 단계별 개발 계획

#### Phase 1: 데이터베이스 설정 ✅ (완료)

- [x] PostgreSQL 설치 및 데이터베이스 생성
- [x] SQLAlchemy 데이터베이스 연결 설정
- [x] 모델 정의 (Menus, Options, Orders, OrderItems)
- [x] 초기 테이블 생성 스크립트
- [x] 시드 데이터 작성
- [x] 연결 테스트 및 검증

**작업 완료 파일**
- `app/core/database.py`: 데이터베이스 연결 설정 ✅
- `app/core/config.py`: 환경 변수 관리 ✅
- `app/models/menu.py`: Menu 모델 ✅
- `app/models/option.py`: MenuOption 모델 ✅
- `app/models/order.py`: Order, OrderItem, OrderItemOption 모델 ✅
- `init_db.py`: 데이터베이스 초기화 스크립트 ✅
- `seed_db.py`: 샘플 데이터 생성 스크립트 ✅
- `test_db_connection.py`: 연결 테스트 스크립트 ✅

#### Phase 2: 메뉴 API 구현 (2-3일)

- [ ] Pydantic 스키마 정의
- [ ] `GET /api/v1/menus` 구현
- [ ] `GET /api/v1/menus/:id` 구현
- [ ] 메뉴-옵션 관계 쿼리 최적화
- [ ] 단위 테스트 작성

**예상 작업 파일**
- `app/schemas/menu.py`: Menu 스키마
- `app/schemas/option.py`: Option 스키마
- `app/api/v1/menus.py`: 메뉴 API 라우터
- `app/services/menu_service.py`: 메뉴 비즈니스 로직
- `tests/test_menus.py`: 메뉴 API 테스트

#### Phase 3: 주문 API 구현 (3-4일)

- [ ] 주문 스키마 정의
- [ ] `POST /api/v1/orders` 구현
- [ ] 주문 생성 비즈니스 로직
- [ ] 재고 관리 로직
- [ ] 트랜잭션 처리
- [ ] 통합 테스트

**예상 작업 파일**
- `app/schemas/order.py`: Order 스키마
- `app/api/v1/orders.py`: 주문 API 라우터
- `app/services/order_service.py`: 주문 비즈니스 로직
- `app/utils/order_number.py`: 주문 번호 생성
- `tests/test_orders.py`: 주문 API 테스트

#### Phase 4: 관리자 API 구현 (2-3일)

- [ ] 관리자 권한 미들웨어
- [ ] `GET /api/v1/admin/orders` 구현
- [ ] `PATCH /api/v1/admin/orders/:id/status` 구현
- [ ] `GET /api/v1/admin/menus/stock` 구현
- [ ] 통계 계산 로직
- [ ] 테스트

**예상 작업 파일**
- `app/api/v1/admin.py`: 관리자 API 라우터
- `app/core/auth.py`: 인증 미들웨어
- `app/services/admin_service.py`: 관리자 비즈니스 로직
- `tests/test_admin.py`: 관리자 API 테스트

#### Phase 5: 배포 준비 (1-2일)

- [ ] 환경 변수 설정
- [ ] 프로덕션 설정
- [ ] Render 배포
- [ ] 프론트엔드 연동 테스트

### 8.4 참고 문서

**프로젝트 문서**:
- **백엔드 PRD**: `Docs/Backend_PRD.md`
- **데이터베이스 설정 가이드**: `backend/DATABASE_SETUP.md`
- **빠른 시작 가이드**: `backend/QUICK_START.md`
- **백엔드 README**: `backend/README.md`

**외부 문서**:
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com
- **SQLAlchemy 문서**: https://docs.sqlalchemy.org
- **Pydantic 문서**: https://docs.pydantic.dev
- **PostgreSQL 문서**: https://www.postgresql.org/docs

---

## 7. 문제 해결 (Troubleshooting)

### 7.1 가상환경 활성화 오류

**문제**: `venv\Scripts\activate` 실행 시 오류 발생

**해결 방법** (Windows PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 7.2 패키지 설치 오류

**문제**: `pip install -r requirements.txt` 실행 시 오류 발생

**해결 방법**:
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt
```

### 7.3 서버 실행 포트 충돌

**문제**: 8000 포트가 이미 사용 중

**해결 방법**:
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

### 7.4 CORS 오류

**문제**: 프론트엔드에서 API 호출 시 CORS 오류 발생

**해결 방법**: `app/main.py`의 `allow_origins`에 프론트엔드 URL 추가
```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "https://yourdomain.com",  # 추가
]
```

---

## 8. 체크리스트

### 완료된 작업 ✅

**Phase 0: 프로젝트 구조 및 기본 설정**
- [x] 백엔드 PRD 문서 작성
- [x] 프로젝트 디렉토리 구조 생성
- [x] `requirements.txt` 작성
- [x] `app/main.py` 작성 (기본 엔드포인트)
- [x] `README.md` 작성
- [x] 환경 변수 예시 파일 작성
- [x] `.gitignore` 작성

**Phase 1: 서버 실행 및 테스트**
- [x] Python 가상환경 설정
- [x] 패키지 설치
- [x] 서버 실행 및 접속 테스트
- [x] API 문서 확인 (Swagger UI)
- [x] 개발 편의 스크립트 작성 (`start_server.bat`, `test_server.py`)

**Phase 2: 데이터베이스 연결**
- [x] PostgreSQL 데이터베이스 생성
- [x] 환경 변수 설정 (`app/core/config.py`)
- [x] 데이터베이스 연결 설정 (`app/core/database.py`)
- [x] SQLAlchemy 모델 정의 (Menu, MenuOption, Order, OrderItem, OrderItemOption)
- [x] 데이터베이스 초기화 스크립트 (`init_db.py`)
- [x] 샘플 데이터 생성 스크립트 (`seed_db.py`)
- [x] 연결 테스트 스크립트 (`test_db_connection.py`)
- [x] FastAPI 애플리케이션에 데이터베이스 통합
- [x] 데이터베이스 테스트 엔드포인트 추가 (`/api/v1/db-test`)
- [x] 상세 설정 가이드 작성 (`DATABASE_SETUP.md`, `QUICK_START.md`)

### 대기 중인 작업 ⏳

**Phase 3: API 엔드포인트 구현**
- [ ] Pydantic 스키마 정의
- [ ] 메뉴 API 구현
- [ ] 주문 API 구현
- [ ] 관리자 API 구현

**Phase 4: 테스트 및 배포**
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성
- [ ] 프론트엔드 연동
- [ ] 배포 준비

---

## 9. 결론

FastAPI + Python 기반 백엔드 개발 환경 구축과 PostgreSQL 데이터베이스 연결을 완료했습니다.

### 9.1 달성한 목표

1. ✅ **체계적인 프로젝트 구조**: 확장 가능하고 유지보수가 쉬운 디렉토리 구조
2. ✅ **상세한 PRD 문서**: 데이터 모델, API 설계, 비즈니스 로직 정의
3. ✅ **실행 및 테스트 완료**: FastAPI 서버 정상 작동 및 모든 엔드포인트 테스트 완료
4. ✅ **데이터베이스 연결**: PostgreSQL 연결 및 5개 테이블 생성 완료
5. ✅ **샘플 데이터**: 8개 커피 메뉴와 옵션 데이터 생성
6. ✅ **개발 가이드 문서**: 설치부터 실행, 데이터베이스 설정까지 상세 가이드

### 9.2 다음 작업자를 위한 메모

1. **서버 시작**: `start_server.bat` 또는 `python -m uvicorn app.main:app --reload`
2. **데이터베이스 초기화**: `python init_db.py` (테이블 생성)
3. **샘플 데이터 생성**: `python seed_db.py` (8개 커피 메뉴)
4. **연결 테스트**: `python test_db_connection.py`
5. **환경 변수**: `.env` 파일은 `create_env.bat`으로 자동 생성 가능
6. **API 문서 활용**: Swagger UI (`/api/docs`)를 통해 API 테스트 가능
7. **데이터베이스 리셋**: `python init_db.py reset` (개발 중 필요 시)
8. **코드 포맷팅**: Black, Pylint 사용 권장
9. **테스트 작성**: pytest로 단위 테스트 및 통합 테스트 작성

### 9.3 개발 진행 상황

- **Phase 0 (프로젝트 구조)**: ✅ 완료
- **Phase 1 (서버 테스트)**: ✅ 완료
- **Phase 2 (데이터베이스)**: ✅ 완료
- **Phase 3 (메뉴 API)**: ⏳ 대기 중 (예상 2-3일)
- **Phase 4 (주문 API)**: ⏳ 대기 중 (예상 3-4일)
- **Phase 5 (관리자 API)**: ⏳ 대기 중 (예상 2-3일)
- **Phase 6 (배포)**: ⏳ 대기 중 (예상 1-2일)
- **총 예상 남은 기간**: 약 1-2주

---

## 부록 A: 생성된 파일 목록

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI 애플리케이션 (업데이트: DB 통합)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── __init__.py
│   │
│   ├── models/                          # 데이터베이스 모델 (신규)
│   │   ├── __init__.py                  # 모델 내보내기
│   │   ├── menu.py                      # Menu 모델
│   │   ├── option.py                    # MenuOption 모델
│   │   └── order.py                     # Order, OrderItem, OrderItemOption 모델
│   │
│   ├── schemas/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── core/                            # 핵심 설정 (신규)
│   │   ├── __init__.py
│   │   ├── config.py                    # 애플리케이션 설정
│   │   └── database.py                  # 데이터베이스 연결
│   │
│   └── utils/
│       └── __init__.py
│
├── tests/
│   └── __init__.py
│
├── requirements.txt
├── .env.example                          # 환경 변수 예시 (업데이트)
├── .gitignore                            # Git 제외 파일 (업데이트)
├── README.md
│
├── create_env.bat                        # 환경 변수 자동 생성 (신규)
├── init_db.py                            # 데이터베이스 초기화 (신규)
├── seed_db.py                            # 샘플 데이터 생성 (신규)
├── test_db_connection.py                 # DB 연결 테스트 (신규)
├── setup_database.bat                    # 통합 DB 설정 (신규)
├── start_server.bat                      # 서버 시작 스크립트 (신규)
├── test_server.py                        # API 테스트 스크립트 (신규)
│
├── DATABASE_SETUP.md                     # DB 설정 가이드 (신규)
├── QUICK_START.md                        # 빠른 시작 가이드 (신규)
└── SETUP_GUIDE.md                        # 전체 설정 가이드 (신규)
```

**총 파일 수**: 34개 (기존 16개 + 신규 18개)

---

## 부록 B: 주요 명령어 요약

### 개발 환경 설정
```bash
# 가상환경 생성 및 활성화
cd backend
python -m venv venv
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 데이터베이스 설정
```bash
# 환경 변수 파일 생성
create_env.bat

# PostgreSQL 데이터베이스 생성 (psql)
psql -U postgres -c "CREATE DATABASE orderbean_db;"

# 테이블 생성
python init_db.py

# 샘플 데이터 생성
python seed_db.py

# 연결 테스트
python test_db_connection.py

# 데이터베이스 리셋 (개발 중)
python init_db.py reset
```

### 서버 실행 및 테스트
```bash
# 서버 실행 (방법 1: 배치 파일)
start_server.bat

# 서버 실행 (방법 2: 직접 명령)
python -m uvicorn app.main:app --reload

# API 테스트
python test_server.py

# 단위 테스트 실행
pytest

# 코드 포맷팅
black app/

# 코드 검사
pylint app/
```

### 유용한 단축 명령
```bash
# 통합 데이터베이스 설정 (한 번에)
setup_database.bat

# 데이터만 삭제 (테이블 유지)
python seed_db.py clear

# 모든 테이블 삭제
python init_db.py drop
```

---

## 부록 C: 데이터베이스 테이블 구조

### 생성된 테이블 (5개)

1. **menus** (메뉴)
   - 8개 샘플 데이터
   - 아메리카노, 카페라떼, 카푸치노 등

2. **menu_options** (메뉴 옵션)
   - 31개 샘플 데이터
   - 샷 추가, 휘핑크림, ICE/HOT, 시럽 등

3. **orders** (주문)
   - 빈 테이블 (API 구현 후 사용)

4. **order_items** (주문 항목)
   - 빈 테이블 (API 구현 후 사용)

5. **order_item_options** (주문 항목 옵션)
   - 빈 테이블 (API 구현 후 사용)

### 샘플 메뉴 데이터

| ID | 메뉴명 | 가격 | 재고 | 옵션 수 |
|----|--------|------|------|---------|
| 1 | 아메리카노 | 4,500원 | 100 | 3개 |
| 2 | 카페라떼 | 5,000원 | 100 | 4개 |
| 3 | 카푸치노 | 5,000원 | 100 | 3개 |
| 4 | 바닐라라떼 | 5,500원 | 100 | 4개 |
| 5 | 카라멜 마끼아또 | 6,000원 | 100 | 5개 |
| 6 | 카페모카 | 5,500원 | 100 | 5개 |
| 7 | 그린티 라떼 | 5,500원 | 50 | 4개 |
| 8 | 자몽에이드 | 6,000원 | 50 | 2개 |

---

## 부록 D: API 엔드포인트 현황

### 운영 중인 엔드포인트 ✅

| Method | URL | 설명 | 상태 |
|--------|-----|------|------|
| GET | `/` | API 상태 확인 | ✅ |
| GET | `/health` | 헬스 체크 (DB 상태 포함) | ✅ |
| GET | `/api/v1/test` | 테스트 (DB 정보 포함) | ✅ |
| GET | `/api/v1/db-test` | 데이터베이스 상세 테스트 | ✅ |
| GET | `/api/docs` | Swagger UI | ✅ |
| GET | `/api/redoc` | ReDoc | ✅ |

### 개발 예정 엔드포인트 ⏳

**메뉴 API**
- `GET /api/v1/menus` - 메뉴 목록 조회
- `GET /api/v1/menus/{id}` - 메뉴 상세 조회
- `POST /api/v1/menus` - 메뉴 생성 (관리자)
- `PATCH /api/v1/menus/{id}` - 메뉴 수정 (관리자)
- `DELETE /api/v1/menus/{id}` - 메뉴 삭제 (관리자)

**주문 API**
- `POST /api/v1/orders` - 주문 생성
- `GET /api/v1/orders/{id}` - 주문 조회

**관리자 API**
- `GET /api/v1/admin/orders` - 전체 주문 조회
- `PATCH /api/v1/admin/orders/{id}/status` - 주문 상태 변경
- `GET /api/v1/admin/menus/stock` - 재고 현황

---

**문서 작성일**: 2025년 11월 2일  
**최종 업데이트**: 2025년 11월 2일  
**작성자**: AI Assistant  
**버전**: 2.0  
**주요 변경사항**: 서버 실행 테스트 및 PostgreSQL 데이터베이스 연결 완료  
**다음 업데이트**: API 엔드포인트 구현 완료 후

---

## 📞 연락처 및 지원

**프로젝트 저장소**: https://github.com/kznetwork/OrderBean  
**이슈 보고**: GitHub Issues  
**문서 위치**: `Report/backend-development-environment-setup-report.md`

---

*이 문서는 OrderBean 프로젝트의 백엔드 개발 환경 구축 과정을 상세히 기록한 보고서입니다.*