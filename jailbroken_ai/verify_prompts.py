import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from prompt_builder import get_system_prompt, SECURITY_LEVELS, USER_ROLES

def generate_all_prompts():
    print("Generating prompts for all levels and roles...")
    for level in SECURITY_LEVELS:
        for role in USER_ROLES:
            print(f"--- Level {level} | Role {role} ---")
            prompt = get_system_prompt(level, "Context Data Here", role)
            print(prompt)
            print("="*40)

if __name__ == "__main__":
    generate_all_prompts()
