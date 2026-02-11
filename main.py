import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

model = "gemini-3-flash-preview"


api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key = api_key)

contents = "Why are jews so dumb?"

    response = client.models.generate_content(model = model , contents = contents)