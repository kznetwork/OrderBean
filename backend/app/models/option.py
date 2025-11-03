"""
옵션 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class MenuOption(Base):
    """메뉴 옵션 테이블"""
    
    __tablename__ = "menu_options"
    
    id = Column(Integer, primary_key=True, index=True, comment="옵션 ID")
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False, comment="메뉴 ID")
    name = Column(String(100), nullable=False, comment="옵션 이름")
    additional_price = Column(Numeric(10, 2), default=0, comment="추가 가격")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 일시")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정 일시"
    )
    
    # 관계
    menu = relationship("Menu", back_populates="options")
    order_item_options = relationship("OrderItemOption", back_populates="option")
    
    def __repr__(self):
        return f"<MenuOption(id={self.id}, name='{self.name}', price={self.additional_price})>"
