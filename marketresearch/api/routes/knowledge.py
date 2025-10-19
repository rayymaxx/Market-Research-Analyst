from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pathlib import Path
import shutil
from typing import List
import sys 
import os

from models import KnowledgeStats, UploadResponse, UserProfile
from auth import verify_simple_token
from services.knowledge_service import KnowledgeService

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# Use simple auth for development
get_user = verify_simple_token

@router.get("/stats", response_model=KnowledgeStats)
async def get_knowledge_stats(user: UserProfile = Depends(get_user)):
    """Get knowledge base statistics"""
    return KnowledgeService.get_stats()

@router.post("/upload", response_model=UploadResponse)
async def upload_knowledge_file(
    file: UploadFile = File(...),
    user: UserProfile = Depends(get_user)
):
    """Upload a file to the knowledge base"""
    return await KnowledgeService.upload_file(file, user.user_id)

@router.get("/files")
async def list_knowledge_files(user: UserProfile = Depends(get_user)):
    """List all files in the knowledge base"""
    return KnowledgeService.list_files()

@router.delete("/files/{filename}")
async def delete_knowledge_file(
    filename: str,
    user: UserProfile = Depends(get_user)
):
    """Delete a file from the knowledge base"""
    success = KnowledgeService.delete_file(filename)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": f"File {filename} deleted successfully"}

@router.post("/reindex")
async def reindex_knowledge_base(user: UserProfile = Depends(get_user)):
    """Reindex the knowledge base"""
    try:
        KnowledgeService.reindex()
        return {"message": "Knowledge base reindexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reindexing failed: {str(e)}")