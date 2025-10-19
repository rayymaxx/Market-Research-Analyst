from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List
import asyncio
from datetime import datetime
import uuid
import sys 
import os 

from models import (
    ResearchRequest, 
    ResearchResponse, 
    ResearchProgress, 
    TaskProgress,
    ResearchStatus,
    TaskStatus,
    ResearchHistory,
    UserProfile
)
from auth import get_current_user, verify_simple_token
from services.research_service import ResearchService

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

router = APIRouter(prefix="/research", tags=["research"])

# Use simple auth for development
get_user = verify_simple_token

@router.post("/start", response_model=ResearchResponse)
async def start_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
    user: UserProfile = Depends(get_user)
):
    """Start a new market research task"""
    try:
        research_id = str(uuid.uuid4())
        
        # Initialize research response
        response = ResearchResponse(
            research_id=research_id,
            status=ResearchStatus.PENDING,
            progress=ResearchProgress(
                current_phase="initializing",
                progress_percentage=0,
                tasks=[
                    TaskProgress(
                        task_name="comprehensive_data_collection_task",
                        status=TaskStatus.WAITING,
                        agent="Digital Intelligence Gatherer"
                    ),
                    TaskProgress(
                        task_name="comprehensive_analysis_task", 
                        status=TaskStatus.WAITING,
                        agent="Quantitative Insights Specialist"
                    ),
                    TaskProgress(
                        task_name="final_comprehensive_report_task",
                        status=TaskStatus.WAITING,
                        agent="Strategic Communications Expert"
                    )
                ]
            )
        )
        
        # Store initial response
        ResearchService.store_research(research_id, response)
        
        # Start research in background
        background_tasks.add_task(
            ResearchService.execute_research,
            research_id,
            request,
            user.user_id
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start research: {str(e)}")

@router.get("/{research_id}/status", response_model=ResearchResponse)
async def get_research_status(
    research_id: str,
    user: UserProfile = Depends(get_user)
):
    """Get the status of a research task"""
    research = ResearchService.get_research(research_id)
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    
    return research

@router.get("/{research_id}/result")
async def get_research_result(
    research_id: str,
    user: UserProfile = Depends(get_user)
):
    """Get the full result of a completed research task"""
    research = ResearchService.get_research(research_id)
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    
    if research.status != ResearchStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Research not completed yet")
    
    return {
        "research_id": research_id,
        "result": research.result,
        "completed_at": research.completed_at
    }

@router.get("/history", response_model=ResearchHistory)
async def get_research_history(
    user: UserProfile = Depends(get_user),
    limit: int = 10,
    offset: int = 0
):
    """Get user's research history"""
    return ResearchService.get_user_history(user.user_id, limit, offset)

@router.delete("/{research_id}")
async def delete_research(
    research_id: str,
    user: UserProfile = Depends(get_user)
):
    """Delete a research task"""
    success = ResearchService.delete_research(research_id, user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Research not found")
    
    return {"message": "Research deleted successfully"}