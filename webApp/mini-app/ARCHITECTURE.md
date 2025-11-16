# 🏗️ Angular App Architecture Guide

This document describes the architectural patterns and folder structure used in this Angular application.

## 📐 Core Principles

### 1. **Three-Layer Architecture**

Every library follows a strict three-layer separation:

```
libs/feature-name/
├── ui/                    # UI Components
├── data-access/          # Services, Facades, Factories
└── domain/               # Models, Constants, Interfaces
```

### 2. **Component Structure**

All components MUST have **separate files** for:
- **TypeScript** (`.ts`) - Component logic
- **HTML** (`.html`) - Template
- **CSS** (`.css`) - Styles

❌ **NO inline templates or styles**

---

## 📂 Folder Structure

### Complete Library Structure

```
libs/
├── search/                           # Feature library
│   ├── ui/                          # UI Layer
│   │   ├── search-container/
│   │   │   ├── search-container.component.ts
│   │   │   ├── search-container.component.html
│   │   │   └── search-container.component.css
│   │   ├── search-input/
│   │   │   ├── search-input.component.ts
│   │   │   ├── search-input.component.html
│   │   │   └── search-input.component.css
│   │   └── ...
│   │
│   ├── data-access/                 # Data Access Layer
│   │   ├── search.service.ts       # API calls
│   │   ├── search.facade.ts        # (optional) State management
│   │   └── search.factory.ts       # (optional) Factory functions
│   │
│   ├── domain/                      # Domain Layer
│   │   ├── search.model.ts         # Interfaces & Types
│   │   └── search.constants.ts     # Constants & Enums
│   │
│   └── src/
│       └── index.ts                 # Public API (barrel export)
│
└── shared/
    ├── ui-layout/                   # Shared UI library
    │   ├── ui/
    │   │   ├── layout/
    │   │   └── bottom-nav/
    │   └── domain/
    │       ├── navigation.model.ts
    │       └── navigation.constants.ts
    │
    └── data-access/                 # Shared data access
        ├── data-access/
        │   ├── api.service.ts
        │   └── api.interceptor.ts
        └── domain/
            ├── api.model.ts
            └── api.config.ts
```

---

## 🎯 Layer Responsibilities

### **1. UI Layer** (`ui/`)

**Purpose**: Presentational components only

**Contains**:
- Components (`.ts`, `.html`, `.css`)
- No business logic
- No direct API calls
- Receives data via `input()`
- Emits events via `output()`

**Example**:
```typescript
// ui/search-input/search-input.component.ts
@Component({
  selector: 'wh-search-input',
  imports: [FormsModule],
  templateUrl: './search-input.component.html',
  styleUrl: './search-input.component.css',
})
export class SearchInputComponent {
  searchQuery = input<string>('');
  searchQueryChange = output<string>();
  
  onInputChange(value: string): void {
    this.searchQueryChange.emit(value);
  }
}
```

---

### **2. Data Access Layer** (`data-access/`)

**Purpose**: Handle all data operations

**Contains**:
- **Services** - API calls, HTTP requests
- **Facades** - Complex state management
- **Factories** - Object creation logic
- **Interceptors** - HTTP interceptors

**Example**:
```typescript
// data-access/search.service.ts
@Injectable({ providedIn: 'root' })
export class SearchService {
  private apiService = inject(ApiService);

  searchItems(query: string): Observable<Item[]> {
    return this.apiService.get<SearchResponse>(`/items/search?q=${query}`)
      .pipe(map(response => response.items));
  }
}
```

---

### **3. Domain Layer** (`domain/`)

**Purpose**: Pure business logic and types

**Contains**:
- **Models** - Interfaces, Types
- **Constants** - Configuration, Enums
- **Validators** - (optional) Pure validation functions
- **NO Angular dependencies**

**Example**:
```typescript
// domain/search.model.ts
export interface Item {
  id: number;
  name: string;
  custom_code?: string;
}

// domain/search.constants.ts
export const SEARCH_CONFIG = {
  MIN_QUERY_LENGTH: 2,
  DEBOUNCE_TIME: 500,
} as const;
```

---

## 📋 Naming Conventions

### Components
```
search-input.component.ts
search-input.component.html
search-input.component.css
```

### Services
```
search.service.ts
api.service.ts
items.facade.ts
```

### Models & Constants
```
search.model.ts
search.constants.ts
api.config.ts
```

---

## 🔗 Dependency Rules

### Allowed Dependencies

```
UI Layer
  ↓
  Can depend on: Domain Layer only
  ❌ Cannot depend on: Data Access Layer

Data Access Layer
  ↓
  Can depend on: Domain Layer only
  ❌ Cannot depend on: UI Layer

Domain Layer
  ↓
  ❌ No dependencies on other layers
  ❌ No Angular-specific code
```

---

## 📦 Library Types & Tags

