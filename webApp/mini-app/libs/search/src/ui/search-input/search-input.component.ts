import { Component, input, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PLACEHOLDERS } from '../../domain/search.constants';

@Component({
  selector: 'wh-search-input',
  imports: [FormsModule],
  templateUrl: './search-input.component.html',
  styleUrl: './search-input.component.css',
})
export class SearchInputComponent {
  searchQuery = input<string>('');
  searchQueryChange = output<string>();
  search = output<void>();

  readonly placeholder = PLACEHOLDERS.SEARCH_INPUT;

  onInputChange(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.searchQueryChange.emit(value);
  }

  clearSearch(): void {
    this.searchQueryChange.emit('');
  }
}

