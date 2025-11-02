import { useEffect } from 'react';
import { useAdminStore } from '../stores/adminStore';
import { AdminHeader } from '../components/admin/AdminHeader';
import { AdminDashboard } from '../components/admin/AdminDashboard';
import { InventorySection } from '../components/admin/InventorySection';
import { OrdersSection } from '../components/admin/OrdersSection';
import './AdminPage.css';

interface AdminPageProps {
  onNavigate?: (tab: 'order' | 'admin') => void;
}

export const AdminPage = ({ onNavigate }: AdminPageProps) => {
  const { 
    orderStats, 
    orders, 
    inventoryItems, 
    initializeMockData,
    updateOrderStatus,
    updateInventoryQuantity,
  } = useAdminStore();

  useEffect(() => {
    // 초기 데이터 로드
    initializeMockData();
  }, [initializeMockData]);

  const handleTabChange = (tab: 'order' | 'admin') => {
    if (onNavigate) {
      onNavigate(tab);
    }
  };

  return (
    <div className="admin-page">
      <AdminHeader activeTab="admin" onTabChange={handleTabChange} />
      <main className="admin-content">
        <AdminDashboard stats={orderStats} />
        <InventorySection 
          items={inventoryItems} 
          onUpdateQuantity={updateInventoryQuantity} 
        />
        <OrdersSection 
          orders={orders} 
          onUpdateStatus={updateOrderStatus} 
        />
      </main>
    </div>
  );
};