### Feature Libraries
```json
{
  "tags": ["type:feature", "scope:search"]
}
```
Examples: `search`, `inventory`, `reports`

### UI Libraries
```json
{
  "tags": ["type:ui", "scope:shared"]
}
```
Examples: `ui-layout`, `ui-components`

### Data Access Libraries
```json
{
  "tags": ["type:data-access", "scope:shared"]
}
```
Examples: `data-access`, `api-client`

---

## ✅ Best Practices

### Components

```typescript
// ✅ GOOD - Separate files
@Component({
  selector: 'wh-item-card',
  imports: [],
  templateUrl: './item-card.component.html',  // ✅ External template
  styleUrl: './item-card.component.css',       // ✅ External styles
})
export class ItemCardComponent {
  item = input.required<Item>();               // ✅ Use input()
  itemClick = output<Item>();                  // ✅ Use output()
  
  // ✅ No business logic, only presentation
}
```

```typescript
// ❌ BAD - Inline template
@Component({
  selector: 'wh-item-card',
  template: `<div>...</div>`,                  // ❌ Inline template
  styles: [`.card { ... }`],                   // ❌ Inline styles
})
export class ItemCardComponent {
  @Input() item!: Item;                        // ❌ Use input() instead
  @Output() itemClick = new EventEmitter();    // ❌ Use output() instead
}
```

### Services

```typescript
// ✅ GOOD - Injectable service
@Injectable({ providedIn: 'root' })
export class SearchService {
  private apiService = inject(ApiService);    // ✅ Use inject()
  
  searchItems(query: string): Observable<Item[]> {
    return this.apiService.get(`/search?q=${query}`);
  }
}
```

### Models

```typescript
// ✅ GOOD - Pure interfaces
export interface Item {
  id: number;
  name: string;
}

export const CONFIG = {
  MAX_ITEMS: 100
} as const;
```

```typescript
// ❌ BAD - Angular dependencies in domain
import { Injectable } from '@angular/core';  // ❌ No Angular in domain

export interface Item { ... }
```

---

## 🎨 Component Patterns

### Smart Component (Container)
```typescript
// ui/search-container/search-container.component.ts
export class SearchContainerComponent {
  private searchService = inject(SearchService);  // ✅ Injects service
  
  results = signal<Item[]>([]);
  
  search(query: string): void {
    this.searchService.searchItems(query).subscribe(
      results => this.results.set(results)
    );
  }
}
```

### Dumb Component (Presentational)
```typescript
// ui/item-card/item-card.component.ts
export class ItemCardComponent {
  item = input.required<Item>();          // ✅ Only receives data
  itemClick = output<Item>();             // ✅ Only emits events
  
  // ✅ No services, no API calls
  // ✅ Pure presentation logic only
}
```

---

## 📖 Export Pattern (index.ts)

```typescript
// libs/search/src/index.ts
// UI
export * from './ui/search-container/search-container.component';
export * from './ui/search-input/search-input.component';

// Data Access
export * from './data-access/search.service';

// Domain
export * from './domain/search.model';
export * from './domain/search.constants';
```

---

## 🚀 Usage Examples

### Importing from Libraries

```typescript
// ✅ GOOD - Import from barrel
import { SearchContainerComponent, SearchService } from '@warehousing/search';

// ❌ BAD - Deep imports
import { SearchContainerComponent } from '@warehousing/search/src/ui/search-container';
```

### Creating New Feature

```bash
# 1. Generate library
nx g @nx/angular:library my-feature --directory=libs/my-feature

# 2. Create folder structure
libs/my-feature/
├── ui/
├── data-access/
└── domain/
```

---

## 📊 Dependency Graph

```
┌─────────────────┐
│   Apps (mini-app)  │
└────────┬────────┘
         │
    ┌────▼──────────────────┐
    │   Feature Libraries   │
    │   (search, ...)      │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │   Shared/UI Libraries │
    │   (ui-layout, ...)   │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │   Data Access         │
    │   (api.service, ...)  │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │   Domain              │
    │   (models, constants) │
    └───────────────────────┘
```

---

## ✨ Summary

| Layer | Contains | Dependencies | Angular? |
|-------|----------|--------------|----------|
| **UI** | Components (`.ts`, `.html`, `.css`) | Domain only | ✅ Yes |
| **Data Access** | Services, Facades, Factories | Domain only | ✅ Yes |
| **Domain** | Models, Constants | None | ❌ No |

---

## 🔍 Checklist

Before creating a component, ask:

- [ ] Is template in separate `.html` file?
- [ ] Is style in separate `.css` file?
- [ ] Using `input()` and `output()` instead of decorators?
- [ ] Using `inject()` for dependencies?
- [ ] No `any` types?
- [ ] Following ui/data-access/domain structure?
- [ ] Exported in `index.ts`?

---

For more information, see:
- [NX Documentation](https://nx.dev/angular)
- [Angular Style Guide](https://angular.io/guide/styleguide)

