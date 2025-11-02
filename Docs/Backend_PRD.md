# OrderBean Backend - Product Requirements Document (PRD)

**버전**: 1.0  
**작성일**: 2025년 11월 2일  
**작성자**: kznetwork  
**프로젝트 타입**: Toy Project / Portfolio - Backend Development

---

## 📑 목차

1. [개요](#1-개요)
2. [데이터 모델](#2-데이터-모델)
3. [API 설계](#3-api-설계)
4. [비즈니스 로직](#4-비즈니스-로직)
5. [기술 스택](#5-기술-스택)
6. [개발 로드맵](#6-개발-로드맵)

---

## 1. 개요

### 1.1 백엔드 개발 목적

OrderBean 백엔드는 커피 주문 관리 시스템의 핵심 비즈니스 로직과 데이터 처리를 담당합니다. RESTful API를 통해 프론트엔드에 데이터를 제공하고, 주문 및 재고 관리 기능을 구현합니다.

### 1.2 핵심 기능

- 메뉴 정보 관리 및 제공
- 주문 처리 및 상태 관리
- 재고 관리
- 옵션 관리
- 관리자 기능 제공

### 1.3 백엔드 아키텍처

```
┌─────────────────────────────────────────┐
│         Frontend (React)                │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────────┐
│         API Layer (FastAPI)             │
│  - Routes/Controllers                   │
│  - Request/Response Validation          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Business Logic Layer               │
│  - 주문 처리 로직                        │
│  - 재고 관리 로직                        │
│  - 상태 변경 로직                        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Data Access Layer (ORM)            │
│  - SQLAlchemy Models                    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Database (PostgreSQL)              │
└─────────────────────────────────────────┘
```

---

## 2. 데이터 모델

### 2.1 ERD (Entity Relationship Diagram)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Menus     │         │   Orders    │         │   Options   │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │◄───┐    │ id (PK)     │    ┌───│ id (PK)     │
│ name        │    │    │ order_number│    │   │ name        │
│ description │    │    │ status      │    │   │ price       │
│ price       │    │    │ total_amount│    │   │ menu_id(FK) │
│ image_url   │    │    │ created_at  │    │   │ created_at  │
│ stock       │    │    │ updated_at  │    │   │ updated_at  │
│ created_at  │    │    └─────────────┘    │   └─────────────┘
│ updated_at  │    │            │          │
└─────────────┘    │            │          │
                   │    ┌───────┴──────────┼──────────┐
                   │    │                  │          │
                   │    ▼                  ▼          │
                   │ ┌─────────────────────────────┐  │
                   │ │   OrderItems                │  │
                   │ ├─────────────────────────────┤  │
                   └►│ id (PK)                     │  │
                     │ order_id (FK)               │  │
                     │ menu_id (FK)                │◄─┘
                     │ quantity                    │
                     │ unit_price                  │
                     │ subtotal                    │
                     │ selected_options (JSON)     │
                     │ created_at                  │
                     └─────────────────────────────┘
```

---

### 2.2 테이블 상세 정의

#### ☕ Menus (메뉴)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 메뉴 고유 ID |
| name | VARCHAR(100) | NOT NULL, UNIQUE | 커피 이름 |
| description | TEXT | NULL | 메뉴 설명 |
| price | DECIMAL(10,2) | NOT NULL | 기본 가격 |
| image_url | VARCHAR(500) | NULL | 이미지 URL |
| stock | INT | NOT NULL, DEFAULT 0 | 재고 수량 |
| is_available | BOOLEAN | DEFAULT TRUE | 판매 가능 여부 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**인덱스**
- PRIMARY KEY: id
- UNIQUE INDEX: name
- INDEX: is_available

**비즈니스 규칙**
- `stock`이 0이면 자동으로 `is_available = FALSE`로 변경
- 주문 시 `stock` 감소
- 음수 재고 불가 (재고 부족 시 주문 거부)

---

#### 🎨 Options (옵션)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 옵션 고유 ID |
| menu_id | INT | FK, NOT NULL | 연결된 메뉴 ID |
| name | VARCHAR(100) | NOT NULL | 옵션 이름 (예: "샷 추가", "사이즈 업") |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | 옵션 추가 가격 |
| option_type | VARCHAR(50) | NOT NULL | 옵션 유형 (size, shot, syrup, ice, etc.) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**인덱스**
- PRIMARY KEY: id
- INDEX: menu_id
- INDEX: option_type

**옵션 유형**
- `size`: 사이즈 (Tall, Grande, Venti)
- `shot`: 샷 추가
- `syrup`: 시럽 추가 (바닐라, 카라멜 등)
- `ice`: 얼음 조절 (많이, 보통, 적게, 없음)
- `whipped`: 휘핑크림 추가/제거

**예시 데이터**
```sql
-- 아메리카노 (menu_id = 1) 옵션
INSERT INTO options (menu_id, name, price, option_type) VALUES
(1, 'Tall', 0, 'size'),
(1, 'Grande', 500, 'size'),
(1, 'Venti', 1000, 'size'),
(1, '샷 추가', 500, 'shot'),
(1, '얼음 적게', 0, 'ice'),
(1, '바닐라 시럽', 500, 'syrup');
```

---

#### 📦 Orders (주문)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 고유 ID |
| order_number | VARCHAR(50) | UNIQUE, NOT NULL | 주문 번호 (ORD-YYYYMMDD-XXX) |
| status | ENUM | NOT NULL | 주문 상태 |
| total_amount | DECIMAL(10,2) | NOT NULL | 총 주문 금액 |
| special_request | TEXT | NULL | 특별 요청사항 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 주문 일시 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 수정일시 |

**status ENUM 값**
- `pending`: 주문 접수 (기본값)
- `preparing`: 제조 중
- `completed`: 완료
- `cancelled`: 취소됨

**주문 번호 생성 규칙**
```python
# 형식: ORD-YYYYMMDD-XXX
# 예시: ORD-20251102-001, ORD-20251102-002
order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{sequence:03d}"
```

**인덱스**
- PRIMARY KEY: id
- UNIQUE INDEX: order_number
- INDEX: status
- INDEX: created_at

**상태 전이 규칙**
```
pending → preparing → completed
   ↓
cancelled (취소는 pending 상태에서만 가능)
```

---

#### 🛒 OrderItems (주문 상세)

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| id | INT | PK, AUTO_INCREMENT | 주문 아이템 ID |
| order_id | INT | FK, NOT NULL | 주문 ID |
| menu_id | INT | FK, NOT NULL | 메뉴 ID |
| quantity | INT | NOT NULL | 수량 |
| unit_price | DECIMAL(10,2) | NOT NULL | 개당 가격 (옵션 포함) |
| subtotal | DECIMAL(10,2) | NOT NULL | 소계 (unit_price * quantity) |
| selected_options | JSON | NULL | 선택된 옵션 정보 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 생성일시 |

**selected_options JSON 구조**
```json
{
  "size": {
    "id": 2,
    "name": "Grande",
    "price": 500
  },
  "extras": [
    {
      "id": 4,
      "name": "샷 추가",
      "price": 500,
      "option_type": "shot"
    },
    {
      "id": 6,
      "name": "바닐라 시럽",
      "price": 500,
      "option_type": "syrup"
    }
  ],
  "ice": {
    "id": 5,
    "name": "얼음 적게",
    "price": 0
  }
}
```

**가격 계산 로직**
```python
# unit_price = 메뉴 기본 가격 + 모든 옵션 가격의 합
unit_price = menu.price + sum(option.price for option in selected_options)

# subtotal = unit_price * quantity
subtotal = unit_price * quantity
```

**인덱스**
- PRIMARY KEY: id
- INDEX: order_id
- INDEX: menu_id

---

### 2.3 관계 정의

1. **Menus ↔ Options**: 1:N (한 메뉴는 여러 옵션 가능)
2. **Orders ↔ OrderItems**: 1:N (한 주문은 여러 메뉴 아이템 포함)
3. **Menus ↔ OrderItems**: 1:N (한 메뉴는 여러 주문에 포함 가능)

---

### 2.4 데이터베이스 제약조건

```sql
-- Foreign Key Constraints
ALTER TABLE options
ADD CONSTRAINT fk_options_menu
FOREIGN KEY (menu_id) REFERENCES menus(id)
ON DELETE CASCADE;

ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_order
FOREIGN KEY (order_id) REFERENCES orders(id)
ON DELETE CASCADE;

ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_menu
FOREIGN KEY (menu_id) REFERENCES menus(id)
ON DELETE RESTRICT;

-- Check Constraints
ALTER TABLE menus
ADD CONSTRAINT chk_menus_price CHECK (price >= 0);

ALTER TABLE menus
ADD CONSTRAINT chk_menus_stock CHECK (stock >= 0);

ALTER TABLE options
ADD CONSTRAINT chk_options_price CHECK (price >= 0);

ALTER TABLE orders
ADD CONSTRAINT chk_orders_total CHECK (total_amount > 0);

ALTER TABLE order_items
ADD CONSTRAINT chk_order_items_quantity CHECK (quantity > 0);

ALTER TABLE order_items
ADD CONSTRAINT chk_order_items_price CHECK (unit_price >= 0);
```

---

## 3. API 설계

### 3.1 API 설계 원칙

- **RESTful API** 표준 준수
- **JSON** 형식 사용
- **HTTP 상태 코드** 명확히 사용
- **API 버전 관리**: `/api/v1/`
- **에러 응답 일관성**
- **FastAPI** 기반 자동 문서 생성 (Swagger/ReDoc)

---

### 3.2 메뉴 API

#### 📌 GET /api/v1/menus

**설명**: 메뉴 목록 조회

**쿼리 파라미터**
- `available` (optional, boolean): 판매 가능한 메뉴만 필터링

**요청 예시**
```http
GET /api/v1/menus?available=true
```

**응답 (200 OK)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "description": "진한 에스프레소와 물",
      "price": 4500,
      "imageUrl": "/images/americano.jpg",
      "stock": 50,
      "isAvailable": true,
      "options": [
        {
          "id": 1,
          "name": "Tall",
          "price": 0,
          "optionType": "size"
        },
        {
          "id": 2,
          "name": "Grande",
          "price": 500,
          "optionType": "size"
        },
        {
          "id": 4,
          "name": "샷 추가",
          "price": 500,
          "optionType": "shot"
        }
      ]
    },
    {
      "id": 2,
      "name": "카페라떼",
      "description": "부드러운 우유와 에스프레소",
      "price": 5000,
      "imageUrl": "/images/latte.jpg",
      "stock": 35,
      "isAvailable": true,
      "options": [...]
    }
  ]
}
```

**비즈니스 로직**
1. 데이터베이스에서 메뉴 목록 조회
2. `available=true`인 경우 `is_available=TRUE`인 메뉴만 필터링
3. 각 메뉴에 연결된 옵션 목록도 함께 조회 (JOIN)
4. 관리자 권한이 아닌 경우 `stock` 정보 숨김 처리

---

#### 📌 GET /api/v1/menus/:id

**설명**: 메뉴 상세 조회

**요청 예시**
```http
GET /api/v1/menus/1
```

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "아메리카노",
    "description": "진한 에스프레소와 물",
    "price": 4500,
    "imageUrl": "/images/americano.jpg",
    "stock": 50,
    "isAvailable": true,
    "options": [
      {
        "id": 1,
        "name": "Tall",
        "price": 0,
        "optionType": "size"
      },
      {
        "id": 2,
        "name": "Grande",
        "price": 500,
        "optionType": "size"
      }
    ]
  }
}
```

**에러 응답 (404 Not Found)**
```json
{
  "success": false,
  "error": {
    "code": "MENU_NOT_FOUND",
    "message": "메뉴를 찾을 수 없습니다."
  }
}
```

---

#### 📌 POST /api/v1/menus (관리자 전용)

**설명**: 메뉴 등록

**요청 헤더**
```
Authorization: Bearer {admin_token}
```

**요청 Body**
```json
{
  "name": "콜드브루",
  "description": "12시간 저온 추출",
  "price": 5500,
  "imageUrl": "/images/coldbrew.jpg",
  "stock": 30
}
```

**응답 (201 Created)**
```json
{
  "success": true,
  "message": "메뉴가 등록되었습니다.",
  "data": {
    "id": 10,
    "name": "콜드브루",
    "price": 5500,
    "stock": 30
  }
}
```

**비즈니스 로직**
1. 관리자 권한 확인
2. 메뉴명 중복 체크
3. 가격, 재고 유효성 검증
4. 데이터베이스에 메뉴 생성
5. 생성된 메뉴 정보 반환

---

#### 📌 PATCH /api/v1/menus/:id/stock (관리자 전용)

**설명**: 메뉴 재고 수정

**요청 Body**
```json
{
  "stock": 20
}
```

**응답 (200 OK)**
```json
{
  "success": true,
  "message": "재고가 수정되었습니다.",
  "data": {
    "id": 1,
    "name": "아메리카노",
    "stock": 20,
    "isAvailable": true
  }
}
```

**비즈니스 로직**
1. 관리자 권한 확인
2. 메뉴 존재 여부 확인
3. 재고 유효성 검증 (음수 불가)
4. 재고 업데이트
5. 재고가 0인 경우 `is_available = FALSE` 자동 설정

---

### 3.3 주문 API

#### 📌 POST /api/v1/orders

**설명**: 주문 생성

**요청 Body**
```json
{
  "items": [
    {
      "menuId": 1,
      "quantity": 2,
      "selectedOptions": [
        {
          "id": 2,
          "name": "Grande",
          "price": 500,
          "optionType": "size"
        },
        {
          "id": 4,
          "name": "샷 추가",
          "price": 500,
          "optionType": "shot"
        }
      ]
    },
    {
      "menuId": 5,
      "quantity": 1,
      "selectedOptions": []
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
    "totalAmount": 15000,
    "items": [
      {
        "menuName": "아메리카노",
        "quantity": 2,
        "unitPrice": 5500,
        "subtotal": 11000,
        "options": [
          {
            "name": "Grande",
            "price": 500
          },
          {
            "name": "샷 추가",
            "price": 500
          }
        ]
      },
      {
        "menuName": "크루아상",
        "quantity": 1,
        "unitPrice": 4000,
        "subtotal": 4000,
        "options": []
      }
    ],
    "createdAt": "2025-11-02T09:30:00Z"
  }
}
```

**비즈니스 로직**
1. **데이터 유효성 검증**
   - 모든 메뉴 ID가 유효한지 확인
   - 모든 옵션 ID가 해당 메뉴에 속하는지 확인
   - 수량이 양수인지 확인

2. **재고 확인**
   ```python
   for item in items:
       menu = get_menu(item.menu_id)
       if menu.stock < item.quantity:
           raise InsufficientStockError(f"{menu.name} 재고가 부족합니다.")
   ```

3. **가격 계산**
   ```python
   for item in items:
       menu = get_menu(item.menu_id)
       option_total = sum(option.price for option in item.selected_options)
       item.unit_price = menu.price + option_total
       item.subtotal = item.unit_price * item.quantity
   
   order.total_amount = sum(item.subtotal for item in items)
   ```

4. **트랜잭션 처리**
   ```python
   with db.transaction():
       # 1. 주문 생성
       order = create_order(status='pending', total_amount=total)
       
       # 2. 주문 아이템 생성
       for item in items:
           create_order_item(order_id=order.id, ...)
       
       # 3. 재고 감소
       for item in items:
           decrease_stock(menu_id=item.menu_id, quantity=item.quantity)
       
       # 4. 재고가 0이면 is_available = False로 설정
       for item in items:
           menu = get_menu(item.menu_id)
           if menu.stock == 0:
               update_menu(menu.id, is_available=False)
   ```

5. **주문 번호 생성**
   ```python
   today = datetime.now().strftime('%Y%m%d')
   sequence = get_today_order_count() + 1
   order_number = f"ORD-{today}-{sequence:03d}"
   ```

**에러 응답 (400 Bad Request)**
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "아메리카노의 재고가 부족합니다. (현재 재고: 1개)"
  }
}
```

---

#### 📌 GET /api/v1/orders/:id

**설명**: 주문 상세 조회

**요청 예시**
```http
GET /api/v1/orders/42
```

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "id": 42,
    "orderNumber": "ORD-20251102-042",
    "status": "preparing",
    "totalAmount": 15000,
    "specialRequest": "빨대 2개 주세요",
    "createdAt": "2025-11-02T09:30:00Z",
    "updatedAt": "2025-11-02T09:35:00Z",
    "items": [
      {
        "id": 101,
        "menuName": "아메리카노",
        "quantity": 2,
        "unitPrice": 5500,
        "subtotal": 11000,
        "selectedOptions": [
          {
            "name": "Grande",
            "price": 500,
            "optionType": "size"
          },
          {
            "name": "샷 추가",
            "price": 500,
            "optionType": "shot"
          }
        ]
      }
    ]
  }
}
```

**에러 응답 (404 Not Found)**
```json
{
  "success": false,
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "주문을 찾을 수 없습니다."
  }
}
```

---

### 3.4 관리자 주문 관리 API

#### 📌 GET /api/v1/admin/orders (관리자 전용)

**설명**: 전체 주문 목록 조회

**쿼리 파라미터**
- `status` (optional): 주문 상태 필터링
- `date` (optional): 특정 날짜의 주문만 조회

**요청 예시**
```http
GET /api/v1/admin/orders?status=pending
```

**응답 (200 OK)**
```json
{
  "success": true,
  "data": {
    "summary": {
      "pending": 8,
      "preparing": 3,
      "completed": 45,
      "todayRevenue": 337500
    },
    "orders": [
      {
        "id": 42,
        "orderNumber": "ORD-20251102-042",
        "status": "pending",
        "totalAmount": 15000,
        "itemCount": 2,
        "specialRequest": "빨대 2개 주세요",
        "createdAt": "2025-11-02T09:30:00Z"
      },
      {
        "id": 41,
        "orderNumber": "ORD-20251102-041",
        "status": "pending",
        "totalAmount": 9000,
        "itemCount": 1,
        "specialRequest": null,
        "createdAt": "2025-11-02T09:25:00Z"
      }
    ]
  }
}
```

**비즈니스 로직**
1. 관리자 권한 확인
2. 상태별 주문 통계 계산
3. 당일 매출 계산
4. 주문 목록 조회 (최신순)
5. 상태 필터 적용 (있는 경우)

---

#### 📌 PATCH /api/v1/admin/orders/:id/status (관리자 전용)

**설명**: 주문 상태 변경

**요청 Body**
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

**비즈니스 로직**
1. 관리자 권한 확인
2. 주문 존재 여부 확인
3. 상태 전이 규칙 검증
   ```python
   # 허용된 상태 전이
   ALLOWED_TRANSITIONS = {
       'pending': ['preparing', 'cancelled'],
       'preparing': ['completed'],
       'completed': [],  # 완료 상태에서는 변경 불가
       'cancelled': []   # 취소 상태에서는 변경 불가
   }
   
   if new_status not in ALLOWED_TRANSITIONS[current_status]:
       raise InvalidStatusTransitionError()
   ```
4. 주문 상태 업데이트
5. `updated_at` 자동 갱신

**에러 응답 (400 Bad Request)**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_STATUS_TRANSITION",
    "message": "완료된 주문은 상태를 변경할 수 없습니다."
  }
}
```

---

#### 📌 GET /api/v1/admin/menus/stock (관리자 전용)

**설명**: 전체 메뉴의 재고 현황 조회

**응답 (200 OK)**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "stock": 50,
      "isAvailable": true,
      "lowStock": false
    },
    {
      "id": 2,
      "name": "카페라떼",
      "stock": 5,
      "isAvailable": true,
      "lowStock": true
    },
    {
      "id": 3,
      "name": "콜드브루",
      "stock": 0,
      "isAvailable": false,
      "lowStock": true
    }
  ]
}
```

**비즈니스 로직**
1. 관리자 권한 확인
2. 모든 메뉴의 재고 정보 조회
3. 재고 10개 이하면 `lowStock: true` 플래그 추가
4. 재고 0개면 `isAvailable: false` 자동 설정

---

### 3.5 에러 응답 표준 형식

모든 에러는 다음 형식을 따릅니다:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적 에러 메시지",
    "details": {}
  }
}
```

