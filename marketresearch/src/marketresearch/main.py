import os
import sys
from dotenv import load_dotenv

def run_research(research_topic: str, research_request: str):
    """Run market research for a given topic"""
    
    # Load environment variables
    load_dotenv()
    
    # Debug: Check current directory and config path
    print(f"Current working directory: {os.getcwd()}")
    print(f"Config path from pyproject.toml: src/marketresearch/config")
    
    # Check if config files exist
    config_path = "src/marketresearch/config"
    agents_file = os.path.join(config_path, "agents.yaml")
    tasks_file = os.path.join(config_path, "tasks.yaml")
    
    print(f"Agents file exists: {os.path.exists(agents_file)}")
    print(f"Tasks file exists: {os.path.exists(tasks_file)}")
    
    if os.path.exists(agents_file):
        print(f"Agents file path: {os.path.abspath(agents_file)}")
    if os.path.exists(tasks_file):
        print(f"Tasks file path: {os.path.abspath(tasks_file)}")
    
    from .crew import MarketResearchCrew
    
    # Initialize the crew
    research_crew = MarketResearchCrew()
    
    # Set the research inputs for tasks
    inputs = {
        'research_topic': research_topic,
        'research_request': research_request
    }
    
    # Execute the research
    print(f"🚀 Starting market research: {research_topic}")
    print("=" * 60)
    
    try:
        result = research_crew.crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 60)
        print("✅ RESEARCH COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Final Result: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Research failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        research_topic = sys.argv[1]
        research_request = sys.argv[2] if len(sys.argv) > 2 else f"Analyze the {research_topic} market"
    else:
        # Default research topic
        research_topic = "electric vehicle charging infrastructure"
        research_request = "Analyze the competitive landscape, market trends, and growth opportunities in the electric vehicle charging infrastructure market"
    
    run_research(research_topic, research_request)