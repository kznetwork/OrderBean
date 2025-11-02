# OrderBean - Product Requirements Document (PRD)

**버전**: 1.1  
**작성일**: 2025년 11월 2일  
**최종 수정일**: 2025년 11월 2일  
**작성자**: kznetwork  
**프로젝트 타입**: Toy Project / Portfolio

---

## 📑 목차

1. [개요](#1-개요)
2. [기능 요구사항](#2-기능-요구사항)
3. [데이터 모델](#3-데이터-모델)
4. [API 개요](#4-api-개요)
5. [사용자 스토리](#5-사용자-스토리)
6. [비기능적 요구사항](#6-비기능적-요구사항)
7. [기술 스택](#7-기술-스택)
8. [개발 로드맵](#8-개발-로드맵)

---

## 1. 개요

### 1.1 프로젝트 소개

OrderBean은 **바쁜 직장인들이 시간을 절약할 수 있도록 돕는 커피 주문 관리 웹 애플리케이션**입니다. 사용자는 메뉴를 선택하고 주문하며, 관리자는 실시간으로 주문을 관리할 수 있는 풀스택 웹 앱입니다.

### 1.2 문제 진술문 (Problem Statement)

> **"바쁜 직장인들이 카페 대기 시간 없이 선주문을 통해 신속하게 커피를 픽업할 수 있도록 하고, 관리자는 실시간으로 주문을 접수하고 처리 상태를 관리할 수 있는 직관적인 웹 기반 주문 관리 시스템이 필요하다."**

### 1.3 대상 사용자

**주요 사용자 (Primary Users)**
- 바쁜 직장인 (20-40대)
- 시간이 촉박한 대학생
- 대기 시간을 줄이고 싶은 카페 이용객

**관리 사용자 (Admin Users)**
- 카페 운영자
- 바리스타
- 매장 매니저

### 1.4 핵심 가치 제안

- ⏰ **시간 절약**: 대기 줄 없이 선주문 후 즉시 픽업
- 📱 **편리성**: 언제 어디서나 웹 브라우저로 주문
- 🎯 **커스터마이징**: 개인 취향에 맞는 옵션 선택
- 📊 **효율적인 관리**: 관리자의 주문 처리 최적화
- 📈 **데이터 인사이트**: 주문 패턴 및 매출 분석

### 1.5 성공 지표 (Success Metrics)

- 주문 완료율: 90% 이상
- 평균 주문 소요 시간: 2분 이내
- 재방문율: 60% 이상
- 고객 만족도: 4.0/5.0 이상
- 관리자 주문 처리 시간: 평균 5분 이내

---

## 2. 기능 요구사항

### 2.1 고객 기능 (Customer Features)

#### 📌 F1. 메뉴 주문 및 커스터마이징

**우선순위**: 🔴 높음 (P0)

**기능 설명**
- 커피 메뉴를 카테고리별로 탐색
- 메뉴 상세 정보 확인 (이미지, 가격, 설명)
- 옵션 커스터마이징:
  - 사이즈 선택 (Tall, Grande, Venti)
  - 샷 추가/감소
  - 얼음량 조절 (많이, 보통, 적게, 없음)
  - 시럽 추가
  - 휘핑크림 추가/제거
- 장바구니 추가 및 수량 조절
- 즐겨찾기 메뉴 저장

**사용자 흐름**
1. 메뉴 페이지 접속
2. 카테고리 선택 또는 검색
3. 메뉴 선택
4. 옵션 커스터마이징
5. 장바구니 담기
6. 주문 확인 및 제출

---

#### 📌 F2. 실시간 주문 상태 추적

**우선순위**: 🔴 높음 (P0)

**기능 설명**
- 주문 번호 자동 발급
- 실시간 주문 상태 확인:
  - ⏳ 접수 완료
  - 👨‍🍳 제조 중
  - ✅ 픽업 대기
  - 📦 픽업 완료
- 예상 픽업 시간 표시
- 주문 완료 알림
- QR 코드 생성 (픽업 확인용)

**상태 전이도**
```
접수 완료 → 제조 중 → 픽업 대기 → 픽업 완료
    ↓
  취소됨
```

---

#### 📌 F3. 주문 내역 및 재주문

**우선순위**: 🟡 중간 (P1)

**기능 설명**
- 과거 주문 내역 조회 (최근 30일)
- 주문 상세 정보 확인
- 한 번의 클릭으로 재주문
- 주문 통계:
  - 월별 총 주문 금액
  - 가장 많이 주문한 메뉴
  - 주문 빈도 그래프
- 영수증 다운로드

---

### 2.2 관리자 기능 (Admin Features)

#### 📌 F4. 주문 관리 대시보드

**우선순위**: 🔴 높음 (P0)

**기능 설명**
- 실시간 주문 현황 대시보드
- 주문 상태 관리:
  - 신규 주문 알림 (알림음 + 팝업)
  - 주문 상태 변경 (접수 → 제조 → 완료)
  - 주문 상세 정보 확인
  - 특별 요청 사항 확인
- 주문 우선순위 조정 (드래그 앤 드롭)
- 대기 시간 관리
- 주문 검색 및 필터링
- 완료/취소 주문 아카이빙

**대시보드 레이아웃**
```
┌─────────────────────────────────────────┐
│  📊 오늘의 통계                          │
│  주문: 45건 | 매출: 337,500원           │
└─────────────────────────────────────────┘
┌──────────┬──────────┬──────────────────┐
│ 대기 중  │ 제조 중  │ 픽업 대기        │
│ (8건)    │ (3건)    │ (2건)            │
│          │          │                  │
│ [주문카드]│ [주문카드]│ [주문카드]       │
│ [주문카드]│ [주문카드]│ [주문카드]       │
└──────────┴──────────┴──────────────────┘
```

---

#### 📌 F5. 메뉴 및 운영 관리

**우선순위**: 🔴 높음 (P0)

**기능 설명**

**메뉴 관리**
- CRUD 작업:
  - 메뉴 등록 (이름, 가격, 카테고리, 이미지, 설명)
  - 메뉴 수정
  - 메뉴 삭제 (soft delete)
- 옵션 관리 (사이즈별 가격, 추가 옵션)
- 품절 메뉴 일시 비활성화
- 메뉴 순서 조정

**통계 및 분석**
- 기간별 매출 통계:
  - 일별 / 주별 / 월별
  - 시간대별 주문 분석
- 인기 메뉴 TOP 5
- 주문 건수 추이 그래프
- 평균 주문 금액
- 고객 재방문율

**운영 관리**
- 영업 시간 설정
- 주문 마감 설정
- 공지사항 관리

---

## 3. 데이터 모델

### 3.1 ERD (Entity Relationship Diagram)

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

---

### 3.2 테이블 상세 정의

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

### 3.3 관계 정의

1. **Users ↔ Orders**: 1:N (한 사용자는 여러 주문 가능)
2. **Orders ↔ OrderItems**: 1:N (한 주문은 여러 메뉴 아이템 포함)
3. **MenuItems ↔ OrderItems**: 1:N (한 메뉴는 여러 주문에 포함 가능)
4. **Users ↔ Favorites**: 1:N (한 사용자는 여러 즐겨찾기 가능)
5. **MenuItems ↔ Favorites**: 1:N (한 메뉴는 여러 사용자의 즐겨찾기 가능)

---

## 4. API 개요

### 4.1 API 설계 원칙

- **RESTful API** 표준 준수
- **JSON** 형식 사용
- **HTTP 상태 코드** 명확히 사용
- **API 버전 관리**: `/api/v1/`
- **인증**: JWT (JSON Web Token)
- **에러 응답 일관성**
- **자동 API 문서**: FastAPI 기반 Swagger/ReDoc 자동 생성

### 4.2 인증 (Authentication)

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

#### 📌 POST /api/v1/auth/logout
로그아웃

**응답 (200 OK)**
```json
{
  "success": true,
  "message": "로그아웃되었습니다."
}
```

---

### 4.3 메뉴 (Menu)

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
    },
    {
      "id": 2,
      "name": "카페라떼",
      "category": "커피",
      "price": 5000,
      "description": "부드러운 우유와 에스프레소",
      "imageUrl": "/images/latte.jpg",
      "isAvailable": true
    }
  ]
}
```

---

#### 📌 GET /api/v1/menus/:id
메뉴 상세 조회

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "아메리카노",
    "category": "커피",
    "price": 4500,
    "description": "진한 에스프레소와 물",
    "imageUrl": "/images/americano.jpg",
    "isAvailable": true,
    "options": {
      "sizes": [
        { "name": "Tall", "additionalPrice": 0 },
        { "name": "Grande", "additionalPrice": 500 },
        { "name": "Venti", "additionalPrice": 1000 }
      ],
      "extras": [
        { "name": "샷 추가", "price": 500 },
        { "name": "바닐라 시럽", "price": 500 }
      ]
    }
  }
}
```

---

#### 📌 POST /api/v1/menus (관리자 전용)
메뉴 등록

**요청 (Authorization: Bearer {token})**
```json
{
  "name": "콜드브루",
  "category": "커피",
  "price": 5500,
  "description": "12시간 저온 추출",
  "imageUrl": "/images/coldbrew.jpg"
}
```

**응답 (201 Created)**
```json
{
  "success": true,
  "message": "메뉴가 등록되었습니다.",
  "data": {
    "id": 10,
    "name": "콜드브루"
  }
}
```

---

#### 📌 PUT /api/v1/menus/:id (관리자 전용)
메뉴 수정

---

#### 📌 DELETE /api/v1/menus/:id (관리자 전용)
메뉴 삭제 (soft delete)

---

### 4.4 주문 (Orders)

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
    },
    {
      "menuItemId": 5,
      "quantity": 1,
      "size": "Tall",
      "options": {}
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
    "estimatedPickupTime": "2025-11-02T09:35:00Z",
    "items": [
      {
        "menuName": "아메리카노",
        "quantity": 2,
        "size": "Grande",
        "itemPrice": 5500,
        "subtotal": 11000
      },
      {
        "menuName": "크루아상",
        "quantity": 1,
        "itemPrice": 4000,
        "subtotal": 4000
      }
    ]
  }
}
```

---

#### 📌 GET /api/v1/orders
주문 목록 조회 (본인 주문만)

**쿼리 파라미터**
- `status` (optional): 주문 상태 필터
- `startDate` (optional): 시작 날짜
- `endDate` (optional): 종료 날짜
- `page` (optional): 페이지 번호 (기본값: 1)
- `limit` (optional): 페이지당 개수 (기본값: 10)

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": 42,
        "orderNumber": "ORD-20251102-042",
        "status": "ready",
        "totalPrice": 15000,
        "createdAt": "2025-11-02T09:30:00Z",
        "itemCount": 3
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 48
    }
  }
}
```

---

#### 📌 GET /api/v1/orders/:id
주문 상세 조회

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "id": 42,
    "orderNumber": "ORD-20251102-042",
    "status": "ready",
    "totalPrice": 15000,
    "specialRequest": "빨대 2개 주세요",
    "pickupTime": "2025-11-02T09:35:00Z",
    "createdAt": "2025-11-02T09:30:00Z",
    "items": [
      {
        "id": 101,
        "menuName": "아메리카노",
        "quantity": 2,
        "size": "Grande",
        "options": {
          "extraShot": 1,
          "ice": "less"
        },
        "itemPrice": 5500,
        "subtotal": 11000
      }
    ],
    "qrCode": "data:image/png;base64,iVBORw0KG..."
  }
}
```

---

#### 📌 GET /api/v1/orders/:id/status
주문 상태 조회 (실시간 폴링용)

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "orderNumber": "ORD-20251102-042",
    "status": "preparing",
    "estimatedTime": 3,
    "updatedAt": "2025-11-02T09:32:00Z"
  }
}
```

---

### 4.5 관리자 - 주문 관리 (Admin Orders)

#### 📌 GET /api/v1/admin/orders (관리자 전용)
전체 주문 목록 조회

**쿼리 파라미터**
- `status` (optional): 주문 상태
- `date` (optional): 특정 날짜
- `sort` (optional): 정렬 (created_at, status)

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "summary": {
      "pending": 8,
      "preparing": 3,
      "ready": 2,
      "completed": 45,
      "todayRevenue": 337500
    },
    "orders": [
      {
        "id": 42,
        "orderNumber": "ORD-20251102-042",
        "customerName": "홍길동",
        "status": "pending",
        "totalPrice": 15000,
        "itemCount": 3,
        "specialRequest": "빨대 2개 주세요",
        "createdAt": "2025-11-02T09:30:00Z"
      }
    ]
  }
}
```

---

#### 📌 PUT /api/v1/admin/orders/:id/status (관리자 전용)
주문 상태 변경

**요청**
```json
{
  "status": "preparing"
}
```

**응답 (200 OK)**
```json
{
  "success": true,
  "message": "주문 상태가 변경되었습니다.",
  "data": {
    "orderId": 42,
    "orderNumber": "ORD-20251102-042",
    "status": "preparing",
    "updatedAt": "2025-11-02T09:32:00Z"
  }
}
```

---

### 4.6 통계 (Statistics)

#### 📌 GET /api/v1/admin/statistics (관리자 전용)
매출 및 주문 통계

**쿼리 파라미터**
- `period`: day, week, month
- `startDate`: 시작 날짜
- `endDate`: 종료 날짜

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "revenue": {
      "total": 337500,
      "average": 7500,
      "daily": [
        { "date": "2025-11-01", "amount": 280000 },
        { "date": "2025-11-02", "amount": 337500 }
      ]
    },
    "orders": {
      "total": 45,
      "completed": 42,
      "cancelled": 3
    },
    "topMenus": [
      { "name": "아메리카노", "count": 28, "revenue": 126000 },
      { "name": "카페라떼", "count": 18, "revenue": 90000 },
      { "name": "바닐라라떼", "count": 15, "revenue": 82500 }
    ],
    "hourlyDistribution": [
      { "hour": 8, "orders": 12 },
      { "hour": 9, "orders": 18 },
      { "hour": 10, "orders": 8 }
    ]
  }
}
```

