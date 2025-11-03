"""
샘플 데이터 생성 스크립트
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine, Base
from app.models.menu import Menu
from app.models.option import MenuOption


async def create_sample_data():
    """샘플 메뉴 및 옵션 데이터 생성"""
    
    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        # 기존 데이터 확인
        result = await session.execute(select(Menu))
        existing_menus = result.scalars().all()
        
        if existing_menus:
            print("⚠️  이미 데이터가 존재합니다. 기존 데이터를 사용합니다.")
            return
        
        print("📝 샘플 메뉴 데이터 생성 중...")
        
        # 커피 메뉴
        menus_data = [
            {
                "name": "아메리카노",
                "description": "진한 에스프레소와 물",
                "price": 4500,
                "stock": 50,
                "image_url": "/images/americano.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "얼음 추가", "price": 0},
                ]
            },
            {
                "name": "카페라떼",
                "description": "부드러운 우유와 에스프레소",
                "price": 5000,
                "stock": 40,
                "image_url": "/images/latte.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "휘핑크림", "price": 500},
                ]
            },
            {
                "name": "바닐라라떼",
                "description": "달콤한 바닐라 시럽과 에스프레소",
                "price": 5500,
                "stock": 35,
                "image_url": "/images/vanilla-latte.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "바닐라 시럽 추가", "price": 500},
                ]
            },
            {
                "name": "카푸치노",
                "description": "풍부한 우유 거품과 에스프레소",
                "price": 5000,
                "stock": 30,
                "image_url": "/images/cappuccino.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "시나몬 파우더", "price": 0},
                ]
            },
            {
                "name": "카라멜 마끼아또",
                "description": "달콤한 카라멜과 에스프레소",
                "price": 6000,
                "stock": 25,
                "image_url": "/images/caramel-macchiato.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "카라멜 시럽 추가", "price": 500},
                ]
            },
            {
                "name": "콜드브루",
                "description": "12시간 저온 추출 커피",
                "price": 5500,
                "stock": 20,
                "image_url": "/images/coldbrew.jpg",
                "options": [
                    {"name": "샷 추가", "price": 500},
                    {"name": "우유 추가", "price": 500},
                ]
            },
        ]
        
        # 메뉴 생성
        for menu_data in menus_data:
            options = menu_data.pop("options", [])
            
            menu = Menu(
                name=menu_data["name"],
                description=menu_data["description"],
                price=menu_data["price"],
                stock=menu_data["stock"],
                image_url=menu_data["image_url"],
                is_available=True,
            )
            session.add(menu)
            await session.flush()
            
            # 옵션 추가
            for option_data in options:
                option = MenuOption(
                    menu_id=menu.id,
                    name=option_data["name"],
                    additional_price=option_data["price"],
                )
                session.add(option)
        
        await session.commit()
        print("✅ 샘플 데이터 생성 완료!")
        print(f"   - {len(menus_data)}개의 메뉴 생성됨")


async def main():
    """메인 함수"""
    try:
        await create_sample_data()
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

