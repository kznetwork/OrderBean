import { OrderStatus } from '../../types/admin';
import './OrdersSection.css';

interface OrderItem {
  menuName: string;
  quantity: number;
}

interface Order {
  id: string;
  orderId: number;
  orderNumber: string;
  customerName: string;
  status: OrderStatus;
  items: OrderItem[];
  totalAmount: number;
  createdAt: string;
}

interface OrdersSectionProps {
  orders: Order[];
  onUpdateStatus: (orderId: string, newStatus: OrderStatus) => void;
}

const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  return `${month}월 ${day}일 ${hours}:${minutes}`;
};

const formatPrice = (price: number): string => {
  return `${price.toLocaleString()}원`;
};

const getStatusButton = (status: OrderStatus) => {
  switch (status) {
    case 'received':
      return { text: '제조 시작', nextStatus: 'preparing' as OrderStatus };
    case 'preparing':
      return { text: '제조 완료', nextStatus: 'completed' as OrderStatus };
    case 'completed':
      return null; // 완료된 주문은 버튼 없음
    case 'cancelled':
      return null; // 취소된 주문은 버튼 없음
    default:
      return null;
  }
};

export const OrdersSection = ({ orders, onUpdateStatus }: OrdersSectionProps) => {
  return (
    <section className="orders-section">
      <h2 className="orders-title">주문 현황</h2>
      {orders.length === 0 ? (
        <p className="empty-message">주문이 없습니다</p>
      ) : (
        <div className="orders-list">
          {orders.map(order => {
            const statusButton = getStatusButton(order.status);
            return (
              <div key={order.id} className={`order-card status-${order.status}`}>
                <div className="order-header">
                  <span className="order-time">{formatDateTime(order.createdAt)}</span>
                </div>
                <div className="order-body">
                  <div className="order-items">
                    {order.items.map((item, index) => (
                      <p key={index} className="order-item">
                        {item.menuName} x {item.quantity}
                      </p>
                    ))}
                  </div>
                  <div className="order-footer">
                    <span className="order-price">{formatPrice(order.totalAmount)}</span>
                    {statusButton && (
                      <button
                        className={`btn-status btn-${order.status}`}
                        onClick={() => onUpdateStatus(order.id, statusButton.nextStatus)}
                      >
                        {statusButton.text}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};


