import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")

def load_config():
    """Loads the YAML configuration file."""
    if not os.path.exists(CONFIG_PATH):
        # Fallback default config if file is missing
        return {
            "model": {
                "name": "llama3",
                "temperature": 0.7,
                "context_window": 4096
            },
            "app": {
                "debug_mode": False
            }
        }
    
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None
