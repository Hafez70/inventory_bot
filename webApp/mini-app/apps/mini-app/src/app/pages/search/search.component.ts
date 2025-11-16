import { Component } from '@angular/core';
import { SearchContainerComponent } from '@search';

@Component({
  selector: 'app-search',
  imports: [SearchContainerComponent],
  template: `
    <div class="search-page h-full">
      <wh-search-container />
    </div>
  `,
  styles: `
    .search-page {
      background-color: #f9fafb;
    }
  `,
})
export class SearchComponent {}

