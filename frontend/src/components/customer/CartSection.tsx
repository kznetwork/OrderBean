import React from 'react';
import { CartItem } from '../../types/menu';
import './CartSection.css';

interface CartSectionProps {
  items: CartItem[];
  totalAmount: number;
  onCheckout: () => void;
}

export const CartSection: React.FC<CartSectionProps> = ({
  items,
  totalAmount,
  onCheckout,
}) => {
  return (
    <div className="cart-section">
      <h2 className="cart-title">장바구니</h2>
      
      <div className="cart-content">
        {/* 왼쪽: 주문 내역 */}
        <div className="cart-items-container">
          <h3 className="cart-subtitle">주문 내역</h3>
          <div className="cart-items">
            {items.length === 0 ? (
              <p className="empty-message">장바구니가 비어있습니다</p>
            ) : (
              items.map(item => (
                <div key={item.id} className="cart-item">
                  <div className="item-left">
                    <span className="item-name">
                      {item.menuName}
                      {item.selectedOptions.length > 0 && (
                        <span className="item-options">
                          {' '}({item.selectedOptions.join(', ')})
                        </span>
                      )}
                    </span>
                    <span className="item-quantity">X {item.quantity}</span>
                  </div>
                  <span className="item-price">{item.totalPrice.toLocaleString()}원</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* 오른쪽: 총액 + 주문하기 버튼 */}
        <div className="cart-summary">
          <div className="summary-content">
            <div className="cart-total">
              <span className="total-label">총 금액</span>
              <span className="total-amount">{totalAmount.toLocaleString()}원</span>
            </div>
            
            <button
              className="checkout-button"
              onClick={onCheckout}
              disabled={items.length === 0}
            >
              주문하기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

