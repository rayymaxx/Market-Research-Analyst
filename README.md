# Market Research AI

AI-powered market research platform using multi-agent systems with RAG-enhanced knowledge base integration.

## 🚀 Features

- **Multi-Agent Intelligence**: 4 specialized AI agents working together
- **RAG-Enhanced Analysis**: Leverages knowledge base for contextual insights
- **Real-time Progress**: Live tracking of research execution
- **Knowledge Management**: Upload and manage research documents
- **Comprehensive Reports**: Export-ready market analysis
- **Analytics Dashboard**: Insights and performance metrics

## 🏗 Architecture

### Backend (FastAPI)
- **API Layer**: RESTful endpoints with authentication
- **Multi-Agent System**: CrewAI with specialized research agents
- **RAG Pipeline**: ChromaDB + LangChain for knowledge retrieval
- **LLM Integration**: Gemini 2.0 with intelligent model routing

### Frontend (React + TypeScript)
- **Modern UI**: Dark theme with glass morphism design
- **Real-time Updates**: Progress polling and live status
- **State Management**: Zustand for efficient state handling
- **Responsive Design**: Mobile-first approach

## 🛠 Tech Stack

**Backend:**
- FastAPI + Uvicorn
- CrewAI (Multi-agent framework)
- LangChain + ChromaDB (RAG)
- Google Gemini 2.0 (LLM)

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS + Framer Motion
- Zustand (State management)
- React Query (API management)

## 📦 Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- Google Gemini API key

### Backend Setup
```bash
cd marketresearch
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Run the API server
cd api
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Quick Start

1. **Start Backend**: `cd marketresearch/api && python run.py`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Begin Research**: Click "Start Research" and enter your topic

## 📖 Usage Guide

See [USAGE_GUIDE.md](./USAGE_GUIDE.md) for detailed instructions.

## 🚢 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for production deployment.

## 📚 API Documentation

API documentation available at `http://localhost:8000/docs` when running the backend.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [Usage Guide](./USAGE_GUIDE.md)
- Review [API Documentation](http://localhost:8000/docs)
- Open an issue on GitHub