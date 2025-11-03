# 🐛 프론트엔드 화면 깜빡임/오류 해결 가이드

## 문제: 화면이 깜빡이고 아무것도 표시되지 않음

---

## 🔥 즉시 해결 방법

### 1단계: 백엔드 서버 확인

**브라우저에서 열어보세요:**
```
http://localhost:8000/api/v1/menus
```

**정상 응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "price": 4500,
      "options": [...]
    }
  ]
}
```

✅ **위와 같은 JSON이 보이면**: 백엔드 정상  
❌ **에러나 아무것도 안 보이면**: `start_backend.bat` 실행

---

### 2단계: 프론트엔드 서버 재시작

```powershell
# 기존 서버 중지 (Ctrl+C)

cd frontend

# .env.local 파일 생성/확인
echo "VITE_API_URL=http://localhost:8000" > .env.local

# 서버 재시작 (중요!)
npm run dev
```

⚠️ **주의**: 환경 변수(.env.local) 변경 후 반드시 서버 재시작!

---

### 3단계: 브라우저 강력 새로고침

```
Ctrl + Shift + R  (또는 Ctrl + F5)
```

---

## 🔍 브라우저 콘솔 확인 (F12)

### 정상적인 로그:
```
🚀 OrderBean App 시작
📡 API URL: http://localhost:8000
📋 메뉴 로드 시작...
✅ 메뉴 로드 성공: 5 개
```

### 에러 상황별 해결:

#### ❌ "Network Error" / "ERR_CONNECTION_REFUSED"
**원인**: 백엔드 서버가 실행되지 않음

**해결**:
```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

#### ❌ "undefined is not an object" / "Cannot read property"
**원인**: 데이터 구조 불일치 (방금 수정됨)

**해결**:
1. 코드가 최신 버전인지 확인
2. 브라우저 캐시 완전 삭제 (Ctrl+Shift+Del)
3. 프론트엔드 서버 재시작

---

#### ❌ CORS Error
**원인**: CORS 설정 문제

**해결**: 백엔드 서버 재시작

---

## 🧪 디버그 모드로 테스트

임시로 `frontend/src/main.tsx` 파일을 수정하여 디버그 페이지를 표시:

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { DebugPage } from './debug';  // 추가
import './App.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <DebugPage />  {/* App 대신 DebugPage */}
  </React.StrictMode>,
);
```

이렇게 하면 API 연결 상태를 자세히 확인할 수 있습니다.

---

## 📝 체크리스트

문제 해결을 위해 다음을 순서대로 확인하세요:

### 백엔드
- [ ] PostgreSQL 실행 중
- [ ] 백엔드 서버 실행 중 (http://localhost:8000)
- [ ] API 응답 정상 (http://localhost:8000/api/v1/menus)
- [ ] 데이터베이스에 메뉴 데이터 존재 (5개)

### 프론트엔드
- [ ] `.env.local` 파일 존재
- [ ] 환경 변수 `VITE_API_URL=http://localhost:8000` 설정
- [ ] 서버 재시작 완료
- [ ] 브라우저 캐시 삭제

### 브라우저
- [ ] F12 콘솔에 에러 없음
- [ ] Network 탭에서 API 요청 성공 (Status: 200)

---

## 🛠️ 코드 수정 사항 (자동 반영됨)

방금 다음 파일들을 수정했습니다:

1. **`frontend/src/pages/CustomerPage.tsx`**
   - ✅ API 데이터 매핑 수정
   - ✅ 옵션 데이터 구조 수정 (label, price)
   - ✅ 주문 생성 시 option_id 타입 변환
   - ✅ 상세 로깅 추가

2. **`frontend/src/App.tsx`**
   - ✅ 에러 처리 추가
   - ✅ 시작 로그 추가
   - ✅ API URL 표시

3. **`frontend/src/debug.tsx`** (새로 생성)
   - ✅ 디버그 페이지 추가

---

## 🔄 완전 리셋 절차

모든 것이 실패하면:

```powershell
# 1. 모든 터미널/서버 중지

# 2. 백엔드 확인 및 시작
cd backend
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. 새 터미널에서 프론트엔드
cd frontend

# 환경 설정 파일 재생성
Remove-Item .env.local -ErrorAction SilentlyContinue
"VITE_API_URL=http://localhost:8000" | Out-File -FilePath .env.local -Encoding UTF8

# node_modules 재설치 (선택사항)
# Remove-Item -Recurse -Force node_modules
# npm install

# 서버 시작
npm run dev

# 4. 브라우저
# - Ctrl+Shift+Del로 캐시 완전 삭제
# - http://localhost:5173 접속
# - Ctrl+Shift+R로 강력 새로고침
```

---

## 💡 예방 팁

앞으로 이런 문제를 방지하려면:

1. **항상 백엔드부터 시작**
   - 먼저 `start_backend.bat` 실행
   - API가 정상인지 확인 후
   - `start_frontend.bat` 실행

2. **환경 변수 변경 시 재시작**
   - `.env.local` 수정 후 반드시 프론트엔드 서버 재시작

3. **브라우저 캐시 정기 삭제**
   - 개발 중에는 브라우저 개발자 도구에서
   - "Disable cache" 옵션 활성화 (F12 → Network 탭)

---

## 📞 여전히 안 되나요?

다음 정보를 확인해주세요:

1. **백엔드 터미널 출력**
   ```
   ✅ 데이터베이스 연결 성공!
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

2. **프론트엔드 터미널 출력**
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:5173/
   ```

3. **브라우저 콘솔 (F12)**
   - 모든 에러 메시지 복사

4. **브라우저 Network 탭**
   - `/api/v1/menus` 요청의 Status와 Response 확인

---

**최종 수정일**: 2025년 11월 3일

