import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { InventorySection } from './InventorySection';
import { InventoryItem } from '../../types/admin';

describe('InventorySection', () => {
  const mockInventory: InventoryItem[] = [
    { id: 1, menuName: '아메리카노(ICE)', quantity: 10, minQuantity: 0, maxQuantity: 999 },
    { id: 2, menuName: '아메리카노(HOT)', quantity: 10, minQuantity: 0, maxQuantity: 999 },
    { id: 3, menuName: '카페라떼', quantity: 10, minQuantity: 0, maxQuantity: 999 },
  ];

  it('섹션 제목 "재고 현황"을 표시한다', () => {
    render(<InventorySection items={mockInventory} onUpdateQuantity={vi.fn()} />);
    expect(screen.getByText('재고 현황')).toBeInTheDocument();
  });

  it('3개의 메뉴를 표시한다', () => {
    render(<InventorySection items={mockInventory} onUpdateQuantity={vi.fn()} />);
    expect(screen.getByText('아메리카노(ICE)')).toBeInTheDocument();
    expect(screen.getByText('아메리카노(HOT)')).toBeInTheDocument();
    expect(screen.getByText('카페라떼')).toBeInTheDocument();
  });

  it('각 메뉴의 재고 개수를 표시한다', () => {
    render(<InventorySection items={mockInventory} onUpdateQuantity={vi.fn()} />);
    const quantities = screen.getAllByText(/10개/);
    expect(quantities).toHaveLength(3);
  });

  it('각 메뉴에 + 버튼과 - 버튼이 있다', () => {
    render(<InventorySection items={mockInventory} onUpdateQuantity={vi.fn()} />);
    const plusButtons = screen.getAllByText('+');
    const minusButtons = screen.getAllByText('-');
    expect(plusButtons).toHaveLength(3);
    expect(minusButtons).toHaveLength(3);
  });

  it('+ 버튼 클릭 시 onUpdateQuantity가 +1로 호출된다', async () => {
    const user = userEvent.setup();
    const handleUpdate = vi.fn();
    render(<InventorySection items={mockInventory} onUpdateQuantity={handleUpdate} />);
    
    const plusButtons = screen.getAllByText('+');
    await user.click(plusButtons[0]);
    
    expect(handleUpdate).toHaveBeenCalledWith(1, 1);
  });

  it('- 버튼 클릭 시 onUpdateQuantity가 -1로 호출된다', async () => {
    const user = userEvent.setup();
    const handleUpdate = vi.fn();
    render(<InventorySection items={mockInventory} onUpdateQuantity={handleUpdate} />);
    
    const minusButtons = screen.getAllByText('-');
    await user.click(minusButtons[0]);
    
    expect(handleUpdate).toHaveBeenCalledWith(1, -1);
  });

  it('재고가 5개 미만이면 "주의" 상태를 표시한다', () => {
    const lowStockInventory: InventoryItem[] = [
      { id: 1, menuName: '아메리카노(ICE)', quantity: 3, minQuantity: 0, maxQuantity: 999 },
    ];
    render(<InventorySection items={lowStockInventory} onUpdateQuantity={vi.fn()} />);
    expect(screen.getByText('주의')).toBeInTheDocument();
  });

  it('재고가 0개이면 "품절" 상태를 표시한다', () => {
    const outOfStockInventory: InventoryItem[] = [
      { id: 1, menuName: '아메리카노(ICE)', quantity: 0, minQuantity: 0, maxQuantity: 999 },
    ];
    render(<InventorySection items={outOfStockInventory} onUpdateQuantity={vi.fn()} />);
    expect(screen.getByText('품절')).toBeInTheDocument();
  });

  it('재고가 5개 이상이면 "정상" 상태를 표시한다', () => {
    const normalInventory: InventoryItem[] = [
      { id: 1, menuName: '아메리카노(ICE)', quantity: 10, minQuantity: 0, maxQuantity: 999 },
    ];
    render(<InventorySection items={normalInventory} onUpdateQuantity={vi.fn()} />);
    expect(screen.getByText('정상')).toBeInTheDocument();
  });
});

