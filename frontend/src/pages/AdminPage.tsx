import { useEffect, useState } from 'react';
import { AdminHeader } from '../components/admin/AdminHeader';
import { AdminDashboard } from '../components/admin/AdminDashboard';
import { InventorySection } from '../components/admin/InventorySection';
import { OrdersSection } from '../components/admin/OrdersSection';
import adminService, { DashboardSummary, AdminOrder, InventoryItem } from '../services/adminService';
import orderService, { OrderStatus } from '../services/orderService';
import './AdminPage.css';

interface AdminPageProps {
  onNavigate?: (tab: 'order' | 'admin') => void;
}

export const AdminPage = ({ onNavigate }: AdminPageProps) => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [orders, setOrders] = useState<AdminOrder[]>([]);
  const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    // 30초마다 데이터 새로고침
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      console.log('🔄 관리자 데이터 로드 시작...');
      setLoading(true);
      
      const [summaryData, ordersData, inventoryData] = await Promise.all([
        adminService.getDashboardSummary(),
        adminService.getOrders(),
        adminService.getInventory(),
      ]);
      
      console.log('✅ 대시보드 요약:', summaryData);
      console.log('✅ 주문 목록:', ordersData.length, '개');
      console.log('✅ 재고 목록:', inventoryData.length, '개');
      
      setSummary(summaryData);
      setOrders(ordersData);
      setInventoryItems(inventoryData);
    } catch (err: any) {
      console.error('❌ 관리자 데이터 로드 실패:', err);
      console.error('에러 상세:', err.response?.data || err.message);
      alert('관리자 데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tab: 'order' | 'admin') => {
    if (onNavigate) {
      onNavigate(tab);
    }
  };

  const handleUpdateOrderStatus = async (orderId: number, status: OrderStatus) => {
    try {
      await orderService.updateOrderStatus(orderId, status);
      await loadData(); // 데이터 새로고침
    } catch (err) {
      console.error('주문 상태 변경 실패:', err);
      alert('주문 상태 변경에 실패했습니다.');
    }
  };

  const handleUpdateInventory = async (menuId: number, quantity: number) => {
    try {
      await adminService.updateInventory(menuId, quantity);
      await loadData(); // 데이터 새로고침
    } catch (err) {
      console.error('재고 업데이트 실패:', err);
      alert('재고 업데이트에 실패했습니다.');
    }
  };

  if (loading && !summary) {
    return <div>로딩 중...</div>;
  }

  return (
    <div className="admin-page">
      <AdminHeader activeTab="admin" onTabChange={handleTabChange} />
      <main className="admin-content">
        {summary && (
          <AdminDashboard stats={{
            totalOrders: summary.today.total_orders,
            completedOrders: summary.status_summary.completed,
            totalRevenue: summary.today.revenue,
            pendingOrders: summary.status_summary.received,
            inProgressOrders: summary.status_summary.preparing,
          }} />
        )}
        <InventorySection 
          items={inventoryItems.map(item => ({
            id: item.id.toString(),
            menuId: item.id,
            name: item.name,
            stock: item.stock,
            price: item.price,
          }))} 
          onUpdateQuantity={(menuIdStr: string, quantity: number) => {
            const menuId = parseInt(menuIdStr);
            handleUpdateInventory(menuId, quantity);
          }} 
        />
        <OrdersSection 
          orders={orders.map(order => ({
            id: order.id.toString(),
            orderId: order.id,
            orderNumber: order.order_number,
            customerName: '고객', // API에서 고객 정보가 없으므로 기본값
            status: order.status,
            items: order.items.map(item => ({
              menuName: item.menu_name,
              quantity: item.quantity,
            })),
            totalAmount: order.total_amount,
            createdAt: order.created_at,
          }))} 
          onUpdateStatus={(orderIdStr: string, status: OrderStatus) => {
            const orderId = parseInt(orderIdStr);
            handleUpdateOrderStatus(orderId, status);
          }} 
        />
      </main>
    </div>
  );
};


