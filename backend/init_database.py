"""
데이터베이스 초기화 및 테스트 데이터 생성
"""
import asyncio
import sys
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

from app.core.database import engine, Base, AsyncSessionLocal
from app.models import Menu, MenuOption, Order, OrderItem, OrderStatus
from datetime import datetime

async def init_database():
    """데이터베이스 초기화"""
    print("="*60)
    print("OrderBean 데이터베이스 초기화")
    print("="*60)
    print()
    
    try:
        # 1. 테이블 생성
        print("📦 [1/2] 데이터베이스 테이블 생성 중...")
        async with engine.begin() as conn:
            # 기존 테이블 삭제 (개발 환경에서만!)
            await conn.run_sync(Base.metadata.drop_all)
            # 새 테이블 생성
            await conn.run_sync(Base.metadata.create_all)
        print("   ✅ 테이블 생성 완료!")
        print()
        
        # 2. 테스트 데이터 생성
        print("🌱 [2/2] 테스트 데이터 생성 중...")
        async with AsyncSessionLocal() as session:
            # 메뉴 데이터
            menus = [
                Menu(
                    name="아메리카노",
                    description="깊고 진한 에스프레소에 물을 더한 커피",
                    price=4000,
                    image_url="/images/americano.jpg",
                    stock_quantity=100,
                    is_available=True
                ),
                Menu(
                    name="카페라떼",
                    description="부드러운 우유와 에스프레소의 조화",
                    price=4500,
                    image_url="/images/latte.jpg",
                    stock_quantity=100,
                    is_available=True
                ),
                Menu(
                    name="카푸치노",
                    description="진한 에스프레소와 우유 거품의 완벽한 균형",
                    price=4500,
                    image_url="/images/cappuccino.jpg",
                    stock_quantity=100,
                    is_available=True
                ),
                Menu(
                    name="바닐라 라떼",
                    description="달콤한 바닐라 시럽이 들어간 라떼",
                    price=5000,
                    image_url="/images/vanilla-latte.jpg",
                    stock_quantity=80,
                    is_available=True
                ),
                Menu(
                    name="카라멜 마키아또",
                    description="부드러운 우유와 카라멜의 달콤한 조화",
                    price=5500,
                    image_url="/images/caramel-macchiato.jpg",
                    stock_quantity=80,
                    is_available=True
                ),
            ]
            
            session.add_all(menus)
            await session.flush()  # ID 할당을 위해 flush
            
            print(f"   ✅ {len(menus)}개의 메뉴 생성 완료!")
            
            # 옵션 데이터
            options = []
            for menu in menus:
                # 사이즈 옵션
                options.extend([
                    MenuOption(menu_id=menu.id, name="사이즈", value="Regular", price=0),
                    MenuOption(menu_id=menu.id, name="사이즈", value="Large", price=500),
                ])
                # 샷 추가 옵션
                options.extend([
                    MenuOption(menu_id=menu.id, name="샷 추가", value="1샷 추가", price=500),
                    MenuOption(menu_id=menu.id, name="샷 추가", value="2샷 추가", price=1000),
                ])
                # 온도 옵션 (아이스/핫)
                options.extend([
                    MenuOption(menu_id=menu.id, name="온도", value="HOT", price=0),
                    MenuOption(menu_id=menu.id, name="온도", value="ICE", price=0),
                ])
            
            session.add_all(options)
            print(f"   ✅ {len(options)}개의 옵션 생성 완료!")
            
            # 테스트 주문 데이터
            test_order = Order(
                order_number="ORD-20251102-001",
                customer_name="홍길동",
                total_price=9000,
                status=OrderStatus.PENDING,
                notes="테스트 주문입니다"
            )
            session.add(test_order)
            await session.flush()
            
            # 주문 항목
            order_items = [
                OrderItem(
                    order_id=test_order.id,
                    menu_id=menus[0].id,  # 아메리카노
                    quantity=2,
                    unit_price=4000,
                    total_price=8000,
                    options='{"사이즈": "Regular", "온도": "ICE"}'
                ),
                OrderItem(
                    order_id=test_order.id,
                    menu_id=menus[1].id,  # 카페라떼
                    quantity=1,
                    unit_price=4500,
                    total_price=4500,
                    options='{"사이즈": "Large", "온도": "HOT", "샷 추가": "1샷 추가"}'
                ),
            ]
            
            # 총액 업데이트
            test_order.total_price = sum(item.total_price for item in order_items)
            
            session.add_all(order_items)
            print(f"   ✅ 테스트 주문 생성 완료!")
            
            # 커밋
            await session.commit()
        
        print()
        print("="*60)
        print("✅ 데이터베이스 초기화 완료!")
        print("="*60)
        print()
        print("📊 생성된 데이터:")
        print(f"   - 메뉴: {len(menus)}개")
        print(f"   - 옵션: {len(options)}개")
        print(f"   - 주문: 1개 (테스트)")
        print()
        print("🚀 서버를 시작하세요:")
        print("   python -m uvicorn app.main:app --reload")
        print()
        print("📚 API 문서:")
        print("   http://localhost:8000/api/docs")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 초기화 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await engine.dispose()


def main():
    """메인 함수"""
    try:
        success = asyncio.run(init_database())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  초기화가 중단되었습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()

