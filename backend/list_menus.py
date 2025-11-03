"""
현재 데이터베이스의 메뉴 목록 확인
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.menu import Menu


async def list_menus():
    """메뉴 목록 표시"""
    print("=" * 60)
    print("데이터베이스 메뉴 목록")
    print("=" * 60)
    print()
    
    async with AsyncSessionLocal() as session:
        try:
            query = select(Menu).order_by(Menu.id)
            result = await session.execute(query)
            menus = result.scalars().all()
            
            if not menus:
                print("⚠️  메뉴가 없습니다.")
                print()
                print("샘플 데이터 생성:")
                print("  python seed_db.py")
                return
            
            print(f"총 {len(menus)}개의 메뉴:")
            print()
            
            for i, menu in enumerate(menus, 1):
                image_status = "✅" if menu.image_url else "❌"
                print(f"{i}. {menu.name}")
                print(f"   ID: {menu.id}")
                print(f"   가격: {menu.price}원")
                print(f"   재고: {menu.stock}")
                print(f"   이미지: {image_status} {menu.image_url or '(없음)'}")
                print()
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(list_menus())

