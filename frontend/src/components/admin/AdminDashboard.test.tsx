import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AdminDashboard } from './AdminDashboard';
import { OrderStats } from '../../types/admin';

describe('AdminDashboard', () => {
  const mockStats: OrderStats = {
    totalOrders: 5,
    pendingOrders: 2,
    preparingOrders: 1,
    completedOrders: 2,
  };

  it('섹션 제목 "관리자 대시보드"를 표시한다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText('관리자 대시보드')).toBeInTheDocument();
  });

  it('총 주문 수를 표시한다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText(/총 주문/)).toBeInTheDocument();
    expect(screen.getByText(/5/)).toBeInTheDocument();
  });

  it('주문 접수 수를 표시한다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText(/주문 접수/)).toBeInTheDocument();
    expect(screen.getByText(/2/)).toBeInTheDocument();
  });

  it('제조 중 수를 표시한다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText(/제조 중/)).toBeInTheDocument();
    expect(screen.getByText(/1/)).toBeInTheDocument();
  });

  it('제조 완료 수를 표시한다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText(/제조 완료/)).toBeInTheDocument();
    expect(screen.getByText(/2/)).toBeInTheDocument();
  });

  it('통계가 형식에 맞게 표시된다', () => {
    render(<AdminDashboard stats={mockStats} />);
    expect(screen.getByText('총 주문 5 / 주문 접수 2 / 제조 중 1 / 제조 완료 2')).toBeInTheDocument();
  });
});


