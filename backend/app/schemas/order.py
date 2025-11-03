"""
주문 스키마 (Pydantic 모델)
"""
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from app.models.order import OrderStatus


class OrderItemOptionCreate(BaseModel):
    """주문 항목 옵션 생성 스키마"""
    option_id: int = Field(..., description="옵션 ID")


class OrderItemOptionResponse(BaseModel):
    """주문 항목 옵션 응답 스키마"""
    id: int
    option_name: str
    additional_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    """주문 항목 생성 스키마"""
    menu_id: int = Field(..., description="메뉴 ID")
    quantity: int = Field(..., gt=0, description="수량")
    options: List[OrderItemOptionCreate] = Field(default=[], description="선택한 옵션들")


class OrderItemResponse(BaseModel):
    """주문 항목 응답 스키마"""
    id: int
    menu_id: int
    menu_name: str = ""
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    options: List[OrderItemOptionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """주문 생성 스키마"""
    items: List[OrderItemCreate] = Field(..., min_length=1, description="주문 항목들")


class OrderUpdate(BaseModel):
    """주문 수정 스키마"""
    status: Optional[OrderStatus] = None


class OrderStatusUpdate(BaseModel):
    """주문 상태 변경 스키마"""
    status: OrderStatus = Field(..., description="변경할 주문 상태")


class Order(BaseModel):
    """주문 응답 스키마"""
    id: int
    order_number: str
    status: OrderStatus
    total_amount: Decimal
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderListItem(BaseModel):
    """주문 목록 항목 스키마"""
    id: int
    order_number: str
    status: OrderStatus
    total_amount: Decimal
    item_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    """주문 목록 응답 스키마"""
    success: bool = True
    data: List[OrderListItem]


class OrderDetail(BaseModel):
    """주문 상세 응답 스키마"""
    success: bool = True
    data: Order


class OrderCreateResponse(BaseModel):
    """주문 생성 응답 스키마"""
    success: bool = True
    message: str = "주문이 완료되었습니다."
    data: Order

