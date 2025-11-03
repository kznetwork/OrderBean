"""
OrderBean 서버 접속 테스트 스크립트
"""
import sys
import time
import json

try:
    import requests
except ImportError:
    print("❌ requests 패키지가 설치되지 않았습니다.")
    print("   다음 명령으로 설치하세요: pip install requests")
    sys.exit(1)


def test_endpoint(url, name):
    """엔드포인트 테스트 함수"""
    try:
        print(f"\n{'='*60}")
        print(f"테스트: {name}")
        print(f"URL: {url}")
        print('-'*60)
        
        response = requests.get(url, timeout=5)
        
        print(f"✅ 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 응답 내용:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"⚠️  예상치 못한 상태 코드: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("   서버가 실행 중인지 확인하세요.")
        return False
    except requests.exceptions.Timeout:
        print("❌ 요청 시간이 초과되었습니다.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def main():
    """메인 테스트 함수"""
    print("\n" + "="*60)
    print("OrderBean FastAPI 서버 접속 테스트")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    # 서버 준비 대기
    print("\n서버 응답 대기 중...")
    time.sleep(2)
    
    # 테스트할 엔드포인트 목록
    endpoints = [
        (f"{base_url}/", "루트 엔드포인트 (API 정보)"),
        (f"{base_url}/health", "헬스 체크"),
        (f"{base_url}/api/v1/test", "테스트 엔드포인트"),
    ]
    
    # 각 엔드포인트 테스트
    results = []
    for url, name in endpoints:
        success = test_endpoint(url, name)
        results.append((name, success))
        time.sleep(0.5)  # 요청 사이 짧은 지연
    
    # 결과 요약
    print("\n" + "="*60)
    print("테스트 결과 요약")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{status} - {name}")
    
    print("\n" + "-"*60)
    print(f"통과: {passed}/{total}")
    print("="*60)
    
    # API 문서 링크 안내
    if passed > 0:
        print("\n📚 API 문서:")
        print(f"   - Swagger UI: {base_url}/api/docs")
        print(f"   - ReDoc: {base_url}/api/redoc")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  테스트가 중단되었습니다.")
        sys.exit(1)

