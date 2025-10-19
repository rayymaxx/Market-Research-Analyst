# src/marketresearch/main.py
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import time

def setup_imports():
    """Setup Python path for absolute imports with correct src structure"""
    # Get the current file path
    current_file = os.path.abspath(__file__)
    # src/marketresearch/main.py -> we need to go up two levels to get to marketresearch directory
    marketresearch_dir = os.path.dirname(current_file)  # src/marketresearch
    src_dir = os.path.dirname(marketresearch_dir)       # src
    project_root = os.path.dirname(src_dir)             # marketresearch (the actual project root)
    
    # Add both project_root and src_dir to Python path
    paths_to_add = [project_root, src_dir]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Source directory: {src_dir}")
    return project_root

def run_research(research_topic: str, research_request: str):
    """Run market research with RAG-enhanced chains"""
    
    # Setup imports first
    setup_imports()
    load_dotenv()
    
    try:
        # Try different import approaches
        try:
            # Approach 1: Direct import from src structure
            from src.marketresearch.crew import MarketResearchCrew
            print("✅ Import successful using src.marketresearch path")
        except ImportError:
            # Approach 2: Try without src prefix
            from marketresearch.crew import MarketResearchCrew
            print("✅ Import successful using marketresearch path")
        
        # Initialize crew
        research_crew = MarketResearchCrew()
        
        # Set inputs
        inputs = {
            'research_topic': research_topic,
            'research_request': research_request,
            'current_date': datetime.now().strftime('%B %d, %Y')
        }
        
        print(f"🚀 Starting RAG-Enhanced Market Research: {research_topic}")
        print("=" * 60)
        
        # Use enhanced kickoff with retry logic
        max_retries = 3
        base_delay = 60  # Start with 1 minute
        
        for attempt in range(max_retries):
            try:
                result = research_crew.kickoff_with_rag(inputs=inputs)
                break  # Success, exit retry loop
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < max_retries - 1:
                        wait_time = base_delay * (2 ** attempt)
                        print(f"🚫 Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print("❌ All retries exhausted due to rate limits")
                        raise
                else:
                    # Non-rate-limit error, don't retry
                    raise
        
        print("\n" + "=" * 60)
        print("✅ RAG-ENHANCED RESEARCH COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Current Python path:")
        for path in sys.path:
            print(f"   - {path}")
        raise
    except Exception as e:
        print(f"❌ Research failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    if len(sys.argv) > 1:
        research_topic = sys.argv[1]
        research_request = sys.argv[2] if len(sys.argv) > 2 else f"Analyze the {research_topic} market"
    else:
        research_topic = "electric vehicle charging infrastructure"
        research_request = "Analyze the competitive landscape, market trends, and growth opportunities in the electric vehicle charging infrastructure market"
    
    run_research(research_topic, research_request)