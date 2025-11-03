# 🔗 OrderBean API 테스트 URL 모음

서버가 실행 중일 때 브라우저에서 바로 클릭하여 테스트할 수 있는 URL 목록입니다.

---

## ✅ 기본 엔드포인트

### 1. 루트 - API 정보
**URL**: http://localhost:8000/

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

---

### 2. 헬스 체크
**URL**: http://localhost:8000/health

**응답 예시**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T16:35:07.005658"
}
```

---

### 3. 테스트 엔드포인트
**URL**: http://localhost:8000/api/v1/test

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

---

## 📚 API 문서

### Swagger UI (추천!)
**URL**: http://localhost:8000/api/docs

**특징**:
- 인터랙티브한 API 문서
- "Try it out" 버튼으로 직접 테스트 가능
- 요청/응답 스키마 자동 표시
- OAuth2 인증 테스트 가능 (향후)

---

### ReDoc
**URL**: http://localhost:8000/api/redoc

**특징**:
- 깔끔하고 읽기 쉬운 문서
- 왼쪽 사이드바로 빠른 네비게이션
- 코드 예제 자동 생성

---

## 🧪 테스트 방법

### 방법 1: 브라우저에서 직접 접속
위의 URL을 브라우저 주소창에 입력하여 GET 요청 테스트

### 방법 2: PowerShell 사용
```powershell
# 기본 요청
Invoke-WebRequest -Uri http://localhost:8000/health

# JSON 응답만 보기
(Invoke-WebRequest -Uri http://localhost:8000/health).Content | ConvertFrom-Json

# 보기 좋게 출력
Invoke-WebRequest -Uri http://localhost:8000/api/v1/test | Select-Object -ExpandProperty Content
```

### 방법 3: Python 스크립트
```bash
python test_server.py
```

### 방법 4: curl (Git Bash 또는 WSL)
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/test
```

---

## 📊 테스트 체크리스트

- [✅] `http://localhost:8000/` - 루트 엔드포인트
- [ ] `http://localhost:8000/health` - 헬스 체크
- [ ] `http://localhost:8000/api/v1/test` - 테스트 엔드포인트
- [ ] `http://localhost:8000/api/docs` - Swagger UI 문서
- [ ] `http://localhost:8000/api/redoc` - ReDoc 문서

모든 항목이 정상적으로 응답하면 ✅ 표시하세요!

---

## 🎯 다음 테스트할 URL

위의 체크리스트를 순서대로 브라우저에서 테스트해보세요:

1. ✅ **완료** - http://localhost:8000/
2. 👉 **다음** - http://localhost:8000/health
3. http://localhost:8000/api/v1/test
4. http://localhost:8000/api/docs (가장 중요!)
5. http://localhost:8000/api/redoc

---

## 💡 Swagger UI 사용법

1. http://localhost:8000/api/docs 접속
2. 테스트할 엔드포인트 클릭 (예: `GET /health`)
3. "Try it out" 버튼 클릭
4. "Execute" 버튼 클릭
5. 응답 확인:
   - Response body: JSON 응답
   - Response headers: HTTP 헤더
   - Response code: 상태 코드 (200, 404 등)

---

**모든 URL이 정상 작동하면 개발 환경 설정이 완료된 것입니다! 🎉**

