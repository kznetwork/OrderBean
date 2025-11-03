# OrderBean Backend 빠른 시작 가이드 🚀

## ✅ 사전 준비 확인

- [x] Python 3.11+ 설치
- [x] PostgreSQL 15+ 설치
- [x] Git 설치

---

## 🎯 3단계로 시작하기

### 1️⃣ 환경 변수 설정

```bash
cd backend
create_env.bat
```

`.env` 파일이 자동 생성됩니다:
- DB_HOST=localhost
- DB_PORT=5432
- DB_NAME=orderbean_db
- DB_USER=postgres
- DB_PASSWORD=postgresql

### 2️⃣ 데이터베이스 초기화

```bash
# PostgreSQL에서 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE orderbean_db;"

# 테이블 생성
python init_db.py

# 샘플 데이터 생성 (선택사항)
python seed_db.py
```

### 3️⃣ 서버 시작

```bash
# 방법 1: 배치 파일
start_server.bat

# 방법 2: 직접 명령
python -m uvicorn app.main:app --reload
```

---

## 🧪 테스트

### 브라우저에서 접속

1. **API 메인**: http://localhost:8000/
2. **헬스 체크**: http://localhost:8000/health
3. **DB 테스트**: http://localhost:8000/api/v1/db-test
4. **API 문서**: http://localhost:8000/api/docs

### Python 스크립트로 테스트

```bash
python test_db_connection.py
```

---

## 📚 주요 파일

| 파일 | 설명 |
|------|------|
| `create_env.bat` | 환경 변수 파일 생성 |
| `init_db.py` | 데이터베이스 테이블 생성 |
| `seed_db.py` | 샘플 데이터 생성 |
| `test_db_connection.py` | 데이터베이스 연결 테스트 |
| `start_server.bat` | 서버 시작 |
| `setup_database.bat` | 통합 설정 스크립트 |

---

## 🔧 자주 사용하는 명령어

```bash
# 데이터베이스 초기화 (리셋)
python init_db.py reset

# 데이터 삭제
python seed_db.py clear

# 연결 테스트
python test_db_connection.py

# 서버 시작
start_server.bat

# 패키지 설치
pip install -r requirements.txt
```

---

## 💡 문제 해결

### PostgreSQL 연결 오류
```bash
# 서비스 시작 (Windows)
net start postgresql-x64-15

# 상태 확인
pg_ctl status
```

### 포트 사용 중
```bash
# 다른 포트로 실행
python -m uvicorn app.main:app --reload --port 8001
```

### 패키지 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 재설치
pip install -r requirements.txt --force-reinstall
```

---

## 📖 자세한 문서

- **전체 설정 가이드**: `SETUP_GUIDE.md`
- **데이터베이스 가이드**: `DATABASE_SETUP.md`
- **프로젝트 README**: `README.md`

---

## 🎉 설정 완료!

모든 설정이 완료되었습니다. 이제 API 개발을 시작할 수 있습니다!

**다음 단계**:
1. API 엔드포인트 개발 (메뉴, 주문 관리)
2. 프론트엔드 연동
3. 배포 준비

---

**작성일**: 2025년 11월 2일
