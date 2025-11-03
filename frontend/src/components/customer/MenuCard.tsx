import React, { useState, useMemo } from 'react';
import { MenuItem, CartItem } from '../../types/menu';
import './MenuCard.css';

interface MenuCardProps {
  menu: MenuItem;
  onAddToCart: (item: CartItem) => void;
}

export const MenuCard: React.FC<MenuCardProps> = ({ menu, onAddToCart }) => {
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);

  const totalPrice = useMemo(() => {
    let price = menu.price;
    selectedOptions.forEach(optionId => {
      const option = menu.options.find(opt => opt.id === optionId);
      if (option) {
        price += option.price;
      }
    });
    return price;
  }, [menu, selectedOptions]);

  const handleOptionChange = (optionId: string) => {
    setSelectedOptions(prev =>
      prev.includes(optionId)
        ? prev.filter(id => id !== optionId)
        : [...prev, optionId]
    );
  };

  const handleAddToCart = () => {
    const cartItem: CartItem = {
      id: `${menu.id}-${Date.now()}`,
      menuId: menu.id,
      menuName: menu.name,
      basePrice: menu.price,
      selectedOptions,
      quantity: 1,
      totalPrice,
    };
    onAddToCart(cartItem);
    setSelectedOptions([]);
  };

  return (
    <div className="menu-card">
      <div className="menu-image">
        {menu.imageUrl ? (
          <img 
            src={menu.imageUrl} 
            alt={menu.name}
            onError={(e) => {
              // 이미지 로드 실패 시 플레이스홀더 표시
              e.currentTarget.style.display = 'none';
              e.currentTarget.nextElementSibling?.classList.remove('hidden');
            }}
          />
        ) : null}
        <div className={`image-placeholder ${menu.imageUrl ? 'hidden' : ''}`}>
          {menu.imageUrl ? '이미지 없음' : '이미지'}
        </div>
      </div>
      
      <div className="menu-info">
        <h3 className="menu-name">{menu.name}</h3>
        <p className="menu-price">{totalPrice.toLocaleString()}원</p>
        <p className="menu-description">{menu.description}</p>
      </div>

      <div className="menu-options">
        {menu.options.map(option => (
          <label key={option.id} className="option-label">
            <input
              type="checkbox"
              checked={selectedOptions.includes(option.id)}
              onChange={() => handleOptionChange(option.id)}
            />
            <span>{option.label} (+{option.price}원)</span>
          </label>
        ))}
      </div>

      <button className="add-to-cart-button" onClick={handleAddToCart}>
        담기
      </button>
    </div>
  );
};


