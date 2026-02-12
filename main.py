import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt

model = "gemini-2.5-flash"


api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key = api_key)


parser = argparse.ArgumentParser(description="ChatBot")

parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help= "Enable Verbode output")

args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text = args.user_prompt)])]

response = client.models.generate_content(
    model = model,
    contents = messages,
    config= types.GenerateContentConfig(
        tools=[]
        system_instruction=system_prompt,
        temperature=0
        ),
    )

if not response.usage_metadata:
    raise RuntimeError("Response does not contain usage metadata.")


if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")
else:
    print(f"Response: {response.text}")
    
    
