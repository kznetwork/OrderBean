import { useState } from 'react';
import { CustomerPage } from './pages/CustomerPage';
import { AdminPage } from './pages/AdminPage';
import './App.css';

function App() {
  console.log('App component loaded');
  const [activeView, setActiveView] = useState<'order' | 'admin'>('order');

  const handleNavigate = (view: 'order' | 'admin') => {
    setActiveView(view);
  };

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
