# 🚀 빠른 이미지 추가 가이드 (5분 완성)

## 📸 준비된 5개 이미지를 추가하는 가장 빠른 방법

---

## ✨ 3단계로 완성!

### 1️⃣ 이미지 파일 저장 (1분)

**Windows 탐색기로:**
```
1. 프로젝트 폴더 열기: C:\DEV\Cursor_pro\OrderBean
2. frontend → public → images 폴더 열기
3. 준비한 5개 이미지 복사해서 붙여넣기
```

**파일명 예시:**
```
americano.jpg       (아메리카노)
cafelatte.jpg       (카페라떼)
cappuccino.jpg      (카푸치노)
vanillalatte.jpg    (바닐라라떼)
caramelmacchiato.jpg (카라멜 마끼아또)
```

💡 **또는 간단하게:**
```
coffee1.jpg
coffee2.jpg
coffee3.jpg
coffee4.jpg
coffee5.jpg
```

---

### 2️⃣ 데이터베이스 업데이트 (2분)

**PowerShell에서 실행:**
```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python update_images.py
```

**출력 예시:**
```
✅ 아메리카노 이미지 업데이트: /images/americano.jpg
✅ 카페라떼 이미지 업데이트: /images/cafelatte.jpg
✅ 카푸치노 이미지 업데이트: /images/cappuccino.jpg
✅ 바닐라라떼 이미지 업데이트: /images/vanillalatte.jpg
✅ 카라멜 마끼아또 이미지 업데이트: /images/caramelmacchiato.jpg
```

---

### 3️⃣ 브라우저 확인 (1분)

```
1. http://localhost:5173 접속
2. Ctrl + Shift + R (강력 새로고침)
3. 메뉴 카드에 이미지 표시 확인!
```

---

## 🎯 파일명이 다른 경우

### 옵션 A: 파일명 변경
```
이미지 파일명을 위의 추천 파일명으로 변경
```

### 옵션 B: 사용자 정의 설정
```powershell
cd backend
python update_images.py custom
```

그러면 대화형으로 파일명을 입력할 수 있습니다:
```
아메리카노: my-coffee1.jpg
카페라떼: my-coffee2.jpg
...
```

---

## ✅ 정상 작동 확인

### 메뉴 카드에 이미지가 표시됨
```
✅ 아메리카노 - 이미지 보임
✅ 카페라떼 - 이미지 보임
✅ 카푸치노 - 이미지 보임
✅ 바닐라라떼 - 이미지 보임
✅ 카라멜 마끼아또 - 이미지 보임
```

### 마우스 올리면 확대 효과
```
이미지가 약간 확대되면서 hover 효과 적용
```

---

## 🔧 문제 해결

### 이미지가 안 보일 때

#### 1. 파일 경로 확인
```
frontend/public/images/americano.jpg ✅
frontend/images/americano.jpg ❌
```

#### 2. 브라우저 캐시 삭제
```
Ctrl + Shift + R (강력 새로고침)
```

#### 3. 데이터베이스 확인
```powershell
cd backend
python update_images.py show
```

출력에서 이미지 경로 확인

#### 4. 개발자 도구 확인
```
F12 → Network 탭
404 에러가 있는지 확인
```

---

## 📊 이미지 사양 권장

### 최적 사양
- **크기**: 300x300px 또는 400x400px
- **비율**: 1:1 (정사각형)
- **용량**: 100KB 이하
- **형식**: JPG (권장), PNG, WebP

### 이미지 압축 도구
- https://tinypng.com (무료)
- https://squoosh.app (Google)

---

## 💡 현재 상태 확인

```powershell
cd backend
python update_images.py show
```

**출력 예시:**
```
현재 메뉴 이미지 경로
============================================================

✅ 아메리카노            → /images/americano.jpg
✅ 카페라떼              → /images/cafelatte.jpg
✅ 카푸치노              → /images/cappuccino.jpg
✅ 바닐라라떼            → /images/vanillalatte.jpg
✅ 카라멜 마끼아또       → /images/caramelmacchiato.jpg
❌ 카페모카              → (없음)
❌ 그린티 라떼           → (없음)
❌ 자몽에이드            → (없음)
```

---

## 🎨 스타일 특징

### 이미지 표시
- 카드 상단에 200px 높이로 표시
- 자동으로 카드 크기에 맞게 크롭
- 원본 비율 유지하면서 전체 영역 채움

### 호버 효과
- 마우스 올리면 이미지가 1.05배 확대
- 부드러운 애니메이션 효과
- 카드 전체가 살짝 위로 올라감

### 에러 처리
- 이미지 로드 실패 시 자동으로 플레이스홀더 표시
- "이미지 없음" 메시지 표시

---

## 🎉 완료!

이제 메뉴 카드에 이미지가 아름답게 표시됩니다!

### 테스트해보기
1. 메뉴 카드 위에 마우스 올려보기
2. 이미지 확대 효과 확인
3. 다양한 메뉴 보기

---

**작성일**: 2025년 11월 3일  
**소요 시간**: 5분

