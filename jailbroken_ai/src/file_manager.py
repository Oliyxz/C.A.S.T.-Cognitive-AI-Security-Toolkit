import os
from typing import List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_available_files() -> List[str]:
    """Returns a list of filenames in the data directory."""
    if not os.path.exists(DATA_DIR):
        return []
    try:
        return [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    except FileNotFoundError:
        return []

def read_file_content(filename: str) -> str:
    """Reads the content of a specific file."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def load_all_data() -> str:
    """Context loader: Reads all files and formats them for the LLM."""
    files = get_available_files()
    context = ""
    for file in files:
        content = read_file_content(file)
        context += f"\n=== START FILE: {file} ===\n{content}\n=== END FILE: {file} ===\n"
    return context
