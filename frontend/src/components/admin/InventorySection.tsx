import { InventoryStatus } from '../../types/admin';
import './InventorySection.css';

interface InventoryItem {
  id: string;
  menuId: number;
  name: string;
  stock: number;
  price: number;
}

interface InventorySectionProps {
  items: InventoryItem[];
  onUpdateQuantity: (itemId: string, newQuantity: number) => void;
}

const getInventoryStatus = (quantity: number): InventoryStatus => {
  if (quantity === 0) return '품절';
  if (quantity < 5) return '주의';
  return '정상';
};

export const InventorySection = ({ items, onUpdateQuantity }: InventorySectionProps) => {
  const handleQuantityChange = (itemId: string, currentStock: number, delta: number) => {
    const newQuantity = Math.max(0, currentStock + delta);
    onUpdateQuantity(itemId, newQuantity);
  };

  return (
    <section className="inventory-section">
      <h2 className="inventory-title">재고 현황</h2>
      <div className="inventory-grid">
        {items.map(item => {
          const status = getInventoryStatus(item.stock);
          return (
            <div 
              key={item.id} 
              className={`inventory-card ${status === '주의' ? 'low-stock' : ''} ${status === '품절' ? 'out-of-stock' : ''}`}
            >
              <h3 className="menu-name">{item.name}</h3>
              <div className="quantity-status-row">
                <p className="quantity">{item.stock}개</p>
                <p className={`status status-${status}`}>{status}</p>
              </div>
              <div className="quantity-controls">
                <button 
                  className="btn-control"
                  onClick={() => handleQuantityChange(item.id, item.stock, 1)}
                  aria-label={`${item.name} 재고 증가`}
                >
                  +
                </button>
                <button 
                  className="btn-control"
                  onClick={() => handleQuantityChange(item.id, item.stock, -1)}
                  disabled={item.stock === 0}
                  aria-label={`${item.name} 재고 감소`}
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