**주요 HTTP 상태 코드**
- `200 OK`: 성공
- `201 Created`: 생성 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음 (관리자 기능)
- `404 Not Found`: 리소스 없음
- `409 Conflict`: 재고 부족, 중복 데이터 등
- `500 Internal Server Error`: 서버 오류

**주요 에러 코드**
- `MENU_NOT_FOUND`: 메뉴를 찾을 수 없음
- `ORDER_NOT_FOUND`: 주문을 찾을 수 없음
- `INSUFFICIENT_STOCK`: 재고 부족
- `INVALID_STATUS_TRANSITION`: 잘못된 상태 전이
- `UNAUTHORIZED`: 인증 필요
- `FORBIDDEN`: 관리자 권한 필요
- `VALIDATION_ERROR`: 입력 데이터 검증 실패

---

## 4. 비즈니스 로직

### 4.1 사용자 흐름 및 백엔드 처리

#### 🔄 흐름 1: 메뉴 표시

**프론트엔드**
1. 사용자가 메뉴 페이지 접속
2. `GET /api/v1/menus?available=true` 호출

**백엔드 처리**
```python
async def get_menus(available: bool = None):
    query = select(Menu).options(selectinload(Menu.options))
    
    if available:
        query = query.where(Menu.is_available == True)
    
    result = await db.execute(query)
    menus = result.scalars().all()
    
    return {
        "success": True,
        "data": [menu.to_dict() for menu in menus]
    }
```

