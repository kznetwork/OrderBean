"""
주문 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class OrderStatus(str, enum.Enum):
    """주문 상태"""
    RECEIVED = "received"      # 주문 접수
    PREPARING = "preparing"    # 제조 중
    COMPLETED = "completed"    # 완료
    CANCELLED = "cancelled"    # 취소


class Order(Base):
    """주문 테이블"""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, comment="주문 ID")
    order_number = Column(String(50), unique=True, nullable=False, index=True, comment="주문 번호")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="총 금액")
    status = Column(
        SQLEnum(OrderStatus),
        default=OrderStatus.RECEIVED,
        nullable=False,
        comment="주문 상태"
    )
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, comment="주문 일시")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정 일시"
    )
    completed_at = Column(DateTime, nullable=True, comment="완료 일시")
    
    # 관계
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, number='{self.order_number}', status='{self.status}')>"


class OrderItem(Base):
    """주문 항목 테이블"""
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, comment="주문 항목 ID")
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, comment="주문 ID")
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False, comment="메뉴 ID")
    quantity = Column(Integer, nullable=False, default=1, comment="수량")
    unit_price = Column(Numeric(10, 2), nullable=False, comment="단가")
    subtotal = Column(Numeric(10, 2), nullable=False, comment="소계")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 일시")
    
    # 관계
    order = relationship("Order", back_populates="items")
    menu = relationship("Menu", back_populates="order_items")
    options = relationship("OrderItemOption", back_populates="order_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, menu_id={self.menu_id}, quantity={self.quantity})>"


class OrderItemOption(Base):
    """주문 항목 옵션 테이블"""
    
    __tablename__ = "order_item_options"
    
    id = Column(Integer, primary_key=True, index=True, comment="주문 항목 옵션 ID")
    order_item_id = Column(
        Integer,
        ForeignKey("order_items.id", ondelete="CASCADE"),
        nullable=False,
        comment="주문 항목 ID"
    )
    option_id = Column(Integer, ForeignKey("menu_options.id"), nullable=False, comment="옵션 ID")
    option_name = Column(String(100), nullable=False, comment="옵션 이름 (스냅샷)")
    additional_price = Column(Numeric(10, 2), nullable=False, comment="추가 가격 (스냅샷)")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 일시")
    
    # 관계
    order_item = relationship("OrderItem", back_populates="options")
    option = relationship("MenuOption", back_populates="order_item_options")
    
    def __repr__(self):
        return f"<OrderItemOption(id={self.id}, option='{self.option_name}')>"
