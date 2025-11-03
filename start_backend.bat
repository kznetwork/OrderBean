@echo off
chcp 65001 >nul
echo ========================================
echo OrderBean 백엔드 서버 시작
echo ========================================
echo.

cd backend

echo [1/3] 데이터베이스 연결 확인 중...
python test_db_connection.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 데이터베이스 연결 실패!
    echo PostgreSQL이 실행 중인지 확인하세요.
    pause
    exit /b 1
)

echo.
echo [2/3] 환경 설정 확인 중...
if not exist .env (
    echo ⚠️ .env 파일이 없습니다.
    echo 환경 변수를 설정해주세요.
    pause
)

echo.
echo [3/3] 백엔드 서버 시작 중...
echo 서버 주소: http://localhost:8000
echo API 문서: http://localhost:8000/api/docs
echo 중지하려면 Ctrl+C를 누르세요.
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