**관리자 화면**
- 관리자는 `GET /api/v1/admin/menus/stock` 호출하여 재고 포함 정보 조회

---

#### 🔄 흐름 2: 장바구니에 메뉴 추가

**프론트엔드**
1. 사용자가 메뉴 선택
2. 옵션 선택
3. 장바구니 상태 관리 (프론트엔드에서 처리)

**백엔드 처리**
- 이 단계에서는 백엔드 호출 없음
- 장바구니는 프론트엔드 상태 관리 (Zustand/Redux)

---

#### 🔄 흐름 3: 주문하기

**프론트엔드**
1. 사용자가 장바구니에서 "주문하기" 버튼 클릭
2. `POST /api/v1/orders` 호출

**백엔드 처리 플로우**
```python
async def create_order(order_data: OrderCreate):
    async with db.begin():  # 트랜잭션 시작
        try:
            # 1. 메뉴 및 옵션 검증
            for item in order_data.items:
                menu = await validate_menu(item.menu_id)
                await validate_options(item.menu_id, item.selected_options)
            
            # 2. 재고 확인
            for item in order_data.items:
                if not await check_stock(item.menu_id, item.quantity):
                    raise InsufficientStockError(f"{menu.name} 재고 부족")
            
            # 3. 가격 계산
            total_amount = 0
            order_items_data = []
            
            for item in order_data.items:
                menu = await get_menu(item.menu_id)
                
                # 옵션 가격 합산
                option_total = sum(opt.price for opt in item.selected_options)
                unit_price = menu.price + option_total
                subtotal = unit_price * item.quantity
                
                total_amount += subtotal
                
                order_items_data.append({
                    "menu_id": item.menu_id,
                    "quantity": item.quantity,
                    "unit_price": unit_price,
                    "subtotal": subtotal,
                    "selected_options": item.selected_options
                })
            
            # 4. 주문 번호 생성
            order_number = await generate_order_number()
            
            # 5. 주문 생성
            order = Order(
                order_number=order_number,
                status="pending",
                total_amount=total_amount,
                special_request=order_data.special_request
            )
            db.add(order)
            await db.flush()  # order.id 생성
            
            # 6. 주문 아이템 생성
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    **item_data
                )
                db.add(order_item)
            
            # 7. 재고 감소
            for item in order_data.items:
                await decrease_stock(item.menu_id, item.quantity)
            
            # 8. 재고 0이면 판매 중지
            for item in order_data.items:
                menu = await get_menu(item.menu_id)
                if menu.stock == 0:
                    menu.is_available = False
            
            await db.commit()
            
            # 9. 주문 정보 반환
            return {
                "success": True,
                "message": "주문이 완료되었습니다.",
                "data": await get_order_detail(order.id)
            }
            
        except Exception as e:
            await db.rollback()
            raise
```

