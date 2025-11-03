# OrderBean 문제 해결 가이드

## 문제: "메뉴를 불러오는데 실패했습니다"

이 오류는 프론트엔드가 백엔드 API에서 메뉴 데이터를 가져오지 못할 때 발생합니다.

---

## 해결 방법

### 1단계: 백엔드 서버 확인

백엔드 서버가 실행 중인지 확인하세요.

**PowerShell에서 실행:**
```powershell
# backend 디렉토리로 이동
cd backend

# UTF-8 인코딩 설정
$env:PYTHONIOENCODING='utf-8'

# 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**예상 출력:**
```
INFO:     Will watch for changes in these directories: ['C:\\DEV\\Cursor_pro\\OrderBean\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
🚀 OrderBean API 서버 시작 중...
📊 데이터베이스: localhost:5432/orderbean_db
✅ 데이터베이스 연결 성공!
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2단계: 백엔드 API 테스트

브라우저에서 다음 URL을 열어 API가 작동하는지 확인하세요:
- http://localhost:8000/ (기본 정보)
- http://localhost:8000/api/docs (Swagger 문서)
- http://localhost:8000/api/v1/menus (메뉴 목록)

**메뉴 API 응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "price": 4500,
      ...
    }
  ]
}
```

### 3단계: 프론트엔드 환경 변수 확인

`frontend/.env.local` 파일이 있는지 확인하고, 없으면 생성하세요:

```env
VITE_API_URL=http://localhost:8000
```

### 4단계: 프론트엔드 서버 재시작

환경 변수를 변경한 후에는 반드시 프론트엔드 서버를 재시작해야 합니다.

```powershell
# 기존 서버 중지 (Ctrl+C)
# frontend 디렉토리로 이동
cd frontend

# 서버 재시작
npm run dev
```

### 5단계: 브라우저 콘솔 확인

브라우저에서 F12를 눌러 개발자 도구를 열고 Console 탭에서 에러 메시지를 확인하세요.

**일반적인 에러 메시지:**

#### 에러 1: Network Error
```
Network Error: connect ECONNREFUSED 127.0.0.1:8000
```
**원인**: 백엔드 서버가 실행되지 않음  
**해결**: 1단계로 돌아가 백엔드 서버 실행

#### 에러 2: CORS Error
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/menus' from origin 'http://localhost:5173' has been blocked by CORS policy
```
**원인**: CORS 설정 문제  
**해결**: 백엔드의 CORS 설정 확인 (아래 참조)

#### 에러 3: 404 Not Found
```
GET http://localhost:8000/api/v1/menus 404 (Not Found)
```
**원인**: API 엔드포인트가 잘못되었거나 서버 라우팅 문제  
**해결**: API 엔드포인트 URL 확인

---

## CORS 문제 해결

백엔드의 CORS 설정을 확인하세요.

**파일**: `backend/app/main.py`

```python
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # 또는 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**파일**: `backend/.env`

```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 데이터베이스 연결 확인

백엔드가 데이터베이스에 연결할 수 없는 경우도 메뉴를 불러올 수 없습니다.

```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py
```

**예상 출력:**
```
✅ 연결 성공!
✅ PostgreSQL 18.0
✅ 현재 데이터베이스: orderbean_db
✅ 발견된 테이블:
   - menus
   - menu_options
   - orders
   - order_items
   - order_item_options
✅ 메뉴 개수: 5
```

데이터베이스 연결에 실패하면 [DATABASE_SETUP.md](backend/DATABASE_SETUP.md)를 참조하세요.

---

## 메뉴 데이터 확인

데이터베이스에 메뉴 데이터가 있는지 확인하세요.

```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python -c "from sqlalchemy import create_engine, text; from app.core.config import settings; engine = create_engine(settings.DATABASE_URL.replace('asyncpg', 'psycopg2')); with engine.connect() as conn: result = conn.execute(text('SELECT COUNT(*) FROM menus')); print(f'메뉴 개수: {result.scalar()}')"
```

메뉴가 없다면 샘플 데이터를 생성하세요:

```powershell
cd backend
python seed_db.py
```

---

## 포트 충돌 확인

다른 애플리케이션이 8000번 포트를 사용하고 있는지 확인하세요.

**Windows PowerShell:**
```powershell
# 8000번 포트를 사용하는 프로세스 확인
netstat -ano | findstr :8000
```

포트가 사용 중이면:
1. 해당 프로세스 종료
2. 또는 다른 포트 사용 (예: 8001)

**다른 포트로 백엔드 실행:**
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**프론트엔드 환경 변수 수정:**
```env
VITE_API_URL=http://localhost:8001
```

---

## 빠른 체크리스트

문제 해결을 위한 빠른 체크리스트:

- [ ] PostgreSQL 데이터베이스가 실행 중입니까?
- [ ] 백엔드 서버가 실행 중입니까? (http://localhost:8000)
- [ ] 백엔드 API가 응답합니까? (http://localhost:8000/api/v1/menus)
- [ ] 프론트엔드 `.env.local` 파일이 있습니까?
- [ ] 프론트엔드 서버를 재시작했습니까?
- [ ] 브라우저 콘솔에 에러가 있습니까?
- [ ] 데이터베이스에 메뉴 데이터가 있습니까?

---

## 여전히 문제가 해결되지 않나요?

### 완전 초기화 방법

```powershell
# 1. 모든 서버 중지 (Ctrl+C)

# 2. 백엔드 재시작
cd backend
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. 새 터미널에서 프론트엔드 재시작
cd frontend
npm run dev

# 4. 브라우저 새로고침 (Ctrl+F5)
```

### 로그 확인

**백엔드 로그 확인:**
- 터미널에서 서버 실행 중 출력되는 모든 메시지 확인
- `INFO`, `WARNING`, `ERROR` 메시지 주의 깊게 확인

**프론트엔드 로그 확인:**
- 브라우저 개발자 도구 (F12) → Console 탭
- Network 탭에서 API 요청 확인
  - Status: 200 (성공), 404 (Not Found), 500 (서버 에러) 등

---

## 문의

여전히 문제가 해결되지 않으면 다음 정보를 포함하여 문의하세요:

1. 백엔드 서버 실행 시 출력 메시지
2. 브라우저 콘솔의 에러 메시지
3. `test_db_connection.py` 실행 결과
4. 운영체제 및 버전

---

**최종 수정일**: 2025년 11월 3일

