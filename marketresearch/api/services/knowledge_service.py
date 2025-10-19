import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import shutil
from fastapi import UploadFile, HTTPException

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent / "src"
sys.path.insert(0, str(src_dir))

from marketresearch.rag_chain_factory import RAGEnhancedChainFactory

from models import KnowledgeStats, UploadResponse

class KnowledgeService:
    """Service for managing knowledge base operations"""
    
    _rag_factory: RAGEnhancedChainFactory = None
    
    @classmethod
    def get_rag_factory(cls) -> RAGEnhancedChainFactory:
        """Get or create RAG factory instance"""
        if cls._rag_factory is None:
            knowledge_path = str(current_dir.parent.parent / "knowledge")
            cls._rag_factory = RAGEnhancedChainFactory(knowledge_path)
        return cls._rag_factory
    
    @classmethod
    def get_stats(cls) -> KnowledgeStats:
        """Get knowledge base statistics"""
        try:
            rag_factory = cls.get_rag_factory()
            stats = rag_factory.rag_pipeline.get_knowledge_stats()
            
            return KnowledgeStats(
                total_documents=stats.get("total_documents", 0),
                company_profiles=stats.get("company_profiles", 0),
                industry_reports=stats.get("industry_reports", 0),
                market_data=stats.get("market_data", 0),
                user_preferences=stats.get("user_preferences", 0),
                last_updated=datetime.now()
            )
        except Exception as e:
            # Return empty stats if RAG system fails
            return KnowledgeStats(
                total_documents=0,
                company_profiles=0,
                industry_reports=0,
                market_data=0,
                user_preferences=0,
                last_updated=datetime.now()
            )
    
    @classmethod
    async def upload_file(cls, file: UploadFile, user_id: str) -> UploadResponse:
        """Upload a file to the knowledge base"""
        try:
            # Create uploaded_files directory if it doesn't exist
            upload_dir = current_dir.parent.parent / "knowledge" / "uploaded_files"
            upload_dir.mkdir(exist_ok=True)
            
            # Validate file type
            allowed_extensions = {'.txt', '.md', '.pdf', '.docx', '.json', '.csv'}
            file_extension = Path(file.filename).suffix.lower()
            
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File type {file_extension} not supported. Allowed: {', '.join(allowed_extensions)}"
                )
            
            # Save the uploaded file
            file_path = upload_dir / file.filename
            
            # Check if file already exists
            if file_path.exists():
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name_parts = file.filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_filename = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
                else:
                    new_filename = f"{file.filename}_{timestamp}"
                file_path = upload_dir / new_filename
            
            # Write file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # TODO: Process the file and add to ChromaDB
            # This would involve parsing the file and adding it to the knowledge base
            processed = False
            
            return UploadResponse(
                message=f"File {file_path.name} uploaded successfully",
                file_path=str(file_path),
                size=file_path.stat().st_size,
                processed=processed
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    @classmethod
    def list_files(cls) -> Dict:
        """List all files in the knowledge base"""
        try:
            knowledge_dir = current_dir.parent.parent / "knowledge"
            files = []
            
            # Scan all subdirectories
            for subdir in knowledge_dir.iterdir():
                if subdir.is_dir():
                    for file_path in subdir.rglob("*"):
                        if file_path.is_file():
                            files.append({
                                "name": file_path.name,
                                "path": str(file_path.relative_to(knowledge_dir)),
                                "size": file_path.stat().st_size,
                                "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                                "category": subdir.name
                            })
            
            return {
                "files": files,
                "total": len(files),
                "categories": list(set(f["category"] for f in files))
            }
            
        except Exception as e:
            return {"files": [], "total": 0, "categories": [], "error": str(e)}
    
    @classmethod
    def delete_file(cls, filename: str) -> bool:
        """Delete a file from the knowledge base"""
        try:
            knowledge_dir = current_dir.parent.parent / "knowledge"
            
            # Search for the file in all subdirectories
            for file_path in knowledge_dir.rglob(filename):
                if file_path.is_file():
                    file_path.unlink()
                    return True
            
            return False
            
        except Exception:
            return False
    
    @classmethod
    def reindex(cls):
        """Reindex the knowledge base"""
        try:
            # Reinitialize the RAG factory to pick up new files
            knowledge_path = str(current_dir.parent.parent / "knowledge")
            cls._rag_factory = RAGEnhancedChainFactory(knowledge_path)
            
        except Exception as e:
            raise Exception(f"Reindexing failed: {str(e)}")