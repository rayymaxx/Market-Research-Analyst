from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from routes.research import router as research_router
from routes.knowledge import router as knowledge_router
from models import HealthCheck
from services.research_service import ResearchService
from services.knowledge_service import KnowledgeService
from datetime import datetime

app = FastAPI(
    title="Market Research AI API",
    description="AI-powered market research with RAG-enhanced multi-agent system",
    version="1.0.0"
)

# CORS middleware for frontend
import os
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

# Add production frontend URL if provided
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research_router)
app.include_router(knowledge_router)

@app.on_event("startup")
async def startup_event():
    """Initialize the research system on startup"""
    try:
        # Initialize services
        # ResearchService.get_crew()
        # KnowledgeService.get_rag_factory()
        print("✅ API Server initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize API server: {e}")
        raise

@app.get("/", response_model=dict)
async def root():
    return {"message": "Market Research AI API", "status": "running"}

@app.get("/health", response_model=HealthCheck)
async def health_check():
    try:
        knowledge_stats = KnowledgeService.get_stats()
        return HealthCheck(
            status="healthy",
            timestamp=datetime.now(),
            crew_initialized=ResearchService._crew_instance is not None,
            rag_initialized=KnowledgeService._rag_factory is not None,
            knowledge_stats=knowledge_stats
        )
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.now(),
            crew_initialized=False,
            rag_initialized=False
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


