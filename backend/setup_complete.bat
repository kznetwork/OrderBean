@echo off
chcp 65001 >nul
echo ========================================
echo OrderBean 완전 설치 스크립트
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] 가상환경 확인...
if not exist "venv\" (
    echo ⚠️  가상환경이 없습니다. 생성 중...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 가상환경 생성 실패!
        pause
        exit /b 1
    )
    echo ✅ 가상환경 생성 완료!
) else (
    echo ✅ 가상환경이 이미 존재합니다.
)
echo.

echo [2/6] 가상환경 활성화...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패!
    pause
    exit /b 1
)
echo ✅ 가상환경 활성화 완료!
echo.

echo [3/6] 패키지 설치 중...
echo (이 과정은 몇 분 소요될 수 있습니다)
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ 패키지 설치 실패!
    pause
    exit /b 1
)
echo ✅ 패키지 설치 완료!
echo.

echo [4/6] 데이터베이스 생성...
python create_database.py
if errorlevel 1 (
    echo ⚠️  데이터베이스 생성 실패 또는 건너뜀
    echo.
    echo PostgreSQL 서비스가 실행 중인지 확인하세요:
    echo   1. Windows + R 키를 누르고 "services.msc" 입력
    echo   2. "postgresql" 서비스를 찾아서 시작
    echo.
    echo 또는 pgAdmin을 사용하여 수동으로 'orderbean_db' 데이터베이스를 생성하세요.
    echo.
    pause
    exit /b 1
)
echo.

echo [5/6] 데이터베이스 테이블 및 샘플 데이터 생성...
python init_database.py
if errorlevel 1 (
    echo ❌ 데이터베이스 초기화 실패!
    pause
    exit /b 1
)
echo.

echo [6/6] 데이터베이스 연결 테스트...
python test_db_connection.py
if errorlevel 1 (
    echo ⚠️  연결 테스트 실패
)
echo.

echo ========================================
echo ✅ 설치 완료!
echo ========================================
echo.
echo 서버를 시작하려면:
echo   start_dev.bat
echo.
echo 또는 수동으로:
echo   uvicorn app.main:app --reload
echo.
echo API 문서:
echo   http://localhost:8000/api/docs
echo.
pause

