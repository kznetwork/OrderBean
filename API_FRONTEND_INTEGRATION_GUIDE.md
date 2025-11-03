# OrderBean API 및 프런트엔드 연동 가이드

**작성일**: 2025년 11월 3일  
**버전**: 1.0

---

## 📋 개요

OrderBean 프로젝트의 백엔드 API와 프런트엔드가 성공적으로 연동되었습니다. 이 문서는 구현된 기능, API 엔드포인트, 그리고 실행 방법을 설명합니다.

---

## ✅ 구현된 기능 현황

### P0 (높음) 우선순위 - 완료

| 기능 | 상태 | 백엔드 | 프런트엔드 |
|------|------|--------|-----------|
| 메뉴 조회 | ✅ | `/api/v1/menus` | `CustomerPage` |
| 주문 생성 | ✅ | `/api/v1/orders` | `CartSection` |
| 주문 상태 추적 | ✅ | `/api/v1/orders/{id}` | `OrdersSection` |
| 관리자 대시보드 | ✅ | `/api/v1/admin/dashboard` | `AdminDashboard` |
| 메뉴 관리 (CRUD) | ✅ | `/api/v1/menus` | `InventorySection` |
| 재고 관리 | ✅ | `/api/v1/admin/inventory` | `InventorySection` |

### P1 (중간) 우선순위 - 완료

| 기능 | 상태 | 백엔드 | 프런트엔드 |
|------|------|--------|-----------|
| 주문 내역 조회 | ✅ | `/api/v1/orders` | - |
| 메뉴 옵션 커스터마이징 | ✅ | 주문 생성 시 포함 | `MenuCard` |
| 통계 대시보드 | ✅ | `/api/v1/admin/statistics` | `AdminDashboard` |

### P1/P2 우선순위 - 미구현 (추후 확장)

| 기능 | 상태 | 비고 |
|------|------|------|
| 즐겨찾기 | ❌ | Phase 2에서 구현 예정 |
| QR 코드 생성 | ❌ | Phase 2에서 구현 예정 |
| 실시간 알림 (WebSocket) | ❌ | 현재는 30초 polling으로 대체 |
| 인증/로그인 | ❌ | Phase 2에서 구현 예정 |

---

## 🔗 API 엔드포인트

### 1. 메뉴 API

#### GET /api/v1/menus
메뉴 목록 조회

