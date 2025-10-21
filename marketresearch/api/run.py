#!/usr/bin/env python3
"""
FastAPI server runner for Market Research AI API
"""
import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    
    # Load .env from parent directory
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    # Run the server
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        raise
    