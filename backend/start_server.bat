@echo off
REM OrderBean FastAPI 서버 시작 스크립트 (Windows)

echo ========================================
echo OrderBean FastAPI Server
echo ========================================
echo.

REM 가상환경 확인 및 활성화 (선택사항)
if exist venv\Scripts\activate.bat (
    echo [1/3] 가상환경 활성화 중...
    call venv\Scripts\activate.bat
) else (
    echo [!] 가상환경이 없습니다. 시스템 Python을 사용합니다.
)

REM 필요한 패키지 확인
echo.
echo [2/3] 패키지 확인 중...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [!] FastAPI가 설치되지 않았습니다.
    echo [!] pip install -r requirements.txt 명령을 실행하세요.
    pause
    exit /b 1
)

REM 서버 시작
echo.
echo [3/3] 서버 시작 중...
echo.
echo ========================================
echo 서버 주소: http://localhost:8000
echo API 문서: http://localhost:8000/api/docs
echo ========================================
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

