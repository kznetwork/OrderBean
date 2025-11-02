import { OrderStats } from '../../types/admin';
import './AdminDashboard.css';

interface AdminDashboardProps {
  stats: OrderStats;
}

export const AdminDashboard = ({ stats }: AdminDashboardProps) => {
  return (
    <section className="admin-dashboard">
      <h2 className="dashboard-title">관리자 대시보드</h2>
      <div className="dashboard-stats">
        <p className="stats-text">
          총 주문 {stats.totalOrders} / 주문 접수 {stats.pendingOrders} / 제조 중 {stats.preparingOrders} / 제조 완료 {stats.completedOrders}
        </p>
      </div>
    </section>
  );
};

