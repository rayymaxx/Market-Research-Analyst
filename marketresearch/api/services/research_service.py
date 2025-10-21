import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import asyncio

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent / "src"
sys.path.insert(0, str(src_dir))

from marketresearch.crew import MarketResearchCrew
from marketresearch.rag_chain_factory import RAGEnhancedChainFactory

from models import (
    ResearchRequest,
    ResearchResponse, 
    ResearchProgress,
    TaskProgress,
    ResearchStatus,
    TaskStatus,
    ResearchHistory,
    ResearchHistoryItem
)

class ResearchService:
    """Service for managing research operations"""
    
    # In-memory storage (replace with database in production)
    _research_store: Dict[str, ResearchResponse] = {}
    _crew_instance: Optional[MarketResearchCrew] = None
    
    @classmethod
    def get_crew(cls) -> MarketResearchCrew:
        """Get or create crew instance"""
        if cls._crew_instance is None:
            cls._crew_instance = MarketResearchCrew()
        return cls._crew_instance
    
    @classmethod
    def store_research(cls, research_id: str, research: ResearchResponse):
        """Store research in memory"""
        cls._research_store[research_id] = research
    
    @classmethod
    def get_research(cls, research_id: str) -> Optional[ResearchResponse]:
        """Get research by ID"""
        return cls._research_store.get(research_id)
    
    @classmethod
    def update_research_status(cls, research_id: str, status: ResearchStatus, **kwargs):
        """Update research status"""
        if research_id in cls._research_store:
            research = cls._research_store[research_id]
            research.status = status
            
            if status == ResearchStatus.COMPLETED:
                research.completed_at = datetime.now()
                if 'result' in kwargs:
                    research.result = kwargs['result']
            
            if status == ResearchStatus.FAILED and 'error' in kwargs:
                research.error = kwargs['error']
            
            if 'progress' in kwargs:
                research.progress = kwargs['progress']
    
    @classmethod
    def update_task_progress(cls, research_id: str, task_name: str, status: TaskStatus, **kwargs):
        """Update individual task progress"""
        if research_id in cls._research_store:
            research = cls._research_store[research_id]
            if research.progress:
                for task in research.progress.tasks:
                    if task.task_name == task_name:
                        task.status = status
                        if status == TaskStatus.RUNNING:
                            task.start_time = datetime.now()
                            research.progress.active_task = task_name
                        elif status == TaskStatus.COMPLETED:
                            task.end_time = datetime.now()
                            if task_name not in research.progress.completed_tasks:
                                research.progress.completed_tasks.append(task_name)
                        
                        if 'tools_used' in kwargs:
                            task.tools_used = kwargs['tools_used']
                        if 'output' in kwargs:
                            task.output = kwargs['output']
                        break
                
                # Update progress percentage
                completed_count = len(research.progress.completed_tasks)
                total_tasks = len(research.progress.tasks)
                research.progress.progress_percentage = int((completed_count / total_tasks) * 100)
    
    @classmethod
    async def execute_research(cls, research_id: str, request: ResearchRequest, user_id: str):
        """Execute research in background"""
        try:
            # Update status to running
            cls.update_research_status(research_id, ResearchStatus.RUNNING)
            
            # Get crew instance
            crew = cls.get_crew()
            
            # Prepare inputs
            inputs = {
                'research_topic': request.research_topic,
                'research_request': request.research_request,
                'current_date': datetime.now().strftime('%B %d, %Y'),
                'user_id': user_id,
                'research_id': research_id
            }
            
            # Task sequence with real-time updates
            tasks = [
                "comprehensive_data_collection_task",
                "comprehensive_analysis_task", 
                "final_comprehensive_report_task"
            ]
            
            # Update first task to running
            cls.update_task_progress(research_id, tasks[0], TaskStatus.RUNNING)
            
            # Execute research with progress tracking
            result = crew.kickoff_with_rag(inputs=inputs)
            
            # Simulate task completion progression
            for i, task_name in enumerate(tasks):
                cls.update_task_progress(research_id, task_name, TaskStatus.COMPLETED)
                if i < len(tasks) - 1:
                    cls.update_task_progress(research_id, tasks[i + 1], TaskStatus.RUNNING)
                    await asyncio.sleep(0.5)  # Brief delay for UI updates
            
            # Convert CrewOutput to string safely
            try:
                if hasattr(result, 'raw') and result.raw:
                    result_text = str(result.raw)
                elif hasattr(result, 'output') and result.output:
                    result_text = str(result.output)
                elif hasattr(result, '__dict__'):
                    # Try to get a meaningful string representation
                    result_text = str(result.__dict__)
                else:
                    result_text = str(result)
                
                # Ensure it's a clean string (no complex objects)
                if not isinstance(result_text, str):
                    result_text = str(result_text)
                    
            except Exception as e:
                result_text = f"Research completed but result serialization failed: {str(e)}"
            
            # Update final status
            cls.update_research_status(
                research_id, 
                ResearchStatus.COMPLETED,
                result=result_text
            )
            
        except Exception as e:
            cls.update_research_status(
                research_id,
                ResearchStatus.FAILED,
                error=str(e)
            )
    
    @classmethod
    def get_user_history(cls, user_id: str, limit: int = 10, offset: int = 0) -> ResearchHistory:
        """Get user's research history"""
        # Filter by user_id (simplified - in production, store user_id with research)
        all_research = list(cls._research_store.values())
        
        # Convert to history items
        history_items = [
            ResearchHistoryItem(
                research_id=research.research_id,
                research_topic=research.progress.current_phase if research.progress else "Unknown",
                status=research.status,
                created_at=research.created_at,
                completed_at=research.completed_at
            )
            for research in all_research
        ]
        
        # Apply pagination
        total = len(history_items)
        paginated_items = history_items[offset:offset + limit]
        
        return ResearchHistory(
            history=paginated_items,
            total=total,
            limit=limit,
            offset=offset
        )
    
    @classmethod
    def delete_research(cls, research_id: str, user_id: str) -> bool:
        """Delete research (with user verification)"""
        if research_id in cls._research_store:
            del cls._research_store[research_id]
            return True
        return False
    
    @classmethod
    def check_pdf_exists(cls, research_id: str) -> bool:
        """Check if PDF file exists for research"""
        import os
        pdf_path = f"research_report_{research_id}.pdf"
        return os.path.exists(pdf_path)