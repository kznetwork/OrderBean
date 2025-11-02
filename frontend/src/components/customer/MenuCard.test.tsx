import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MenuCard } from './MenuCard';
import { MenuItem } from '../../types/menu';

const mockMenu: MenuItem = {
  id: 1,
  name: '아메리카노(ICE)',
  price: 4000,
  description: '간단한 설명',
  imageUrl: '/images/americano.jpg',
  category: '커피',
  options: [
    { id: 'shot', label: '샷 추가', price: 500 },
    { id: 'syrup', label: '시럽 추가', price: 0 },
  ],
};

describe('MenuCard', () => {
  it('메뉴 이름이 표시되어야 한다', () => {
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    expect(screen.getByText('아메리카노(ICE)')).toBeInTheDocument();
  });

  it('메뉴 가격이 표시되어야 한다', () => {
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    expect(screen.getByText('4,000원')).toBeInTheDocument();
  });

  it('메뉴 설명이 표시되어야 한다', () => {
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    expect(screen.getByText('간단한 설명')).toBeInTheDocument();
  });

  it('옵션 체크박스가 표시되어야 한다', () => {
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    expect(screen.getByLabelText('샷 추가 (+500원)')).toBeInTheDocument();
    expect(screen.getByLabelText('시럽 추가 (+0원)')).toBeInTheDocument();
  });

  it('담기 버튼이 표시되어야 한다', () => {
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    expect(screen.getByRole('button', { name: '담기' })).toBeInTheDocument();
  });

  it('옵션 선택 시 가격이 업데이트되어야 한다', async () => {
    const user = userEvent.setup();
    render(<MenuCard menu={mockMenu} onAddToCart={() => {}} />);
    
    const shotCheckbox = screen.getByLabelText('샷 추가 (+500원)');
    await user.click(shotCheckbox);
    
    expect(screen.getByText('4,500원')).toBeInTheDocument();
  });

  it('담기 버튼 클릭 시 onAddToCart가 호출되어야 한다', async () => {
    const user = userEvent.setup();
    const onAddToCart = vi.fn();
    render(<MenuCard menu={mockMenu} onAddToCart={onAddToCart} />);
    
    const addButton = screen.getByRole('button', { name: '담기' });
    await user.click(addButton);
    
    expect(onAddToCart).toHaveBeenCalled();
    expect(onAddToCart).toHaveBeenCalledWith(
      expect.objectContaining({
        menuId: 1,
        menuName: '아메리카노(ICE)',
        basePrice: 4000,
        quantity: 1,
      })
    );
  });
});

