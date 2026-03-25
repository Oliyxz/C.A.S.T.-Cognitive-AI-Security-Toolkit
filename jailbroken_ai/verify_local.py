import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from config_loader import load_config
from file_manager import load_all_data
from prompt_builder import get_system_prompt

print("--- Testing Config Loader ---")
config = load_config()
if config:
    print(f"SUCCESS: Config loaded.")
else:
    print("FAILURE: Config load failed.")

print("\n--- Testing File Manager ---")
data = load_all_data()
if "Project Omega" in data:
    print("SUCCESS: Data loaded.")
else:
    print("FAILURE: Data missing.")

print("\n--- Testing Prompt Builder (Roles) ---")
# Test HR Role
prompt_hr = get_system_prompt(1, data, "HR")
if "access to SALARY" in prompt_hr and "NOT have access to Project Omega" in prompt_hr:
    print("SUCCESS: HR Role instructions present.")
else:
    print("FAILURE: HR Role instructions missing.")
    # print(prompt_hr)

# Test User Role
prompt_user = get_system_prompt(1, data, "User")
if "NO access to confidential data" in prompt_user:
    print("SUCCESS: User Role instructions present.")
else:
    print("FAILURE: User Role instructions missing.")
