/**
 * 메뉴 API 서비스
 */
import apiClient from './api';

export interface MenuOption {
  id: number;
  menu_id: number;
  name: string;
  additional_price: number;
  created_at: string;
}

export interface Menu {
  id: number;
  name: string;
  description: string | null;
  price: number;
  image_url: string | null;
  stock: number;
  is_available: boolean;
  options: MenuOption[];
  created_at: string;
  updated_at: string;
}

export interface MenuListResponse {
  success: boolean;
  data: Menu[];
}

export interface MenuDetailResponse {
  success: boolean;
  data: Menu;
}

export interface MenuCreateData {
  name: string;
  description?: string;
  price: number;
  image_url?: string;
  stock: number;
  is_available: boolean;
  options?: Array<{
    name: string;
    additional_price: number;
  }>;
}

export interface MenuUpdateData {
  name?: string;
  description?: string;
  price?: number;
  image_url?: string;
  stock?: number;
  is_available?: boolean;
}

const menuService = {
  /**
   * 메뉴 목록 조회
   */
  async getMenus(availableOnly: boolean = true): Promise<Menu[]> {
    const response = await apiClient.get<MenuListResponse>(
      `/api/v1/menus?available_only=${availableOnly}`
    );
    return response.data.data;
  },

  /**
   * 메뉴 상세 조회
   */
  async getMenu(menuId: number): Promise<Menu> {
    const response = await apiClient.get<MenuDetailResponse>(
      `/api/v1/menus/${menuId}`
    );
    return response.data.data;
  },

  /**
   * 메뉴 생성 (관리자)
   */
  async createMenu(menuData: MenuCreateData): Promise<Menu> {
    const response = await apiClient.post<MenuDetailResponse>(
      '/api/v1/menus',
      menuData
    );
    return response.data.data;
  },

  /**
   * 메뉴 수정 (관리자)
   */
  async updateMenu(menuId: number, menuData: MenuUpdateData): Promise<Menu> {
    const response = await apiClient.put<MenuDetailResponse>(
      `/api/v1/menus/${menuId}`,
      menuData
    );
    return response.data.data;
  },

  /**
   * 메뉴 삭제 (관리자)
   */
  async deleteMenu(menuId: number): Promise<void> {
    await apiClient.delete(`/api/v1/menus/${menuId}`);
  },
};

export default menuService;

