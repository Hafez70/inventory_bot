import { Component, input } from '@angular/core';
import { ItemCardComponent } from '../item-card/item-card.component';
import { Item } from '../../domain/search.model';
import { EMPTY_STATES } from '../../domain/search.constants';

@Component({
  selector: 'wh-search-results',
  imports: [ItemCardComponent],
  templateUrl: './search-results.component.html',
  styleUrl: './search-results.component.css',
})
export class SearchResultsComponent {
  items = input<Item[]>([]);
  hasSearched = input<boolean>(false);

  readonly emptyStates = EMPTY_STATES;
}

