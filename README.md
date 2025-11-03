# OrderBean ☕

> **바쁜 직장인들을 위한 커피 주문 관리 웹 애플리케이션**

OrderBean은 카페 대기 시간 없이 선주문을 통해 신속하게 커피를 픽업할 수 있도록 돕는 풀스택 웹 애플리케이션입니다.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

## 📋 프로젝트 개요

OrderBean은 고객과 관리자 모두를 위한 직관적인 주문 관리 시스템입니다. 
고객은 웹에서 메뉴를 선택하고 주문하며, 관리자는 실시간으로 주문을 관리할 수 있습니다.

**프로젝트 타입**: Toy Project / Portfolio  
**개발 기간**: 2025년 11월 - 진행 중

## 🎯 주요 기능

### ✅ 구현 완료 (Phase 1)

#### 고객 기능
- ☕ **메뉴 조회**: 카테고리별 메뉴 탐색 및 상세 정보 확인
- 🛒 **장바구니**: 메뉴 추가, 수량 조절, 옵션 선택
- 📦 **주문 생성**: 원클릭 주문 완료
- 🎨 **옵션 커스터마이징**: 샷 추가, 시럽 등 다양한 옵션 선택

#### 관리자 기능
- 📊 **대시보드**: 실시간 주문 통계 및 매출 현황
- 📋 **주문 관리**: 주문 상태 변경 (접수 → 제조 → 완료)
- 📦 **재고 관리**: 메뉴별 재고 수량 조절
- 📈 **통계 분석**: 시간대별, 메뉴별 판매 통계

### 🔜 Phase 2 예정
- 🔐 인증 시스템 (회원가입/로그인)
- ⭐ 즐겨찾기 기능
- 📱 QR 코드 생성
- 🔔 실시간 알림 (WebSocket)

## 🛠️ 기술 스택

### Frontend
- **React 18+** + TypeScript
- **Vite** (빌드 도구)
- **Zustand** (상태 관리)
- **Axios** (HTTP 클라이언트)
- **CSS3** (스타일링)

### Backend
- **Python 3.11+**
- **FastAPI** (비동기 웹 프레임워크)
- **SQLAlchemy 2.0** (ORM)
- **PostgreSQL 15+** (데이터베이스)
- **Alembic** (마이그레이션)
- **Uvicorn** (ASGI 서버)

### DevOps
- **Git** / **GitHub**
- **Render** (배포 예정)

## 📦 설치 및 실행

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 1. 저장소 클론
```bash
git clone https://github.com/kznetwork/OrderBean.git
cd OrderBean
```

### 2. 백엔드 설정 및 실행

```bash
# backend 디렉토리로 이동
cd backend

# Python 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
# .env 파일을 생성하고 데이터베이스 정보 입력

# 데이터베이스 연결 테스트 (Windows PowerShell)
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py

# 서버 실행
$env:PYTHONIOENCODING='utf-8'
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**백엔드 주소**:
- API: http://localhost:8000
- Swagger 문서: http://localhost:8000/api/docs
- ReDoc 문서: http://localhost:8000/api/redoc

### 3. 프런트엔드 설정 및 실행

```bash
# frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**프런트엔드 주소**: http://localhost:5173

## 🚀 빠른 시작

1. PostgreSQL 데이터베이스가 실행 중인지 확인
2. 백엔드 서버 실행 (터미널 1)
3. 프런트엔드 서버 실행 (터미널 2)
4. 브라우저에서 http://localhost:5173 접속
5. 고객 페이지에서 메뉴를 확인하고 주문
6. 관리자 페이지에서 주문 관리

## 📚 문서

- [PRD (제품 요구사항 문서)](Docs/PRD_Up1.md)
- [API 및 프런트엔드 연동 가이드](API_FRONTEND_INTEGRATION_GUIDE.md)
- [백엔드 개발 가이드](backend/README.md)
- [데이터베이스 설정 가이드](backend/DATABASE_SETUP.md)

## 📁 프로젝트 구조

```
OrderBean/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   │   └── v1/
│   │   │       ├── menus.py      # 메뉴 API
│   │   │       ├── orders.py     # 주문 API
│   │   │       └── admin.py      # 관리자 API
│   │   ├── models/         # SQLAlchemy 모델
│   │   ├── schemas/        # Pydantic 스키마
│   │   ├── core/           # 설정 및 데이터베이스
│   │   └── main.py         # FastAPI 앱
│   ├── alembic/            # 데이터베이스 마이그레이션
│   └── requirements.txt    # Python 의존성
│
├── frontend/               # React 프런트엔드
│   ├── src/
│   │   ├── components/    # React 컴포넌트
│   │   │   ├── customer/  # 고객 페이지 컴포넌트
│   │   │   └── admin/     # 관리자 페이지 컴포넌트
│   │   ├── services/      # API 서비스
│   │   ├── stores/        # Zustand 스토어
│   │   ├── pages/         # 페이지 컴포넌트
│   │   └── types/         # TypeScript 타입
│   └── package.json       # npm 의존성
│
└── Docs/                  # 프로젝트 문서
```

## 🔗 주요 API 엔드포인트

### 메뉴 관리
- `GET /api/v1/menus` - 메뉴 목록 조회
- `GET /api/v1/menus/{id}` - 메뉴 상세 조회
- `POST /api/v1/menus` - 메뉴 생성 (관리자)
- `PUT /api/v1/menus/{id}` - 메뉴 수정 (관리자)
- `DELETE /api/v1/menus/{id}` - 메뉴 삭제 (관리자)

### 주문 관리
- `POST /api/v1/orders` - 주문 생성
- `GET /api/v1/orders` - 주문 목록 조회
- `GET /api/v1/orders/{id}` - 주문 상세 조회
- `PUT /api/v1/orders/{id}/status` - 주문 상태 변경 (관리자)

### 관리자 기능
- `GET /api/v1/admin/dashboard` - 대시보드 요약
- `GET /api/v1/admin/orders` - 전체 주문 조회
- `GET /api/v1/admin/statistics` - 통계 조회
- `GET /api/v1/admin/inventory` - 재고 현황
- `PUT /api/v1/admin/inventory/{id}` - 재고 업데이트

상세 API 문서는 서버 실행 후 http://localhost:8000/api/docs 에서 확인할 수 있습니다.

## 🎨 스크린샷

### 고객 페이지
- 메뉴 목록 및 장바구니
- 주문 옵션 선택

### 관리자 페이지
- 실시간 대시보드
- 주문 관리
- 재고 관리

## 🐛 알려진 이슈

1. 인증 시스템이 아직 구현되지 않음
2. WebSocket 실시간 알림 대신 30초 polling 사용
3. 즐겨찾기 기능 미구현
4. QR 코드 생성 미구현

## 🤝 기여

이 프로젝트는 개인 학습 목적으로 제작되었습니다.

## 📝 라이선스

이 프로젝트는 개인 학습 목적의 Toy Project입니다.

## 👤 작성자

kznetwork

## 📅 프로젝트 시작일

2025년 11월 2일


