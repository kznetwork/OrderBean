import { create } from 'zustand';
import { Order, OrderStats, InventoryItem, OrderStatus } from '../types/admin';

interface AdminState {
  // 주문 통계
  orderStats: OrderStats;
  
  // 주문 목록
  orders: Order[];
  
  // 재고 목록
  inventoryItems: InventoryItem[];
  
  // Actions
  initializeMockData: () => void;
  updateOrderStatus: (orderId: number, newStatus: OrderStatus) => void;
  updateInventoryQuantity: (itemId: number, delta: number) => void;
  calculateOrderStats: () => void;
}

export const useAdminStore = create<AdminState>((set, get) => ({
  // State
  orderStats: {
    totalOrders: 0,
    pendingOrders: 0,
    preparingOrders: 0,
    completedOrders: 0,
  },
  orders: [],
  inventoryItems: [],
  
  // Actions
  initializeMockData: () => {
    const mockOrders: Order[] = [
      {
        id: 1,
        orderNumber: 'ORD-001',
        createdAt: '2025-07-31T13:00:00',
        items: [
          {
            menuName: '아메리카노(ICE)',
            quantity: 1,
          },
        ],
        totalPrice: 4000,
        status: 'pending',
      },
    ];
    
    const mockInventory: InventoryItem[] = [
      {
        id: 1,
        menuName: '아메리카노(ICE)',
        quantity: 10,
        minQuantity: 0,
        maxQuantity: 999,
      },
      {
        id: 2,
        menuName: '아메리카노(HOT)',
        quantity: 10,
        minQuantity: 0,
        maxQuantity: 999,
      },
      {
        id: 3,
        menuName: '카페라떼',
        quantity: 10,
        minQuantity: 0,
        maxQuantity: 999,
      },
    ];
    
    set({ 
      orders: mockOrders, 
      inventoryItems: mockInventory 
    });
    
    get().calculateOrderStats();
  },
  
  updateOrderStatus: (orderId, newStatus) => {
    set(state => ({
      orders: state.orders.map(order =>
        order.id === orderId ? { ...order, status: newStatus } : order
      ),
    }));
    get().calculateOrderStats();
  },
  
  updateInventoryQuantity: (itemId, delta) => {
    set(state => ({
      inventoryItems: state.inventoryItems.map(item => {
        if (item.id === itemId) {
          const newQuantity = item.quantity + delta;
          // 최소/최대 제한 적용
          const clampedQuantity = Math.max(
            item.minQuantity ?? 0,
            Math.min(item.maxQuantity ?? 999, newQuantity)
          );
          return { ...item, quantity: clampedQuantity };
        }
        return item;
      }),
    }));
  },
  
  calculateOrderStats: () => {
    const { orders } = get();
    const stats: OrderStats = {
      totalOrders: orders.length,
      pendingOrders: orders.filter(o => o.status === 'pending').length,
      preparingOrders: orders.filter(o => o.status === 'preparing').length,
      completedOrders: orders.filter(o => o.status === 'completed').length,
    };
    set({ orderStats: stats });
  },
}));

