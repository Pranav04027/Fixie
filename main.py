from dotenv import load_dotenv

load_dotenv()
import argparse
import sys
from run_agent import run_agent

parser = argparse.ArgumentParser(description="Chat Bot")

parser.add_argument("user_prompt", type=str, nargs="?", help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("--file", "-f", type=str, help="Read prompt from file")

args = parser.parse_args()

# Get prompt from file, argument, or stdin
if args.file:
    try:
        with open(args.file, "r") as f:
            prompt = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        exit(1)
elif args.user_prompt:
    prompt = args.user_prompt
else:
    # Read from stdin
    prompt = sys.stdin.read()


# Create a simple namespace-like object for compatibility
class Args:
    def __init__(self, user_prompt, verbose):
        self.user_prompt = user_prompt
        self.verbose = verbose


args_obj = Args(prompt, args.verbose)

try:
    result = run_agent(args_obj)
    print(result)
except Exception as e:
    print(f"Error while running the agent: {e}", file=sys.stderr)
    exit(1)
