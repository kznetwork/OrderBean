@echo off
REM 데이터베이스 설정 통합 스크립트

echo ========================================
echo OrderBean 데이터베이스 설정
echo ========================================
echo.

REM 1. .env 파일 생성
echo [1/4] 환경 변수 파일 생성 중...
call create_env.bat
echo.

REM 2. PostgreSQL 연결 확인
echo [2/4] PostgreSQL 연결 확인 중...
psql -U postgres -c "SELECT version();" >nul 2>&1
if errorlevel 1 (
    echo [!] PostgreSQL에 연결할 수 없습니다.
    echo [!] PostgreSQL이 실행 중인지 확인하세요.
    echo.
    pause
    exit /b 1
)
echo PostgreSQL 연결 성공!
echo.

REM 3. 데이터베이스 생성
echo [3/4] 데이터베이스 생성 중...
psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname='orderbean_db';" | findstr /C:"1 row" >nul
if errorlevel 1 (
    psql -U postgres -c "CREATE DATABASE orderbean_db;"
    echo 데이터베이스 'orderbean_db'가 생성되었습니다.
) else (
    echo 데이터베이스 'orderbean_db'가 이미 존재합니다.
)
echo.

REM 4. 테이블 생성
echo [4/4] 테이블 생성 중...
python init_db.py
echo.

REM 5. 샘플 데이터 입력 (선택사항)
echo ========================================
set /p seed="샘플 데이터를 생성하시겠습니까? (y/n): "
if /i "%seed%"=="y" (
    echo.
    python seed_db.py
)

echo.
echo ========================================
echo ✅ 데이터베이스 설정 완료!
echo ========================================
echo.
echo 서버를 시작하려면:
echo   start_server.bat
echo.
pause