---

### 4.7 즐겨찾기 (Favorites)

#### 📌 GET /api/v1/favorites
내 즐겨찾기 목록

**응답 (200 OK)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "menuItem": {
        "id": 2,
        "name": "카페라떼",
        "price": 5000,
        "imageUrl": "/images/latte.jpg"
      },
      "customOptions": {
        "size": "Grande",
        "extraShot": 1,
        "ice": "less"
      }
    }
  ]
}
```

---

#### 📌 POST /api/v1/favorites
즐겨찾기 추가

**요청**
```json
{
  "menuItemId": 2,
  "customOptions": {
    "size": "Grande",
    "extraShot": 1,
    "ice": "less"
  }
}
```

---

#### 📌 DELETE /api/v1/favorites/:id
즐겨찾기 삭제

---

### 4.8 에러 응답 형식

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

## 5. 사용자 스토리

### 5.1 Feature 1: 메뉴 주문 및 커스터마이징

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

### 5.2 Feature 2: 실시간 주문 상태 추적

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

### 5.3 Feature 3: 주문 내역 및 재주문

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

### 5.4 Feature 4: 관리자 주문 관리 대시보드

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

### 5.5 Feature 5: 메뉴 및 운영 관리

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

## 6. 비기능적 요구사항

### 6.1 성능 (Performance)

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

### 6.2 보안 (Security)

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

### 6.3 확장성 (Scalability)

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

### 6.4 사용성 (Usability)

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

### 6.5 신뢰성 (Reliability)

**가용성**
- 목표 가동률: 99% (연간 약 3.65일 다운타임 허용)
- 정기 점검: 매주 수요일 새벽 2-4시

**데이터 무결성**
- 트랜잭션 처리 (ACID 원칙)
- 주문 데이터 불일치 방지
- 재고 동시성 제어

**에러 복구**
- 자동 재시도 메커니즘 (최대 3회)
- 장애 발생 시 에러 로그 저장
- 관리자 알림 시스템

---

### 6.6 유지보수성 (Maintainability)

**코드 품질**
- ESLint / Prettier 적용 (Frontend)
- Pylint / Black 적용 (Backend)
- 단위 테스트 커버리지: 60% 이상
- 코드 리뷰 프로세스

**문서화**
- API 문서 자동 생성 (FastAPI Swagger/ReDoc)
- README 및 개발 가이드 작성
- 주요 로직에 주석 추가

**모니터링**
- 에러 로그 수집 및 분석
- 성능 모니터링 (응답 시간, 메모리 사용량)
- 주요 지표 대시보드

---

## 7. 기술 스택

### 7.1 Frontend

**프레임워크 & 언어**
- **React 18+** (확정)
- **TypeScript** (타입 안정성)
- **Vite** (빌드 도구)

**상태 관리**
- **Zustand** (경량 상태 관리) 또는
- **Redux Toolkit** (복잡한 상태 관리 시)
- **React Query** (서버 상태 관리)

**스타일링**
- **Tailwind CSS** (유틸리티 기반)
- **Shadcn/ui** (UI 컴포넌트 라이브러리)
- **Headless UI** (접근성 기반 컴포넌트)

**HTTP 클라이언트**
- **Axios** (인터셉터, 에러 처리)

**라우팅**
- **React Router v6**

**폼 관리**
- **React Hook Form**
- **Zod** (스키마 검증)

**통계/차트**
- **Recharts** 또는 **Chart.js**

**기타 라이브러리**
- **QRCode.js** (QR 코드 생성)
- **date-fns** (날짜 처리)
- **clsx** (조건부 클래스 관리)

---

### 7.2 Backend

**프레임워크 & 언어**
- **Python 3.11+** (확정)
- **FastAPI** (고성능 비동기 웹 프레임워크)
- **Uvicorn** (ASGI 서버)

**데이터베이스**
- **PostgreSQL 15+** (관계형 데이터베이스)
- **asyncpg** (비동기 PostgreSQL 드라이버)

**ORM**
- **SQLAlchemy 2.0** (ORM)
- **Alembic** (데이터베이스 마이그레이션)

**인증 & 보안**
- **FastAPI Users** (인증 시스템)
- **OAuth2** with **JWT** (토큰 기반 인증)
- **python-jose** (JWT 생성/검증)
- **passlib[bcrypt]** (비밀번호 해싱)

**데이터 검증**
- **Pydantic v2** (데이터 모델 및 검증)

**테스트**
- **pytest** (단위/통합 테스트)
- **pytest-asyncio** (비동기 테스트)
- **httpx** (API 테스트 클라이언트)

**문서화**
- **Swagger UI** (자동 생성 - FastAPI 내장)
- **ReDoc** (자동 생성 - FastAPI 내장)

**실시간 통신**
- **WebSocket** (FastAPI 내장 지원)
- 또는 **Polling** (간단한 대안)

**기타 라이브러리**
- **python-dotenv** (환경 변수 관리)
- **python-multipart** (파일 업로드)
- **qrcode** (QR 코드 생성)

---

### 7.3 배포 (Deployment)

**통합 배포 플랫폼**
- **Render** (Frontend + Backend + PostgreSQL 통합 호스팅)
  - **Web Service**: FastAPI 백엔드
  - **Static Site**: React 프론트엔드
  - **PostgreSQL Database**: 관리형 데이터베이스

**Render 배포 장점**
- 무료 플랜 제공 (프로토타입 단계)
- PostgreSQL 통합 지원
- 자동 배포 (GitHub 연동)
- HTTPS 자동 적용
- 환경 변수 관리 간편

**대안 플랫폼 (선택적)**
- **Vercel** (Frontend 전용)
- **Railway** (Backend + DB)
- **Heroku** (올인원)

**데이터베이스 호스팅**
- **Render PostgreSQL** (추천)
- **Supabase** (대안)
- **AWS RDS** (프로덕션 단계)

---

### 7.4 DevOps

**버전 관리**
- **Git**
- **GitHub**

**CI/CD**
- **GitHub Actions** (추천)
  - 자동 테스트 실행
  - Render 자동 배포
- **Render 자동 배포** (Git Push 시 자동)

**코드 품질**
- **ESLint + Prettier** (Frontend)
- **Pylint + Black** (Backend)
- **pre-commit hooks** (Git 커밋 전 검증)

**환경 변수 관리**
- `.env` 파일 (로컬 개발)
- Render 환경 변수 설정 (프로덕션)

---

### 7.5 개발 도구

**IDE**
- **VS Code** (추천)
- **PyCharm** (Python 개발)
- **WebStorm** (Frontend 개발)

**API 테스트**
- **Postman**
- **Insomnia**
- **FastAPI Swagger UI** (내장)

**데이터베이스 관리**
- **DBeaver**
- **pgAdmin**
- **Postico** (macOS)

**디자인 & 프로토타이핑**
- **Figma** (와이어프레임/디자인)

---

### 7.6 기술 스택 요약표

| 계층(Layer) | 사용 기술 | 설명 |
|------------|----------|------|
| **프론트엔드 (UI)** | React + TypeScript + Vite | 빠른 프로토타입 또는 완성형 웹 인터페이스 |
| **백엔드 (API)** | FastAPI (Python 3.11+) | 고성능 비동기 Python 웹 프레임워크 |
| **데이터베이스** | PostgreSQL 15+ | 안정적이고 ORM 기반의 DB 설계 |
| **인증/세션** | FastAPI Users + OAuth2 + JWT | 로그인, JWT 인증 |
| **테스트** | pytest (단위/통합 테스트) | 단위/통합 테스트 |
| **문서화** | Swagger / ReDoc (FastAPI 자동 문서) | API 자동 문서 생성 |
| **배포/환경** | Render (Web Service + Static + PostgreSQL) | 백엔드, DB, 프론트엔드 통합 설정 환경 구성 |
| **ORM** | SQLAlchemy 2.0 + Alembic | 데이터베이스 모델링 및 마이그레이션 |
| **스타일링** | Tailwind CSS + Shadcn/ui | 빠른 UI 개발 |
| **상태관리** | Zustand / Redux Toolkit + React Query | 클라이언트/서버 상태 관리 |

---

## 8. 개발 로드맵

### Phase 1: 기본 기능 구현 (4주)

**Week 1: 프로젝트 설정 및 DB 구축**
- [ ] 프로젝트 초기 설정
  - Frontend: React + Vite + TypeScript 프로젝트 생성
  - Backend: FastAPI + Poetry/pip 환경 설정
- [ ] 데이터베이스 스키마 생성 (SQLAlchemy models)
- [ ] Alembic 마이그레이션 설정
- [ ] API 기본 구조 설정 (FastAPI routers)
- [ ] 개발 환경 구성 (.env, ESLint, Black, Pylint)
- [ ] Render 프로젝트 초기 배포 테스트

**Week 2: 인증 및 메뉴 기능**
- [ ] 회원가입 / 로그인 / 로그아웃 (FastAPI Users)
- [ ] JWT 인증 미들웨어
- [ ] 메뉴 CRUD API (FastAPI endpoints)
- [ ] 메뉴 목록 / 상세 페이지 (React components)
- [ ] API 문서 확인 (Swagger/ReDoc)

**Week 3: 주문 기능 (고객)**
- [ ] 장바구니 기능 (Zustand/Redux)
- [ ] 주문 생성 API (FastAPI)
- [ ] 주문 확인 페이지 (React)
- [ ] 주문 내역 조회 (FastAPI + React)

**Week 4: 주문 관리 (관리자)**
- [ ] 관리자 대시보드 UI (React)
- [ ] 주문 상태 변경 API (FastAPI)
- [ ] 실시간 주문 알림 (WebSocket/Polling)
- [ ] 기본 테스트 (pytest for Backend)

---

### Phase 2: 고급 기능 (2주)

**Week 5: 커스터마이징 및 통계**
- [ ] 메뉴 옵션 커스터마이징 (React forms)
- [ ] 즐겨찾기 기능 (FastAPI + React)
- [ ] 관리자 통계 대시보드 (FastAPI aggregation)
- [ ] 매출 그래프 (Recharts)

**Week 6: 최적화 및 UX 개선**
- [ ] 반응형 디자인 완성 (Tailwind CSS)
- [ ] 로딩 상태 처리 (React Query)
- [ ] 에러 처리 개선 (FastAPI exception handlers)
- [ ] QR 코드 생성 (Python qrcode + React display)

---

### Phase 3: 배포 및 테스트 (1주)

**Week 7: 배포 및 마무리**
- [ ] 프로덕션 빌드 최적화
  - Frontend: Vite build 최적화
  - Backend: Uvicorn production settings
- [ ] Render 배포
  - Static Site (React Frontend)
  - Web Service (FastAPI Backend)
  - PostgreSQL Database 연결
- [ ] E2E 테스트 (Playwright/Cypress 선택적)
- [ ] pytest 단위 테스트 커버리지 확인
- [ ] 문서 정리 (README, API 문서)
- [ ] 환경 변수 및 시크릿 설정

---

## 9. 우선순위 매트릭스

| 기능 | 우선순위 | 난이도 | 예상 시간 |
|------|---------|-------|----------|
| 회원가입/로그인 (FastAPI Users) | 🔴 P0 | 중 | 2일 |
| 메뉴 조회 (FastAPI + React) | 🔴 P0 | 낮 | 1일 |
| 주문 생성 (FastAPI) | 🔴 P0 | 중 | 3일 |
| 주문 상태 추적 | 🔴 P0 | 중 | 2일 |
| 관리자 대시보드 | 🔴 P0 | 높 | 4일 |
| 메뉴 관리 (CRUD) | 🔴 P0 | 중 | 2일 |
| 주문 내역 조회 | 🟡 P1 | 낮 | 1일 |
| 커스터마이징 | 🟡 P1 | 중 | 3일 |
| 즐겨찾기 | 🟡 P1 | 낮 | 1일 |
| 통계 대시보드 | 🟡 P1 | 중 | 3일 |
| 실시간 알림 (WebSocket) | 🟡 P1 | 높 | 3일 |
| QR 코드 | 🟢 P2 | 낮 | 1일 |
| 재주문 | 🟢 P2 | 낮 | 1일 |

---

## 10. 리스크 및 대응 방안

### 10.1 기술적 리스크

| 리스크 | 확률 | 영향도 | 대응 방안 |
|-------|------|-------|----------|
| FastAPI 비동기 처리 복잡도 | 중 | 중 | 동기 함수로 시작 후 점진적 비동기 전환 |
| 실시간 업데이트 구현 어려움 | 중 | 중 | WebSocket 대신 Polling 사용 |
| 데이터베이스 성능 이슈 | 낮 | 높 | 인덱싱 및 쿼리 최적화, SQLAlchemy lazy loading 활용 |
| Render 무료 플랜 제약 | 중 | 중 | Cold start 이슈 안내, 유료 플랜 고려 |
| 보안 취약점 | 중 | 높 | OWASP 체크리스트 준수, FastAPI Users 활용 |

### 10.2 일정 리스크

| 리스크 | 확률 | 대응 방안 |
|-------|------|----------|
| FastAPI 학습 곡선 | 중 | 공식 문서 및 튜토리얼 사전 학습 |
| 기능 개발 지연 | 높 | MVP 기능 우선 개발, P2 기능 연기 |
| 테스트 시간 부족 | 중 | 개발 중 지속적인 pytest 테스트 |
| 디자인 작업 지연 | 중 | Tailwind CSS + Shadcn/ui 적극 활용 |

---

## 11. 참고 자료

### 11.1 유사 서비스

- 스타벅스 사이렌오더
- 메가커피 앱
- 투썸플레이스 주문 앱

### 11.2 기술 문서

**Frontend**
- [React 공식 문서](https://react.dev)
- [TypeScript 공식 문서](https://www.typescriptlang.org/docs/)
- [Vite 공식 문서](https://vitejs.dev)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [Shadcn/ui 문서](https://ui.shadcn.com)

**Backend**
- [FastAPI 공식 문서](https://fastapi.tiangolo.com)
- [FastAPI Users 문서](https://fastapi-users.github.io/fastapi-users/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org)
- [Pydantic 문서](https://docs.pydantic.dev)
- [Alembic 문서](https://alembic.sqlalchemy.org)

**Database & Deployment**
- [PostgreSQL 문서](https://www.postgresql.org/docs/)
- [Render 문서](https://render.com/docs)

**Authentication**
- [JWT 소개](https://jwt.io)
- [OAuth2 스펙](https://oauth.net/2/)

---

## 12. 문서 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-11-02 | kznetwork | 초안 작성 |
| 1.1 | 2025-11-02 | kznetwork | 기술 스택을 Python + FastAPI + React + Render로 확정 및 업데이트 |

---

**문서 승인**
- 작성자: kznetwork
- 검토자: (TBD)
- 승인일: 2025-11-02

---

**다음 단계**: [개발 환경 설정 및 프로젝트 초기화](./technical-setup.md)

