from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ResearchStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStatus(str, Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchRequest(BaseModel):
    research_topic: str = Field(..., description="The main topic to research")
    research_request: str = Field(..., description="Detailed research request")
    user_id: Optional[str] = Field(default="default", description="User identifier")

class TaskProgress(BaseModel):
    task_name: str
    status: TaskStatus
    agent: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    tools_used: List[str] = []
    output: Optional[str] = None

class ResearchProgress(BaseModel):
    current_phase: str
    completed_tasks: List[str] = []
    active_task: Optional[str] = None
    tasks: List[TaskProgress] = []
    progress_percentage: int = 0

class ResearchResponse(BaseModel):
    research_id: str
    status: ResearchStatus
    result: Optional[str] = None
    progress: Optional[ResearchProgress] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

class KnowledgeStats(BaseModel):
    total_documents: int
    company_profiles: int
    industry_reports: int
    market_data: int
    user_preferences: int
    last_updated: datetime = Field(default_factory=datetime.now)

class UploadResponse(BaseModel):
    message: str
    file_path: str
    size: int
    processed: bool = False

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class ResearchHistoryItem(BaseModel):
    research_id: str
    research_topic: str
    status: ResearchStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

class ResearchHistory(BaseModel):
    history: List[ResearchHistoryItem]
    total: int
    limit: int
    offset: int = 0

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    crew_initialized: bool
    rag_initialized: bool
    knowledge_stats: Optional[KnowledgeStats] = None