# OrderBean Backend

FastAPI 기반 커피 주문 관리 시스템 백엔드 API

## 기술 스택

- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ with asyncpg
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (JSON Web Token)
- **Server**: Uvicorn (ASGI)

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션 진입점
│   ├── api/                 # API 엔드포인트
│   │   └── v1/
│   ├── models/              # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── services/            # 비즈니스 로직
│   ├── core/                # 설정 및 데이터베이스
│   └── utils/               # 유틸리티 함수
├── tests/                   # 테스트 파일
├── alembic/                 # 데이터베이스 마이그레이션
├── requirements.txt         # Python 패키지 의존성
├── .env.example             # 환경 변수 예시
└── README.md
```

## 시작하기

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집 (필요한 경우)
```

### 4. 서버 실행

```bash
# 개발 서버 실행 (핫 리로드 활성화)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 또는
python -m uvicorn app.main:app --reload
```

### 5. API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API 엔드포인트

### 기본 엔드포인트

- `GET /` - API 상태 확인
- `GET /health` - 헬스 체크
- `GET /api/v1/test` - 테스트 엔드포인트

### 향후 구현 예정

- `GET /api/v1/menus` - 메뉴 목록 조회
- `POST /api/v1/orders` - 주문 생성
- `GET /api/v1/admin/orders` - 관리자 주문 조회

## 개발

### 코드 포맷팅

```bash
# Black으로 코드 포맷팅
black app/

# Pylint로 코드 검사
pylint app/
```

### 테스트 실행

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app tests/
```

## 배포

### Render 배포

1. GitHub 저장소와 연결
2. 환경 변수 설정
3. 빌드 명령어: `pip install -r requirements.txt`
4. 시작 명령어: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 라이선스

MIT License

