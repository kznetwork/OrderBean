# OrderBean 프로젝트 요구사항 명세서 (PRD)

**버전**: 1.0  
**작성일**: 2025년 11월 2일  
**작성자**: kznetwork  
**프로젝트 타입**: Toy Project / Portfolio

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [문제 진술문](#문제-진술문)
3. [아이디어 브레인스토밍](#아이디어-브레인스토밍)
4. [기능적 요구사항](#기능적-요구사항)
5. [데이터 모델](#데이터-모델)
6. [API 개요](#api-개요)
7. [사용자 스토리 (Gherkin)](#사용자-스토리-gherkin)
8. [비기능적 요구사항](#비기능적-요구사항)
9. [기술 스택 및 로드맵](#기술-스택-및-로드맵)

---

## 🎯 프로젝트 개요

OrderBean은 바쁜 직장인들이 시간을 절약할 수 있도록 돕는 커피 주문 웹 앱입니다. 사용자는 커피 메뉴를 주문하고, 관리자는 주문을 관리할 수 있는 간단한 풀스택 웹 애플리케이션입니다.

---

## 📌 문제 진술문

**"바쁜 직장인들이 카페 대기 시간 없이 선주문을 통해 신속하게 커피를 픽업할 수 있도록 하고, 관리자는 실시간으로 주문을 접수하고 처리 상태를 관리할 수 있는 직관적인 웹 기반 주문 관리 시스템이 필요하다."**

### 핵심 요소
- **대상 사용자**: 바쁜 직장인들
- **해결하는 문제**: 카페 대기 시간
- **사용자 기능**: 선주문 및 신속한 픽업
- **관리자 기능**: 실시간 주문 접수 및 처리 상태 관리
- **솔루션**: 직관적인 웹 기반 주문 관리 시스템

---

## 💡 아이디어 브레인스토밍

### 1️⃣ 스마트 커피 선주문 플랫폼 ⭐ (선택)

**해결하는 문제:**
- 바쁜 아침 시간대 카페 대기 줄이 길어 시간을 낭비하는 문제
- 원하는 커스터마이징 옵션을 카운터에서 설명하기 어려운 문제
- 카페 혼잡도를 미리 알 수 없어 방문 시간을 계획하기 어려운 문제

**대상 사용자:**
- 출근길 직장인 (20-40대)
- 시간이 촉박한 대학생
- 대기 시간을 줄이고 싶은 모든 카페 이용객
- 소규모 독립 카페 운영자

**주요 기능:**
1. **실시간 선주문 및 픽업 시간 예약** - GPS 기반으로 근처 카페 검색 및 미리 주문
2. **나만의 커스텀 레시피 저장** - 자주 주문하는 음료의 커스터마이징 옵션 저장 (얼음량, 샷 추가 등)
3. **카페 실시간 혼잡도 표시** - 현재 대기 인원과 예상 대기 시간 확인
4. **주문 히스토리 및 단골 카페 관리** - 자주 가는 카페와 주문 패턴 분석
5. **멤버십 및 스탬프 통합 관리** - 여러 카페의 포인트와 쿠폰을 하나의 앱에서 관리

---

### 2️⃣ 취향 기반 커피 큐레이션 서비스

**해결하는 문제:**
- 커피 종류가 너무 많아 자신의 취향에 맞는 커피를 찾기 어려운 문제
- 새로운 카페나 원두를 시도하고 싶지만 실패할까 두려운 문제
- 커피 용어(산미, 바디감 등)를 잘 몰라 선택에 어려움을 겪는 문제

**대상 사용자:**
- 커피 입문자 및 초보자
- 새로운 커피 경험을 찾는 커피 애호가
- 선물용 커피를 찾는 사람들
- 스페셜티 커피에 관심 있는 밀레니얼/Z세대

**주요 기능:**
1. **AI 기반 취향 분석 퀴즈** - 간단한 질문을 통해 선호하는 맛 프로필 파악 (쓴맛 vs 신맛, 진함 vs 부드러움)
2. **개인 맞춤 커피 추천** - 취향 데이터 기반으로 원두, 카페 메뉴, 추출 방식 추천
3. **커피 맛 프로필 시각화** - 산미, 쓴맛, 단맛, 바디감 등을 레이더 차트로 쉽게 표현
4. **테이스팅 노트 및 평가 기록** - 마신 커피에 대한 개인적인 평가와 메모 저장
5. **유사 취향 사용자의 추천 공유** - 비슷한 취향을 가진 사람들이 좋아하는 커피 발견

---

### 3️⃣ 홈카페 레시피 & 커뮤니티 플랫폼

**해결하는 문제:**
- 집에서 커피를 내리고 싶지만 레시피와 추출 방법을 찾기 어려운 문제
- 원두 구매 후 보관 기간과 소진 계획을 관리하기 어려운 문제
- 커피 도구(그라인더, 드리퍼 등) 구매 시 선택 기준을 모르는 문제
- 홈카페에 대한 피드백을 받을 곳이 없는 문제

**대상 사용자:**
- 홈카페를 즐기는 커피 애호가
- 커피 도구를 구매하려는 입문자
- 바리스타 지망생
- 절약하면서도 좋은 커피를 마시고 싶은 사람들

**주요 기능:**
1. **단계별 추출 레시피 가이드** - 핸드드립, 모카포트, 프렌치프레스 등 도구별 상세 레시피와 타이머
2. **원두 재고 관리 시스템** - 구매한 원두의 로스팅 날짜, 남은 양, 소진 추천 기한 관리
3. **커피 도구 비교 및 리뷰** - 그라인더, 드리퍼, 저울 등 장비별 가격대별 추천과 사용자 리뷰
4. **커피 다이어리 및 추출 로그** - 물 온도, 추출 시간, 원두 양 등을 기록하여 최적의 레시피 찾기
5. **홈카페 커뮤니티** - 사진 공유, 레시피 교환, 질문 답변, 월간 챌린지 이벤트

---

## 🎯 기능적 요구사항

### 🧑‍💼 고객 기능

#### 1. 간편 메뉴 주문 및 커스터마이징
- 커피 메뉴를 직관적으로 탐색하고 선택
- 옵션 변경 (사이즈, 샷 추가, 얼음량, 시럽 등)
- 장바구니에 담고 한 번에 주문
- 자주 주문하는 메뉴를 즐겨찾기로 저장

#### 2. 실시간 주문 상태 추적
- 주문 접수, 제조 중, 완료 등 현재 상태를 실시간으로 확인
- 픽업 예상 시간 안내
- 주문 완료 시 알림 제공
- 주문 번호 및 QR 코드 표시로 간편한 픽업

#### 3. 주문 내역 및 재주문
- 과거 주문 내역 조회
- 이전 주문을 한 번의 클릭으로 재주문
- 월별 주문 통계 및 누적 금액 확인
- 자주 주문하는 메뉴 패턴 분석

---

### 👨‍💼 관리자 기능

#### 4. 주문 관리 대시보드
- 실시간으로 접수되는 주문을 한눈에 확인
- 주문 상태 변경 (접수 → 제조 중 → 완료 → 픽업 완료)
- 주문 우선순위 조정 및 대기 시간 관리
- 완료된 주문과 대기 중인 주문을 구분하여 표시
- 주문 상세 정보 및 특별 요청 사항 확인

#### 5. 메뉴 및 운영 관리
- 메뉴 등록, 수정, 삭제 (이름, 가격, 이미지, 옵션)
- 품절 메뉴 일시 비활성화
- 일별/주별/월별 매출 및 주문 통계 확인
- 인기 메뉴 및 시간대별 주문 분석
- 영업 시간 설정 및 주문 마감 관리

---

## 🗄️ 데이터 모델

### ERD (Entity Relationship Diagram)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Users     │         │   Orders    │         │  MenuItems  │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)     │    ┌───│ id (PK)     │
│ email       │    │    │ user_id (FK)│◄───┘   │ name        │
│ password    │    │    │ order_number│         │ category    │
│ name        │    │    │ status      │         │ price       │
│ phone       │    │    │ total_price │         │ description │
│ role        │    │    │ created_at  │         │ image_url   │
│ created_at  │    │    │ updated_at  │         │ is_available│
│ updated_at  │    │    │ pickup_time │         │ created_at  │
└─────────────┘    │    └─────────────┘         └─────────────┘
                   │            │                       │
                   │            │                       │
                   │    ┌───────┴───────┐               │
                   │    │               │               │
                   │    ▼               ▼               │
                   │ ┌─────────────────────┐            │
                   │ │   OrderItems        │            │
                   │ ├─────────────────────┤            │
                   └►│ id (PK)             │            │
                     │ order_id (FK)       │────────────┘
                     │ menu_item_id (FK)   │
                     │ quantity            │
                     │ size                │
                     │ options (JSON)      │
                     │ item_price          │
                     │ created_at          │
                     └─────────────────────┘

┌─────────────┐
│ Favorites   │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│────► Users.id
│ menu_item_id│────► MenuItems.id
│ options     │
│ created_at  │
└─────────────┘
```

### 테이블 상세 정의

#### 👤 Users (사용자)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 사용자 고유 ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 이메일 (로그인 ID) |
| password | VARCHAR(255) | NOT NULL | 암호화된 비밀번호 |
| name | VARCHAR(100) | NOT NULL | 사용자 이름 |
| phone | VARCHAR(20) | NULL | 전화번호 |
| role | ENUM('customer', 'admin') | DEFAULT 'customer' | 권한 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**인덱스**
- PRIMARY KEY: id
- UNIQUE INDEX: email
- INDEX: role

---

#### 🍕 MenuItems (메뉴)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 메뉴 고유 ID |
| name | VARCHAR(100) | NOT NULL | 메뉴명 |
| category | VARCHAR(50) | NOT NULL | 카테고리 (커피, 논커피, 디저트) |
| price | DECIMAL(10,2) | NOT NULL | 기본 가격 |
| description | TEXT | NULL | 메뉴 설명 |
| image_url | VARCHAR(500) | NULL | 이미지 URL |
| is_available | BOOLEAN | DEFAULT TRUE | 판매 가능 여부 |
| display_order | INT | DEFAULT 0 | 표시 순서 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**인덱스**
- PRIMARY KEY: id
- INDEX: category
- INDEX: is_available

---

#### 📦 Orders (주문)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 고유 ID |
| user_id | INT | FK, NULL | 사용자 ID (비회원은 NULL) |
| order_number | VARCHAR(50) | UNIQUE, NOT NULL | 주문 번호 (ORD-YYYYMMDD-XXX) |
| status | ENUM | NOT NULL | 주문 상태 |
| total_price | DECIMAL(10,2) | NOT NULL | 총 금액 |
| special_request | TEXT | NULL | 특별 요청사항 |
| pickup_time | TIMESTAMP | NULL | 예상 픽업 시간 |
| completed_at | TIMESTAMP | NULL | 완료 시간 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 주문 생성일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**status ENUM 값**
- `pending`: 접수 완료
- `preparing`: 제조 중
- `ready`: 픽업 대기
- `completed`: 픽업 완료
- `cancelled`: 취소됨

**인덱스**
- PRIMARY KEY: id
- UNIQUE INDEX: order_number
- INDEX: user_id
- INDEX: status
- INDEX: created_at

---

#### 🛒 OrderItems (주문 상세)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 아이템 ID |
| order_id | INT | FK, NOT NULL | 주문 ID |
| menu_item_id | INT | FK, NOT NULL | 메뉴 ID |
| quantity | INT | NOT NULL | 수량 |
| size | VARCHAR(20) | NULL | 사이즈 (Tall, Grande, Venti) |
| options | JSON | NULL | 추가 옵션 (샷, 얼음, 시럽 등) |
| item_price | DECIMAL(10,2) | NOT NULL | 개당 가격 (옵션 포함) |
| subtotal | DECIMAL(10,2) | NOT NULL | 소계 (item_price * quantity) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |

**options JSON 예시**
```json
{
  "extraShot": 1,
  "ice": "less",
  "syrup": ["vanilla"],
  "whippedCream": true
}
```

**인덱스**
- PRIMARY KEY: id
- INDEX: order_id
- INDEX: menu_item_id

---

#### ⭐ Favorites (즐겨찾기)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 즐겨찾기 ID |
| user_id | INT | FK, NOT NULL | 사용자 ID |
| menu_item_id | INT | FK, NOT NULL | 메뉴 ID |
| custom_options | JSON | NULL | 커스텀 옵션 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |

**인덱스**
- PRIMARY KEY: id
- UNIQUE INDEX: (user_id, menu_item_id)
- INDEX: user_id

---

### 관계 정의

1. **Users ↔ Orders**: 1:N (한 사용자는 여러 주문 가능)
2. **Orders ↔ OrderItems**: 1:N (한 주문은 여러 메뉴 아이템 포함)
3. **MenuItems ↔ OrderItems**: 1:N (한 메뉴는 여러 주문에 포함 가능)
4. **Users ↔ Favorites**: 1:N (한 사용자는 여러 즐겨찾기 가능)
5. **MenuItems ↔ Favorites**: 1:N (한 메뉴는 여러 사용자의 즐겨찾기 가능)

---

## 🔌 API 개요

### API 설계 원칙

- **RESTful API** 표준 준수
- **JSON** 형식 사용
- **HTTP 상태 코드** 명확히 사용
- **API 버전 관리**: `/api/v1/`
- **인증**: JWT (JSON Web Token)
- **에러 응답 일관성**

### 인증 (Authentication)

#### 📌 POST /api/v1/auth/register
사용자 회원가입

**요청**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "홍길동",
  "phone": "010-1234-5678"
}
```

**응답 (201 Created)**
```json
{
  "success": true,
  "message": "회원가입이 완료되었습니다.",
  "data": {
    "userId": 1,
    "email": "user@example.com",
    "name": "홍길동"
  }
}
```

---

#### 📌 POST /api/v1/auth/login
로그인

**요청**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "홍길동",
      "role": "customer"
    }
  }
}
```

---

### 메뉴 (Menu)

#### 📌 GET /api/v1/menus
메뉴 목록 조회

**쿼리 파라미터**
- `category` (optional): 카테고리 필터
- `available` (optional): 판매 가능 여부 (true/false)

**응답 (200 OK)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "category": "커피",
      "price": 4500,
      "description": "진한 에스프레소와 물",
      "imageUrl": "/images/americano.jpg",
      "isAvailable": true
    }
  ]
}
```

---

#### 📌 GET /api/v1/menus/:id
메뉴 상세 조회

#### 📌 POST /api/v1/menus (관리자 전용)
메뉴 등록

#### 📌 PUT /api/v1/menus/:id (관리자 전용)
메뉴 수정

#### 📌 DELETE /api/v1/menus/:id (관리자 전용)
메뉴 삭제

---

### 주문 (Orders)

#### 📌 POST /api/v1/orders
주문 생성

**요청**
```json
{
  "items": [
    {
      "menuItemId": 1,
      "quantity": 2,
      "size": "Grande",
      "options": {
        "extraShot": 1,
        "ice": "less"
      }
    }
  ],
  "specialRequest": "빨대 2개 주세요"
}
```

**응답 (201 Created)**
```json
{
  "success": true,
  "message": "주문이 완료되었습니다.",
  "data": {
    "orderId": 42,
    "orderNumber": "ORD-20251102-042",
    "status": "pending",
    "totalPrice": 15000,
    "estimatedPickupTime": "2025-11-02T09:35:00Z"
  }
}
```

---

#### 📌 GET /api/v1/orders
주문 목록 조회 (본인 주문만)

#### 📌 GET /api/v1/orders/:id
주문 상세 조회

#### 📌 GET /api/v1/orders/:id/status
주문 상태 조회 (실시간 폴링용)

---

### 관리자 - 주문 관리

#### 📌 GET /api/v1/admin/orders (관리자 전용)
전체 주문 목록 조회

#### 📌 PUT /api/v1/admin/orders/:id/status (관리자 전용)
주문 상태 변경

**요청**
```json
{
  "status": "preparing"
}
```

---

### 통계 (Statistics)

#### 📌 GET /api/v1/admin/statistics (관리자 전용)
매출 및 주문 통계

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "revenue": {
      "total": 337500,
      "average": 7500
    },
    "orders": {
      "total": 45,
      "completed": 42,
      "cancelled": 3
    },
    "topMenus": [
      { "name": "아메리카노", "count": 28, "revenue": 126000 }
    ]
  }
}
```

---

### 즐겨찾기 (Favorites)

#### 📌 GET /api/v1/favorites
내 즐겨찾기 목록

#### 📌 POST /api/v1/favorites
즐겨찾기 추가

#### 📌 DELETE /api/v1/favorites/:id
즐겨찾기 삭제

---

### 에러 응답 형식

모든 에러는 다음 형식을 따릅니다:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "details": {}
  }
}
```

**주요 HTTP 상태 코드**
- `200 OK`: 성공
- `201 Created`: 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스 없음
- `500 Internal Server Error`: 서버 오류

---

## 🥒 사용자 스토리 (Gherkin)

### Feature 1: 간편 메뉴 주문 및 커스터마이징

```gherkin
Feature: 메뉴 주문 및 커스터마이징
  As a 바쁜 직장인
  I want to 커피 메뉴를 빠르게 선택하고 옵션을 커스터마이징할 수 있기를
  So that 내 취향에 맞는 커피를 주문할 수 있다

  Scenario: 기본 메뉴 주문
    Given 사용자가 메뉴 페이지에 접속했을 때
    When 사용자가 "아메리카노" 메뉴를 선택하고
    And "장바구니 담기" 버튼을 클릭하면
    Then 장바구니에 "아메리카노" 1개가 추가되어야 한다
    And 장바구니 아이콘에 "(1)" 배지가 표시되어야 한다

  Scenario: 커피 옵션 커스터마이징
    Given 사용자가 "카페라떼" 메뉴를 선택했을 때
    When 사용자가 사이즈를 "Grande"로 변경하고
    And "샷 추가" 옵션을 선택하고
    And "얼음 적게" 옵션을 선택하면
    Then 총 가격이 기본 가격 + 추가 옵션 금액으로 계산되어야 한다
    And 옵션 요약에 "Grande / 샷 추가 / 얼음 적게"가 표시되어야 한다

  Scenario: 즐겨찾기 메뉴 저장 및 재사용
    Given 사용자가 "바닐라라떼 (Tall, 샷 추가, 휘핑 추가)"를 주문했을 때
    When 사용자가 "즐겨찾기 저장" 버튼을 클릭하면
    Then 해당 커스터마이징 옵션이 즐겨찾기 목록에 저장되어야 한다
    And 다음 방문 시 즐겨찾기 탭에서 해당 메뉴를 확인할 수 있어야 한다
```

---

### Feature 2: 실시간 주문 상태 추적

```gherkin
Feature: 실시간 주문 상태 추적
  As a 주문한 고객
  I want to 내 주문의 현재 상태를 실시간으로 확인할 수 있기를
  So that 픽업 시간을 예측하고 불필요한 대기를 피할 수 있다

  Scenario: 주문 완료 후 상태 확인
    Given 사용자가 커피 2잔을 주문했을 때
    When 주문이 성공적으로 완료되면
    Then 주문 번호 "ORD-20251102-001"이 발급되어야 한다
    And 주문 상태가 "접수 완료"로 표시되어야 한다
    And 예상 픽업 시간 "약 5분 후"가 표시되어야 한다

  Scenario: 주문 상태 실시간 업데이트
    Given 사용자가 주문 상태 페이지를 보고 있을 때
    And 현재 주문 상태가 "접수 완료"일 때
    When 관리자가 주문 상태를 "제조 중"으로 변경하면
    Then 사용자 화면에 "제조 중" 상태가 자동으로 업데이트되어야 한다
    And 진행률 표시줄이 50%로 표시되어야 한다

  Scenario: 주문 완료 알림
    Given 사용자의 주문이 "제조 중" 상태일 때
    When 관리자가 주문 상태를 "픽업 대기"로 변경하면
    Then 사용자에게 "주문이 완료되었습니다" 알림이 표시되어야 한다
    And QR 코드가 화면에 표시되어야 한다
    And "픽업 위치: 카운터"가 표시되어야 한다
```

---

### Feature 3: 주문 내역 및 재주문

```gherkin
Feature: 주문 내역 조회 및 재주문
  As a 단골 고객
  I want to 이전 주문 내역을 확인하고 쉽게 재주문할 수 있기를
  So that 매번 메뉴를 선택하는 번거로움 없이 빠르게 주문할 수 있다

  Scenario: 주문 내역 조회
    Given 사용자가 지난 30일간 5번의 주문을 했을 때
    When 사용자가 "주문 내역" 페이지에 접속하면
    Then 최신 주문부터 역순으로 5개의 주문이 표시되어야 한다
    And 각 주문에는 날짜, 주문 번호, 메뉴, 총 금액이 표시되어야 한다

  Scenario: 한 번의 클릭으로 재주문
    Given 사용자가 주문 내역에서 "아메리카노 2잔 (2024-11-01)" 주문을 확인했을 때
    When 사용자가 "재주문" 버튼을 클릭하면
    Then 동일한 메뉴와 옵션이 장바구니에 자동으로 추가되어야 한다
    And 주문 확인 페이지로 이동해야 한다

  Scenario: 월별 주문 통계 확인
    Given 사용자가 11월에 총 15,000원어치 커피를 주문했을 때
    When 사용자가 "통계" 탭을 클릭하면
    Then "11월 총 주문 금액: 15,000원"이 표시되어야 한다
    And "가장 많이 주문한 메뉴: 아메리카노 (8회)"가 표시되어야 한다
    And 주별 주문 그래프가 표시되어야 한다
```

---

### Feature 4: 관리자 주문 관리 대시보드

```gherkin
Feature: 관리자 주문 관리 대시보드
  As a 카페 관리자
  I want to 실시간으로 들어오는 주문을 효율적으로 관리할 수 있기를
  So that 고객에게 빠르고 정확한 서비스를 제공할 수 있다

  Scenario: 신규 주문 알림 및 접수
    Given 관리자가 대시보드를 보고 있을 때
    When 새로운 주문 "ORD-20251102-005"가 접수되면
    Then 알림음과 함께 "새 주문 1건" 팝업이 표시되어야 한다
    And 대기 주문 목록 최상단에 해당 주문이 표시되어야 한다
    And 주문 상세 정보 (메뉴, 옵션, 특별 요청)가 표시되어야 한다

  Scenario: 주문 상태 변경
    Given 관리자가 주문 "ORD-20251102-003" (아메리카노 2잔)을 선택했을 때
    When 관리자가 "제조 시작" 버튼을 클릭하면
    Then 해당 주문의 상태가 "제조 중"으로 변경되어야 한다
    And 주문 카드가 "제조 중" 섹션으로 이동해야 한다
    And 타이머가 자동으로 시작되어야 한다

  Scenario: 주문 우선순위 조정
    Given 대기 중인 주문이 5건 있을 때
    And "ORD-20251102-006"이 급한 주문일 때
    When 관리자가 해당 주문을 드래그하여 목록 최상단으로 이동하면
    Then 주문 순서가 재정렬되어야 한다
    And 우선순위 뱃지 "긴급"이 표시되어야 한다

  Scenario: 완료 주문 처리
    Given 주문 "ORD-20251102-002"의 제조가 완료되었을 때
    When 관리자가 "픽업 대기" 버튼을 클릭하면
    Then 해당 주문이 "완료" 섹션으로 이동해야 한다
    And 고객에게 알림이 전송되어야 한다
    And 제조 소요 시간이 기록되어야 한다
```

---

### Feature 5: 메뉴 및 운영 관리

```gherkin
Feature: 메뉴 및 운영 관리
  As a 카페 관리자
  I want to 메뉴를 쉽게 관리하고 매출 통계를 확인할 수 있기를
  So that 효율적으로 카페를 운영하고 의사결정에 활용할 수 있다

  Scenario: 신규 메뉴 등록
    Given 관리자가 "메뉴 관리" 페이지에 접속했을 때
    When 관리자가 "신규 메뉴 추가" 버튼을 클릭하고
    And 메뉴명 "콜드브루", 가격 "5500원", 카테고리 "커피"를 입력하고
    And 메뉴 이미지를 업로드하고
    And "저장" 버튼을 클릭하면
    Then "콜드브루" 메뉴가 메뉴 목록에 추가되어야 한다
    And 고객 메뉴 페이지에 즉시 표시되어야 한다

  Scenario: 품절 메뉴 관리
    Given "카라멜 마끼아또" 메뉴가 활성화되어 있을 때
    When 관리자가 해당 메뉴의 "품절" 토글을 활성화하면
    Then 고객 메뉴 페이지에서 해당 메뉴가 비활성화되어야 한다
    And "일시 품절" 표시가 나타나야 한다
    And 고객이 해당 메뉴를 주문할 수 없어야 한다

  Scenario: 일별 매출 통계 확인
    Given 오늘 총 20건의 주문이 완료되었을 때
    And 총 매출이 150,000원일 때
    When 관리자가 "통계" 페이지의 "오늘" 탭을 클릭하면
    Then "오늘 총 주문: 20건"이 표시되어야 한다
    And "오늘 총 매출: 150,000원"이 표시되어야 한다
    And "평균 주문 금액: 7,500원"이 표시되어야 한다
    And "인기 메뉴 TOP 3" 목록이 표시되어야 한다

  Scenario: 영업 시간 외 주문 차단
    Given 관리자가 영업 시간을 "09:00 - 18:00"으로 설정했을 때
    When 현재 시각이 18:30이면
    Then 고객 메뉴 페이지에 "영업 종료" 메시지가 표시되어야 한다
    And 모든 주문 버튼이 비활성화되어야 한다
    And "영업 시작: 내일 오전 9시"가 표시되어야 한다
```

---

## 🔧 비기능적 요구사항

### ⚡ 성능 기대치 (Performance Requirements)

**응답 시간**
- 메뉴 페이지 로딩: 2초 이내
- 주문 제출 후 확인: 1초 이내
- 주문 상태 업데이트 반영: 3초 이내
- 관리자 대시보드 로딩: 3초 이내

**동시 사용자**
- 최소 50명의 동시 접속자 지원
- 피크 시간대(오전 8-9시) 100명까지 안정적 처리

**데이터베이스**
- 단일 쿼리 응답 시간: 100ms 이내
- 주문 내역 조회 (최근 30일): 500ms 이내

**리소스 최적화**
- 이미지 파일 크기: 500KB 이하
- 페이지 전체 로드 크기: 3MB 이하
- API 응답 페이로드: 가능한 한 1MB 이하

---

### 🔒 보안 요구 사항 (Security Requirements)

**인증 및 권한**
- 관리자 페이지는 로그인 인증 필수
- 세션 타임아웃: 30분 (관리자), 24시간 (고객)
- 비밀번호 최소 요구사항: 8자 이상, 영문+숫자 조합

**데이터 보호**
- 비밀번호는 bcrypt 해싱 (최소 10 rounds)
- 민감한 정보 (개인정보) 암호화 저장
- SQL Injection 방지를 위한 Prepared Statement 사용

**통신 보안**
- HTTPS 적용 (프로덕션 환경)
- API 요청에 CSRF 토큰 사용
- XSS 공격 방지를 위한 입력값 검증 및 이스케이핑

**접근 제어**
- 고객은 자신의 주문만 조회 가능
- 관리자만 메뉴 수정 및 주문 관리 가능
- 직접 URL 접근 차단 (권한 없는 페이지)

**백업**
- 데이터베이스 일일 자동 백업
- 최소 7일간 백업 보관

---

### 📈 확장성 고려 사항 (Scalability Considerations)

**아키텍처**
- Frontend와 Backend 분리 (API 기반)
- RESTful API 설계로 향후 모바일 앱 대응 가능
- 상태 관리를 서버에서 처리 (stateless API)

**데이터베이스**
- 주문 테이블 인덱싱 (order_date, status, user_id)
- 오래된 주문 데이터 아카이빙 전략 (6개월 이상)
- 페이지네이션 적용 (주문 내역, 관리자 통계)

**코드 구조**
- 모듈화된 컴포넌트 구조
- 환경 변수로 설정 관리 (.env)
- 기능별 라우팅 분리

**미래 확장 가능성**
- 다중 카페 지점 추가 가능한 DB 스키마 설계
- 결제 시스템 통합 여지 (API 인터페이스)
- 알림 시스템 확장 가능 (이메일, SMS, 푸시)

**현실적인 제약**
- 초기에는 단일 서버 구성
- 수평적 확장보다는 수직적 확장 우선
- CDN은 선택 사항 (예산 고려)

---

### 🎨 사용성 표준 (Usability Standards)

**반응형 디자인**
- 모바일 (375px 이상): 세로 스크롤 최소화
- 태블릿 (768px 이상): 메뉴 그리드 2열
- 데스크톱 (1024px 이상): 메뉴 그리드 3-4열
- 관리자 대시보드: 최소 1024px 권장

**접근성 (Accessibility)**
- 명확한 버튼 레이블과 아이콘
- 충분한 색상 대비 (WCAG 2.1 AA 기준)
- 키보드 네비게이션 지원 (Tab, Enter)
- 터치 타겟 최소 크기: 44x44px

**사용자 경험**
- 3번의 클릭 이내 주문 완료
- 로딩 시 스피너 또는 스켈레톤 UI 표시
- 오류 발생 시 명확한 에러 메시지
- 성공/실패 액션 후 즉각적인 피드백

**일관성**
- 통일된 컬러 스키마 (주요 색상 3-4개)
- 일관된 버튼 스타일 (Primary, Secondary, Danger)
- 표준 폰트 사용 (한글: Noto Sans KR / 영문: Roboto)
- 일관된 간격 시스템 (4px, 8px, 16px, 24px)

**다국어 지원**
- 초기에는 한국어만 지원
- 향후 영어 추가 가능하도록 텍스트 리소스 분리

**브라우저 호환성**
- Chrome (최신 2개 버전)
- Safari (최신 2개 버전)
- Edge (최신 2개 버전)
- Firefox (최신 2개 버전)
- IE는 지원하지 않음

**에러 처리**
- 네트워크 오류 시 재시도 옵션 제공
- 404 페이지 커스터마이징
- 500 에러 시 사용자 친화적 메시지

---

## 📊 우선순위 매트릭스 (Toy Project용)

| 요구사항 | 우선순위 | 구현 난이도 | 비고 |
|---------|---------|-----------|------|
| 기본 인증/권한 | 🔴 높음 | 중 | 필수 보안 |
| 반응형 디자인 | 🔴 높음 | 중 | 모바일 필수 |
| 페이지 로딩 2초 이내 | 🟡 중간 | 중 | 최적화 필요 |
| HTTPS 적용 | 🟡 중간 | 낮 | 배포 시 필수 |
| 실시간 업데이트 | 🟡 중간 | 높 | WebSocket/Polling |
| 접근성 WCAG AA | 🟢 낮음 | 중 | 시간 여유 시 |
| 100명 동시 접속 | 🟢 낮음 | 높 | 부하 테스트 |
| 다국어 지원 | 🟢 낮음 | 중 | 추후 확장 |

---

## ✅ 검증 방법

각 비기능적 요구사항의 검증 방법:

**성능**
- Lighthouse 성능 점수 70점 이상
- Chrome DevTools Network 탭으로 로딩 시간 측정

**보안**
- 로그인 테스트 (권한별 접근 제어)
- OWASP Top 10 기본 체크리스트

**확장성**
- 코드 리뷰로 모듈화 확인
- 1000개 주문 데이터 로드 테스트

**사용성**
- 3명 이상의 베타 테스터 피드백
- 모바일/데스크톱 실제 기기 테스트

---

## 💻 기술 스택 및 로드맵

### 추천 기술 스택

#### Frontend
- **React** + TypeScript (추천)
- Tailwind CSS (스타일링)
- Redux Toolkit / Zustand (상태 관리)
- React Router (라우팅)
- Axios (HTTP 클라이언트)
- Chart.js (통계 그래프)
- QRCode.js (QR 코드 생성)

#### Backend
- **Node.js + Express** (추천)
- TypeORM / Prisma (ORM)
- JWT + bcrypt (인증)
- Socket.io (실시간 통신, 선택적)

#### Database
- **PostgreSQL** (추천)
- Supabase / Railway (호스팅)

#### DevOps
- Vercel (Frontend 배포)
- Railway / Heroku (Backend 배포)
- GitHub Actions (CI/CD)

---

### 개발 로드맵 (7주)

#### Phase 1: 기본 기능 구현 (4주)

**Week 1: 프로젝트 설정 및 DB 구축**
- [ ] 프로젝트 초기 설정 (Frontend + Backend)
- [ ] 데이터베이스 스키마 생성
- [ ] API 기본 구조 설정
- [ ] 개발 환경 구성

**Week 2: 인증 및 메뉴 기능**
- [ ] 회원가입 / 로그인 / 로그아웃
- [ ] JWT 인증 미들웨어
- [ ] 메뉴 CRUD API
- [ ] 메뉴 목록 / 상세 페이지

**Week 3: 주문 기능 (고객)**
- [ ] 장바구니 기능
- [ ] 주문 생성 API
- [ ] 주문 확인 페이지
- [ ] 주문 내역 조회

**Week 4: 주문 관리 (관리자)**
- [ ] 관리자 대시보드 UI
- [ ] 주문 상태 변경 API
- [ ] 실시간 주문 알림
- [ ] 기본 테스트

#### Phase 2: 고급 기능 (2주)

**Week 5: 커스터마이징 및 통계**
- [ ] 메뉴 옵션 커스터마이징
- [ ] 즐겨찾기 기능
- [ ] 관리자 통계 대시보드
- [ ] 매출 그래프

**Week 6: 최적화 및 UX 개선**
- [ ] 반응형 디자인 완성
- [ ] 로딩 상태 처리
- [ ] 에러 처리 개선
- [ ] QR 코드 생성

#### Phase 3: 배포 및 테스트 (1주)

**Week 7: 배포 및 마무리**
- [ ] 프로덕션 빌드 최적화
- [ ] Frontend 배포 (Vercel)
- [ ] Backend 배포 (Railway/Heroku)
- [ ] E2E 테스트
- [ ] 문서 정리

---

### 우선순위 매트릭스

| 기능 | 우선순위 | 난이도 | 예상 시간 |
|------|---------|-------|----------|
| 회원가입/로그인 | 🔴 P0 | 중 | 2일 |
| 메뉴 조회 | 🔴 P0 | 낮 | 1일 |
| 주문 생성 | 🔴 P0 | 중 | 3일 |
| 주문 상태 추적 | 🔴 P0 | 중 | 2일 |
| 관리자 대시보드 | 🔴 P0 | 높 | 4일 |
| 메뉴 관리 (CRUD) | 🔴 P0 | 중 | 2일 |
| 주문 내역 조회 | 🟡 P1 | 낮 | 1일 |
| 커스터마이징 | 🟡 P1 | 중 | 3일 |
| 즐겨찾기 | 🟡 P1 | 낮 | 1일 |
| 통계 대시보드 | 🟡 P1 | 중 | 3일 |
| 실시간 알림 | 🟡 P1 | 높 | 3일 |
| QR 코드 | 🟢 P2 | 낮 | 1일 |

---

## 📝 다음 단계

1. ✅ **요구사항 명세 완료**
2. 🔲 **기술 스택 확정**
3. 🔲 **프로젝트 초기 설정**
4. 🔲 **데이터베이스 구축**
5. 🔲 **API 개발 시작**

---

**문서 버전**: 1.0  
**최종 수정일**: 2025년 11월 2일  
**작성자**: kznetwork

//**