**Query Parameters:**
- `available_only` (boolean): 판매 가능한 메뉴만 조회 (기본값: true)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "아메리카노",
      "description": "진한 에스프레소와 물",
      "price": 4500,
      "image_url": "/images/americano.jpg",
      "stock": 100,
      "is_available": true,
      "options": [
        {
          "id": 1,
          "name": "샷 추가",
          "additional_price": 500
        }
      ]
    }
  ]
}
```

#### POST /api/v1/menus (관리자)
메뉴 생성

**Request Body:**
```json
{
  "name": "카페라떼",
  "description": "부드러운 우유와 에스프레소",
  "price": 5000,
  "stock": 50,
  "is_available": true,
  "options": [
    {
      "name": "샷 추가",
      "additional_price": 500
    }
  ]
}
```

---

### 2. 주문 API

#### POST /api/v1/orders
주문 생성

**Request Body:**
```json
{
  "items": [
    {
      "menu_id": 1,
      "quantity": 2,
      "options": [
        {
          "option_id": 1
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "주문이 완료되었습니다.",
  "data": {
    "id": 1,
    "order_number": "ORD-20251103-093845",
    "status": "received",
    "total_amount": 10000,
    "items": [
      {
        "id": 1,
        "menu_name": "아메리카노",
        "quantity": 2,
        "unit_price": 5000,
        "subtotal": 10000,
        "options": [
          {
            "id": 1,
            "option_name": "샷 추가",
            "additional_price": 500
          }
        ]
      }
    ],
    "created_at": "2025-11-03T00:38:45Z",
    "updated_at": "2025-11-03T00:38:45Z",
    "completed_at": null
  }
}
```

#### GET /api/v1/orders
주문 목록 조회

**Query Parameters:**
- `status` (optional): 주문 상태 필터 (received, preparing, completed, cancelled)
- `limit` (optional): 페이지당 개수 (기본값: 10)
- `offset` (optional): 건너뛸 개수 (기본값: 0)

#### PUT /api/v1/orders/{id}/status (관리자)
주문 상태 변경

**Request Body:**
```json
{
  "status": "preparing"
}
```

---

### 3. 관리자 API

#### GET /api/v1/admin/dashboard
대시보드 요약 정보

**Response:**
```json
{
  "success": true,
  "data": {
    "today": {
      "total_orders": 45,
      "revenue": 337500,
      "average_order_amount": 7500
    },
    "status_summary": {
      "received": 8,
      "preparing": 3,
      "completed": 42,
      "cancelled": 0
    }
  }
}
```

#### GET /api/v1/admin/orders
관리자 주문 목록 조회

**Query Parameters:**
- `status` (optional): 주문 상태 필터
- `date` (optional): 특정 날짜 (YYYY-MM-DD 형식)
- `limit` (optional): 페이지당 개수 (기본값: 50)
- `offset` (optional): 건너뛸 개수 (기본값: 0)

#### GET /api/v1/admin/statistics
통계 조회

**Query Parameters:**
- `period` (required): 조회 기간 (day, week, month)

**Response:**
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
      "completed": 42
    },
    "top_menus": [
      {
        "name": "아메리카노",
        "count": 28,
        "revenue": 126000
      }
    ],
    "hourly_distribution": [
      {
        "hour": 9,
        "orders": 18
      }
    ]
  }
}
```

#### GET /api/v1/admin/inventory
재고 현황 조회

#### PUT /api/v1/admin/inventory/{menu_id}?stock={quantity}
재고 수량 업데이트

---

## 🚀 실행 방법

### 1. 백엔드 서버 실행

```powershell
# backend 디렉토리로 이동
cd backend

# UTF-8 인코딩 설정 (Windows PowerShell)
$env:PYTHONIOENCODING='utf-8'

# 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**서버 주소:**
- API: http://localhost:8000
- Swagger 문서: http://localhost:8000/api/docs
- ReDoc 문서: http://localhost:8000/api/redoc

### 2. 프런트엔드 서버 실행

```powershell
# frontend 디렉토리로 이동
cd frontend

# 개발 서버 실행
npm run dev
```

**프런트엔드 주소:**
- 기본: http://localhost:5173

### 3. 데이터베이스 확인

```powershell
# backend 디렉토리에서
$env:PYTHONIOENCODING='utf-8'
python test_db_connection.py
```

---

## 📦 프런트엔드 서비스 구조

### API 클라이언트 (`src/services/`)

#### `api.ts`
- Axios 인스턴스 생성
- 기본 URL: `http://localhost:8000`
- 요청/응답 인터셉터 설정

#### `menuService.ts`
- `getMenus(availableOnly)`: 메뉴 목록 조회
- `getMenu(menuId)`: 메뉴 상세 조회
- `createMenu(menuData)`: 메뉴 생성 (관리자)
- `updateMenu(menuId, menuData)`: 메뉴 수정 (관리자)
- `deleteMenu(menuId)`: 메뉴 삭제 (관리자)

#### `orderService.ts`
- `createOrder(orderData)`: 주문 생성
- `getOrders(status, limit, offset)`: 주문 목록 조회
- `getOrder(orderId)`: 주문 상세 조회
- `updateOrderStatus(orderId, status)`: 주문 상태 변경 (관리자)

#### `adminService.ts`
- `getDashboardSummary()`: 대시보드 요약 정보
- `getOrders(status, date, limit, offset)`: 관리자 주문 목록
- `getStatistics(period)`: 통계 조회
- `getInventory()`: 재고 현황 조회
- `updateInventory(menuId, stock)`: 재고 수량 업데이트

---

## 🎯 주요 컴포넌트

### 고객 페이지

#### `CustomerPage`
- 메뉴 목록 표시
- 장바구니 기능
- 주문 생성

#### `MenuCard`
- 메뉴 상세 정보 표시
- 옵션 선택
- 장바구니 담기

#### `CartSection`
- 장바구니 아이템 표시
- 수량 조절
- 총 금액 계산
- 주문하기

### 관리자 페이지

#### `AdminPage`
- 대시보드 요약 표시
- 주문 목록 관리
- 재고 관리
- 30초마다 자동 새로고침

#### `AdminDashboard`
- 오늘의 통계
- 상태별 주문 개수
- 총 매출

#### `OrdersSection`
- 주문 목록 표시
- 주문 상태 변경
- 주문 상세 정보

#### `InventorySection`
- 메뉴별 재고 현황
- 재고 수량 조절

---

## 🔄 데이터 흐름

### 주문 생성 플로우

1. **고객**: `MenuCard`에서 메뉴 선택 및 옵션 선택
2. **고객**: "장바구니 담기" 클릭 → `customerStore`에 저장
3. **고객**: `CartSection`에서 "주문하기" 클릭
4. **프런트엔드**: `orderService.createOrder()` 호출
5. **백엔드**: `/api/v1/orders` POST 요청 처리
   - 메뉴 존재 확인
   - 재고 확인 및 차감
   - 옵션 가격 계산
   - 주문 생성
6. **백엔드**: 주문 정보 반환
7. **프런트엔드**: 성공 메시지 표시, 장바구니 비우기

### 주문 상태 변경 플로우

1. **관리자**: `OrdersSection`에서 주문 선택
2. **관리자**: 상태 변경 버튼 클릭 (예: "제조 시작")
3. **프런트엔드**: `orderService.updateOrderStatus()` 호출
4. **백엔드**: `/api/v1/orders/{id}/status` PUT 요청 처리
5. **백엔드**: 주문 상태 업데이트
6. **프런트엔드**: 목록 새로고침

---

## 🐛 알려진 이슈 및 제한사항

1. **인증 미구현**: 현재 모든 API가 인증 없이 접근 가능
2. **실시간 업데이트**: WebSocket 대신 30초 polling 사용
3. **즐겨찾기 기능**: 아직 구현되지 않음
4. **QR 코드 생성**: 아직 구현되지 않음
5. **에러 처리**: 기본적인 에러 처리만 구현됨

---

## 📝 API 테스트 방법

### 1. Swagger UI 사용
http://localhost:8000/api/docs 접속

### 2. cURL 사용

```bash
# 메뉴 목록 조회
curl http://localhost:8000/api/v1/menus

# 주문 생성
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "menu_id": 1,
        "quantity": 2,
        "options": [{"option_id": 1}]
      }
    ]
  }'

# 대시보드 조회
curl http://localhost:8000/api/v1/admin/dashboard
```

---

## 🔧 환경 변수

### 백엔드 (`.env`)
```env
# 데이터베이스
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderbean_db
DB_USER=postgres
DB_PASSWORD=your_password

# 애플리케이션
APP_NAME=OrderBean
APP_VERSION=1.0.0
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 프런트엔드 (`.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## 📊 데이터베이스 스키마

현재 데이터베이스에는 다음 테이블이 있습니다:

1. `menus` - 메뉴 정보
2. `menu_options` - 메뉴 옵션 (샷 추가, 시럽 등)
3. `orders` - 주문 정보
4. `order_items` - 주문 항목
5. `order_item_options` - 주문 항목별 선택된 옵션

**현재 데이터:**
- 메뉴: 5개
- 옵션: 30개
- 주문: 1개

---

## 🚦 다음 단계

### Phase 2 구현 예정 기능

1. **인증 시스템**
   - 회원가입 / 로그인
   - JWT 토큰 기반 인증
   - 관리자 권한 분리

2. **즐겨찾기**
   - Favorites 테이블 추가
   - 즐겨찾기 CRUD API
   - 프런트엔드 UI 구현

3. **QR 코드**
   - Python qrcode 라이브러리 사용
   - 주문 완료 시 QR 코드 생성
   - 프런트엔드에서 표시

4. **실시간 알림**
   - WebSocket 구현
   - 신규 주문 실시간 알림
   - 주문 상태 변경 실시간 반영

---

## 📞 문의 및 지원

**작성자**: kznetwork  
**버전**: 1.0  
**최종 수정일**: 2025년 11월 3일

---

## 🎉 결론

OrderBean의 핵심 기능(P0 우선순위)이 모두 구현되었고, 백엔드 API와 프런트엔드가 성공적으로 연동되었습니다. 메뉴 조회, 주문 생성, 주문 관리, 재고 관리, 통계 기능이 모두 정상 작동합니다.

Phase 1의 주요 목표를 달성했으며, Phase 2에서 인증, 즐겨찾기, QR 코드 등의 고급 기능을 추가할 수 있습니다.

