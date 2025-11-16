import { Component, signal, effect, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SearchInputComponent } from '../search-input/search-input.component';
import { SearchResultsComponent } from '../search-results/search-results.component';
import { SearchService } from '../../data-access/search.service';
import { Item } from '../../domain/search.model';
import { SEARCH_CONFIG } from '../../domain/search.constants';

@Component({
  selector: 'wh-search-container',
  imports: [FormsModule, SearchInputComponent, SearchResultsComponent],
  templateUrl: './search-container.component.html',
  styleUrl: './search-container.component.css',
})
export class SearchContainerComponent {
  private searchService = inject(SearchService);

  searchQuery = signal('');
  searchResults = signal<Item[]>([]);
  isLoading = signal(false);
  hasSearched = signal(false);

  private searchTimeout: ReturnType<typeof setTimeout> | null = null;

  constructor() {
    // Auto-search when query changes (debounced)
    effect(() => {
      const query = this.searchQuery();
      if (query.trim().length >= SEARCH_CONFIG.MIN_QUERY_LENGTH) {
        this.debounceSearch();
      } else if (query.trim().length === 0) {
        this.searchResults.set([]);
        this.hasSearched.set(false);
      }
    });
  }

  onSearchQueryChange(query: string): void {
    this.searchQuery.set(query);
  }

  debounceSearch(): void {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }
    this.searchTimeout = setTimeout(() => {
      this.handleSearch();
    }, SEARCH_CONFIG.DEBOUNCE_TIME);
  }

  handleSearch(): void {
    const query = this.searchQuery().trim();
    
    if (!query || query.length < SEARCH_CONFIG.MIN_QUERY_LENGTH) {
      return;
    }

    this.isLoading.set(true);
    this.hasSearched.set(true);

    this.searchService.searchItems(query).subscribe({
      next: (results) => {
        this.searchResults.set(results);
        this.isLoading.set(false);
      },
      error: (error) => {
        console.error('Search error:', error);
        this.searchResults.set([]);
        this.isLoading.set(false);
      },
    });
  }
}

