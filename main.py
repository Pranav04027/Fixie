import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

model = "gemini-2.5-flash"


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key = api_key)

parser = argparse.ArgumentParser(description="ChatBot")

parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help= "Enable Verbode output")

args = parser.parse_args()

messages = [types.Content(
    role="user",
    parts=[types.Part(text = args.user_prompt)]
    )]

response = client.models.generate_content(
    model = model,
    contents = messages,
    config= types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0
        ),
    )

if not response.usage_metadata:
    raise RuntimeError("Response does not contain usage metadata.")

func_call = response.candidates[0].content.parts[0].function_call # pyright: ignore[reportOptionalMemberAccess, reportOptionalSubscript]

function_call_result = call_function(func_call)


# Calling function: get_file_content({'file_path': 'main.py'})
if func_call:
    function_call_result = call_function(func_call)
else:
    print("No function call returned.")

if not function_call_result.parts:
    raise ValueError("The parts was empty of result")
    
if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
    raise ValueError(".function_response property of the first item in the list of parts, i.e. .parts[0].function_response. It should be a FunctionResponse")

if function_call_result.parts[0].function_response.response is None:
    raise ValueError("NO function_call_result.parts[0].function_response.response")

function_result_list = function_call_result.parts[0]

if args.verbose:
    print(f"-> {function_call_result.parts[0].function_response.response}")





# if args.verbose:
#     print(f"User prompt: {args.user_prompt}")
#     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
#     print(f"Response: {response.text}")
# else:
#     print(f"Response: {response.text}")
    

    
