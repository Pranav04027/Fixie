from google import genai
from google.genai import types
import os
from prompts import system_prompt
from call_function import available_functions, call_function


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")


def run_agent(args, MODEL="gemini-2.5-flash"):
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=available_functions)],   #type: ignore
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if not response or not response.candidates:
            raise RuntimeError("No valid response fro`m model")

        model_content = response.candidates[0].content
        if not model_content or not model_content.parts:
            raise RuntimeError("Empty model content")

        messages.append(model_content)

        # find function calls
        function_calls = []
        
        for p in model_content.parts:
            if p.function_call:
                function_calls.append(p.function_call)
            
            if p.thought:
                print(f"DEBUG Thought: {p.thought}")

        # If no function call → final answer
        if not function_calls:
            result = ""
            for part in model_content.parts:
                result.join(part.text or "")
            
            if result:
                return result
            else:
                "Task Complete"
                
        tool_parts = []
        for fc in function_calls:
            result = call_function(fc, args.verbose)

            tool_parts.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response=result,
                    )
                )
            )

        # Send tool results back to model
        messages.append(types.Content(role="user", parts=tool_parts))

    raise RuntimeError("Agent exceeded maximum iterations.")
