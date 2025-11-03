import React, { useState, useEffect } from 'react';
import { CustomerHeader } from '../components/customer/CustomerHeader';
import { MenuCard } from '../components/customer/MenuCard';
import { CartSection } from '../components/customer/CartSection';
import { useCustomerStore } from '../stores/customerStore';
import menuService, { Menu } from '../services/menuService';
import orderService from '../services/orderService';
import './CustomerPage.css';

interface CustomerPageProps {
  onNavigate?: (tab: 'order' | 'admin') => void;
}

export const CustomerPage: React.FC<CustomerPageProps> = ({ onNavigate }) => {
  const [activeTab, setActiveTab] = useState<'order' | 'admin'>('order');
  const [menus, setMenus] = useState<Menu[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { cartItems, addToCart, getTotalAmount, clearCart } = useCustomerStore();

  // 메뉴 데이터 로드
  useEffect(() => {
    loadMenus();
  }, []);

  const loadMenus = async () => {
    try {
      console.log('📋 메뉴 로드 시작...');
      setLoading(true);
      setError(null);
      
      const data = await menuService.getMenus(true);
      console.log('✅ 메뉴 로드 성공:', data.length, '개');
      console.log('메뉴 데이터:', data);
      
      setMenus(data);
    } catch (err: any) {
      console.error('❌ 메뉴 로드 실패:', err);
      console.error('에러 상세:', err.response?.data || err.message);
      setError('메뉴를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tab: 'order' | 'admin') => {
    setActiveTab(tab);
    if (onNavigate) {
      onNavigate(tab);
    }
  };

  const handleCheckout = async () => {
    if (cartItems.length === 0) {
      alert('장바구니가 비어있습니다.');
      return;
    }

    try {
      // 주문 데이터 생성
      const orderData = {
        items: cartItems.map(item => ({
          menu_id: item.menuId,
          quantity: item.quantity,
          options: item.selectedOptions.map(optId => ({
            option_id: parseInt(optId), // string을 number로 변환
          })),
        })),
      };

      console.log('주문 데이터:', orderData);

      // 주문 생성
      const order = await orderService.createOrder(orderData);
      
      alert(`주문이 완료되었습니다!\n주문번호: ${order.order_number}\n총 금액: ${order.total_amount.toLocaleString()}원`);
      
      // 장바구니 비우기
      clearCart();
      
      // 메뉴 다시 로드 (재고 업데이트)
      await loadMenus();
    } catch (err: any) {
      console.error('주문 실패:', err);
      const errorMessage = err.response?.data?.detail || '주문 처리 중 오류가 발생했습니다.';
      alert(`주문 실패: ${errorMessage}`);
    }
  };

  return (
    <div className="customer-page">
      <CustomerHeader activeTab={activeTab} onTabChange={handleTabChange} />
      
      <main className="main-content">
        <section className="menu-section">
          <h2 className="section-title">메뉴</h2>
          {loading && <p>메뉴를 불러오는 중...</p>}
          {error && <p className="error-message">{error}</p>}
          {!loading && !error && (
            <div className="menu-grid">
              {menus.map(menu => (
                <MenuCard
                  key={menu.id}
                  menu={{
                    id: menu.id,
                    name: menu.name,
                    price: menu.price,
                    description: menu.description || '',
                    imageUrl: menu.image_url || '',
                    category: '',
                    options: menu.options.map(opt => ({
                      id: opt.id.toString(),
                      label: opt.name,
                      price: opt.additional_price,
                    })),
                  }}
                  onAddToCart={addToCart}
                />
              ))}
            </div>
          )}
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

