import os
import yaml

def test_config_loading():
    """Test if config files can be loaded"""
    config_path = "/home/rayymond/Market-Research-Analyst/marketresearch/src/marketresearch/config"
    
    # Try to load agents.yaml
    try:
        with open(os.path.join(config_path, "agents.yaml"), 'r') as f:
            agents_config = yaml.safe_load(f)
        print("✅ Successfully loaded agents.yaml")
        print(f"Agents found: {list(agents_config.keys())}")
    except Exception as e:
        print(f"❌ Failed to load agents.yaml: {e}")
    
    # Try to load tasks.yaml
    try:
        with open(os.path.join(config_path, "tasks.yaml"), 'r') as f:
            tasks_config = yaml.safe_load(f)
        print("✅ Successfully loaded tasks.yaml")
        print(f"Tasks found: {list(tasks_config.keys())}")
    except Exception as e:
        print(f"❌ Failed to load tasks.yaml: {e}")

if __name__ == "__main__":
    test_config_loading()