---

#### 🔄 흐름 4: 주문 현황 관리

**프론트엔드 (관리자)**
1. 관리자가 관리자 대시보드 접속
2. `GET /api/v1/admin/orders` 호출
3. 실시간 주문 현황 표시

**백엔드 처리**
```python
async def get_admin_orders(status: str = None):
    # 통계 계산
    summary = await calculate_order_summary()
    
    # 주문 목록 조회
    query = select(Order).order_by(Order.created_at.desc())
    
    if status:
        query = query.where(Order.status == status)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return {
        "success": True,
        "data": {
            "summary": summary,
            "orders": [order.to_dict() for order in orders]
        }
    }

async def calculate_order_summary():
    today = datetime.now().date()
    
    # 상태별 주문 수
    pending_count = await count_orders_by_status("pending")
    preparing_count = await count_orders_by_status("preparing")
    completed_count = await count_orders_by_status("completed", today)
    
    # 당일 매출
    today_revenue = await calculate_revenue(today)
    
    return {
        "pending": pending_count,
        "preparing": preparing_count,
        "completed": completed_count,
        "todayRevenue": today_revenue
    }
```

**주문 상태 변경**
```python
async def update_order_status(order_id: int, new_status: str):
    order = await get_order_or_404(order_id)
    
    # 상태 전이 검증
    if not is_valid_transition(order.status, new_status):
        raise InvalidStatusTransitionError(
            f"'{order.status}'에서 '{new_status}'로 변경할 수 없습니다."
        )
    
    order.status = new_status
    await db.commit()
    
    return {
        "success": True,
        "message": "주문 상태가 변경되었습니다.",
        "data": order.to_dict()
    }

def is_valid_transition(current: str, new: str) -> bool:
    transitions = {
        "pending": ["preparing", "cancelled"],
        "preparing": ["completed"],
        "completed": [],
        "cancelled": []
    }
    return new in transitions.get(current, [])
```

