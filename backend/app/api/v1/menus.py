"""
메뉴 API 엔드포인트
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.menu import Menu
from app.models.option import MenuOption
from app.schemas.menu import (
    MenuList,
    MenuDetail,
    MenuCreate,
    MenuUpdate,
    Menu as MenuSchema,
)

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("", response_model=MenuList)
async def get_menus(
    available_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    메뉴 목록 조회
    
    - **available_only**: 판매 가능한 메뉴만 조회 (기본값: True)
    """
    query = select(Menu).options(selectinload(Menu.options))
    
    if available_only:
        query = query.where(Menu.is_available == True)
    
    query = query.order_by(Menu.id)
    
    result = await db.execute(query)
    menus = result.scalars().all()
    
    return MenuList(data=menus)


@router.get("/{menu_id}", response_model=MenuDetail)
async def get_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    메뉴 상세 조회
    
    - **menu_id**: 조회할 메뉴 ID
    """
    query = select(Menu).where(Menu.id == menu_id).options(selectinload(Menu.options))
    result = await db.execute(query)
    menu = result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="메뉴를 찾을 수 없습니다."
        )
    
    return MenuDetail(data=menu)


@router.post("", response_model=MenuDetail, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    메뉴 생성 (관리자 전용)
    
    - **menu_data**: 생성할 메뉴 정보
    """
    # 메뉴 생성
    menu = Menu(
        name=menu_data.name,
        description=menu_data.description,
        price=menu_data.price,
        image_url=menu_data.image_url,
        stock=menu_data.stock,
        is_available=menu_data.is_available,
    )
    
    db.add(menu)
    await db.flush()  # menu.id를 얻기 위해
    
    # 옵션 추가
    if menu_data.options:
        for option_data in menu_data.options:
            option = MenuOption(
                menu_id=menu.id,
                name=option_data.name,
                additional_price=option_data.additional_price,
            )
            db.add(option)
    
    await db.commit()
    await db.refresh(menu)
    
    # 옵션 데이터를 포함하여 다시 로드
    query = select(Menu).where(Menu.id == menu.id).options(selectinload(Menu.options))
    result = await db.execute(query)
    menu = result.scalar_one()
    
    return MenuDetail(data=menu)


@router.put("/{menu_id}", response_model=MenuDetail)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    메뉴 수정 (관리자 전용)
    
    - **menu_id**: 수정할 메뉴 ID
    - **menu_data**: 수정할 메뉴 정보
    """
    query = select(Menu).where(Menu.id == menu_id)
    result = await db.execute(query)
    menu = result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="메뉴를 찾을 수 없습니다."
        )
    
    # 수정된 필드만 업데이트
    update_data = menu_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(menu, field, value)
    
    await db.commit()
    await db.refresh(menu)
    
    # 옵션 데이터를 포함하여 다시 로드
    query = select(Menu).where(Menu.id == menu.id).options(selectinload(Menu.options))
    result = await db.execute(query)
    menu = result.scalar_one()
    
    return MenuDetail(data=menu)


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    메뉴 삭제 (관리자 전용)
    
    - **menu_id**: 삭제할 메뉴 ID
    
    Note: Soft delete 대신 실제 삭제를 수행합니다.
    실제 프로덕션에서는 is_available=False로 설정하는 것이 좋습니다.
    """
    query = select(Menu).where(Menu.id == menu_id)
    result = await db.execute(query)
    menu = result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="메뉴를 찾을 수 없습니다."
        )
    
    # Soft delete (is_available = False)
    menu.is_available = False
    await db.commit()
    
    return None

