from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models import UserProfile

security = HTTPBearer()

# For development - simple token verification (no JWT)
def verify_simple_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserProfile:
    """Simple token verification for development"""
    # Accept any token for development
    return UserProfile(
        user_id="dev_user",
        username="developer",
        email="dev@example.com"
    )

def get_current_user(user: UserProfile = Depends(verify_simple_token)) -> UserProfile:
    """Get current authenticated user"""
    return user


