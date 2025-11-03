"""
샘플 데이터 생성 스크립트
"""
import asyncio
import sys
from pathlib import Path
from decimal import Decimal

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import AsyncSessionLocal
from app.models import Menu, MenuOption


async def seed_menus():
    """샘플 메뉴 데이터 생성"""
    print("="*60)
    print("샘플 데이터 생성")
    print("="*60)
    print()
    
    async with AsyncSessionLocal() as session:
        try:
            print("🔄 메뉴 데이터 생성 중...")
            
            # 샘플 메뉴 데이터
            menus_data = [
                {
                    "name": "아메리카노",
                    "description": "진한 에스프레소에 물을 더한 클래식 커피",
                    "price": Decimal("4500"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "카페라떼",
                    "description": "에스프레소와 부드러운 우유의 조화",
                    "price": Decimal("5000"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "휘핑크림", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "카푸치노",
                    "description": "에스프레소와 우유 거품이 어우러진 커피",
                    "price": Decimal("5000"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "시나몬 토핑", "additional_price": Decimal("300")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "바닐라라떼",
                    "description": "달콤한 바닐라 시럽이 들어간 라떼",
                    "price": Decimal("5500"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "바닐라 시럽 추가", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "카라멜 마끼아또",
                    "description": "달콤한 카라멜과 우유, 에스프레소의 완벽한 조합",
                    "price": Decimal("6000"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "카라멜 시럽 추가", "additional_price": Decimal("500")},
                        {"name": "휘핑크림", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "카페모카",
                    "description": "초콜릿과 에스프레소의 달콤쌉싸름한 맛",
                    "price": Decimal("5500"),
                    "stock": 100,
                    "options": [
                        {"name": "샷 추가", "additional_price": Decimal("500")},
                        {"name": "초코 시럽 추가", "additional_price": Decimal("500")},
                        {"name": "휘핑크림", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "그린티 라떼",
                    "description": "진한 녹차와 우유의 건강한 조합",
                    "price": Decimal("5500"),
                    "stock": 50,
                    "options": [
                        {"name": "녹차 파우더 추가", "additional_price": Decimal("500")},
                        {"name": "꿀 추가", "additional_price": Decimal("500")},
                        {"name": "ICE", "additional_price": Decimal("0")},
                        {"name": "HOT", "additional_price": Decimal("0")},
                    ]
                },
                {
                    "name": "자몽에이드",
                    "description": "상큼한 자몽의 청량한 맛",
                    "price": Decimal("6000"),
                    "stock": 50,
                    "options": [
                        {"name": "자몽 과육 추가", "additional_price": Decimal("1000")},
                        {"name": "탄산 추가", "additional_price": Decimal("0")},
                    ]
                },
            ]
            
            # 메뉴 및 옵션 생성
            menu_count = 0
            option_count = 0
            
            for menu_data in menus_data:
                options_data = menu_data.pop("options", [])
                
                # 메뉴 생성
                menu = Menu(**menu_data)
                session.add(menu)
                await session.flush()  # ID 할당을 위해 flush
                menu_count += 1
                
                # 옵션 생성
                for option_data in options_data:
                    option = MenuOption(menu_id=menu.id, **option_data)
                    session.add(option)
                    option_count += 1
            
            await session.commit()
            
            print(f"✅ 메뉴 {menu_count}개 생성 완료")
            print(f"✅ 옵션 {option_count}개 생성 완료")
            print()
            
            print("="*60)
            print("✅ 샘플 데이터 생성 완료!")
            print("="*60)
            print()
            print("생성된 메뉴:")
            for menu_data in menus_data:
                print(f"  - {menu_data['name']}: {menu_data['price']}원")
            print()
            
        except Exception as e:
            await session.rollback()
            print()
            print("="*60)
            print("❌ 오류 발생!")
            print("="*60)
            print(f"오류 메시지: {e}")
            print()
            print("해결 방법:")
            print("  1. 데이터베이스가 초기화되었는지 확인하세요: python init_db.py")
            print("  2. 이미 샘플 데이터가 존재하는 경우 재생성: python init_db.py reset")
            print()


async def clear_data():
    """모든 데이터 삭제"""
    print("="*60)
    print("⚠️  경고: 모든 데이터를 삭제합니다!")
    print("="*60)
    print()
    
    async with AsyncSessionLocal() as session:
        try:
            # 모든 메뉴 삭제 (cascade로 옵션도 함께 삭제됨)
            from sqlalchemy import delete
            await session.execute(delete(Menu))
            await session.commit()
            
            print("✅ 모든 데이터가 삭제되었습니다.")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 오류 발생: {e}")


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "clear":
            asyncio.run(clear_data())
        else:
            print(f"알 수 없는 명령: {command}")
            print("사용법:")
            print("  python seed_db.py       - 샘플 데이터 생성")
            print("  python seed_db.py clear - 모든 데이터 삭제")
    else:
        asyncio.run(seed_menus())


if __name__ == "__main__":
    main()