---

### 4.2 재고 관리 로직

#### 재고 감소

```python
async def decrease_stock(menu_id: int, quantity: int):
    """주문 시 재고 감소"""
    menu = await get_menu_or_404(menu_id)
    
    if menu.stock < quantity:
        raise InsufficientStockError(
            f"{menu.name}의 재고가 부족합니다. (현재 재고: {menu.stock}개)"
        )
    
    menu.stock -= quantity
    
    # 재고가 0이면 판매 중지
    if menu.stock == 0:
        menu.is_available = False
    
    await db.commit()
```

#### 재고 증가 (관리자)

```python
async def increase_stock(menu_id: int, quantity: int):
    """관리자가 재고 추가"""
    menu = await get_menu_or_404(menu_id)
    
    menu.stock += quantity
    
    # 재고가 추가되면 판매 재개
    if menu.stock > 0 and not menu.is_available:
        menu.is_available = True
    
    await db.commit()
    
    return menu
```

#### 재고 설정 (관리자)

```python
async def set_stock(menu_id: int, stock: int):
    """관리자가 재고 직접 설정"""
    if stock < 0:
        raise ValidationError("재고는 음수일 수 없습니다.")
    
    menu = await get_menu_or_404(menu_id)
    menu.stock = stock
    
    # 재고에 따라 판매 가능 여부 설정
    menu.is_available = (stock > 0)
    
    await db.commit()
    
    return menu
```

