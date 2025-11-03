# 🖼️ 메뉴 이미지 추가 가이드

## 📋 준비된 이미지 목록

5개의 커피 이미지를 준비하셨다면, 다음 메뉴에 매칭하시면 됩니다:

1. **아메리카노** (Americano)
2. **카페라떼** (Cafe Latte)
3. **카푸치노** (Cappuccino)
4. **바닐라라떼** (Vanilla Latte)
5. **카라멜 마끼아또** (Caramel Macchiato)

---

## 📂 1단계: 이미지 파일 저장

### 저장 위치
```
frontend/public/images/
```

### 파일명 규칙 (권장)
```
americano.jpg (또는 .png)
cafelatte.jpg
cappuccino.jpg
vanillalatte.jpg
caramelmacchiato.jpg
```

**또는 간단하게:**
```
coffee1.jpg
coffee2.jpg
coffee3.jpg
coffee4.jpg
coffee5.jpg
```

### 이미지 저장 방법

**Windows 탐색기에서:**
1. 프로젝트 폴더 열기: `C:\DEV\Cursor_pro\OrderBean`
2. `frontend\public\images` 폴더로 이동
3. 준비한 5개의 이미지 파일을 이 폴더에 복사

**또는 드래그 앤 드롭:**
- VS Code에서 `frontend/public/images` 폴더에 이미지 파일 드래그

---

## 🗄️ 2단계: 데이터베이스에 이미지 경로 업데이트

이미지를 저장한 후, 데이터베이스에 이미지 경로를 업데이트해야 합니다.

### 옵션 A: 자동 업데이트 스크립트 (권장)

`backend` 폴더에 `update_images.py` 파일이 생성됩니다.

**실행 방법:**
```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python update_images.py
```

### 옵션 B: 수동 SQL 실행

데이터베이스 클라이언트(DBeaver, pgAdmin 등)에서:

```sql
-- 아메리카노
UPDATE menus SET image_url = '/images/americano.jpg' WHERE name = '아메리카노';

-- 카페라떼
UPDATE menus SET image_url = '/images/cafelatte.jpg' WHERE name = '카페라떼';

-- 카푸치노
UPDATE menus SET image_url = '/images/cappuccino.jpg' WHERE name = '카푸치노';

-- 바닐라라떼
UPDATE menus SET image_url = '/images/vanillalatte.jpg' WHERE name = '바닐라라떼';

-- 카라멜 마끼아또
UPDATE menus SET image_url = '/images/caramelmacchiato.jpg' WHERE name = '카라멜 마끼아또';
```

---

## 🎨 3단계: 프론트엔드에서 이미지 표시

프론트엔드는 이미 이미지를 표시하도록 구현되어 있습니다!

**현재 코드 (`MenuCard.tsx`):**
```typescript
<div className="menu-image">
  {menu.imageUrl ? (
    <img src={menu.imageUrl} alt={menu.name} />
  ) : (
    <div className="image-placeholder">이미지</div>
  )}
</div>
```

이미지 경로가 설정되면 자동으로 표시됩니다.

---

## ✅ 4단계: 확인

1. **이미지 저장 확인**
   ```
   frontend/public/images/ 폴더에 이미지 파일 있는지 확인
   ```

2. **데이터베이스 업데이트 확인**
   ```powershell
   cd backend
   python update_images.py
   ```
   
   출력:
   ```
   ✅ 아메리카노 이미지 업데이트: /images/americano.jpg
   ✅ 카페라떼 이미지 업데이트: /images/cafelatte.jpg
   ...
   ```

3. **브라우저에서 확인**
   - 프론트엔드 서버가 실행 중인지 확인
   - http://localhost:5173 접속
   - **Ctrl + F5** (강력 새로고침)
   - 메뉴 카드에 이미지가 표시되는지 확인

---

## 🎯 이미지 사양 권장사항

### 파일 크기
- **권장**: 100KB 이하
- **최대**: 500KB

### 해상도
- **권장**: 300x300px 또는 400x400px
- **비율**: 1:1 (정사각형)

### 파일 형식
- **권장**: JPG (용량이 작음)
- **대안**: PNG (투명 배경 필요 시)
- **최신**: WebP (최적 압축)

### 이미지 최적화 (선택사항)
무료 온라인 도구:
- https://tinypng.com (PNG/JPG 압축)
- https://squoosh.app (Google, 다양한 포맷)

---

## 🔧 이미지가 안 보일 때

### 체크리스트

1. **파일 경로 확인**
   ```
   frontend/public/images/americano.jpg ✅
   frontend/images/americano.jpg ❌ (잘못된 위치)
   ```

2. **파일명 확인**
   - 대소문자 구분
   - 공백 없음
   - 특수문자 없음 (영문, 숫자, 하이픈, 언더스코어만)

3. **데이터베이스 확인**
   ```sql
   SELECT name, image_url FROM menus;
   ```
   
   `image_url` 컬럼이 `/images/xxx.jpg` 형식인지 확인

4. **브라우저 캐시 삭제**
   - **Ctrl + Shift + R** (강력 새로고침)
   - 또는 **Ctrl + Shift + Del** → 캐시 삭제

5. **개발자 도구 확인**
   - F12 → Network 탭
   - 이미지 파일 요청 확인
   - 404 에러가 있는지 확인

---

## 📝 예시: 전체 프로세스

### 1. 이미지 파일 준비
```
coffee1.jpg → americano.jpg로 이름 변경
coffee2.jpg → cafelatte.jpg로 이름 변경
coffee3.jpg → cappuccino.jpg로 이름 변경
coffee4.jpg → vanillalatte.jpg로 이름 변경
coffee5.jpg → caramelmacchiato.jpg로 이름 변경
```

### 2. 파일 복사
```
5개의 .jpg 파일을 frontend/public/images/ 폴더에 복사
```

### 3. 데이터베이스 업데이트
```powershell
cd backend
$env:PYTHONIOENCODING='utf-8'
python update_images.py
```

### 4. 확인
```
http://localhost:5173 접속
Ctrl + F5
메뉴 카드에 이미지 표시 확인!
```

---

## 🎨 CSS 스타일링 (이미 적용됨)

메뉴 카드 이미지는 다음과 같이 스타일링되어 있습니다:

```css
.menu-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px 8px 0 0;
}

.menu-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

이미지가 카드에 맞게 자동으로 크롭됩니다.

---

## 🚀 빠른 시작

**가장 간단한 방법:**

1. 이미지 5개를 `frontend/public/images/` 폴더에 복사
   ```
   coffee1.jpg
   coffee2.jpg
   coffee3.jpg
   coffee4.jpg
   coffee5.jpg
   ```

2. 백엔드에서 자동 업데이트 스크립트 실행
   ```powershell
   cd backend
   python update_images.py
   ```

3. 브라우저 새로고침
   ```
   Ctrl + F5
   ```

끝! 🎉

---

## 📞 문제 해결

### 이미지가 깨져 보일 때
- 이미지 파일이 손상되었을 수 있습니다
- 다른 이미지로 교체 시도

### 이미지 로딩이 느릴 때
- 이미지 파일 크기 확인 (100KB 이하 권장)
- 온라인 압축 도구 사용

### 특정 이미지만 안 보일 때
- 파일명 확인
- 데이터베이스의 image_url 확인
- 브라우저 콘솔(F12)에서 404 에러 확인

---

**작성일**: 2025년 11월 3일

