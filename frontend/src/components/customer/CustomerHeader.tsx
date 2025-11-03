import React from 'react';
import './CustomerHeader.css';

interface CustomerHeaderProps {
  activeTab: 'order' | 'admin';
  onTabChange: (tab: 'order' | 'admin') => void;
}

export const CustomerHeader: React.FC<CustomerHeaderProps> = ({ activeTab, onTabChange }) => {
  return (
    <header className="customer-header">
      <div className="brand-name">OrderBean – 커피 주문</div>
      <nav className="nav-tabs">
        <button
          className={`tab-button ${activeTab === 'order' ? 'active' : ''}`}
          onClick={() => onTabChange('order')}
        >
          주문하기
        </button>
        <button
          className={`tab-button ${activeTab === 'admin' ? 'active' : ''}`}
          onClick={() => onTabChange('admin')}
        >
          관리자
        </button>
      </nav>
    </header>
  );
};

