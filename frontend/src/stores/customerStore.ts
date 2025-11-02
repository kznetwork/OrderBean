import { create } from 'zustand';
import { CartItem } from '../types/menu';

interface CustomerState {
  cartItems: CartItem[];
  addToCart: (item: CartItem) => void;
  removeFromCart: (itemId: string) => void;
  clearCart: () => void;
  getTotalAmount: () => number;
}

export const useCustomerStore = create<CustomerState>((set, get) => ({
  cartItems: [],
  
  addToCart: (item) => set((state) => {
    // 같은 메뉴와 같은 옵션을 가진 아이템이 있는지 확인
    const existingItemIndex = state.cartItems.findIndex(
      cartItem => 
        cartItem.menuId === item.menuId &&
        JSON.stringify(cartItem.selectedOptions.sort()) === JSON.stringify(item.selectedOptions.sort())
    );

    if (existingItemIndex !== -1) {
      // 기존 아이템이 있으면 수량과 총 가격만 증가
      const updatedItems = [...state.cartItems];
      updatedItems[existingItemIndex] = {
        ...updatedItems[existingItemIndex],
        quantity: updatedItems[existingItemIndex].quantity + 1,
        totalPrice: updatedItems[existingItemIndex].totalPrice + item.totalPrice,
      };
      return { cartItems: updatedItems };
    } else {
      // 새로운 아이템이면 추가
      return { cartItems: [...state.cartItems, item] };
    }
  }),
  
  removeFromCart: (itemId) => set((state) => ({
    cartItems: state.cartItems.filter(item => item.id !== itemId)
  })),
  
  clearCart: () => set({ cartItems: [] }),
  
  getTotalAmount: () => {
    const { cartItems } = get();
    return cartItems.reduce((total, item) => total + item.totalPrice, 0);
  },
}));

