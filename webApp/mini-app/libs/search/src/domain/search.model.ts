export interface Item {
  id: number;
  name: string;
  custom_code?: string;
  description?: string;
  image_path?: string;
  video_url?: string;
  brand_id?: number;
  brand_name?: string;
  category_id?: number;
  category_name?: string;
  subcategory_id?: number;
  subcategory_name?: string;
  measure_type_id?: number;
  measure_type_name?: string;
  available_count?: number;
  low_stock_threshold?: number;
  created_at?: string;
  updated_at?: string;
}

export interface SearchItemsResponse {
  items: Item[];
  total: number;
}

export interface ItemDetailsResponse {
  item: Item;
}

