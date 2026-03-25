import sys
import os
import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from red_team import RedTeamAttacker
from chatbot import get_chatbot_response
from prompt_builder import USER_ROLES
from evaluator import SecurityEvaluator
from logger import TestLogger
from config_loader import load_config

def run_red_team_test(security_level: int, user_role: str, strategy: str, turns: int = None):
    # Load Config
    config = load_config()
    if turns is None:
        turns = config["testing"]["red_team"]["max_turns"]

    print(f"--- Starting Red Team Test ---")
    print(f"Target Level: {security_level}")
    print(f"Simulated Role: {user_role}")
    print(f"Strategy: {strategy}")
    print(f"Turns: {turns}")
    print("-" * 30)

    # Initialize Components
    attacker = RedTeamAttacker(strategy, security_level)
    evaluator = SecurityEvaluator()
    logger = TestLogger()
    
    # Initialize Chatbot History (Blue Team Context)
    blue_team_history = []
    
    # Interaction Loop
    last_response = None
    evaluation_result = {"outcome": "IN PROGRESS", "reason": "Test ongoing"}
    
    for turn in range(1, turns + 1):
        print(f"\n[Turn {turn}/{turns}]")
        
        # 1. Red Team Attacks
        attack = attacker.generate_attack(last_response)
        print(f"Red Team: {attack}")
        
        # 2. Blue Team Responds
        blue_team_history.append({"role": "user", "content": attack})
        
        print("Blue Team: ", end="", flush=True)
        response_stream = get_chatbot_response(blue_team_history, security_level, user_role)
        
        full_response = ""
        if isinstance(response_stream, str):
            full_response = response_stream
            print(full_response)
        else:
            for chunk in response_stream:
                print(chunk, end="", flush=True)
                full_response += chunk
            print() 
            
        # 3. Evaluation
        blue_team_history.append({"role": "assistant", "content": full_response})
        
        print("Evaluating...", end="", flush=True)
        # Evaluate as RED_TEAM to check for security breaches
        current_eval = evaluator.evaluate_interaction(blue_team_history, security_level, "RED_TEAM")
        print(f" {current_eval['outcome']}")
        
        # Update Red Team History
        attacker.update_history(attack, full_response)
        last_response = full_response
        evaluation_result = current_eval

        # Stop early if goal achieved (optional, but good for saving tokens/time if successful)
        if current_eval['outcome'] == "SUCCESS":
             print("\n--- Attack Successful! Stopping test early. ---")
             break

    # Save Log using Logger
    log_path = logger.log_conversation(
        team="RED_TEAM",
        level=security_level,
        strategy=strategy,
        history=blue_team_history,
        evaluation_outcome=evaluation_result['outcome'],
        evaluation_reason=evaluation_result['reason']
    )
            
    print(f"\n--- Test Complete. Log saved to {log_path} ---")

if __name__ == "__main__":
    # Default execution for testing
    import argparse
    parser = argparse.ArgumentParser(description="Run a Red Team test.")
    parser.add_argument("--level", type=int, default=2, help="Security Level (0-7)")
    parser.add_argument("--role", type=str, default="User", choices=USER_ROLES.keys(), help="User Role to simulate")
    parser.add_argument("--strategy", type=str, default="emotional_manipulation", help="Strategy filename (without .md)")
    parser.add_argument("--turns", type=int, help="Number of turns (overrides config)")
    
    args = parser.parse_args()
    
    run_red_team_test(args.level, args.role, args.strategy, args.turns)
