# SelamAI - Dashboard Landing Page

A modern, minimal, and professional Dashboard Landing Page for SelamAI - an AI platform wrapper with OpenAI-inspired aesthetics.

## Features

- **Modern Design**: Clean, professional aesthetic inspired by OpenAI, ChatGPT, Notion, and Linear
- **Fully Responsive**: Mobile-first design that works beautifully across all screen sizes
- **Interactive Components**: Smooth animations powered by Framer Motion
- **shadcn/ui**: Built with high-quality, accessible UI components
- **TypeScript**: Type-safe development with Next.js 16 and React

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **Icons**: Lucide React

## Sections

1. **Header**: Sticky navigation with smooth scroll effects and mobile menu
2. **Hero Section**: Eye-catching headline with gradient backgrounds and interactive preview cards
3. **Dashboard Preview**: Showcase of API usage metrics, credits, and available AI models
4. **Feature Highlights**: Key product features with hover effects and animations
5. **API Playground Preview**: Code editor simulation with multi-language support
6. **Documentation**: Resources and guides section
7. **Pricing**: Clear pricing tiers with comparison
8. **Early Access**: Call-to-action for sign-up
9. **Footer**: Comprehensive links and social media integration

## Getting Started

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the landing page.

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main landing page
│   └── globals.css         # Global styles and theme
├── components/
│   ├── landing/            # Landing page sections
│   │   ├── header.tsx
│   │   ├── hero.tsx
│   │   ├── dashboard-preview.tsx
│   │   ├── feature-highlights.tsx
│   │   ├── playground-preview.tsx
│   │   ├── documentation.tsx
│   │   ├── pricing.tsx
│   │   ├── early-access.tsx
│   │   └── footer.tsx
│   └── ui/                 # shadcn/ui components
└── lib/
    └── utils.ts            # Utility functions
```

## Design System

- **Color Palette**: Neutral grays with blue and purple accents
- **Typography**: Clean, modern fonts (Geist Sans)
- **Spacing**: Consistent spacing scale
- **Shadows**: Subtle elevation with soft shadows
- **Radius**: Rounded corners for a modern feel
- **Animations**: Smooth transitions and micro-interactions

## Accessibility

- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- Focus indicators
- Screen reader friendly

## License

MIT