---

### 4.3 주문 번호 생성 로직

```python
async def generate_order_number() -> str:
    """
    주문 번호 생성: ORD-YYYYMMDD-XXX
    예시: ORD-20251102-001
    """
    today = datetime.now().strftime('%Y%m%d')
    
    # 당일 주문 수 조회
    today_start = datetime.now().replace(hour=0, minute=0, second=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59)
    
    query = select(func.count(Order.id)).where(
        Order.created_at >= today_start,
        Order.created_at <= today_end
    )
    result = await db.execute(query)
    count = result.scalar() or 0
    
    sequence = count + 1
    order_number = f"ORD-{today}-{sequence:03d}"
    
    return order_number
```

---

## 5. 기술 스택

### 5.1 백엔드 프레임워크

**핵심 기술**
- **Python 3.11+**: 최신 Python 버전
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **Pydantic v2**: 데이터 검증 및 직렬화

**FastAPI 선택 이유**
- 자동 API 문서 생성 (Swagger/ReDoc)
- 타입 힌트 기반 자동 검증
- 비동기 처리 지원 (async/await)
- 빠른 성능 (Starlette 기반)
- 직관적인 라우팅 및 의존성 주입

---

### 5.2 데이터베이스

**데이터베이스**
- **PostgreSQL 15+**: 관계형 데이터베이스
- **asyncpg**: 비동기 PostgreSQL 드라이버

