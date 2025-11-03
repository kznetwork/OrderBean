import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { OrdersSection } from './OrdersSection';
import { Order } from '../../types/admin';

describe('OrdersSection', () => {
  const mockOrders: Order[] = [
    {
      id: 1,
      orderNumber: 'ORD-001',
      createdAt: '2025-07-31T13:00:00',
      items: [
        { menuName: '아메리카노(ICE)', quantity: 1 },
      ],
      totalPrice: 4000,
      status: 'pending',
    },
    {
      id: 2,
      orderNumber: 'ORD-002',
      createdAt: '2025-07-31T13:05:00',
      items: [
        { menuName: '카페라떼', quantity: 2 },
      ],
      totalPrice: 10000,
      status: 'preparing',
    },
  ];

  it('섹션 제목 "주문 현황"을 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('주문 현황')).toBeInTheDocument();
  });

  it('주문 리스트를 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('아메리카노(ICE) x 1')).toBeInTheDocument();
    expect(screen.getByText('카페라떼 x 2')).toBeInTheDocument();
  });

  it('주문 일자와 시간을 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('7월 31일 13:00')).toBeInTheDocument();
    expect(screen.getByText('7월 31일 13:05')).toBeInTheDocument();
  });

  it('주문 금액을 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('4,000원')).toBeInTheDocument();
    expect(screen.getByText('10,000원')).toBeInTheDocument();
  });

  it('pending 상태일 때 "주문 접수" 버튼을 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('주문 접수')).toBeInTheDocument();
  });

  it('preparing 상태일 때 "제조 완료" 버튼을 표시한다', () => {
    render(<OrdersSection orders={mockOrders} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('제조 완료')).toBeInTheDocument();
  });

  it('"주문 접수" 버튼 클릭 시 상태가 preparing으로 변경된다', async () => {
    const user = userEvent.setup();
    const handleUpdate = vi.fn();
    render(<OrdersSection orders={mockOrders} onUpdateStatus={handleUpdate} />);
    
    const acceptButton = screen.getByText('주문 접수');
    await user.click(acceptButton);
    
    expect(handleUpdate).toHaveBeenCalledWith(1, 'preparing');
  });

  it('"제조 완료" 버튼 클릭 시 상태가 ready로 변경된다', async () => {
    const user = userEvent.setup();
    const handleUpdate = vi.fn();
    render(<OrdersSection orders={mockOrders} onUpdateStatus={handleUpdate} />);
    
    const completeButton = screen.getByText('제조 완료');
    await user.click(completeButton);
    
    expect(handleUpdate).toHaveBeenCalledWith(2, 'ready');
  });

  it('주문이 없을 때 빈 상태 메시지를 표시한다', () => {
    render(<OrdersSection orders={[]} onUpdateStatus={vi.fn()} />);
    expect(screen.getByText('주문이 없습니다')).toBeInTheDocument();
  });
});


