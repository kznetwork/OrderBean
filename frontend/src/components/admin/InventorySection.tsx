import { InventoryItem, InventoryStatus } from '../../types/admin';
import './InventorySection.css';

interface InventorySectionProps {
  items: InventoryItem[];
  onUpdateQuantity: (itemId: number, delta: number) => void;
}

const getInventoryStatus = (quantity: number): InventoryStatus => {
  if (quantity === 0) return '품절';
  if (quantity < 5) return '주의';
  return '정상';
};

export const InventorySection = ({ items, onUpdateQuantity }: InventorySectionProps) => {
  return (
    <section className="inventory-section">
      <h2 className="inventory-title">재고 현황</h2>
      <div className="inventory-grid">
        {items.map(item => {
          const status = getInventoryStatus(item.quantity);
          return (
            <div 
              key={item.id} 
              className={`inventory-card ${status === '주의' ? 'low-stock' : ''} ${status === '품절' ? 'out-of-stock' : ''}`}
            >
              <h3 className="menu-name">{item.menuName}</h3>
              <div className="quantity-status-row">
                <p className="quantity">{item.quantity}개</p>
                <p className={`status status-${status}`}>{status}</p>
              </div>
              <div className="quantity-controls">
                <button 
                  className="btn-control"
                  onClick={() => onUpdateQuantity(item.id, 1)}
                  aria-label={`${item.menuName} 재고 증가`}
                >
                  +
                </button>
                <button 
                  className="btn-control"
                  onClick={() => onUpdateQuantity(item.id, -1)}
                  aria-label={`${item.menuName} 재고 감소`}
                >
                  -
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

