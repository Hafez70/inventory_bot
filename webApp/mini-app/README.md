# Warehousing Telegram Mini App

A mobile-first Angular 20 application built with NX workspace following clean architecture principles.

## 🏗️ Architecture

This project follows a **strict three-layer architecture**:

```
📦 Library Structure
├── ui/             # Components (.ts + .html + .css)
├── data-access/    # Services, Facades, Factories
└── domain/         # Models, Constants (no Angular deps)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed guidelines.

## ✨ Features

- 🎯 **Angular 20** with standalone components
- 🔥 **Signal-based** reactive state
- 🎨 **Tailwind CSS** styling
- 📱 **Mobile-first** design
- 🔄 **Bottom navigation**
- 🔍 **Item search**
- 🌐 **FastAPI integration**
- 🏗️ **NX Workspace** modular architecture

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 📂 Project Structure

```
webApp/mini-app/
├── apps/mini-app/           # Main application
├── libs/
│   ├── search/             # Search feature
│   │   ├── ui/            # Components
│   │   ├── data-access/   # Services
│   │   └── domain/        # Models
│   └── shared/
│       ├── ui-layout/     # Layout components
│       └── data-access/   # API services
├── ARCHITECTURE.md         # Architecture guide
└── DEPLOYMENT.md          # Deployment guide
```

## 📖 Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Architecture patterns and guidelines
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment instructions
- **[README.detailed.md](./README.detailed.md)** - Comprehensive documentation

## 🎯 Code Standards

- ✅ Separate `.html` and `.css` files (NO inline)
- ✅ Use `input()` / `output()` (NO `@Input` / `@Output`)
- ✅ Use `inject()` for DI
- ✅ NO `any` types
- ✅ OnPush change detection (default with signals)
- ✅ Follow ui/data-access/domain structure

## 🛠️ Common Commands

```bash
# Development
npm start                    # Start dev server
npm run build                # Build production
npm test                     # Run tests
npm run lint                 # Lint code

# NX Commands
nx serve mini-app            # Serve app
nx test search               # Test search library
nx graph                     # View dependency graph
```

## 📱 Pages

- **Home** (`/home`) - Welcome & dashboard
- **Search** (`/search`) - Item search

## 🔐 Authentication

Automatic Telegram Web App init data integration via HTTP interceptor.

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 📄 License

MIT
