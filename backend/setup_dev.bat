@echo off
REM OrderBean 개발 환경 설정 스크립트 (Windows)

echo ========================================
echo OrderBean 개발 환경 설정
echo ========================================
echo.

REM 1. Python 버전 확인
echo [1/4] Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo [!] Python이 설치되지 않았습니다.
    echo [!] https://www.python.org/downloads/ 에서 Python 3.11 이상을 설치하세요.
    pause
    exit /b 1
)
echo.

REM 2. 가상환경 생성
echo [2/4] 가상환경 생성 중...
if exist venv (
    echo 가상환경이 이미 존재합니다.
) else (
    python -m venv venv
    echo 가상환경이 생성되었습니다.
)
echo.

REM 3. 가상환경 활성화 및 패키지 설치
echo [3/4] 가상환경 활성화 및 패키지 설치 중...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM 4. 설치 확인
echo [4/4] 설치 확인 중...
python -c "import fastapi; import uvicorn; print('✅ FastAPI와 Uvicorn이 성공적으로 설치되었습니다.')"
echo.

echo ========================================
echo 개발 환경 설정 완료!
echo ========================================
echo.
echo 다음 명령으로 서버를 시작할 수 있습니다:
echo   start_server.bat
echo.
echo 또는 직접 명령:
echo   python -m uvicorn app.main:app --reload
echo.
pause

