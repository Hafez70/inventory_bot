import { Component, input } from '@angular/core';
import { Item } from '../../domain/search.model';

@Component({
  selector: 'wh-item-card',
  imports: [],
  templateUrl: './item-card.component.html',
  styleUrl: './item-card.component.css',
})
export class ItemCardComponent {
  item = input.required<Item>();

  getImageUrl(): string {
    const imagePath = this.item().image_path;
    if (!imagePath) return '';
    
    // Assuming API serves images from /images/ endpoint
    return `/api/images/${imagePath}`;
  }

  isLowStock(): boolean {
    const available = this.item().available_count || 0;
    const threshold = this.item().low_stock_threshold || 0;
    return available > 0 && available <= threshold;
  }

  handleClick(): void {
    // TODO: Navigate to item details
    console.log('Item clicked:', this.item());
  }
}

