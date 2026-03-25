import sys
import os
import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from usability_tester import UsabilityTester
from chatbot import get_chatbot_response
from prompt_builder import USER_ROLES
from evaluator import SecurityEvaluator
from logger import TestLogger
from config_loader import load_config

def run_usability_test(security_level: int, user_role: str, strategy: str, turns: int = None):
    # Load Config
    config = load_config()
    if turns is None:
        turns = config["testing"]["gold_team"]["max_turns"]

    print(f"--- Starting Usability Test ---")
    print(f"Target Level: {security_level}")
    print(f"Simulated Role: {user_role}")
    print(f"Strategy: {strategy}")
    print(f"Turns: {turns}")
    print("-" * 30)

    # Initialize Components
    tester = UsabilityTester(strategy)
    evaluator = SecurityEvaluator()
    logger = TestLogger()
    
    # Initialize Chatbot History (Blue Team Context)
    blue_team_history = []
    
    # Interaction Loop
    last_response = None
    evaluation_result = {"outcome": "IN PROGRESS", "reason": "Test ongoing"}
    
    for turn in range(1, turns + 1):
        print(f"\n[Turn {turn}/{turns}]")
        
        # 1. Valid User Asks
        query = tester.generate_query(last_response)
        print(f"User: {query}")
        
        # 2. Blue Team Responds
        blue_team_history.append({"role": "user", "content": query})
        
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
        # Evaluate as USABILITY to check for refusals
        current_eval = evaluator.evaluate_interaction(blue_team_history, security_level, "USABILITY")
        print(f" {current_eval['outcome']}")
        
        # Update Tester History
        tester.update_history(query, full_response)
        last_response = full_response
        evaluation_result = current_eval
        
        # Stop early if failed (refusal encountered)
        if current_eval['outcome'] == "REFUSAL":
             print("\n--- False Positive Detected! Stopping test early. ---")
             break

    # Save Log using Logger
    log_path = logger.log_conversation(
        team="GOLD_TEAM",
        level=security_level,
        strategy=strategy,
        history=blue_team_history,
        evaluation_outcome=evaluation_result['outcome'],
        evaluation_reason=evaluation_result['reason']
    )
            
    print(f"\n--- Test Complete. Log saved to {log_path} ---")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a Usability test.")
    parser.add_argument("--level", type=int, default=2, help="Security Level (0-7)")
    parser.add_argument("--role", type=str, default="User", choices=USER_ROLES.keys(), help="User Role to simulate")
    parser.add_argument("--strategy", type=str, default="public_info_request", help="Strategy filename (without .md)")
    parser.add_argument("--turns", type=int, help="Number of turns (overrides config)")
    
    args = parser.parse_args()
    
    run_usability_test(args.level, args.role, args.strategy, args.turns)