**ORM 및 마이그레이션**
- **SQLAlchemy 2.0**: ORM (Object-Relational Mapping)
- **Alembic**: 데이터베이스 스키마 마이그레이션

**PostgreSQL 선택 이유**
- 안정적인 트랜잭션 처리 (ACID)
- JSON 컬럼 지원 (OrderItems의 selected_options)
- 풍부한 인덱싱 기능
- 무료 호스팅 지원 (Render, Supabase)

---

### 5.3 인증 및 보안

**인증**
- **FastAPI Users**: 사용자 인증 시스템
- **OAuth2** with **JWT**: 토큰 기반 인증
- **python-jose**: JWT 생성/검증
- **passlib[bcrypt]**: 비밀번호 해싱

**보안 고려사항**
- 비밀번호 bcrypt 해싱 (최소 12 rounds)
- JWT 토큰 만료 시간 설정
- HTTPS 적용 (프로덕션)
- CORS 정책 설정

---

### 5.4 테스트

**테스트 프레임워크**
- **pytest**: 단위 테스트 및 통합 테스트
- **pytest-asyncio**: 비동기 함수 테스트
- **httpx**: FastAPI 테스트 클라이언트
- **faker**: 테스트 데이터 생성

**테스트 커버리지 목표**
- 단위 테스트: 70% 이상
- 통합 테스트: 주요 API 엔드포인트

---

### 5.5 배포

**배포 플랫폼**
- **Render**: 백엔드 호스팅
  - Web Service: FastAPI 애플리케이션
  - PostgreSQL: 관리형 데이터베이스

**환경 변수 관리**
- `.env` 파일 (로컬 개발)
- Render 환경 변수 (프로덕션)

**필수 환경 변수**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# Environment
ENVIRONMENT=production
```

---

### 5.6 개발 도구

**IDE**
- VS Code 또는 PyCharm

**API 테스트**
- Postman 또는 Insomnia
- FastAPI Swagger UI (내장)

**데이터베이스 관리**
- DBeaver 또는 pgAdmin

---

## 6. 개발 로드맵

### Phase 1: 프로젝트 설정 및 기본 구조 (1주)

**Day 1-2: 환경 설정**
- [ ] Python 가상환경 생성
- [ ] 의존성 설치 (FastAPI, SQLAlchemy, etc.)
- [ ] 프로젝트 구조 설정
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── api/
  │   │   ├── __init__.py
  │   │   ├── v1/
  │   │   │   ├── __init__.py
  │   │   │   ├── menus.py
  │   │   │   ├── orders.py
  │   │   │   └── admin.py
  │   ├── models/
  │   │   ├── __init__.py
  │   │   ├── menu.py
  │   │   ├── option.py
  │   │   ├── order.py
  │   │   └── order_item.py
  │   ├── schemas/
  │   │   ├── __init__.py
  │   │   ├── menu.py
  │   │   ├── option.py
  │   │   └── order.py
  │   ├── services/
  │   │   ├── __init__.py
  │   │   ├── menu_service.py
  │   │   └── order_service.py
  │   ├── core/
  │   │   ├── __init__.py
  │   │   ├── config.py
  │   │   └── database.py
  │   └── utils/
  │       ├── __init__.py
  │       └── exceptions.py
  ├── alembic/
  ├── tests/
  ├── .env.example
  ├── requirements.txt
  └── README.md
  ```

**Day 3-4: 데이터베이스 설정**
- [ ] PostgreSQL 연결 설정
- [ ] SQLAlchemy 모델 정의 (Menus, Options, Orders, OrderItems)
- [ ] Alembic 마이그레이션 초기화
- [ ] 초기 마이그레이션 생성 및 적용
- [ ] 시드 데이터 작성 (테스트용 메뉴 데이터)

**Day 5-7: 기본 API 구조**
- [ ] FastAPI 애플리케이션 설정
- [ ] CORS 설정
- [ ] 에러 핸들러 설정
- [ ] Pydantic 스키마 정의
- [ ] API 라우터 설정

---

### Phase 2: 메뉴 API 구현 (1주)

