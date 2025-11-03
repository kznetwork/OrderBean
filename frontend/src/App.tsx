import { useState, useEffect } from 'react';
import { CustomerPage } from './pages/CustomerPage';
import { AdminPage } from './pages/AdminPage';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState<'order' | 'admin'>('order');
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    console.log('🚀 OrderBean App 시작');
    console.log('📡 API URL:', import.meta.env.VITE_API_URL || 'http://localhost:8000');
  }, []);

  const handleNavigate = (view: 'order' | 'admin') => {
    console.log(`🔄 페이지 전환: ${view}`);
    setActiveView(view);
  };

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h1>오류가 발생했습니다</h1>
        <p>{error.message}</p>
        <button onClick={() => window.location.reload()}>새로고침</button>
      </div>
    );
  }

  return (
    <div>
      {activeView === 'order' ? (
        <CustomerPage onNavigate={handleNavigate} />
      ) : (
        <AdminPage onNavigate={handleNavigate} />
      )}
    </div>
  );
}

export default App;
