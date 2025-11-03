@echo off
chcp 65001 >nul
echo ========================================
echo OrderBean 프론트엔드 서버 시작
echo ========================================
echo.

cd frontend

echo [1/3] 백엔드 연결 확인 중...
curl -s http://localhost:8000 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ 백엔드 서버가 실행되지 않았습니다!
    echo 먼저 start_backend.bat를 실행하세요.
    echo.
    pause
    exit /b 1
)
echo ✅ 백엔드 서버 연결 확인

echo.
echo [2/3] 환경 변수 설정 중...
echo VITE_API_URL=http://localhost:8000 > .env.local
echo ✅ .env.local 파일 생성/업데이트 완료

echo.
echo [3/3] 프론트엔드 서버 시작 중...
echo 서버 주소: http://localhost:5173
echo 중지하려면 Ctrl+C를 누르세요.
echo.
echo 💡 팁: 환경 변수가 변경되었으므로 서버가 재시작됩니다.
echo 💡 브라우저에서 Ctrl+Shift+R로 강력 새로고침하세요.
echo.

npm run dev

pause