**Day 8-10: 메뉴 조회 API**
- [ ] `GET /api/v1/menus` 구현
- [ ] `GET /api/v1/menus/:id` 구현
- [ ] 메뉴-옵션 관계 쿼리 최적화
- [ ] Pydantic 응답 모델 정의
- [ ] 단위 테스트 작성

**Day 11-14: 관리자 메뉴 관리 API**
- [ ] 관리자 권한 미들웨어 구현
- [ ] `POST /api/v1/menus` 구현
- [ ] `PATCH /api/v1/menus/:id/stock` 구현
- [ ] `GET /api/v1/admin/menus/stock` 구현
- [ ] 재고 관리 로직 구현
- [ ] 통합 테스트 작성

---

### Phase 3: 주문 API 구현 (2주)

**Day 15-18: 주문 생성 API**
- [ ] `POST /api/v1/orders` 구현
- [ ] 주문 데이터 검증 로직
- [ ] 재고 확인 로직
- [ ] 가격 계산 로직
- [ ] 트랜잭션 처리
- [ ] 주문 번호 생성 로직
- [ ] 재고 감소 로직

**Day 19-21: 주문 조회 API**
- [ ] `GET /api/v1/orders/:id` 구현
- [ ] 주문 상세 정보 조회
- [ ] 단위 테스트 작성

**Day 22-28: 관리자 주문 관리 API**
- [ ] `GET /api/v1/admin/orders` 구현
- [ ] 주문 통계 계산 로직
- [ ] `PATCH /api/v1/admin/orders/:id/status` 구현
- [ ] 주문 상태 전이 검증 로직
- [ ] 통합 테스트 작성
- [ ] API 문서 확인 및 보완

---

### Phase 4: 테스트 및 최적화 (1주)

**Day 29-32: 테스트**
- [ ] 전체 API 엔드포인트 테스트
- [ ] 에러 케이스 테스트
- [ ] 경계값 테스트
- [ ] 동시성 테스트 (재고 처리)
- [ ] 테스트 커버리지 확인

**Day 33-35: 최적화 및 문서화**
- [ ] 쿼리 최적화 (N+1 문제 해결)
- [ ] 인덱스 추가
- [ ] API 문서 보완 (Swagger)
- [ ] README 작성
- [ ] 배포 가이드 작성

---

### Phase 5: 배포 (3일)

**Day 36-38: Render 배포**
- [ ] Render Web Service 생성
- [ ] PostgreSQL 데이터베이스 연결
- [ ] 환경 변수 설정
- [ ] 데이터베이스 마이그레이션 실행
- [ ] 시드 데이터 입력
- [ ] 프로덕션 테스트
- [ ] 프론트엔드 연동 테스트

---

## 7. 부록

### 7.1 SQLAlchemy 모델 예시

```python
# app/models/menu.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String(500))
    stock = Column(Integer, nullable=False, default=0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    options = relationship("Option", back_populates="menu", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="menu")
```

```python
# app/models/option.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Option(Base):
    __tablename__ = "options"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, default=0)
    option_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    menu = relationship("Menu", back_populates="options")
```

---

### 7.2 Pydantic 스키마 예시

```python
# app/schemas/order.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class OptionInOrder(BaseModel):
    id: int
    name: str
    price: Decimal
    option_type: str

class OrderItemCreate(BaseModel):
    menu_id: int = Field(..., gt=0, description="메뉴 ID")
    quantity: int = Field(..., gt=0, le=100, description="수량 (1-100)")
    selected_options: List[OptionInOrder] = []

class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_items=1, max_items=20)
    special_request: Optional[str] = Field(None, max_length=500)
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('주문 항목이 최소 1개 이상이어야 합니다.')
        return v

class OrderItemResponse(BaseModel):
    id: int
    menu_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    selected_options: List[OptionInOrder]

class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total_amount: Decimal
    special_request: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
```

---

### 7.3 API 응답 포맷 헬퍼

```python
# app/utils/response.py
from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(
    data: Any,
    message: Optional[str] = None,
    status_code: int = 200
) -> JSONResponse:
    """성공 응답 포맷"""
    response = {"success": True}
    if message:
        response["message"] = message
    response["data"] = data
    
    return JSONResponse(
        content=response,
        status_code=status_code
    )

def error_response(
    code: str,
    message: str,
    details: Optional[dict] = None,
    status_code: int = 400
) -> JSONResponse:
    """에러 응답 포맷"""
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        response["error"]["details"] = details
    
    return JSONResponse(
        content=response,
        status_code=status_code
    )
```

---

## 문서 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-11-02 | kznetwork | 백엔드 PRD 초안 작성 |

---

**문서 승인**
- 작성자: kznetwork
- 검토자: (TBD)
- 승인일: 2025-11-02

---

**다음 단계**: 백엔드 개발 환경 설정 및 데이터베이스 스키마 구현

