import './AdminHeader.css';

interface AdminHeaderProps {
  activeTab: 'order' | 'admin';
  onTabChange: (tab: 'order' | 'admin') => void;
}

export const AdminHeader = ({ activeTab, onTabChange }: AdminHeaderProps) => {
  return (
    <header className="admin-header">
      <div className="admin-header-content">
        <h1 className="brand-name">OrderBean – 커피 주문</h1>
        <nav className="admin-nav">
          <button
            className={`nav-tab ${activeTab === 'order' ? 'active' : ''}`}
            onClick={() => onTabChange('order')}
          >
            주문하기
          </button>
          <button
            className={`nav-tab ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => onTabChange('admin')}
          >
            관리자
          </button>
        </nav>
      </div>
    </header>
  );
};

