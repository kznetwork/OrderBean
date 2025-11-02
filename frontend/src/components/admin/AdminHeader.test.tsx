import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AdminHeader } from './AdminHeader';

describe('AdminHeader', () => {
  it('브랜드명 "OrderBean – 커피 주문"을 표시한다', () => {
    render(<AdminHeader activeTab="admin" onTabChange={vi.fn()} />);
    expect(screen.getByText('OrderBean – 커피 주문')).toBeInTheDocument();
  });

  it('주문하기 탭과 관리자 탭을 표시한다', () => {
    render(<AdminHeader activeTab="admin" onTabChange={vi.fn()} />);
    expect(screen.getByText('주문하기')).toBeInTheDocument();
    expect(screen.getByText('관리자')).toBeInTheDocument();
  });

  it('활성 탭이 시각적으로 구분된다', () => {
    render(<AdminHeader activeTab="admin" onTabChange={vi.fn()} />);
    const adminTab = screen.getByText('관리자');
    expect(adminTab.className).toContain('active');
  });

  it('탭 클릭 시 onTabChange 콜백이 호출된다', async () => {
    const user = userEvent.setup();
    const handleTabChange = vi.fn();
    render(<AdminHeader activeTab="admin" onTabChange={handleTabChange} />);
    
    const orderTab = screen.getByText('주문하기');
    await user.click(orderTab);
    
    expect(handleTabChange).toHaveBeenCalledWith('order');
  });
});

