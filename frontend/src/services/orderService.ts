/**
 * 주문 API 서비스
 */
import apiClient from './api';

export type OrderStatus = 'received' | 'preparing' | 'completed' | 'cancelled';

export interface OrderItemOption {
  id: number;
  option_name: string;
  additional_price: number;
}

export interface OrderItem {
  id: number;
  menu_id: number;
  menu_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  options: OrderItemOption[];
}

export interface Order {
  id: number;
  order_number: string;
  status: OrderStatus;
  total_amount: number;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface OrderListItem {
  id: number;
  order_number: string;
  status: OrderStatus;
  total_amount: number;
  item_count: number;
  created_at: string;
}

export interface OrderCreateData {
  items: Array<{
    menu_id: number;
    quantity: number;
    options: Array<{
      option_id: number;
    }>;
  }>;
}

export interface OrderListResponse {
  success: boolean;
  data: OrderListItem[];
}

export interface OrderDetailResponse {
  success: boolean;
  data: Order;
}

export interface OrderCreateResponse {
  success: boolean;
  message: string;
  data: Order;
}

const orderService = {
  /**
   * 주문 생성
   */
  async createOrder(orderData: OrderCreateData): Promise<Order> {
    const response = await apiClient.post<OrderCreateResponse>(
      '/api/v1/orders',
      orderData
    );
    return response.data.data;
  },

  /**
   * 주문 목록 조회
   */
  async getOrders(
    status?: OrderStatus,
    limit: number = 10,
    offset: number = 0
  ): Promise<OrderListItem[]> {
    let url = `/api/v1/orders?limit=${limit}&offset=${offset}`;
    if (status) {
      url += `&status=${status}`;
    }
    const response = await apiClient.get<OrderListResponse>(url);
    return response.data.data;
  },

  /**
   * 주문 상세 조회
   */
  async getOrder(orderId: number): Promise<Order> {
    const response = await apiClient.get<OrderDetailResponse>(
      `/api/v1/orders/${orderId}`
    );
    return response.data.data;
  },

  /**
   * 주문 상태 변경 (관리자)
   */
  async updateOrderStatus(
    orderId: number,
    status: OrderStatus
  ): Promise<void> {
    await apiClient.put(`/api/v1/orders/${orderId}/status`, { status });
  },
};

export default orderService;

