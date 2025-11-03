@echo off
echo ========================================
echo OrderBean Backend Server
echo ========================================
echo.

REM Python 가상환경 활성화
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✅ 가상환경 활성화 완료
) else (
    echo ⚠️  가상환경이 없습니다. setup_dev.bat를 먼저 실행하세요.
    pause
    exit /b 1
)

echo.
echo 📊 샘플 데이터 확인 및 생성...
python seed_sample_data.py

echo.
echo 🚀 FastAPI 서버 시작...
echo    - API 문서: http://localhost:8000/api/docs
echo    - 서버 주소: http://localhost:8000
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

