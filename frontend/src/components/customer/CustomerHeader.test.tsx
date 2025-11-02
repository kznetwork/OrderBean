import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CustomerHeader } from './CustomerHeader';

describe('CustomerHeader', () => {
  it('브랜드명 "COZY"가 표시되어야 한다', () => {
    render(<CustomerHeader activeTab="order" onTabChange={() => {}} />);
    expect(screen.getByText('COZY')).toBeInTheDocument();
  });

  it('"주문하기" 탭이 표시되어야 한다', () => {
    render(<CustomerHeader activeTab="order" onTabChange={() => {}} />);
    expect(screen.getByText('주문하기')).toBeInTheDocument();
  });

  it('"관리자" 탭이 표시되어야 한다', () => {
    render(<CustomerHeader activeTab="order" onTabChange={() => {}} />);
    expect(screen.getByText('관리자')).toBeInTheDocument();
  });

  it('activeTab이 "order"일 때 주문하기 탭이 활성화되어야 한다', () => {
    render(<CustomerHeader activeTab="order" onTabChange={() => {}} />);
    const orderTab = screen.getByText('주문하기').closest('button');
    expect(orderTab).toHaveClass('active');
  });

  it('탭 클릭 시 onTabChange가 호출되어야 한다', () => {
    const onTabChange = vi.fn();
    render(<CustomerHeader activeTab="order" onTabChange={onTabChange} />);
    
    const adminTab = screen.getByText('관리자');
    adminTab.click();
    
    expect(onTabChange).toHaveBeenCalledWith('admin');
  });
});

