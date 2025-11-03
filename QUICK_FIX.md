# 🚨 긴급 문제 해결 - "메뉴를 불러오는데 실패했습니다"

## 🔧 빠른 해결 방법

### 방법 1: 자동 실행 스크립트 사용 (권장)

**1단계: 백엔드 서버 시작**
```
start_backend.bat 파일을 더블클릭
```

**2단계: 프론트엔드 서버 시작 (새 터미널)**
```
start_frontend.bat 파일을 더블클릭
```

**3단계: 브라우저 새로고침**
- http://localhost:5173 에서 Ctrl+F5 (강력 새로고침)

---

### 방법 2: 수동 실행

#### PowerShell 터미널 1 - 백엔드
```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### PowerShell 터미널 2 - 프론트엔드
```powershell
cd frontend

# .env.local 파일 생성 (처음 한 번만)
echo "VITE_API_URL=http://localhost:8000" > .env.local

# 서버 시작
npm run dev
```

---

## ✅ 확인 사항

실행 후 다음을 확인하세요:

### 1. 백엔드 서버 확인
브라우저에서 열기:
- http://localhost:8000 → "OrderBean API Server" 메시지 표시
- http://localhost:8000/api/v1/menus → 메뉴 JSON 데이터 표시

**정상 응답 예시:**
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

### 2. 프론트엔드 서버 확인
- http://localhost:5173 접속
- 메뉴 카드가 표시되어야 함

---

## 🐛 여전히 안 되나요?

### 체크리스트

- [ ] PostgreSQL이 실행 중인가요?
  ```powershell
  # 서비스 확인
  Get-Service -Name postgresql*
  ```

- [ ] 백엔드 서버가 정상 실행되나요?
  - "✅ 데이터베이스 연결 성공!" 메시지 확인

- [ ] 포트 8000이 사용 가능한가요?
  ```powershell
  # 8000번 포트 확인
  netstat -ano | findstr :8000
  ```

- [ ] 메뉴 데이터가 있나요?
  ```powershell
  cd backend
  $env:PYTHONIOENCODING='utf-8'
  python test_db_connection.py
  ```
  출력에서 "✅ 메뉴 개수: 5" 확인

---

## 🔄 완전 리셋

모든 것이 실패하면 완전히 재시작:

```powershell
# 1. 모든 터미널 닫기 (Ctrl+C)

# 2. 데이터베이스 확인
cd backend
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py

# 3. 백엔드 시작 (터미널 1)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. 프론트엔드 시작 (터미널 2)
cd frontend
Remove-Item .env.local -ErrorAction SilentlyContinue
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev

# 5. 브라우저에서 Ctrl+Shift+Del로 캐시 삭제 후 재접속
```

---

## 📞 에러 메시지별 해결

### "Network Error"
→ 백엔드 서버가 실행되지 않음. `start_backend.bat` 실행

### "CORS policy"
→ 백엔드 서버 재시작 필요

### "404 Not Found"
→ API URL 확인: `frontend/.env.local`에 `VITE_API_URL=http://localhost:8000` 추가

### "메뉴를 불러오는데 실패했습니다"
→ 위의 모든 단계 확인

---

**작성일**: 2025년 11월 3일

