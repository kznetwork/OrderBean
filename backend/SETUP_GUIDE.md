# OrderBean Backend 개발 환경 설정 가이드

## 🎉 설치 완료!

FastAPI 백엔드 서버가 성공적으로 설치 및 실행되었습니다.

## ✅ 설치된 환경

### Python 패키지
```
FastAPI==0.109.0         # 웹 프레임워크
uvicorn==0.27.0          # ASGI 서버
sqlalchemy==2.0.25       # ORM
asyncpg==0.29.0          # PostgreSQL 드라이버
pydantic==2.5.3          # 데이터 검증
python-jose==3.3.0       # JWT 인증
passlib==1.7.4           # 비밀번호 해싱
pytest==7.4.4            # 테스트 프레임워크
```

### 프로젝트 구조
```
backend/
├── app/
│   ├── main.py              # ✅ FastAPI 애플리케이션 (실행 중)
│   ├── api/                 # API 라우터
│   │   └── v1/              # API v1 엔드포인트
│   ├── models/              # 데이터베이스 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── services/            # 비즈니스 로직
│   ├── core/                # 설정 및 유틸리티
│   └── utils/               # 헬퍼 함수
├── tests/                   # 테스트 파일
├── requirements.txt         # Python 의존성
├── setup_dev.bat           # 🆕 개발 환경 설정 스크립트
├── start_server.bat        # 🆕 서버 시작 스크립트
├── test_server.py          # 🆕 서버 테스트 스크립트
└── README.md               # 프로젝트 문서
```

## 🚀 서버 실행 방법

### 방법 1: 배치 파일 사용 (권장)
```bash
# backend 디렉토리에서 실행
start_server.bat
```

### 방법 2: 직접 명령어 실행
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 방법 3: 가상환경 사용
```bash
cd backend

# 가상환경 활성화
venv\Scripts\activate

# 서버 시작
uvicorn app.main:app --reload
```

## 🧪 테스트 방법

### 방법 1: 웹 브라우저
브라우저에서 다음 URL을 방문하세요:
- **메인**: http://localhost:8000/
- **헬스 체크**: http://localhost:8000/health
- **테스트 API**: http://localhost:8000/api/v1/test
- **API 문서**: http://localhost:8000/api/docs

### 방법 2: Python 테스트 스크립트
```bash
# 터미널 1: 서버 실행
start_server.bat

# 터미널 2: 테스트 실행
python test_server.py
```

### 방법 3: curl (PowerShell)
```powershell
# 루트 엔드포인트
Invoke-WebRequest -Uri http://localhost:8000/ | Select-Object -ExpandProperty Content

# 헬스 체크
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content

# 테스트 엔드포인트
Invoke-WebRequest -Uri http://localhost:8000/api/v1/test | Select-Object -ExpandProperty Content
```

## 📚 API 문서

### Swagger UI (인터랙티브)
http://localhost:8000/api/docs

**기능**:
- 모든 API 엔드포인트 목록
- 각 엔드포인트의 파라미터 및 응답 스키마
- 직접 API 테스트 가능 ("Try it out" 버튼)
- 자동 생성된 예시 요청/응답

### ReDoc (읽기 전용)
http://localhost:8000/api/redoc

**기능**:
- 깔끔한 문서 레이아웃
- 검색 기능
- 스키마 탐색

## 🎯 현재 사용 가능한 API 엔드포인트

### 1. 루트 엔드포인트
```
GET /
```
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

### 2. 헬스 체크
```
GET /health
```
**응답 예시**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T16:35:07.005658"
}
```

### 3. 테스트 엔드포인트
```
GET /api/v1/test
```
**응답 예시**:
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

## 🔧 개발 설정

### CORS 설정
현재 다음 출처에서의 요청을 허용합니다:
- http://localhost:5173 (Vite 개발 서버)
- http://localhost:3000 (대체 포트)

추가 출처를 허용하려면 `app/main.py` 파일을 수정하세요.

### 포트 변경
기본 포트 8000을 변경하려면:
```bash
uvicorn app.main:app --reload --port 3000
```

### 디버그 모드
FastAPI는 `--reload` 옵션으로 자동 핫 리로드를 지원합니다.
코드를 수정하면 서버가 자동으로 재시작됩니다.

## 🐛 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001
```

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt --force-reinstall
```

### 가상환경 활성화 오류
```bash
# PowerShell 실행 정책 변경 (관리자 권한 필요)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 다음 단계

### 1. 데이터베이스 설정
- PostgreSQL 설치 및 연결
- 환경 변수 설정 (.env 파일)
- 데이터베이스 마이그레이션 (Alembic)

### 2. API 엔드포인트 개발
- **메뉴 관리 API**
  - `GET /api/v1/menus` - 메뉴 목록 조회
  - `POST /api/v1/menus` - 메뉴 생성 (관리자)
  - `PUT /api/v1/menus/{id}` - 메뉴 수정 (관리자)
  
- **주문 관리 API**
  - `POST /api/v1/orders` - 주문 생성
  - `GET /api/v1/orders/{id}` - 주문 조회
  - `GET /api/v1/admin/orders` - 주문 목록 (관리자)
  - `PATCH /api/v1/admin/orders/{id}/status` - 주문 상태 변경

- **옵션 관리 API**
  - `GET /api/v1/options` - 옵션 목록 조회
  - `POST /api/v1/options` - 옵션 생성 (관리자)

### 3. 인증 시스템 구현
- JWT 토큰 기반 인증
- 관리자 권한 관리
- 비밀번호 암호화

### 4. 테스트 작성
- 단위 테스트 (pytest)
- API 통합 테스트
- 부하 테스트

### 5. 프론트엔드 연동
- React 앱과 API 연결
- 에러 핸들링
- 로딩 상태 관리

## 📞 참고 자료

- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **SQLAlchemy 문서**: https://docs.sqlalchemy.org/
- **Pydantic 문서**: https://docs.pydantic.dev/
- **Uvicorn 문서**: https://www.uvicorn.org/

## ✨ 개발 팁

1. **API 문서 활용**: `/api/docs`에서 실시간으로 API를 테스트할 수 있습니다.
2. **타입 힌팅**: Python 타입 힌팅을 사용하면 자동 검증과 문서 생성이 됩니다.
3. **비동기 처리**: `async/await`를 사용하여 성능을 향상시킬 수 있습니다.
4. **에러 핸들링**: FastAPI의 HTTPException을 활용하세요.
5. **코드 품질**: Black으로 포맷팅, Pylint로 코드 검사를 자동화하세요.

---

**설치 완료일**: 2025년 11월 2일  
**서버 상태**: ✅ 정상 작동  
**다음 업데이트**: 데이터베이스 연결 및 API 엔드포인트 구현

