# Whey Protein Ranking Frontend

A modern, beautiful React TypeScript frontend for ranking and comparing whey protein supplements.

## Features

- 🥛 **Product Catalog**: View all whey protein products with detailed information
- 💰 **EAA/Price Ranking**: Compare products by Essential Amino Acids per price ratio
- 💪 **Protein Concentration Ranking**: Compare products by protein concentration percentage
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast & Modern**: Built with Vite, React 19, and TypeScript
- 🎨 **Beautiful UI**: Styled with Tailwind CSS

## Architecture

This project follows SOLID principles:

- **Single Responsibility**: Each component has one clear purpose
- **Open/Closed**: Components are extensible without modification
- **Liskov Substitution**: Proper interface contracts
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Services are injected as dependencies

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Card.tsx        # Generic card component
│   ├── Dashboard.tsx   # Main dashboard orchestrator
│   ├── LoadingSpinner.tsx
│   ├── RankingCard.tsx
│   ├── TabNavigation.tsx
│   └── WheyProteinCard.tsx
├── hooks/              # Custom React hooks
│   └── useWheyProtein.ts
├── services/           # API services and repositories
│   └── whey-protein.service.ts
├── types/              # TypeScript type definitions
│   └── whey-protein.ts
├── utils/              # Utility functions
│   └── formatters.ts
├── App.tsx
├── main.tsx
└── index.css
```

## Setup

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Start the development server:
```bash
npm run dev
```

3. Make sure your backend API is running on `http://localhost:8000`

## API Integration

The frontend connects to the FastAPI backend with the following endpoints:

- `GET /whey-proteins/` - Get all products
- `GET /whey-proteins/{id}` - Get specific product
- `POST /whey-proteins/` - Create new product
- `PUT /whey-proteins/{id}` - Update product
- `DELETE /whey-proteins/{id}` - Delete product
- `GET /whey-proteins/rankings/eea-price` - Get EAA/price ranking
- `GET /whey-proteins/rankings/protein-concentration` - Get protein concentration ranking

## Technologies Used

- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Fetch API** - HTTP client

## Contributing

1. Follow the existing code structure and SOLID principles
2. Add proper TypeScript types for new features
3. Ensure components are reusable and focused
4. Test your changes thoroughly