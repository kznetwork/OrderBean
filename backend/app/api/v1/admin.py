"""
관리자 API 엔드포인트
"""
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_, case
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.menu import Menu

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db)
):
    """
    관리자 대시보드 요약 정보
    
    - 오늘의 주문 통계
    - 상태별 주문 개수
    - 오늘의 매출
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 오늘의 주문들
    today_orders_query = select(Order).where(Order.created_at >= today_start)
    today_orders_result = await db.execute(today_orders_query)
    today_orders = today_orders_result.scalars().all()
    
    # 상태별 개수
    status_counts = {
        "received": 0,
        "preparing": 0,
        "completed": 0,
        "cancelled": 0,
    }
    
    total_revenue = Decimal("0.00")
    
    for order in today_orders:
        status_counts[order.status.value] = status_counts.get(order.status.value, 0) + 1
        if order.status == OrderStatus.COMPLETED:
            total_revenue += order.total_amount
    
    return {
        "success": True,
        "data": {
            "today": {
                "total_orders": len(today_orders),
                "revenue": float(total_revenue),
                "average_order_amount": float(total_revenue / len(today_orders)) if today_orders else 0,
            },
            "status_summary": {
                "received": status_counts["received"],
                "preparing": status_counts["preparing"],
                "completed": status_counts["completed"],
                "cancelled": status_counts["cancelled"],
            },
        },
    }


@router.get("/orders")
async def get_admin_orders(
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    date: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    관리자 주문 목록 조회 (전체 주문)
    
    - **status**: 주문 상태 필터
    - **date**: 특정 날짜 필터 (YYYY-MM-DD 형식)
    - **limit**: 페이지당 개수
    - **offset**: 건너뛸 개수
    """
    query = select(Order).options(selectinload(Order.items).selectinload(OrderItem.menu))
    
    # 상태 필터
    if status_filter:
        query = query.where(Order.status == status_filter)
    
    # 날짜 필터
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            next_date = target_date + timedelta(days=1)
            query = query.where(
                and_(
                    Order.created_at >= target_date,
                    Order.created_at < next_date
                )
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="날짜 형식이 올바르지 않습니다. (YYYY-MM-DD 형식 사용)"
            )
    
    # 최신 주문 먼저
    query = query.order_by(desc(Order.created_at)).limit(limit).offset(offset)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # 응답 데이터 구성
    orders_data = []
    for order in orders:
        orders_data.append({
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": float(order.total_amount),
            "item_count": len(order.items),
            "items": [
                {
                    "menu_name": item.menu.name,
                    "quantity": item.quantity,
                }
                for item in order.items
            ],
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
        })
    
    return {
        "success": True,
        "data": orders_data,
    }


@router.get("/statistics")
async def get_statistics(
    period: str = Query("day", regex="^(day|week|month)$"),
    db: AsyncSession = Depends(get_db)
):
    """
    매출 및 주문 통계
    
    - **period**: 조회 기간 (day, week, month)
    """
    now = datetime.utcnow()
    
    # 기간 설정
    if period == "day":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = now - timedelta(days=7)
    else:  # month
        start_date = now - timedelta(days=30)
    
    # 해당 기간의 주문들
    orders_query = select(Order).where(
        and_(
            Order.created_at >= start_date,
            Order.status == OrderStatus.COMPLETED
        )
    ).options(selectinload(Order.items).selectinload(OrderItem.menu))
    
    orders_result = await db.execute(orders_query)
    orders = orders_result.scalars().all()
    
    # 매출 계산
    total_revenue = sum(order.total_amount for order in orders)
    total_orders = len(orders)
    average_order = total_revenue / total_orders if total_orders > 0 else Decimal("0.00")
    
    # 메뉴별 판매 통계
    menu_stats = {}
    for order in orders:
        for item in order.items:
            menu_name = item.menu.name
            if menu_name not in menu_stats:
                menu_stats[menu_name] = {
                    "name": menu_name,
                    "count": 0,
                    "revenue": Decimal("0.00"),
                }
            menu_stats[menu_name]["count"] += item.quantity
            menu_stats[menu_name]["revenue"] += item.subtotal
    
    # TOP 메뉴 (판매량 기준)
    top_menus = sorted(
        menu_stats.values(),
        key=lambda x: x["count"],
        reverse=True
    )[:5]
    
    # 시간대별 주문 분포 (오늘만)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    hourly_distribution = [0] * 24
    
    today_orders_query = select(Order).where(Order.created_at >= today_start)
    today_orders_result = await db.execute(today_orders_query)
    today_orders = today_orders_result.scalars().all()
    
    for order in today_orders:
        hour = order.created_at.hour
        hourly_distribution[hour] += 1
    
    return {
        "success": True,
        "data": {
            "revenue": {
                "total": float(total_revenue),
                "average": float(average_order),
            },
            "orders": {
                "total": total_orders,
                "completed": total_orders,
            },
            "top_menus": [
                {
                    "name": menu["name"],
                    "count": menu["count"],
                    "revenue": float(menu["revenue"]),
                }
                for menu in top_menus
            ],
            "hourly_distribution": [
                {"hour": hour, "orders": count}
                for hour, count in enumerate(hourly_distribution)
                if count > 0
            ],
        },
    }


@router.get("/inventory")
async def get_inventory(
    db: AsyncSession = Depends(get_db)
):
    """
    재고 현황 조회
    
    - 전체 메뉴의 재고 상태
    """
    query = select(Menu).order_by(Menu.id)
    result = await db.execute(query)
    menus = result.scalars().all()
    
    inventory_data = []
    for menu in menus:
        inventory_data.append({
            "id": menu.id,
            "name": menu.name,
            "stock": menu.stock,
            "is_available": menu.is_available,
            "price": float(menu.price),
        })
    
    return {
        "success": True,
        "data": inventory_data,
    }


@router.put("/inventory/{menu_id}")
async def update_inventory(
    menu_id: int,
    stock: int = Query(..., ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    재고 수량 업데이트
    
    - **menu_id**: 메뉴 ID
    - **stock**: 새로운 재고 수량
    """
    query = select(Menu).where(Menu.id == menu_id)
    result = await db.execute(query)
    menu = result.scalar_one_or_none()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="메뉴를 찾을 수 없습니다."
        )
    
    menu.stock = stock
    
    # 재고가 0이면 자동으로 비활성화
    if stock == 0:
        menu.is_available = False
    
    await db.commit()
    await db.refresh(menu)
    
    return {
        "success": True,
        "message": "재고가 업데이트되었습니다.",
        "data": {
            "id": menu.id,
            "name": menu.name,
            "stock": menu.stock,
            "is_available": menu.is_available,
        },
    }

