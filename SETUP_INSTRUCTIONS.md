# 🚀 OrderBean 데이터베이스 설정 완료!

PostgreSQL 데이터베이스 설정이 준비되었습니다. 이제 아래 단계를 따라 프로젝트를 실행하세요.

## ✅ 완료된 작업

1. ✅ `.env` 파일 생성 (데이터베이스 설정 포함)
2. ✅ `requirements.txt` 업데이트 (psycopg2-binary 추가)
3. ✅ 데이터베이스 생성 스크립트 작성 (`create_database.py`)
4. ✅ 완전 자동 설치 스크립트 작성 (`setup_complete.bat`)
5. ✅ 상세 설정 가이드 작성 (`DATABASE_SETUP_GUIDE.md`)

## 🎯 빠른 시작 (권장)

### 방법 1: 자동 설치 스크립트 사용

PowerShell 또는 CMD를 열고:

```powershell
cd C:\DEV\Cursor_pro\OrderBean\backend
setup_complete.bat
```

이 스크립트는 자동으로:
1. Python 가상환경 생성
2. 필요한 패키지 설치
3. PostgreSQL 데이터베이스 생성
4. 테이블 및 샘플 데이터 생성
5. 연결 테스트

### 방법 2: 수동 설치

#### 1단계: 가상환경 생성 및 활성화

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
```

**PowerShell 오류 발생 시**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2단계: 패키지 설치

```powershell
pip install -r requirements.txt
```

#### 3단계: PostgreSQL 서비스 확인

1. `Windows + R` → `services.msc`
2. `postgresql` 서비스 찾기
3. 실행 중인지 확인 (중지되어 있으면 시작)

#### 4단계: 데이터베이스 생성

```powershell
python create_database.py
```

#### 5단계: 테이블 생성 및 샘플 데이터

```powershell
python init_database.py
```

#### 6단계: 연결 테스트

```powershell
python test_db_connection.py
```

## 🚀 서버 실행

### 백엔드 서버

```powershell
# 방법 1: 배치 파일 사용
start_dev.bat

# 방법 2: 직접 실행
uvicorn app.main:app --reload
```

서버 주소:
- 🌐 API: http://localhost:8000
- 📚 문서: http://localhost:8000/api/docs
- ❤️ 헬스체크: http://localhost:8000/health

### 프론트엔드 (선택사항)

**새 터미널**을 열고:

```powershell
cd frontend
npm install    # 처음 한 번만
npm run dev
```

프론트엔드: http://localhost:5173

## 📊 생성된 샘플 데이터

### 메뉴 (5개)
1. 아메리카노 - 4,000원
2. 카페라떼 - 4,500원
3. 카푸치노 - 4,500원
4. 바닐라 라떼 - 5,000원
5. 카라멜 마키아또 - 5,500원

### 각 메뉴별 옵션
- 사이즈: Regular, Large (+500원)
- 샷 추가: 1샷 (+500원), 2샷 (+1,000원)
- 온도: HOT, ICE

### 테스트 주문
- 1개의 샘플 주문 포함

## 🔧 데이터베이스 설정 정보

`.env` 파일에 다음과 같이 설정되어 있습니다:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=postgresql
```

## 🧪 API 테스트

### Swagger UI 사용

http://localhost:8000/api/docs 에서:

1. **메뉴 조회**
   - `GET /api/v1/menus`
   - "Try it out" → "Execute"

2. **주문 생성**
   - `POST /api/v1/orders`
   - 예제 데이터:
   ```json
   {
     "items": [
       {
         "menu_id": 1,
         "quantity": 2,
         "options": [{"option_id": 1}]
       }
     ]
   }
   ```

3. **주문 상태 변경**
   - `PUT /api/v1/orders/{order_id}/status`
   - 상태: `pending`, `preparing`, `completed`, `cancelled`

## ❓ 문제 해결

### PostgreSQL 연결 실패

1. PostgreSQL 서비스 실행 확인
2. `.env` 파일의 비밀번호 확인
3. 포트 5432가 사용 중인지 확인

### 패키지 설치 오류

```powershell
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt --upgrade
```

### 데이터베이스 생성 권한 오류

pgAdmin 또는 psql을 사용하여 수동으로 생성:

```sql
CREATE DATABASE orderbean_db;
```

## 📚 추가 문서

- `backend/DATABASE_SETUP_GUIDE.md` - 상세 설정 가이드
- `QUICK_START.md` - 프로젝트 실행 가이드
- `README_API_INTEGRATION.md` - API 통합 가이드

## 🎉 다음 단계

1. ✅ 데이터베이스 설정 완료
2. 🔄 백엔드 서버 시작
3. 🔄 프론트엔드 시작
4. 🔄 기능 테스트
5. 🔄 개발 시작!

## 💡 유용한 명령어

```powershell
# 데이터베이스 재설정
python init_database.py

# 추가 샘플 데이터 생성
python seed_sample_data.py

# 연결 테스트
python test_db_connection.py

# 서버 시작
uvicorn app.main:app --reload
```

---

**설정 완료 날짜**: 2025년 11월 3일  
**프로젝트**: OrderBean  
**데이터베이스**: PostgreSQL (orderbean_db)

궁금한 점이 있으시면 `backend/DATABASE_SETUP_GUIDE.md` 문서를 참고하세요! 🚀

