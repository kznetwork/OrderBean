# OrderBean - 프론트엔드 UI PRD (관리자 화면)

**버전**: 1.0  
**작성일**: 2025년 11월 2일  
**작성자**: kznetwork  
**대상**: 관리자/운영자 인터페이스

---

## 📑 목차

1. [개요](#1-개요)
2. [화면 구조](#2-화면-구조)
3. [컴포넌트 상세 명세](#3-컴포넌트-상세-명세)
4. [관리자 인터랙션](#4-관리자-인터랙션)
5. [반응형 디자인](#5-반응형-디자인)
6. [상태 관리](#6-상태-관리)
7. [API 연동](#7-api-연동)
8. [디자인 시스템](#8-디자인-시스템)

---

## 1. 개요

### 1.1 목적

OrderBean 애플리케이션의 관리자용 주문 관리 및 재고 관리 인터페이스를 정의합니다. 관리자가 실시간으로 주문을 처리하고 재고를 효율적으로 관리할 수 있도록 설계된 UI/UX를 제공합니다.

### 1.2 주요 기능

- 실시간 주문 현황 대시보드
- 주문 상태 관리 (접수, 제조 중, 완료)
- 재고 관리 (재고 수량 조정)
- 주문 내역 확인
- 사용자 화면 전환

### 1.3 디자인 원칙

- **가시성**: 주문 상태를 한눈에 파악
- **효율성**: 빠른 주문 처리 및 상태 변경
- **명확성**: 직관적인 버튼과 명확한 정보 표시
- **실시간성**: 새로운 주문 즉시 표시

---

## 2. 화면 구조

### 2.1 전체 레이아웃

```
┌─────────────────────────────────────────────┐
│  Header (브랜드명 + 네비게이션)              │
├─────────────────────────────────────────────┤
│  Dashboard (주문 통계)                       │
│  총 주문 1 / 주문 접수 1 / 제조중 0 / 완료 0│
├─────────────────────────────────────────────┤
│  Inventory Section (재고 현황)              │
│  [메뉴1 10개 +/-] [메뉴2 10개 +/-] ...     │
├─────────────────────────────────────────────┤
│  Orders Section (주문 현황)                 │
│  - 주문 리스트                               │
│  - 주문 상세 정보                            │
│  - 상태 변경 버튼                            │
└─────────────────────────────────────────────┘
```

### 2.2 화면 영역 분류

| 영역 | 컴포넌트 | 비율 |
|------|---------|------|
| Header | 브랜드 + 네비게이션 | 10% |
| Dashboard | 주문 통계 | 15% |
| Inventory Section | 재고 관리 | 25% |
| Orders Section | 주문 목록 | 50% |

---

## 3. 컴포넌트 상세 명세

### 3.1 Admin Header Component

**컴포넌트명**: `AdminHeader`

**구성요소**
- 브랜드명: "COZY"
- 네비게이션 탭:
  - "주문하기" (사용자 화면으로 전환)
  - "관리자" (현재 화면, 활성 상태)

**UI 상세**
```
┌────────────────────────────────────────────┐
│  COZY              [주문하기]  [관리자]    │
└────────────────────────────────────────────┘
```

**스타일링**
- 배경색: 흰색 (`#FFFFFF`)
- 브랜드명 폰트: 볼드, 24px
- 탭 버튼: 14px, 패딩 12px 24px
- 활성 탭: 배경색 강조 또는 언더라인
- 하단 보더: 1px 회색

**Props**
```typescript
interface AdminHeaderProps {
  activeTab: 'order' | 'admin';
  onTabChange: (tab: 'order' | 'admin') => void;
}
```

**동작**
- "주문하기" 클릭 시 사용자 화면으로 전환

---

### 3.2 Dashboard Component

**컴포넌트명**: `AdminDashboard`

**구성요소**
1. 섹션 제목: "관리자 대시보드"
2. 주문 통계 표시:
   - 총 주문 (전체 주문 건수)
   - 주문 접수 (pending 상태)
   - 제조 중 (preparing 상태)
   - 제조 완료 (completed 상태)

**UI 상세**
```
┌─────────────────────────────────────────────────┐
│  관리자 대시보드                                 │
├─────────────────────────────────────────────────┤
│  총 주문 1 / 주문 접수 1 / 제조 중 0 / 제조 완료 0│
└─────────────────────────────────────────────────┘
```

**스타일링**
- 배경: 연한 파란색 또는 흰색 (`#F0F9FF`)
- 패딩: 24px
- 보더: 1px solid #E5E7EB
- 보더 반경: 8px
- 통계 텍스트: 16px, 굵기 500
- 숫자 강조: 볼드, 색상 강조

**Props**
```typescript
interface AdminDashboardProps {
  stats: OrderStats;
  onRefresh?: () => void;
}

interface OrderStats {
  totalOrders: number;
  pendingOrders: number;
  preparingOrders: number;
  completedOrders: number;
}
```

**동작**
1. 실시간 업데이트 (폴링 또는 WebSocket)
2. 각 통계 클릭 시 해당 상태의 주문 필터링 (선택적)
3. 새로운 주문 시 시각적 피드백 (숫자 증가 애니메이션)

**상태**
```typescript
const [orderStats, setOrderStats] = useState<OrderStats>({
  totalOrders: 0,
  pendingOrders: 0,
  preparingOrders: 0,
  completedOrders: 0,
});
```

---

### 3.3 Inventory Section Component

**컴포넌트명**: `InventorySection`

**구성요소**
1. 섹션 제목: "재고 현황"
2. 메뉴별 재고 카드:
   - 메뉴명
   - 현재 재고 수량
   - 수량 증가 버튼 [+]
   - 수량 감소 버튼 [-]

**UI 상세**
```
┌─────────────────────────────────────────────────────┐
│  재고 현황                                           │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │아메리카노(ICE)│  │아메리카노(HOT)│  │  카페라떼    ││
│  │    10개      │  │    10개      │  │    10개      ││
│  │   [+] [-]    │  │   [+] [-]    │  │   [+] [-]    ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
└─────────────────────────────────────────────────────┘
```

**스타일링**
- 배경: 연한 회색 (`#F9FAFB`)
- 패딩: 24px
- 보더: 1px solid #E5E7EB
- 보더 반경: 8px
- 카드 간격: 16px

**Individual Inventory Card**
- 배경: 흰색
- 패딩: 16px
- 보더 반경: 8px
- 메뉴명: 14px, 볼드
- 수량: 18px, 볼드
- 버튼: 32x32px, 보더 1px solid

**Props**
```typescript
interface InventorySectionProps {
  inventoryItems: InventoryItem[];
  onUpdateInventory: (itemId: number, newQuantity: number) => void;
}

interface InventoryItem {
  id: number;
  menuName: string;
  quantity: number;
  minQuantity?: number;
  maxQuantity?: number;
}
```

**동작**
1. [+] 버튼 클릭:
   - 수량 1 증가
   - 최대 수량 제한 (예: 999개)
   - API 호출하여 서버 업데이트
   - 성공 시 UI 업데이트
   
2. [-] 버튼 클릭:
   - 수량 1 감소
   - 최소 수량 제한 (0개 이하로 내려가지 않음)
   - API 호출하여 서버 업데이트
   - 성공 시 UI 업데이트

3. 재고 부족 경고:
   - 재고가 5개 이하일 때 카드에 경고 표시 (노란색 보더)
   - 재고가 0개일 때 빨간색 경고

**상태**
```typescript
const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
const [isUpdating, setIsUpdating] = useState<Record<number, boolean>>({});
```

---

### 3.4 Orders Section Component

**컴포넌트명**: `OrdersSection`

**구성요소**
1. 섹션 제목: "주문 현황"
2. 주문 카드 목록:
   - 주문 시간
   - 주문 메뉴 (수량 포함)
   - 주문 금액
   - 상태 변경 버튼

**UI 상세**
```
┌─────────────────────────────────────────────────┐
│  주문 현황                                       │
├─────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐│
│  │ 7월 31일 13:00                              ││
│  │ 아메리카노(ICE) x 1            4,000원     ││
│  │                          [주문 접수]        ││
│  └─────────────────────────────────────────────┘│
│                                                  │
│  ┌─────────────────────────────────────────────┐│
│  │ 7월 31일 13:05                              ││
│  │ 카페라떼 x 2                   10,000원    ││
│  │                          [제조 시작]        ││
│  └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

**스타일링**
- 배경: 흰색
- 패딩: 24px
- 주문 카드:
  - 배경: 흰색
  - 보더: 1px solid #E5E7EB
  - 보더 반경: 8px
  - 패딩: 16px
  - 마진 하단: 12px
  - 호버 시: 그림자 강조

**상태별 색상 구분**
- 주문 접수 (pending): 파란색 액센트
- 제조 중 (preparing): 주황색 액센트
- 제조 완료 (ready): 녹색 액센트
- 픽업 완료 (completed): 회색

**Props**
```typescript
interface OrdersSectionProps {
  orders: Order[];
  onUpdateOrderStatus: (orderId: number, newStatus: OrderStatus) => void;
  onViewOrderDetail?: (orderId: number) => void;
}

interface Order {
  id: number;
  orderNumber: string;
  createdAt: string;
  items: OrderItem[];
  totalPrice: number;
  status: OrderStatus;
  specialRequest?: string;
}

interface OrderItem {
  menuName: string;
  quantity: number;
  options?: string[];
}

type OrderStatus = 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled';
```

**동작**

1. **주문 접수 버튼 (pending → preparing)**
   - 클릭 시 "제조 시작하시겠습니까?" 확인
   - 확인 시 상태를 'preparing'으로 변경
   - API 호출
   - 성공 시 버튼이 "제조 완료"로 변경

2. **제조 완료 버튼 (preparing → ready)**
   - 클릭 시 상태를 'ready'로 변경
   - API 호출
   - 고객에게 알림 전송 (선택적)
   - 성공 시 버튼이 "픽업 완료"로 변경

3. **픽업 완료 버튼 (ready → completed)**
   - 클릭 시 상태를 'completed'로 변경
   - 주문 카드가 완료 섹션으로 이동 또는 리스트에서 제거

4. **주문 상세 보기**
   - 카드 클릭 시 주문 상세 모달 표시
   - 특별 요청사항 확인
   - 주문 내역 상세

**상태**
```typescript
const [orders, setOrders] = useState<Order[]>([]);
const [isProcessing, setIsProcessing] = useState<Record<number, boolean>>({});
const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
```

---

## 4. 관리자 인터랙션

### 4.1 주문 처리 플로우

```
1. 새 주문 접수 알림
   ↓
2. 관리자 대시보드 업데이트
   - "주문 접수" 카운트 증가
   - 주문 리스트에 새 주문 표시
   ↓
3. 관리자가 주문 확인
   - 주문 내역 확인
   - 특별 요청 확인
   ↓
4. [주문 접수] 버튼 클릭
   - 상태: pending → preparing
   - 버튼: "제조 완료"로 변경
   - 대시보드: "제조 중" 카운트 증가
   ↓
5. 제조 완료 후 [제조 완료] 버튼 클릭
   - 상태: preparing → ready
   - 버튼: "픽업 완료"로 변경
   - 대시보드: "제조 완료" 카운트 증가
   - 고객에게 알림 전송
   ↓
6. 고객 픽업 후 [픽업 완료] 버튼 클릭
   - 상태: ready → completed
   - 주문 카드 아카이빙
   - 대시보드 업데이트
```

### 4.2 재고 관리 플로우

```
1. 재고 현황 확인
   ↓
2. 재고 조정 필요 시
   - [+] 버튼 클릭: 재고 증가
   - [-] 버튼 클릭: 재고 감소
   ↓
3. API 호출 및 서버 업데이트
   ↓
4. 성공 시 UI 업데이트
   - 수량 표시 변경
   - 저재고 경고 표시 (필요 시)
   ↓
5. 실패 시 에러 처리
   - 에러 메시지 표시
   - 이전 상태로 롤백
```

### 4.3 인터랙션 상태

| 상태 | 설명 | UI 변화 |
|------|------|---------|
| Default | 초기 상태 | 기본 스타일 |
| Hover | 마우스 오버 | 그림자 강조, 커서 변경 |
| Active | 클릭 시 | 버튼 눌림 효과 |
| Processing | API 호출 중 | 스피너 표시, 버튼 비활성화 |
| Success | 성공 완료 | 체크 아이콘, 녹색 피드백 |
| Error | 오류 발생 | 에러 메시지, 빨간색 강조 |
| Low Stock | 재고 부족 | 노란색 경고 |
| Out of Stock | 재고 없음 | 빨간색 경고 |

---

## 5. 반응형 디자인

### 5.1 브레이크포인트

```css
/* Mobile - 권장하지 않음 (관리자 화면은 최소 태블릿 이상) */
@media (max-width: 767px) { }

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Desktop - 권장 */
@media (min-width: 1024px) { }
```

### 5.2 레이아웃 변화

**태블릿 (768px ~ 1023px)**
```
┌─────────────────┐
│     Header      │
├─────────────────┤
│   Dashboard     │
├─────────────────┤
│  Inventory      │
│  [Card1][Card2] │
│  [Card3]        │
├─────────────────┤
│     Orders      │
│   [Order 1]     │
│   [Order 2]     │
└─────────────────┘
```
- 재고 카드: 2열 그리드
- 주문 카드: 1열 (전체 너비)
- 패딩: 16px

**데스크톱 (≥ 1024px) - 권장**
```
┌──────────────────────────┐
│         Header           │
├──────────────────────────┤
│       Dashboard          │
├──────────────────────────┤
│       Inventory          │
│  [Card1][Card2][Card3]   │
├──────────────────────────┤
│         Orders           │
│  [Order 1]               │
│  [Order 2]               │
└──────────────────────────┘
```
- 재고 카드: 3-4열 그리드
- 주문 카드: 1-2열 (옵션)
- 최대 너비: 1440px (중앙 정렬)
- 패딩: 32px

### 5.3 최소 화면 크기

- **권장 최소 너비**: 1024px (데스크톱)
- **절대 최소 너비**: 768px (태블릿)
- 768px 미만에서는 경고 메시지 표시:
  - "관리자 화면은 최소 768px 이상의 화면에서 사용을 권장합니다."

---

## 6. 상태 관리

### 6.1 전역 상태 (Zustand/Redux)

```typescript
interface AdminState {
  // 주문 통계
  orderStats: OrderStats;
  isStatsLoading: boolean;

  // 주문 목록
  orders: Order[];
  isOrdersLoading: boolean;
  ordersError: string | null;

  // 재고 목록
  inventoryItems: InventoryItem[];
  isInventoryLoading: boolean;
  inventoryError: string | null;

  // UI 상태
  selectedOrder: Order | null;
  isOrderDetailModalOpen: boolean;

  // Actions
  fetchOrderStats: () => Promise<void>;
  fetchOrders: () => Promise<void>;
  updateOrderStatus: (orderId: number, status: OrderStatus) => Promise<void>;
  fetchInventory: () => Promise<void>;
  updateInventoryQuantity: (itemId: number, quantity: number) => Promise<void>;
  selectOrder: (order: Order) => void;
  closeOrderDetailModal: () => void;

  // Real-time updates
  subscribeToOrders: () => void;
  unsubscribeFromOrders: () => void;
}
```

### 6.2 로컬 상태 (Component State)

**InventoryCard**
- 수량 조정 중 로딩 상태
- 낙관적 업데이트 (Optimistic Update)

**OrderCard**
- 상태 변경 중 로딩 상태
- 확인 다이얼로그 표시 여부

### 6.3 실시간 업데이트

**폴링 방식**
```typescript
useEffect(() => {
  const interval = setInterval(() => {
    fetchOrders();
    fetchOrderStats();
  }, 5000); // 5초마다 업데이트

  return () => clearInterval(interval);
}, []);
```

**WebSocket 방식 (선택적)**
```typescript
useEffect(() => {
  const ws = new WebSocket('ws://api.orderbean.com/admin/ws');
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'NEW_ORDER') {
      addNewOrder(data.order);
      showNotification('새 주문이 접수되었습니다!');
    }
  };

  return () => ws.close();
}, []);
```

---

## 7. API 연동

### 7.1 필요한 API 엔드포인트

**주문 통계 조회**
```typescript
GET /api/v1/admin/statistics/orders
Response: {
  success: boolean;
  data: {
    totalOrders: number;
    pendingOrders: number;
    preparingOrders: number;
    completedOrders: number;
  }
}
```

**주문 목록 조회**
```typescript
GET /api/v1/admin/orders?status=all&date=today
Response: {
  success: boolean;
  data: Order[];
}
```

**주문 상태 변경**
```typescript
PUT /api/v1/admin/orders/:id/status
Request: {
  status: 'preparing' | 'ready' | 'completed';
}
Response: {
  success: boolean;
  data: Order;
}
```

**재고 조회**
```typescript
GET /api/v1/admin/inventory
Response: {
  success: boolean;
  data: InventoryItem[];
}
```

**재고 업데이트**
```typescript
PUT /api/v1/admin/inventory/:id
Request: {
  quantity: number;
}
Response: {
  success: boolean;
  data: InventoryItem;
}
```

### 7.2 에러 처리

**네트워크 에러**
```typescript
try {
  await updateOrderStatus(orderId, 'preparing');
} catch (error) {
  if (error.isNetworkError) {
    showToast('네트워크 연결을 확인해주세요', 'error');
  } else if (error.response?.status === 404) {
    showToast('주문을 찾을 수 없습니다', 'error');
  } else if (error.response?.status === 403) {
    showToast('권한이 없습니다', 'error');
  }
}
```

**낙관적 업데이트**
```typescript
const updateInventory = async (itemId: number, newQuantity: number) => {
  // 1. UI 먼저 업데이트 (낙관적)
  setInventoryItems(prev => 
    prev.map(item => 
      item.id === itemId ? { ...item, quantity: newQuantity } : item
    )
  );

  try {
    // 2. API 호출
    await api.updateInventory(itemId, newQuantity);
  } catch (error) {
    // 3. 실패 시 롤백
    setInventoryItems(prevItems); // 이전 상태로 복원
    showToast('재고 업데이트에 실패했습니다', 'error');
  }
};
```

### 7.3 알림 시스템

**새 주문 알림**
```typescript
const showNewOrderNotification = (order: Order) => {
  // 브라우저 알림 (권한 필요)
  if (Notification.permission === 'granted') {
    new Notification('새 주문 접수!', {
      body: `${order.items[0].menuName} 외 ${order.items.length}건`,
      icon: '/logo.png',
    });
  }

  // 사운드 알림
  const audio = new Audio('/sounds/new-order.mp3');
  audio.play();

  // Toast 알림
  showToast('새 주문이 접수되었습니다!', 'info');
};
```

---

## 8. 디자인 시스템

### 8.1 컬러 팔레트

**Primary Colors (관리자용)**
```css
--admin-primary-50: #EFF6FF;
--admin-primary-100: #DBEAFE;
--admin-primary-500: #3B82F6;
--admin-primary-600: #2563EB;
--admin-primary-700: #1D4ED8;
```

**Status Colors**
```css
--status-pending: #3B82F6;    /* 파란색 - 주문 접수 */
--status-preparing: #F59E0B;  /* 주황색 - 제조 중 */
--status-ready: #10B981;      /* 녹색 - 제조 완료 */
--status-completed: #6B7280;  /* 회색 - 픽업 완료 */
--status-cancelled: #EF4444;  /* 빨간색 - 취소됨 */
```

**Alert Colors**
```css
--alert-low-stock: #FEF3C7;   /* 연한 노란색 - 저재고 */
--alert-out-stock: #FEE2E2;   /* 연한 빨간색 - 재고 없음 */
```

**Neutral Colors**
```css
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-300: #D1D5DB;
--gray-500: #6B7280;
--gray-900: #111827;
```

### 8.2 타이포그래피

**폰트 패밀리**
```css
font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
```

**폰트 크기**
```css
--text-xs: 12px;    /* 보조 정보 */
--text-sm: 14px;    /* 일반 텍스트 */
--text-base: 16px;  /* 기본 */
--text-lg: 18px;    /* 강조 */
--text-xl: 20px;    /* 제목 */
--text-2xl: 24px;   /* 큰 제목 */
```

### 8.3 버튼 스타일

**Status Change Button**
```css
.btn-status {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

/* 주문 접수 */
.btn-status-pending {
  background: var(--status-pending);
  color: white;
}

/* 제조 완료 */
.btn-status-preparing {
  background: var(--status-preparing);
  color: white;
}

/* 픽업 완료 */
.btn-status-ready {
  background: var(--status-ready);
  color: white;
}

.btn-status:hover {
  opacity: 0.9;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.btn-status:disabled {
  background: var(--gray-300);
  cursor: not-allowed;
}
```

**Inventory Button**
```css
.btn-inventory {
  width: 32px;
  height: 32px;
  border: 1px solid var(--gray-300);
  border-radius: 4px;
  background: white;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-inventory:hover {
  background: var(--gray-50);
  border-color: var(--gray-400);
}

.btn-inventory:active {
  transform: scale(0.95);
}

.btn-inventory:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 8.4 카드 스타일

**Dashboard Card**
```css
.dashboard-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

**Inventory Card**
```css
.inventory-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s ease;
}

.inventory-card:hover {
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.inventory-card.low-stock {
  border-color: var(--status-preparing);
  background: var(--alert-low-stock);
}

.inventory-card.out-of-stock {
  border-color: var(--status-cancelled);
  background: var(--alert-out-stock);
}
```

**Order Card**
```css
.order-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-left: 4px solid var(--status-pending);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.order-card:hover {
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.order-card.pending {
  border-left-color: var(--status-pending);
}

.order-card.preparing {
  border-left-color: var(--status-preparing);
}

.order-card.ready {
  border-left-color: var(--status-ready);
}
```

### 8.5 애니메이션

**새 주문 등장**
```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.order-card.new {
  animation: slideIn 0.3s ease-out;
}
```

**통계 숫자 증가**
```css
@keyframes countUp {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.stat-number.updated {
  animation: countUp 0.3s ease;
}
```

**펄스 효과 (새 주문 알림)**
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.notification-badge {
  animation: pulse 2s infinite;
}
```

---

## 9. 접근성 (Accessibility)

### 9.1 시맨틱 HTML

```html
<header>
  <nav aria-label="관리자 네비게이션">
    <!-- 네비게이션 -->
  </nav>
</header>

<main>
  <section aria-label="주문 통계">
    <!-- 대시보드 -->
  </section>

  <section aria-label="재고 관리">
    <!-- 재고 현황 -->
  </section>

  <section aria-label="주문 목록">
    <!-- 주문 현황 -->
  </section>
</main>
```

### 9.2 키보드 네비게이션

- Tab 키로 모든 버튼 접근
- Enter/Space로 버튼 활성화
- 화살표 키로 주문 카드 간 이동 (선택적)

### 9.3 스크린 리더

```html
<button 
  aria-label="아메리카노 아이스 재고 1개 증가"
  onClick={handleIncrease}
>
  +
</button>

<div role="status" aria-live="polite">
  <!-- 주문 상태 변경 알림 -->
</div>

<div role="alert" aria-live="assertive">
  <!-- 중요 알림 (새 주문 등) -->
</div>
```

---

## 10. 성능 최적화

### 10.1 실시간 업데이트 최적화

**폴링 간격 조정**
```typescript
// 주문이 많을 때는 간격 단축, 적을 때는 연장
const getPollingInterval = (orderCount: number) => {
  if (orderCount > 10) return 3000;  // 3초
  if (orderCount > 5) return 5000;   // 5초
  return 10000; // 10초
};
```

**WebSocket 연결 관리**
```typescript
// 관리자 화면에만 WebSocket 연결
// 화면 벗어나면 연결 해제하여 리소스 절약
useEffect(() => {
  if (isAdminActive) {
    subscribeToOrders();
  }
  return () => {
    unsubscribeFromOrders();
  };
}, [isAdminActive]);
```

### 10.2 리스트 최적화

**가상화 (Virtualization)**
```typescript
// react-window 사용 (주문 목록이 많을 때)
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={orders.length}
  itemSize={120}
  width="100%"
>
  {({ index, style }) => (
    <OrderCard order={orders[index]} style={style} />
  )}
</FixedSizeList>
```

### 10.3 메모이제이션

```typescript
// 주문 통계 계산 캐싱
const orderStats = useMemo(() => {
  return {
    totalOrders: orders.length,
    pendingOrders: orders.filter(o => o.status === 'pending').length,
    preparingOrders: orders.filter(o => o.status === 'preparing').length,
    completedOrders: orders.filter(o => o.status === 'completed').length,
  };
}, [orders]);

// 컴포넌트 메모이제이션
export const OrderCard = React.memo(({ order, onUpdateStatus }) => {
  // ...
}, (prevProps, nextProps) => {
  return prevProps.order.id === nextProps.order.id &&
         prevProps.order.status === nextProps.order.status;
});
```

---

## 11. 알림 시스템

### 11.1 알림 유형

| 유형 | 트리거 | 표시 방법 |
|------|--------|----------|
| 새 주문 | 새 주문 접수 | 브라우저 알림 + 사운드 + Toast |
| 상태 변경 성공 | 주문 상태 업데이트 완료 | Toast |
| 재고 업데이트 | 재고 수량 변경 완료 | Toast |
| 저재고 경고 | 재고 5개 이하 | 카드 강조 + Toast |
| 에러 발생 | API 오류 | Toast (에러) |

### 11.2 브라우저 알림 권한 요청

```typescript
const requestNotificationPermission = async () => {
  if ('Notification' in window) {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      showToast('알림이 활성화되었습니다', 'success');
    }
  }
};

// 관리자 화면 진입 시 권한 요청
useEffect(() => {
  requestNotificationPermission();
}, []);
```

### 11.3 사운드 알림

```typescript
class SoundManager {
  private audio: HTMLAudioElement;

  constructor() {
    this.audio = new Audio();
  }

  playNewOrder() {
    this.audio.src = '/sounds/new-order.mp3';
    this.audio.play();
  }

  playSuccess() {
    this.audio.src = '/sounds/success.mp3';
    this.audio.play();
  }

  playError() {
    this.audio.src = '/sounds/error.mp3';
    this.audio.play();
  }
}
```

---

## 12. 테스트 시나리오

### 12.1 단위 테스트

**AdminDashboard 컴포넌트**
- [ ] 주문 통계가 올바르게 표시되는가?
- [ ] 통계 숫자가 실시간으로 업데이트되는가?

**InventoryCard 컴포넌트**
- [ ] [+] 버튼 클릭 시 수량이 증가하는가?
- [ ] [-] 버튼 클릭 시 수량이 감소하는가?
- [ ] 0 이하로 감소하지 않는가?
- [ ] 저재고 경고가 표시되는가?

**OrderCard 컴포넌트**
- [ ] 주문 정보가 올바르게 렌더링되는가?
- [ ] 상태별로 버튼이 올바르게 표시되는가?
- [ ] 상태 변경 시 버튼이 변경되는가?

### 12.2 통합 테스트

- [ ] 새 주문 접수 → 대시보드 업데이트 → 주문 리스트 표시 플로우
- [ ] 주문 상태 변경 → API 호출 → UI 업데이트 플로우
- [ ] 재고 조정 → API 호출 → UI 업데이트 플로우

### 12.3 E2E 테스트 시나리오

```gherkin
Scenario: 주문 접수 및 처리
  Given 관리자가 관리자 화면에 접속했을 때
  When 새 주문이 접수되면
  Then 주문 목록에 새 주문이 표시되어야 한다
  And 대시보드의 "주문 접수" 카운트가 증가해야 한다
  When 관리자가 "주문 접수" 버튼을 클릭하면
  Then 버튼이 "제조 완료"로 변경되어야 한다
  And 대시보드의 "제조 중" 카운트가 증가해야 한다

Scenario: 재고 관리
  Given 관리자가 재고 현황을 확인했을 때
  When 아메리카노 재고의 [+] 버튼을 클릭하면
  Then 재고 수량이 1 증가해야 한다
  When 재고가 5개 이하가 되면
  Then 저재고 경고가 표시되어야 한다
```

---

## 13. 구현 체크리스트

### Phase 1: 기본 UI 구현
- [ ] AdminHeader 컴포넌트
- [ ] AdminDashboard 컴포넌트
- [ ] InventorySection 컴포넌트
- [ ] OrdersSection 컴포넌트
- [ ] 기본 레이아웃

### Phase 2: 인터랙션
- [ ] 주문 상태 변경 기능
- [ ] 재고 수량 조정 기능
- [ ] 주문 상세 모달
- [ ] 확인 다이얼로그

### Phase 3: API 연동
- [ ] 주문 조회 API
- [ ] 주문 상태 변경 API
- [ ] 재고 조회 API
- [ ] 재고 업데이트 API
- [ ] 실시간 업데이트 (폴링/WebSocket)

### Phase 4: 알림 시스템
- [ ] 브라우저 알림
- [ ] 사운드 알림
- [ ] Toast 알림
- [ ] 저재고 경고

### Phase 5: 최적화 & 테스트
- [ ] 성능 최적화
- [ ] 접근성 개선
- [ ] 단위 테스트
- [ ] E2E 테스트

---

## 14. 보안 고려사항

### 14.1 권한 체크

```typescript
// 관리자 화면 접근 시 권한 확인
const AdminPage = () => {
  const { user } = useAuth();

  if (!user || user.role !== 'admin') {
    return <Navigate to="/login" />;
  }

  return <AdminDashboard />;
};
```

### 14.2 민감한 작업 재확인

```typescript
// 주문 취소 등 중요한 작업은 재확인
const handleCancelOrder = async (orderId: number) => {
  const confirmed = await confirm('정말 주문을 취소하시겠습니까?');
  if (!confirmed) return;

  try {
    await api.cancelOrder(orderId);
    showToast('주문이 취소되었습니다', 'success');
  } catch (error) {
    showToast('주문 취소에 실패했습니다', 'error');
  }
};
```

### 14.3 세션 타임아웃

```typescript
// 30분 동안 활동이 없으면 자동 로그아웃
const SESSION_TIMEOUT = 30 * 60 * 1000; // 30분

useIdleTimer({
  timeout: SESSION_TIMEOUT,
  onIdle: () => {
    logout();
    showToast('세션이 만료되어 로그아웃되었습니다', 'info');
  },
});
```

---

## 15. 참고 자료

### UI/UX 참고
- [Material Design - Data Tables](https://material.io/components/data-tables)
- [Admin Dashboard Best Practices](https://www.smashingmagazine.com/2015/04/web-based-admin-interfaces/)

### React 관련
- [React Query](https://tanstack.com/query/latest)
- [React Hook Form](https://react-hook-form.com)
- [Zustand](https://github.com/pmndrs/zustand)

### 실시간 통신
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Socket.io](https://socket.io)

---

## 부록

### A. 컴포넌트 파일 구조

```
src/
├── components/
│   ├── admin/
│   │   ├── AdminHeader.tsx
│   │   ├── AdminDashboard.tsx
│   │   ├── InventorySection.tsx
│   │   ├── InventoryCard.tsx
│   │   ├── OrdersSection.tsx
│   │   ├── OrderCard.tsx
│   │   └── OrderDetailModal.tsx
│   └── common/
│       ├── Button.tsx
│       ├── ConfirmDialog.tsx
│       └── Toast.tsx
├── pages/
│   └── AdminPage.tsx
├── stores/
│   └── adminStore.ts
├── api/
│   ├── orderApi.ts
│   └── inventoryApi.ts
├── hooks/
│   ├── useOrders.ts
│   ├── useInventory.ts
│   └── useNotifications.ts
├── types/
│   ├── order.ts
│   └── inventory.ts
└── styles/
    └── admin.css
```

### B. 상태 관리 예시 (Zustand)

```typescript
import create from 'zustand';

export const useAdminStore = create<AdminState>((set, get) => ({
  // State
  orders: [],
  orderStats: {
    totalOrders: 0,
    pendingOrders: 0,
    preparingOrders: 0,
    completedOrders: 0,
  },
  inventoryItems: [],

  // Actions
  fetchOrders: async () => {
    const response = await api.getOrders();
    set({ orders: response.data });
  },

  updateOrderStatus: async (orderId, newStatus) => {
    await api.updateOrderStatus(orderId, newStatus);
    
    // 낙관적 업데이트
    set(state => ({
      orders: state.orders.map(order =>
        order.id === orderId ? { ...order, status: newStatus } : order
      ),
    }));
  },

  updateInventoryQuantity: async (itemId, quantity) => {
    await api.updateInventory(itemId, quantity);
    
    set(state => ({
      inventoryItems: state.inventoryItems.map(item =>
        item.id === itemId ? { ...item, quantity } : item
      ),
    }));
  },
}));
```

---

**문서 버전**: 1.0  
**최종 수정일**: 2025년 11월 2일  
**다음 단계**: 프로토타입 개발 및 사용자 테스트

