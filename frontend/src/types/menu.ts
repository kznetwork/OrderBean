export interface MenuOption {
  id: string;
  label: string;
  price: number;
}

export interface MenuItem {
  id: number;
  name: string;
  price: number;
  description: string;
  imageUrl: string;
  category: string;
  options: MenuOption[];
}

export interface CartItem {
  id: string;
  menuId: number;
  menuName: string;
  basePrice: number;
  selectedOptions: string[];
  quantity: number;
  totalPrice: number;
}


