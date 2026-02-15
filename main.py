from dotenv import load_dotenv
load_dotenv()
import argparse
from run_agent import run_agent

parser = argparse.ArgumentParser(description= "Chat Bot")
    
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbse output")
    
args = parser.parse_args()
    
try:
    print(run_agent(args))
except Exception as e:
    print(f"Error while running the agent: {e}")
    exit(1)