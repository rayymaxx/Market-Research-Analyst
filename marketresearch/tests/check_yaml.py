import yaml
import os

def check_yaml_structure():
    """Check the exact structure of your YAML files"""
    
    # Check agents.yaml
    with open('/home/rayymond/Market-Research-Analyst/marketresearch/src/marketresearch/config/agents.yaml', 'r') as f:
        agents = yaml.safe_load(f)
    
    print("=== AGENTS.YAML STRUCTURE ===")
    print(f"Top-level keys: {list(agents.keys())}")
    for key, value in agents.items():
        print(f"\nAgent: {key}")
        print(f"  Role: {value.get('role', 'MISSING')}")
        print(f"  Goal: {value.get('goal', 'MISSING')[:100]}...")
    
    # Check tasks.yaml
    with open('/home/rayymond/Market-Research-Analyst/marketresearch/src/marketresearch/config/tasks.yaml', 'r') as f:
        tasks = yaml.safe_load(f)
    
    print("\n=== TASKS.YAML STRUCTURE ===")
    print(f"Top-level keys: {list(tasks.keys())}")
    for key, value in tasks.items():
        print(f"\nTask: {key}")
        print(f"  Agent: {value.get('agent', 'MISSING')}")

if __name__ == "__main__":
    check_yaml_structure()