from google import genai
from google.genai import types
import os
from prompts import system_prompt
from call_function import available_functions, call_function


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

def run_agent(args, MODEL = "gemini-2.5-flash"):
    
    client = genai.Client(api_key= api_key)
    
    messages = [types.Content(
      role="User",
      parts=[types.Part(text = args.user_prompt)]  
    )]
    
    
    for _ in range(20):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if not response.candidates:
            raise RuntimeError("No candidates returned from model.")

        for candidate in response.candidates:
            if not candidate.content:
                raise RuntimeError("Candidate content is None.")
            messages.append(candidate.content)

        first_candidate = response.candidates[0]

        if not first_candidate.content or not first_candidate.content.parts:
            raise RuntimeError("Candidate content parts missing.")

        part = first_candidate.content.parts[0]

        if not part.function_call:
            return part.text or "No response."

        function_result = call_function(part.function_call)

        if not function_result.parts:
            raise RuntimeError("Function returned no parts.")

        messages.append(types.Content(role="user", parts=function_result.parts))



    raise RuntimeError("Agent exceeded maximum iterations without final response.")