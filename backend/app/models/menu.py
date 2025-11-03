"""
메뉴 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Menu(Base):
    """메뉴 테이블"""
    
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True, comment="메뉴 ID")
    name = Column(String(100), nullable=False, comment="커피 이름")
    description = Column(Text, nullable=True, comment="설명")
    price = Column(Numeric(10, 2), nullable=False, comment="가격")
    image_url = Column(String(500), nullable=True, comment="이미지 URL")
    stock = Column(Integer, default=0, comment="재고 수량")
    is_available = Column(Boolean, default=True, comment="판매 가능 여부")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 일시")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정 일시"
    )
    
    # 관계
    options = relationship("MenuOption", back_populates="menu", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="menu")
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', price={self.price})>"
