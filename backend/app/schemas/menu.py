"""
메뉴 스키마 (Pydantic 모델)
"""
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MenuOptionBase(BaseModel):
    """메뉴 옵션 기본 스키마"""
    name: str = Field(..., description="옵션 이름")
    additional_price: Decimal = Field(..., description="추가 가격")


class MenuOptionCreate(MenuOptionBase):
    """메뉴 옵션 생성 스키마"""
    pass


class MenuOptionUpdate(BaseModel):
    """메뉴 옵션 수정 스키마"""
    name: Optional[str] = None
    additional_price: Optional[Decimal] = None


class MenuOption(MenuOptionBase):
    """메뉴 옵션 응답 스키마"""
    id: int
    menu_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuBase(BaseModel):
    """메뉴 기본 스키마"""
    name: str = Field(..., max_length=100, description="메뉴명")
    description: Optional[str] = Field(None, description="메뉴 설명")
    price: Decimal = Field(..., gt=0, description="가격")
    image_url: Optional[str] = Field(None, max_length=500, description="이미지 URL")
    stock: int = Field(default=0, ge=0, description="재고 수량")
    is_available: bool = Field(default=True, description="판매 가능 여부")


class MenuCreate(MenuBase):
    """메뉴 생성 스키마"""
    options: Optional[List[MenuOptionCreate]] = Field(default=[], description="메뉴 옵션")


class MenuUpdate(BaseModel):
    """메뉴 수정 스키마"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    image_url: Optional[str] = Field(None, max_length=500)
    stock: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None


class Menu(MenuBase):
    """메뉴 응답 스키마"""
    id: int
    options: List[MenuOption] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuList(BaseModel):
    """메뉴 목록 응답 스키마"""
    success: bool = True
    data: List[Menu]


class MenuDetail(BaseModel):
    """메뉴 상세 응답 스키마"""
    success: bool = True
    data: Menu

