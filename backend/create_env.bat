@echo off
REM 환경 변수 파일 생성 스크립트

echo ========================================
echo .env 파일 생성
echo ========================================
echo.

if exist .env (
    echo [!] .env 파일이 이미 존재합니다.
    set /p overwrite="덮어쓰시겠습니까? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo 작업이 취소되었습니다.
        pause
        exit /b 0
    )
)

echo # OrderBean Backend Environment Variables> .env
echo.>> .env
echo # Database Configuration>> .env
echo DB_HOST=localhost>> .env
echo DB_PORT=5432>> .env
echo DB_NAME=orderbean_db>> .env
echo DB_USER=postgres>> .env
echo DB_PASSWORD=postgresql>> .env
echo.>> .env
echo # Database URL>> .env
echo DATABASE_URL=postgresql+asyncpg://postgres:postgresql@localhost:5432/orderbean_db>> .env
echo.>> .env
echo # Application Settings>> .env
echo APP_NAME=OrderBean API>> .env
echo APP_VERSION=1.0.0>> .env
echo DEBUG=True>> .env
echo ENVIRONMENT=development>> .env
echo.>> .env
echo # Security>> .env
echo SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7>> .env
echo ALGORITHM=HS256>> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30>> .env
echo.>> .env
echo # CORS Settings>> .env
echo ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000>> .env
echo.>> .env
echo # Server Settings>> .env
echo HOST=0.0.0.0>> .env
echo PORT=8000>> .env

echo.
echo ========================================
echo ✅ .env 파일이 생성되었습니다!
echo ========================================
echo.
echo 데이터베이스 설정:
echo   - Host: localhost
echo   - Port: 5432
echo   - Database: orderbean_db
echo   - User: postgres
echo   - Password: postgresql
echo.
pause

