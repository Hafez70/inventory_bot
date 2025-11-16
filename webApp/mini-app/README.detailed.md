# 📱 Warehousing Telegram Mini App

A mobile-first Angular 20 application built with NX workspace for the Telegram bot warehouse management system.

## ✨ Features

- 🎯 **Angular 20** with standalone components
- 🔥 **Signal-based** reactive state management
- 🎨 **Tailwind CSS** for styling
- 📱 **Mobile-first** responsive design
- 🔄 **Bottom navigation** for easy mobile access
- 🔍 **Item search** functionality
- 🌐 **FastAPI integration**
- 🏗️ **NX Workspace** with modular architecture
- 📦 **Reusable libraries** for scalability

---

## 🏗️ Architecture

This project follows **NX best practices** with a clear separation of concerns:

```
webApp/mini-app/
├── apps/
│   └── mini-app/           # Main application
│       ├── src/
│       │   ├── app/        # App root & routing
│       │   ├── pages/      # Feature pages
│       │   └── environments/
│       └── project.json
│
├── libs/
│   ├── shared/
│   │   ├── ui-layout/      # Layout components (Bottom Nav, etc.)
│   │   └── data-access/    # API services & models
│   └── search/             # Search feature library
│
├── nx.json                 # NX workspace config
├── package.json           # Dependencies
└── tailwind.config.js     # Tailwind CSS config
```

### Library Types

- **`type:app`** - Application projects
- **`type:feature`** - Feature modules (e.g., search)
- **`type:ui`** - Reusable UI components (e.g., layout)
- **`type:data-access`** - API services and data models
- **`scope:shared`** - Shared across multiple apps/features

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- NX CLI (optional): `npm install -g nx`

### Installation

```bash
cd webApp/mini-app
npm install
```

### Development Server

```bash
npm start
```

Navigate to `http://localhost:4200/`

---

## 📦 Build

```bash
# Development build
npm run build

# Production build
nx build mini-app --configuration=production
```

Output: `dist/apps/mini-app/`

---

## 🧪 Testing

```bash
# Run all tests
npm test

# Test specific library
nx test shared-ui-layout

# Test with coverage
nx test mini-app --coverage
```

---

## 🎨 Key Features

### 1. Mobile-First Layout

- Responsive design optimized for mobile devices
- Safe area insets for notched devices
- Bottom navigation bar for easy thumb access

### 2. Search Functionality

- Real-time search with debouncing
- Searches across: name, custom code, description
- Empty states and loading indicators
- Item cards with images and stock info

### 3. Signal-Based State Management

All components use Angular Signals for reactive state:

```typescript
searchQuery = signal('');
searchResults = signal<Item[]>([]);
isLoading = signal(false);
```

### 4. API Integration

Integrated with FastAPI backend via `ItemsService`:

```typescript
this.itemsService.searchItems(query).subscribe({
  next: (results) => this.searchResults.set(results),
  error: (error) => console.error(error),
});
```

### 5. Telegram Web App SDK

- Automatic init data passing for authentication
- Theme variables integration
- Safe area insets support

---

## 📚 Libraries

### `@warehousing/shared/ui-layout`

Layout components:
- `LayoutComponent` - Main app layout wrapper
- `BottomNavComponent` - Bottom navigation bar

### `@warehousing/search`

Search feature:
- `SearchContainerComponent` - Smart container
- `SearchInputComponent` - Search input with clear button
- `SearchResultsComponent` - Results list with empty states
- `ItemCardComponent` - Item display card

### `@warehousing/shared/data-access`

API integration:
- `ApiService` - Base HTTP service
- `ItemsService` - Items API endpoints
- `apiInterceptor` - Telegram init data interceptor
- Models: `Item`, `SearchItemsResponse`

---

## 🔧 Configuration

### API Endpoint

Edit `libs/shared/data-access/src/lib/config/api.config.ts`:

```typescript
export const DEFAULT_API_CONFIG: ApiConfig = {
  baseUrl: '/api',  // Change for different environments
};
```

Or use environment files (see `DEPLOYMENT.md`).

### Tailwind Theme

Edit `tailwind.config.js` to customize colors and spacing.

### Routes

Edit `apps/mini-app/src/app/app.routes.ts` to add new routes.

---

## 📱 Pages

### Home (`/home`)
- Welcome screen
- Dashboard placeholder (future feature)
- Quick stats

### Search (`/search`)
- Item search functionality
- Real-time results
- Item cards with details

---

## 🎯 OnPush Change Detection

All components use `ChangeDetectionStrategy.OnPush` (implied with signals).

---

## 🔐 Authentication

The app uses Telegram Web App init data for authentication:

1. Init data is automatically captured from `window.Telegram.WebApp`
2. Passed in HTTP headers via `apiInterceptor`
3. Validated on the backend (FastAPI)

---

## 📖 Commands Reference

```bash
# Development
npm start              # Start dev server
npm run build          # Build for production
npm test               # Run tests
npm run lint           # Lint code

# NX Commands
nx serve mini-app                    # Serve app
nx build mini-app                    # Build app
nx test mini-app                     # Test app
nx lint mini-app                     # Lint app
nx graph                             # Visualize dependencies

# Library Commands
nx build search                      # Build search library
nx test shared-ui-layout             # Test layout library
nx lint shared-data-access           # Lint data-access library
```

---

## 🌍 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions:

- Deploy to cPanel
- Configure Telegram Bot
- Set up environments
- Troubleshooting

---

## 🛣️ Roadmap

- [ ] Item details page
- [ ] Low stock notifications
- [ ] Inventory management
- [ ] Brand and category filters
- [ ] Image upload
- [ ] Offline support (PWA)
- [ ] Dashboard with analytics

---

## 📝 Code Style

- **TypeScript** strict mode enabled
- **ESLint** for linting
- **Prettier** (optional) for formatting
- **OnPush** change detection strategy
- **Signal-based** state management
- **No** `@Input`/`@Output` - use `input()`/`output()`
- **No** `any` type allowed

---

## 🤝 Contributing

1. Follow the NX architecture guidelines
2. Use signals for reactive state
3. Create reusable libraries for shared functionality
4. Write tests for new features
5. Follow the existing code style

---

## 📄 License

MIT

---

## 🔗 Related Projects

- **Bot**: `../bot/` - Telegram bot implementation
- **API**: `../api/` - FastAPI backend
- **Database**: `../database/` - SQLite database

---

## 💡 Tips

### Adding a New Feature Library

```bash
nx g @nx/angular:library my-feature --directory=libs/my-feature --tags=type:feature
```

### Adding a New UI Component

```bash
nx g @nx/angular:component my-component --project=shared-ui-layout --export
```

### Visualizing Dependencies

```bash
nx graph
```

This opens an interactive graph showing all project dependencies.

---

## 🐛 Known Issues

- None at the moment

---

## 📞 Support

For issues and questions, please open an issue on GitHub.

