# Backend 개발 환경 구축 보고서

**프로젝트**: OrderBean  
**작업일**: 2025년 11월 2일  
**작업자**: AI Assistant  
**작업 내용**: FastAPI + Python 백엔드 개발 환경 구축

---

## 📋 목차

1. [작업 개요](#1-작업-개요)
2. [백엔드 PRD 작성](#2-백엔드-prd-작성)
3. [프로젝트 구조 생성](#3-프로젝트-구조-생성)
4. [주요 파일 설명](#4-주요-파일-설명)
5. [개발 환경 설정 가이드](#5-개발-환경-설정-가이드)
6. [다음 단계](#6-다음-단계)

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

## 6. 다음 단계

### 6.1 즉시 진행 가능한 작업

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

### 6.2 단계별 개발 계획

#### Phase 1: 데이터베이스 설정 (1-2일)

- [ ] PostgreSQL 설치 및 데이터베이스 생성
- [ ] SQLAlchemy 데이터베이스 연결 설정
- [ ] 모델 정의 (Menus, Options, Orders, OrderItems)
- [ ] Alembic 마이그레이션 초기화
- [ ] 초기 마이그레이션 생성 및 적용
- [ ] 시드 데이터 작성

**예상 작업 파일**
- `app/core/database.py`: 데이터베이스 연결 설정
- `app/core/config.py`: 환경 변수 관리
- `app/models/menu.py`: Menu 모델
- `app/models/option.py`: Option 모델
- `app/models/order.py`: Order 모델
- `app/models/order_item.py`: OrderItem 모델

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

### 6.3 참고 문서

- **백엔드 PRD**: `Docs/Backend_PRD.md`
- **FastAPI 공식 문서**: https://fastapi.tiangolo.com
- **SQLAlchemy 문서**: https://docs.sqlalchemy.org
- **Alembic 문서**: https://alembic.sqlalchemy.org

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

- [x] 백엔드 PRD 문서 작성
- [x] 프로젝트 디렉토리 구조 생성
- [x] `requirements.txt` 작성
- [x] `app/main.py` 작성 (기본 엔드포인트)
- [x] `README.md` 작성
- [x] 환경 변수 예시 파일 작성
- [x] `.gitignore` 작성

### 대기 중인 작업 ⏳

- [ ] Python 가상환경 설정
- [ ] 패키지 설치
- [ ] 서버 실행 및 접속 테스트
- [ ] 데이터베이스 연결 설정
- [ ] SQLAlchemy 모델 정의
- [ ] API 엔드포인트 구현
- [ ] 테스트 작성

---

## 9. 결론

FastAPI + Python 기반 백엔드 개발을 위한 기본 환경 구축을 완료했습니다.

### 9.1 달성한 목표

1. ✅ **체계적인 프로젝트 구조**: 확장 가능하고 유지보수가 쉬운 디렉토리 구조
2. ✅ **상세한 PRD 문서**: 데이터 모델, API 설계, 비즈니스 로직 정의
3. ✅ **즉시 실행 가능한 코드**: 기본 FastAPI 애플리케이션과 테스트 엔드포인트
4. ✅ **개발 가이드 문서**: 설치부터 실행까지 단계별 가이드

### 9.2 다음 작업자를 위한 메모

1. **가상환경 설정 필수**: 프로젝트 격리를 위해 반드시 가상환경 사용
2. **환경 변수 관리**: `.env` 파일은 Git에 커밋하지 않기 (`.gitignore`에 포함됨)
3. **API 문서 활용**: Swagger UI (`/api/docs`)를 통해 API 테스트 가능
4. **코드 포맷팅**: Black, Pylint 사용 권장
5. **테스트 작성**: pytest로 단위 테스트 및 통합 테스트 작성

### 9.3 예상 개발 일정

- **Phase 1 (데이터베이스)**: 1-2일
- **Phase 2 (메뉴 API)**: 2-3일
- **Phase 3 (주문 API)**: 3-4일
- **Phase 4 (관리자 API)**: 2-3일
- **Phase 5 (배포)**: 1-2일
- **총 예상 기간**: 약 2-3주

---

## 부록 A: 생성된 파일 목록

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── env_example.txt
├── .gitignore
└── README.md
```

**총 파일 수**: 16개

---

## 부록 B: 주요 명령어 요약

```bash
# 가상환경 생성 및 활성화
cd backend
python -m venv venv
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload

# 테스트 실행
pytest

# 코드 포맷팅
black app/

# 코드 검사
pylint app/
```

---

**문서 작성일**: 2025년 11월 2일  
**작성자**: AI Assistant  
**버전**: 1.0  
**다음 업데이트**: 서버 실행 테스트 완료 후

//**