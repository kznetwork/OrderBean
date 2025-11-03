import './AdminDashboard.css';

interface OrderStats {
  totalOrders: number;
  completedOrders: number;
  totalRevenue: number;
  pendingOrders: number;
  inProgressOrders: number;
}

interface AdminDashboardProps {
  stats: OrderStats;
}

export const AdminDashboard = ({ stats }: AdminDashboardProps) => {
  const formatPrice = (price: number) => {
    return price.toLocaleString('ko-KR');
  };

  return (
    <section className="admin-dashboard">
      <h2 className="dashboard-title">관리자 대시보드</h2>
      <div className="dashboard-stats">
        <div className="stat-item">
          <span className="stat-label">오늘 총 주문:</span>
          <span className="stat-value">{stats.totalOrders}건</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">접수 대기:</span>
          <span className="stat-value pending">{stats.pendingOrders}건</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">제조 중:</span>
          <span className="stat-value preparing">{stats.inProgressOrders}건</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">완료:</span>
          <span className="stat-value completed">{stats.completedOrders}건</span>
        </div>
        <div className="stat-item revenue">
          <span className="stat-label">오늘 매출:</span>
          <span className="stat-value">{formatPrice(stats.totalRevenue)}원</span>
        </div>
      </div>
    </section>
  );
};


