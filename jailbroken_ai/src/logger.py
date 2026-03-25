import os
import datetime
import csv
import json

class TestLogger:
    def __init__(self):
        self.base_log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests")
        self.red_team_dir = os.path.join(self.base_log_dir, "red_team_attempts")
        self.gold_team_dir = os.path.join(self.base_log_dir, "gold_team_attempts")
        self.outcomes_file = os.path.join(self.base_log_dir, "test_outcomes.csv")
        
        # Ensure directories exist
        os.makedirs(self.red_team_dir, exist_ok=True)
        os.makedirs(self.gold_team_dir, exist_ok=True)
        
        # Initialize CSV if it doesn't exist
        if not os.path.exists(self.outcomes_file):
            with open(self.outcomes_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Team", "Security Level", "Strategy", "Outcome", "Reason", "Log File"])

    def log_conversation(self, team: str, level: int, strategy: str, history: list, evaluation_outcome: str, evaluation_reason: str):
        """
        Logs the conversation to a file and updates the outcome CSV.
        team: "RED_TEAM" or "GOLD_TEAM" (or "USABILITY")
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine directory
        if team.upper() == "RED_TEAM":
            log_dir = self.red_team_dir
            team_label = "Red Team"
        else:
            log_dir = self.gold_team_dir
            team_label = "Gold Team"
            
        # 1. Save Conversation Log (Markdown/Text)
        filename = f"{team_label}_{strategy}_L{level}_{timestamp_file}.md"
        filepath = os.path.join(log_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {team_label} Test Log\n")
            f.write(f"Date: {timestamp}\n")
            f.write(f"Level: {level}\n")
            f.write(f"Strategy: {strategy}\n")
            f.write(f"Outcome: {evaluation_outcome}\n")
            f.write(f"Reason: {evaluation_reason}\n")
            f.write("-" * 40 + "\n\n")
            
            for turn in history:
                role = turn.get("role", "Unknown")
                content = turn.get("content", "")
                f.write(f"**{role.upper()}:** {content}\n\n")
                
        # 2. Append to CSV Outcome Log
        with open(self.outcomes_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Store relative path for cleaner logs
            rel_path = os.path.relpath(filepath, os.path.dirname(self.base_log_dir))
            writer.writerow([timestamp, team_label, level, strategy, evaluation_outcome, evaluation_reason, rel_path])
            
        return filepath
