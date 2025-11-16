import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService } from '@shared';
import { Item, SearchItemsResponse, ItemDetailsResponse } from '../domain/search.model';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  private apiService = inject(ApiService);

  /**
   * Search items by query string
   * Searches in: name, custom_code, description
   */
  searchItems(query: string): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>(`/items/search?q=${encodeURIComponent(query)}`)
      .pipe(map((response) => response.items));
  }

  /**
   * Get item by ID
   */
  getItemById(id: number): Observable<Item> {
    return this.apiService
      .get<ItemDetailsResponse>(`/items/${id}`)
      .pipe(map((response) => response.item));
  }

  /**
   * Get all items
   */
  getAllItems(): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>('/items')
      .pipe(map((response) => response.items));
  }

  /**
   * Get items by brand
   */
  getItemsByBrand(brandId: number): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>(`/items/brand/${brandId}`)
      .pipe(map((response) => response.items));
  }

  /**
   * Get items by category
   */
  getItemsByCategory(categoryId: number): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>(`/items/category/${categoryId}`)
      .pipe(map((response) => response.items));
  }

  /**
   * Get items by subcategory
   */
  getItemsBySubcategory(subcategoryId: number): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>(`/items/subcategory/${subcategoryId}`)
      .pipe(map((response) => response.items));
  }

  /**
   * Get low stock items
   */
  getLowStockItems(): Observable<Item[]> {
    return this.apiService
      .get<SearchItemsResponse>('/items/low-stock')
      .pipe(map((response) => response.items));
  }
}

