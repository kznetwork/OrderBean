import { MenuItem } from '../types/menu';

export const menuData: MenuItem[] = [
  {
    id: 1,
    name: '아메리카노(ICE)',
    price: 4000,
    description: '간단한 설명...',
    imageUrl: '/images/americano-ice.jpg',
    category: '커피',
    options: [
      { id: 'shot', label: '샷 추가', price: 500 },
      { id: 'syrup', label: '시럽 추가', price: 0 },
    ],
  },
  {
    id: 2,
    name: '아메리카노(HOT)',
    price: 4000,
    description: '간단한 설명...',
    imageUrl: '/images/americano-hot.jpg',
    category: '커피',
    options: [
      { id: 'shot', label: '샷 추가', price: 500 },
      { id: 'syrup', label: '시럽 추가', price: 0 },
    ],
  },
  {
    id: 3,
    name: '카페라떼',
    price: 5000,
    description: '간단한 설명...',
    imageUrl: '/images/latte.jpg',
    category: '커피',
    options: [
      { id: 'shot', label: '샷 추가', price: 500 },
      { id: 'syrup', label: '샷 추가', price: 0 },
    ],
  },
];

