"""
주문 API 엔드포인트
"""
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.order import Order, OrderItem, OrderItemOption, OrderStatus
from app.models.menu import Menu
from app.models.option import MenuOption
from app.schemas.order import (
    OrderCreate,
    OrderCreateResponse,
    OrderList,
    OrderDetail,
    OrderStatusUpdate,
    OrderListItem,
    OrderItemResponse,
    OrderItemOptionResponse,
    Order as OrderSchema,
)

router = APIRouter(prefix="/orders", tags=["orders"])


def generate_order_number() -> str:
    """주문 번호 생성 (ORD-YYYYMMDD-XXX 형식)"""
    now = datetime.utcnow()
    date_str = now.strftime("%Y%m%d")
    # 간단한 타임스탬프 기반 번호 (실제로는 DB 시퀀스 사용 권장)
    time_str = now.strftime("%H%M%S")
    return f"ORD-{date_str}-{time_str}"


@router.post("", response_model=OrderCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    주문 생성
    
    - **order_data**: 주문 정보 (메뉴 ID, 수량, 옵션)
    """
    # 주문 생성
    order = Order(
        order_number=generate_order_number(),
        status=OrderStatus.RECEIVED,
        total_amount=Decimal("0.00"),
    )
    db.add(order)
    await db.flush()  # order.id를 얻기 위해
    
    total_amount = Decimal("0.00")
    
    # 주문 항목 추가
    for item_data in order_data.items:
        # 메뉴 조회
        menu_query = select(Menu).where(Menu.id == item_data.menu_id)
        menu_result = await db.execute(menu_query)
        menu = menu_result.scalar_one_or_none()
        
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"메뉴 ID {item_data.menu_id}를 찾을 수 없습니다."
            )
        
        if not menu.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"메뉴 '{menu.name}'는 현재 판매 불가능합니다."
            )
        
        # 재고 확인 및 차감
        if menu.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"메뉴 '{menu.name}'의 재고가 부족합니다. (현재 재고: {menu.stock})"
            )
        
        menu.stock -= item_data.quantity
        
        # 옵션 가격 계산
        options_price = Decimal("0.00")
        for option_data in item_data.options:
            option_query = select(MenuOption).where(MenuOption.id == option_data.option_id)
            option_result = await db.execute(option_query)
            option = option_result.scalar_one_or_none()
            
            if not option:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"옵션 ID {option_data.option_id}를 찾을 수 없습니다."
                )
            
            options_price += option.additional_price
        
        # 항목별 가격 계산
        unit_price = menu.price + options_price
        subtotal = unit_price * item_data.quantity
        
        # 주문 항목 생성
        order_item = OrderItem(
            order_id=order.id,
            menu_id=menu.id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        db.add(order_item)
        await db.flush()  # order_item.id를 얻기 위해
        
        # 주문 항목 옵션 추가
        for option_data in item_data.options:
            option_query = select(MenuOption).where(MenuOption.id == option_data.option_id)
            option_result = await db.execute(option_query)
            option = option_result.scalar_one()
            
            order_item_option = OrderItemOption(
                order_item_id=order_item.id,
                option_id=option.id,
                option_name=option.name,
                additional_price=option.additional_price,
            )
            db.add(order_item_option)
        
        total_amount += subtotal
    
    # 총 금액 업데이트
    order.total_amount = total_amount
    
    await db.commit()
    await db.refresh(order)
    
    # 주문 상세 정보 로드
    query = (
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.menu),
            selectinload(Order.items)
            .selectinload(OrderItem.options)
        )
    )
    result = await db.execute(query)
    order = result.scalar_one()
    
    # 응답 데이터 구성
    order_dict = {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "completed_at": order.completed_at,
        "items": [
            {
                "id": item.id,
                "menu_id": item.menu_id,
                "menu_name": item.menu.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
                "options": [
                    {
                        "id": opt.id,
                        "option_name": opt.option_name,
                        "additional_price": opt.additional_price,
                    }
                    for opt in item.options
                ],
            }
            for item in order.items
        ],
    }
    
    return OrderCreateResponse(
        success=True,
        message="주문이 완료되었습니다.",
        data=order_dict
    )


@router.get("", response_model=OrderList)
async def get_orders(
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    주문 목록 조회
    
    - **status**: 주문 상태 필터 (선택)
    - **limit**: 페이지당 개수 (기본값: 10)
    - **offset**: 건너뛸 개수 (기본값: 0)
    """
    query = select(Order).options(selectinload(Order.items))
    
    if status_filter:
        query = query.where(Order.status == status_filter)
    
    query = query.order_by(desc(Order.created_at)).limit(limit).offset(offset)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # 주문 목록 데이터 구성
    order_list = [
        OrderListItem(
            id=order.id,
            order_number=order.order_number,
            status=order.status,
            total_amount=order.total_amount,
            item_count=len(order.items),
            created_at=order.created_at,
        )
        for order in orders
    ]
    
    return OrderList(data=order_list)


@router.get("/{order_id}", response_model=OrderDetail)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    주문 상세 조회
    
    - **order_id**: 조회할 주문 ID
    """
    query = (
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.menu),
            selectinload(Order.items)
            .selectinload(OrderItem.options)
        )
    )
    result = await db.execute(query)
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="주문을 찾을 수 없습니다."
        )
    
    # 응답 데이터 구성
    order_dict = {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "completed_at": order.completed_at,
        "items": [
            {
                "id": item.id,
                "menu_id": item.menu_id,
                "menu_name": item.menu.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
                "options": [
                    {
                        "id": opt.id,
                        "option_name": opt.option_name,
                        "additional_price": opt.additional_price,
                    }
                    for opt in item.options
                ],
            }
            for item in order.items
        ],
    }
    
    return OrderDetail(data=order_dict)


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    주문 상태 변경 (관리자 전용)
    
    - **order_id**: 주문 ID
    - **status_data**: 변경할 상태
    """
    query = select(Order).where(Order.id == order_id)
    result = await db.execute(query)
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="주문을 찾을 수 없습니다."
        )
    
    order.status = status_data.status
    
    # 완료 상태로 변경 시 완료 시간 기록
    if status_data.status == OrderStatus.COMPLETED:
        order.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(order)
    
    return {
        "success": True,
        "message": "주문 상태가 변경되었습니다.",
        "data": {
            "order_id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "updated_at": order.updated_at,
        },
    }

