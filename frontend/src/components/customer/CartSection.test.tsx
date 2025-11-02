import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CartSection } from './CartSection';
import { CartItem } from '../../types/menu';

const mockCartItems: CartItem[] = [
  {
    id: '1',
    menuId: 1,
    menuName: '아메리카노(ICE)',
    basePrice: 4000,
    selectedOptions: ['shot'],
    quantity: 1,
    totalPrice: 4500,
  },
  {
    id: '2',
    menuId: 2,
    menuName: '아메리카노(HOT)',
    basePrice: 4000,
    selectedOptions: [],
    quantity: 2,
    totalPrice: 8000,
  },
];

describe('CartSection', () => {
  it('"장바구니" 제목이 표시되어야 한다', () => {
    render(<CartSection items={[]} totalAmount={0} onCheckout={() => {}} />);
    expect(screen.getByText('장바구니')).toBeInTheDocument();
  });

  it('장바구니가 비어있을 때 빈 메시지가 표시되어야 한다', () => {
    render(<CartSection items={[]} totalAmount={0} onCheckout={() => {}} />);
    expect(screen.getByText('장바구니가 비어있습니다')).toBeInTheDocument();
  });

  it('장바구니 아이템이 표시되어야 한다', () => {
    render(
      <CartSection 
        items={mockCartItems} 
        totalAmount={12500} 
        onCheckout={() => {}} 
      />
    );
    
    expect(screen.getByText(/아메리카노\(ICE\)/)).toBeInTheDocument();
    expect(screen.getByText(/아메리카노\(HOT\)/)).toBeInTheDocument();
  });

  it('아이템 수량이 표시되어야 한다', () => {
    render(
      <CartSection 
        items={mockCartItems} 
        totalAmount={12500} 
        onCheckout={() => {}} 
      />
    );
    
    expect(screen.getByText(/X 1/)).toBeInTheDocument();
    expect(screen.getByText(/X 2/)).toBeInTheDocument();
  });

  it('총 금액이 표시되어야 한다', () => {
    render(
      <CartSection 
        items={mockCartItems} 
        totalAmount={12500} 
        onCheckout={() => {}} 
      />
    );
    
    expect(screen.getByText('총 금액')).toBeInTheDocument();
    expect(screen.getByText('12,500원')).toBeInTheDocument();
  });

  it('주문하기 버튼이 표시되어야 한다', () => {
    render(
      <CartSection 
        items={mockCartItems} 
        totalAmount={12500} 
        onCheckout={() => {}} 
      />
    );
    
    expect(screen.getByRole('button', { name: '주문하기' })).toBeInTheDocument();
  });

  it('장바구니가 비어있을 때 주문하기 버튼이 비활성화되어야 한다', () => {
    render(<CartSection items={[]} totalAmount={0} onCheckout={() => {}} />);
    
    const checkoutButton = screen.getByRole('button', { name: '주문하기' });
    expect(checkoutButton).toBeDisabled();
  });

  it('주문하기 버튼 클릭 시 onCheckout이 호출되어야 한다', async () => {
    const user = userEvent.setup();
    const onCheckout = vi.fn();
    
    render(
      <CartSection 
        items={mockCartItems} 
        totalAmount={12500} 
        onCheckout={onCheckout} 
      />
    );
    
    const checkoutButton = screen.getByRole('button', { name: '주문하기' });
    await user.click(checkoutButton);
    
    expect(onCheckout).toHaveBeenCalled();
  });
});


