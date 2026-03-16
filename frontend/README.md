# MedSeg AI Platform - Frontend

React-based web interface for medical image segmentation platform.

## Setup (Week 2+)

```bash
cd frontend
npm install
npm run dev
```

## Technology Stack

- **Framework**: React 18 / Vite
- **UI Library**: TailwindCSS
- **API Client**: Axios
- **State Management**: Redux/Context API
- **Authentication**: JWT (from backend)

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── components/      # Reusable React components
│   ├── pages/           # Page components (routes)
│   ├── services/        # API calls to backend
│   ├── hooks/           # Custom React hooks
│   ├── context/         # Context providers
│   ├── utils/           # Helper functions
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── .env.example         # Environment template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
└── tailwind.config.js   # TailwindCSS config
```

## Development

Will connect to backend API at: `http://localhost:8000/api/v1`

## Status

🚧 **Not started** - Week 2 development

See [README.md](../README.md) for full project documentation.
