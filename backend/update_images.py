"""
메뉴 이미지 경로 업데이트 스크립트
"""
import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal
from app.models.menu import Menu


async def update_menu_images():
    """메뉴 이미지 경로 업데이트"""
    print("=" * 60)
    print("메뉴 이미지 경로 업데이트")
    print("=" * 60)
    print()
    
    # 이미지 매핑 (메뉴명 → 이미지 파일명)
    image_mapping = {
        "아메리카노": "/images/americano.jpg",
        "카페라떼": "/images/cafelatte.jpg",
        "카푸치노": "/images/cappuccino.jpg",
        "바닐라라떼": "/images/vanillalatte.jpg",
        "카라멜 마끼아또": "/images/caramelmacchiato.jpg",
        "카페모카": "/images/cafemocha.jpg",
        "그린티 라떼": "/images/greentealatte.jpg",
        "자몽에이드": "/images/grapefruitade.jpg",
    }
    
    async with AsyncSessionLocal() as session:
        try:
            updated_count = 0
            
            for menu_name, image_url in image_mapping.items():
                # 메뉴 찾기
                query = select(Menu).where(Menu.name == menu_name)
                result = await session.execute(query)
                menu = result.scalar_one_or_none()
                
                if menu:
                    # 이미지 URL 업데이트
                    menu.image_url = image_url
                    updated_count += 1
                    print(f"✅ {menu_name} 이미지 업데이트: {image_url}")
                else:
                    print(f"⚠️  {menu_name} 메뉴를 찾을 수 없습니다.")
            
            await session.commit()
            
            print()
            print("=" * 60)
            print(f"✅ {updated_count}개 메뉴의 이미지 경로가 업데이트되었습니다!")
            print("=" * 60)
            print()
            print("다음 단계:")
            print("  1. 이미지 파일을 frontend/public/images/ 폴더에 복사하세요")
            print("  2. 파일명이 위의 경로와 일치하는지 확인하세요")
            print("  3. 브라우저에서 Ctrl+F5로 새로고침하세요")
            print()
            
        except Exception as e:
            await session.rollback()
            print()
            print("=" * 60)
            print("❌ 오류 발생!")
            print("=" * 60)
            print(f"오류 메시지: {e}")
            print()


async def show_current_images():
    """현재 메뉴의 이미지 경로 표시"""
    print("=" * 60)
    print("현재 메뉴 이미지 경로")
    print("=" * 60)
    print()
    
    async with AsyncSessionLocal() as session:
        try:
            query = select(Menu).order_by(Menu.id)
            result = await session.execute(query)
            menus = result.scalars().all()
            
            if not menus:
                print("⚠️  메뉴가 없습니다.")
                return
            
            for menu in menus:
                image_status = "✅" if menu.image_url else "❌"
                image_path = menu.image_url or "(없음)"
                print(f"{image_status} {menu.name:20s} → {image_path}")
            
            print()
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")


async def set_custom_images():
    """사용자 정의 이미지 경로 설정 (대화형)"""
    print("=" * 60)
    print("사용자 정의 이미지 경로 설정")
    print("=" * 60)
    print()
    print("이미지 파일명을 입력하세요 (예: coffee1.jpg)")
    print("건너뛰려면 Enter만 누르세요")
    print()
    
    menus_to_update = [
        "아메리카노",
        "카페라떼",
        "카푸치노",
        "바닐라라떼",
        "카라멜 마끼아또",
    ]
    
    image_mapping = {}
    
    for menu_name in menus_to_update:
        filename = input(f"{menu_name}: ").strip()
        if filename:
            # 자동으로 /images/ 경로 추가
            if not filename.startswith("/"):
                filename = f"/images/{filename}"
            image_mapping[menu_name] = filename
    
    if not image_mapping:
        print("\n⚠️  입력된 이미지가 없습니다.")
        return
    
    print()
    print("=" * 60)
    print("다음 이미지가 설정됩니다:")
    print("=" * 60)
    for menu_name, image_url in image_mapping.items():
        print(f"  {menu_name} → {image_url}")
    print()
    
    confirm = input("계속하시겠습니까? (y/n): ").strip().lower()
    if confirm != 'y':
        print("취소되었습니다.")
        return
    
    async with AsyncSessionLocal() as session:
        try:
            updated_count = 0
            
            for menu_name, image_url in image_mapping.items():
                query = select(Menu).where(Menu.name == menu_name)
                result = await session.execute(query)
                menu = result.scalar_one_or_none()
                
                if menu:
                    menu.image_url = image_url
                    updated_count += 1
                    print(f"✅ {menu_name} 이미지 업데이트: {image_url}")
                else:
                    print(f"⚠️  {menu_name} 메뉴를 찾을 수 없습니다.")
            
            await session.commit()
            
            print()
            print(f"✅ {updated_count}개 메뉴의 이미지 경로가 업데이트되었습니다!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ 오류 발생: {e}")


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "show":
            asyncio.run(show_current_images())
        elif command == "custom":
            asyncio.run(set_custom_images())
        else:
            print(f"알 수 없는 명령: {command}")
            print()
            print("사용법:")
            print("  python update_images.py        - 기본 이미지 경로로 자동 업데이트")
            print("  python update_images.py show   - 현재 이미지 경로 확인")
            print("  python update_images.py custom - 사용자 정의 이미지 경로 설정")
    else:
        asyncio.run(update_menu_images())


if __name__ == "__main__":
    main()

