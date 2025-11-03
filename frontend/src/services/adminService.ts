/**
 * 관리자 API 서비스
 */
import apiClient from './api';
import { OrderStatus } from './orderService';

export interface DashboardSummary {
  today: {
    total_orders: number;
    revenue: number;
    average_order_amount: number;
  };
  status_summary: {
    received: number;
    preparing: number;
    completed: number;
    cancelled: number;
  };
}

export interface AdminOrder {
  id: number;
  order_number: string;
  status: OrderStatus;
  total_amount: number;
  item_count: number;
  items: Array<{
    menu_name: string;
    quantity: number;
  }>;
  created_at: string;
  updated_at: string;
}

export interface TopMenu {
  name: string;
  count: number;
  revenue: number;
}

export interface Statistics {
  revenue: {
    total: number;
    average: number;
  };
  orders: {
    total: number;
    completed: number;
  };
  top_menus: TopMenu[];
  hourly_distribution: Array<{
    hour: number;
    orders: number;
  }>;
}

export interface InventoryItem {
  id: number;
  name: string;
  stock: number;
  is_available: boolean;
  price: number;
}

const adminService = {
  /**
   * 대시보드 요약 정보
   */
  async getDashboardSummary(): Promise<DashboardSummary> {
    const response = await apiClient.get('/api/v1/admin/dashboard');
    return response.data.data;
  },

  /**
   * 관리자 주문 목록 조회
   */
  async getOrders(
    status?: OrderStatus,
    date?: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<AdminOrder[]> {
    let url = `/api/v1/admin/orders?limit=${limit}&offset=${offset}`;
    if (status) {
      url += `&status=${status}`;
    }
    if (date) {
      url += `&date=${date}`;
    }
    const response = await apiClient.get(url);
    return response.data.data;
  },

  /**
   * 통계 조회
   */
  async getStatistics(period: 'day' | 'week' | 'month' = 'day'): Promise<Statistics> {
    const response = await apiClient.get(`/api/v1/admin/statistics?period=${period}`);
    return response.data.data;
  },

  /**
   * 재고 현황 조회
   */
  async getInventory(): Promise<InventoryItem[]> {
    const response = await apiClient.get('/api/v1/admin/inventory');
    return response.data.data;
  },

  /**
   * 재고 수량 업데이트
   */
  async updateInventory(menuId: number, stock: number): Promise<void> {
    await apiClient.put(`/api/v1/admin/inventory/${menuId}?stock=${stock}`);
  },
};

export default adminService;

