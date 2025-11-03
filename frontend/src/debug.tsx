/**
 * 디버깅용 테스트 페이지
 * API 연결 및 데이터 로딩 확인
 */
import { useEffect, useState } from 'react';
import menuService from './services/menuService';

export const DebugPage = () => {
  const [status, setStatus] = useState<string>('확인 중...');
  const [apiUrl, setApiUrl] = useState<string>('');
  const [menus, setMenus] = useState<any[]>([]);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      // 1. 환경 변수 확인
      const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      setApiUrl(url);
      console.log('🔍 API URL:', url);

      // 2. 백엔드 연결 테스트
      setStatus('백엔드 연결 테스트 중...');
      const response = await fetch(url);
      const data = await response.json();
      console.log('✅ 백엔드 응답:', data);

      // 3. 메뉴 API 테스트
      setStatus('메뉴 데이터 로드 중...');
      const menuData = await menuService.getMenus(true);
      console.log('✅ 메뉴 데이터:', menuData);
      setMenus(menuData);

      setStatus('✅ 모든 테스트 통과!');
    } catch (err: any) {
      console.error('❌ 에러:', err);
      setError(err.message);
      setStatus('❌ 테스트 실패');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🔍 OrderBean 디버그 페이지</h1>
      
      <div style={{ marginBottom: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h2>연결 상태</h2>
        <p><strong>상태:</strong> {status}</p>
        <p><strong>API URL:</strong> {apiUrl}</p>
        {error && <p style={{ color: 'red' }}><strong>에러:</strong> {error}</p>}
      </div>

      <div style={{ marginBottom: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h2>환경 변수</h2>
        <pre>{JSON.stringify({
          VITE_API_URL: import.meta.env.VITE_API_URL,
          MODE: import.meta.env.MODE,
          DEV: import.meta.env.DEV,
          PROD: import.meta.env.PROD,
        }, null, 2)}</pre>
      </div>

      {menus.length > 0 && (
        <div style={{ marginBottom: '20px', padding: '10px', background: '#f0f0f0' }}>
          <h2>메뉴 데이터 ({menus.length}개)</h2>
          <pre style={{ maxHeight: '300px', overflow: 'auto' }}>
            {JSON.stringify(menus, null, 2)}
          </pre>
        </div>
      )}

      <div style={{ marginTop: '20px' }}>
        <button onClick={checkConnection} style={{ padding: '10px 20px', marginRight: '10px' }}>
          다시 테스트
        </button>
        <button onClick={() => window.location.href = '/'} style={{ padding: '10px 20px' }}>
          메인 페이지로
        </button>
      </div>

      <div style={{ marginTop: '30px', padding: '10px', background: '#fff3cd' }}>
        <h3>⚠️ 문제 해결 팁</h3>
        <ul>
          <li>백엔드 서버가 실행 중인지 확인: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a></li>
          <li>메뉴 API 직접 확인: <a href="http://localhost:8000/api/v1/menus" target="_blank">http://localhost:8000/api/v1/menus</a></li>
          <li>브라우저 콘솔(F12)에서 에러 메시지 확인</li>
          <li>.env.local 파일에 VITE_API_URL=http://localhost:8000 설정 확인</li>
          <li>프론트엔드 서버 재시작 필요 (환경 변수 변경 시)</li>
        </ul>
      </div>
    </div>
  );
};

