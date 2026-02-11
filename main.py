import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
import argparse

model = "gemini-3-flash-preview"


api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key = api_key)


parser = argparse.ArgumentParser(description="ChatBot")
parser.add_argument("user_prompt", type=str, help="User Prompt")
args = parser.parse_args()

contents = args.user_prompt

response = client.models.generate_content(model = model , contents = contents)

if not response.usage_metadata:
    raise RuntimeError("Response does not contain usage metadata.")



print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)