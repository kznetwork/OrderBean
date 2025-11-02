import React, { useState } from 'react';
import { CustomerHeader } from '../components/customer/CustomerHeader';
import { MenuCard } from '../components/customer/MenuCard';
import { CartSection } from '../components/customer/CartSection';
import { useCustomerStore } from '../stores/customerStore';
import { menuData } from '../data/menuData';
import './CustomerPage.css';

interface CustomerPageProps {
  onNavigate?: (tab: 'order' | 'admin') => void;
}

export const CustomerPage: React.FC<CustomerPageProps> = ({ onNavigate }) => {
  const [activeTab, setActiveTab] = useState<'order' | 'admin'>('order');
  const { cartItems, addToCart, getTotalAmount } = useCustomerStore();

  const handleTabChange = (tab: 'order' | 'admin') => {
    setActiveTab(tab);
    if (onNavigate) {
      onNavigate(tab);
    }
  };

  const handleCheckout = () => {
    if (cartItems.length > 0) {
      alert(`주문이 완료되었습니다!\n총 금액: ${getTotalAmount().toLocaleString()}원`);
    }
  };

  return (
    <div className="customer-page">
      <CustomerHeader activeTab={activeTab} onTabChange={handleTabChange} />
      
      <main className="main-content">
        <section className="menu-section">
          <h2 className="section-title">재고 현황</h2>
          <div className="menu-grid">
            {menuData.map(menu => (
              <MenuCard
                key={menu.id}
                menu={menu}
                onAddToCart={addToCart}
              />
            ))}
          </div>
        </section>

        <aside className="cart-aside">
          <CartSection
            items={cartItems}
            totalAmount={getTotalAmount()}
            onCheckout={handleCheckout}
          />
        </aside>
      </main>
    </div>
  );
};

