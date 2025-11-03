export type OrderStatus = 'received' | 'preparing' | 'completed' | 'cancelled';

export interface OrderItem {
  menuName: string;
  quantity: number;
  options?: string[];
}

export interface Order {
  id: number;
  orderNumber: string;
  createdAt: string;
  items: OrderItem[];
  totalPrice: number;
  status: OrderStatus;
  specialRequest?: string;
}

export interface OrderStats {
  totalOrders: number;
  pendingOrders: number;
  preparingOrders: number;
  completedOrders: number;
}

export interface InventoryItem {
  id: number;
  menuName: string;
  quantity: number;
  minQuantity?: number;
  maxQuantity?: number;
}

export type InventoryStatus = '정상' | '주의' | '품절';


