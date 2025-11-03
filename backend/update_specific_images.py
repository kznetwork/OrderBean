"""
사용자 지정 이미지 경로로 메뉴 업데이트
"""
import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.menu import Menu


async def update_menu_images():
    """메뉴 이미지 경로 업데이트 - 사용자 지정"""
    print("=" * 60)
    print("메뉴 이미지 경로 업데이트 (사용자 지정)")
    print("=" * 60)
    print()
    
    # 사용자가 지정한 이미지 매핑
    image_mapping = {
        "Americano": "/images/Americano.jpg",
        "Cafe Latte": "/images/Cafe-Latte.jpg",
        "Cappuccino": "/images/Cappuccino.jpg",
        "Vanilla Latte": "/images/Vanilla-Latte.jpg",
        "Caramel Macchiato": "/images/Caramel-Macchiato.jpg",
    }
    
    async with AsyncSessionLocal() as session:
        try:
            updated_count = 0
            not_found = []
            
            for menu_name, image_url in image_mapping.items():
                # 메뉴 찾기
                query = select(Menu).where(Menu.name == menu_name)
                result = await session.execute(query)
                menu = result.scalar_one_or_none()
                
                if menu:
                    # 이미지 URL 업데이트
                    menu.image_url = image_url
                    updated_count += 1
                    print(f"✅ {menu_name:20s} → {image_url}")
                else:
                    not_found.append(menu_name)
                    print(f"⚠️  {menu_name:20s} → 메뉴를 찾을 수 없습니다")
            
            await session.commit()
            
            print()
            print("=" * 60)
            print(f"✅ {updated_count}개 메뉴의 이미지 경로가 업데이트되었습니다!")
            print("=" * 60)
            print()
            
            if not_found:
                print("⚠️  다음 메뉴를 찾을 수 없습니다:")
                for menu_name in not_found:
                    print(f"   - {menu_name}")
                print()
            
            print("📸 이미지 파일 확인:")
            print("   frontend/public/images/Americano.jpg")
            print("   frontend/public/images/Cafe-Latte.jpg")
            print("   frontend/public/images/Cappuccino.jpg")
            print("   frontend/public/images/Vanilla-Latte.jpg")
            print("   frontend/public/images/Caramel-Macchiato.jpg")
            print()
            
            print("다음 단계:")
            print("  1. 브라우저에서 http://localhost:5173 접속")
            print("  2. Ctrl + Shift + R (강력 새로고침)")
            print("  3. 메뉴 카드에 이미지가 표시되는지 확인")
            print()
            
        except Exception as e:
            await session.rollback()
            print()
            print("=" * 60)
            print("❌ 오류 발생!")
            print("=" * 60)
            print(f"오류 메시지: {e}")
            print()


if __name__ == "__main__":
    asyncio.run(update_menu_images())

