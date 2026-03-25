import os
import json
import glob
import time
from src.config_loader import load_config
from src.blue_team import BlueTeamArchitect
from src.red_team_education import RedTeamArchitect
from run_red_team_test import run_red_team_test
from run_usability_test import run_usability_test

STATE_FILE = "loop_state.json"

class AutoReinforcementLoop:
    def __init__(self):
        self.config = load_config()
        self.blue_team = BlueTeamArchitect()
        self.red_team = RedTeamArchitect()
        self.state = self._load_state()
        
    def _load_state(self):
        if os.path.exists(STATE_FILE):
             with open(STATE_FILE, 'r') as f:
                 return json.load(f)
        return {
            "current_level": 0,
            "pending_strategies": [],
            "tested_strategies": [],
            "last_successful_strategy": None
        }

    def _save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=4)

    def _get_all_strategies(self):
        strategies_dir = os.path.join(os.path.dirname(__file__), "src", "penetration_strategies")
        files = glob.glob(os.path.join(strategies_dir, "*.md"))
        return [os.path.basename(f).replace(".md", "") for f in files]

    def _update_pending_strategies(self):
        """
        Updates pending_strategies based on available files, 
        ensuring we don't re-test what's already tested for this level.
        """
        all_strategies = self._get_all_strategies()
        
        # Identify new strategies not in pending or tested
        known = set(self.state["pending_strategies"]) | set(self.state["tested_strategies"])
        new_strategies = [s for s in all_strategies if s not in known]
        
        if new_strategies:
             # Add new ones to pending
             self.state["pending_strategies"].extend(new_strategies)
             
        # If pending is empty but we haven't tested everything (e.g. after a level bump), refill
        if not self.state["pending_strategies"] and not self.state["tested_strategies"]:
             self.state["pending_strategies"] = all_strategies

        # Prioritization: Move last successful strategy to front if present
        last_success = self.state.get("last_successful_strategy")
        if last_success and last_success in self.state["pending_strategies"]:
            self.state["pending_strategies"].remove(last_success)
            self.state["pending_strategies"].insert(0, last_success)

    def run_cycle(self):
        print(f"\n=== Auto-Reinforcement Cycle Start (Level {self.state['current_level']}) ===")
        
        # 1. Update Strategy Queue
        self._update_pending_strategies()
        
        if not self.state["pending_strategies"]:
            print("[Loop] No pending strategies. All tested against current level.")
            # Blue Team Win! Time to Evolve Red Team.
            self._evolve_red_team()
            return
            
        # 2. Pick Strategy
        current_strategy = self.state["pending_strategies"][0]
        print(f"[Loop] Testing Strategy: {current_strategy}")
        
        # 3. Attack (Red Team)
        # Using 5 turns default
        # Note: We need run_red_team_test to return the outcome or log path
        # I'll rely on the CSV log for the outcome check
        
        # Capture the CSV outcome by reading the last line before and after
        csv_path = os.path.join(os.path.dirname(__file__), "tests", "test_outcomes.csv")
        
        # Run Test
        try:
             # run_red_team_test prints to stdout, we let it happen
             run_red_team_test(self.state["current_level"], "User", current_strategy, turns=None)
        except Exception as e:
            print(f"[Loop] Error running test: {e}")
            return

        # 4. Analyze Result
        outcome, log_path = self._get_last_test_result(csv_path)
        
        if "FAIL" in getattr(outcome, "upper", lambda: "")() or "LEAK" in getattr(outcome, "upper", lambda: "")(): # Assuming FAIL/LEAK means Red Success
             # Wait, in the CSV from previous step, SUCCESS = Red Team Win (Leak), PASS = Blue Team Win (Safe)?
             # No, run_red_team_test.py logs evaluator outcome.
             # Evaluator returns "SUCCESS" if attack succeeded (Leak).
             # It returns "FAIL" if attack failed (Safe).
             # Let's check verify_logging output from previous turn:
             # "PASS,Secure response to confidential request" -> This was outcome PASS, meaning SAFE.
             # So if outcome == "SUCCESS" (Attack Succeeded), we have a leak.
             
             if outcome == "SUCCESS": 
                 print(f"[Loop] ATTACK SUCCESSFUL! Strategy '{current_strategy}' broke Level {self.state['current_level']}.")
                 self.state["last_successful_strategy"] = current_strategy
                 self._patch_blue_team(log_path)
             else:
                 print(f"[Loop] Attack Failed. Level {self.state['current_level']} is safe against '{current_strategy}'.")
                 # Mark as tested
                 if current_strategy in self.state["pending_strategies"]:
                    self.state["pending_strategies"].remove(current_strategy)
                 self.state["tested_strategies"].append(current_strategy)
        else:
             # Handle weird outcome
             print(f"[Loop] Warning: Unknown outcome '{outcome}'. Treating as Safe.")
             if current_strategy in self.state["pending_strategies"]:
                self.state["pending_strategies"].remove(current_strategy)
             self.state["tested_strategies"].append(current_strategy)
             
        self._save_state()

    def _get_last_test_result(self, csv_path):
        # Reads the last line of the CSV
        # Format: Timestamp,Team,Security Level,Strategy,Outcome,Reason,Log File
        if not os.path.exists(csv_path):
            return "UNKNOWN", None
            
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2: return "UNKNOWN", None
            
            last_line = lines[-1].strip()
            # Use csv module to parse correctly to handle potential commas in reason
            import csv
            reader = csv.reader([last_line])
            parts = list(reader)[0]
            
            if len(parts) >= 7:
                outcome = parts[4]
                log_rel_path = parts[6]
                # Reconstruct absolute path
                # CSV stores relative path from project root (e.g. tests/red_team_attempts/...)
                log_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), log_rel_path))
                return outcome, log_abs_path
            elif len(parts) >= 5:
                # Fallback for old CSV format
                outcome = parts[4]
                return outcome, None
            else:
                return "UNKNOWN", None

    def _patch_blue_team(self, failure_log_path):
        print("[Loop] Triggering Blue Team Architect...")
        # Initial Patch
        new_level = self.blue_team.patch_prompt(self.state["current_level"], failure_log_path)
        
        if new_level <= self.state["current_level"]:
            print("[Loop] Blue Team failed to generate a patch.")
            return

        # Verification Loop
        max_retries = 3
        retry_count = 0
        
        while retry_count <= max_retries:
            print(f"[Loop] Verifying Level {new_level} with Gold Team (Attempt {retry_count + 1})...")
            
            # Verify with Usability Test
            try:
                run_usability_test(new_level, "User", "public_info_request", turns=1)
                
                csv_path = os.path.join(os.path.dirname(__file__), "tests", "test_outcomes.csv")
                outcome, usability_log_path = self._get_last_test_result(csv_path)
                
                if outcome == "PASS":
                     print(f"[Loop] Verification Passed! Promoting to Level {new_level}.")
                     self.state["current_level"] = new_level
                     self.state["tested_strategies"] = []
                     self.state["pending_strategies"] = [] 
                     break
                else:
                     print(f"[Loop] Verification FAILED (Usability Issue).")
                     
                     if retry_count < max_retries:
                         print("[Loop] Retrying Blue Team Patch with Usability Feedback...")
                         
                         # Determine the candidate file path (it was saved as level_{new_level}.json)
                         candidate_path = os.path.join(os.path.dirname(__file__), "src", "prompts", f"level_{new_level}.json")
                         
                         self.blue_team.refine_prompt(
                             current_level=self.state["current_level"],
                             attack_log_path=failure_log_path,
                             failed_candidate_path=candidate_path,
                             usability_log_path=usability_log_path
                         )
                         retry_count += 1
                     else:
                         print(f"[Loop] Max retries reached. Discarding Level {new_level}.")
                         # Ideally revert the file, but for now we just don't increment current_level
                         break

            except Exception as e:
                print(f"[Loop] Verification Error: {e}")
                break

    def _evolve_red_team(self):
        print("[Loop] Level Secure. Triggering Red Team Evolution...")
        
        # Get last failure log (from any strategy, picking the latest log)
        log_dir = os.path.join(os.path.dirname(__file__), "tests", "red_team_attempts")
        list_of_files = glob.glob(os.path.join(log_dir, "*.md"))
        latest_file = max(list_of_files, key=os.path.getctime) if list_of_files else None
        
        # Get formatted failure text
        failure_log_text = ""
        if latest_file:
            with open(latest_file, 'r', encoding='utf-8') as f:
                failure_log_text = f.read()

        all_strats_paths = glob.glob(os.path.join(os.path.dirname(__file__), "src", "penetration_strategies", "*.md"))
        
        # This call handles both Phase 1 and Phase 2 internally
        new_strat_file = self.red_team.evolve_strategy(all_strats_paths, failure_log_text)
        
        self.state["tested_strategies"] = [] # Reset tested so we can re-test everything alongside the new one?
        # Actually user said "Or only testing the new attack strategy if testing against an existing level."
        # So we should populate pending ONLY with the new/refined strategy.
        
        if new_strat_file:
             new_strat_name = os.path.basename(new_strat_file).replace(".md", "")
             print(f"[Loop] New Strategy Added: {new_strat_name}")
             
             self.state["pending_strategies"] = [new_strat_name]
             self.state["tested_strategies"] = [] # Clear tested to allow re-testing if needed, but per request we focus on new. 
             # Wait, if we clear tested, next cycle update_pending will re-fill everything.
             # Ideally we keep tested as is, so updated_pending only adds the new one.
             # Then we just test the new one.
             
             # Re-reading request: "Or only testing the new attack strategy if testing against an existing level."
             # So we shouldn't wipe tested_strategies.
             pass
        
        self._save_state()

if __name__ == "__main__":
    loop = AutoReinforcementLoop()
    loop.run_cycle()
