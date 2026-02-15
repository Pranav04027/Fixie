from google.genai import types

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions =[
        schema_write_file,
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
    ]


def call_function(function_call = None, verbose=False):
    
    if not function_call:
        return {"error": "No Function_call object recived by call_function"}
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return {"error": f"Unknown function: {function_name}"}

    if function_call.args:
        args = dict(function_call.args)
    else:
        args = {}

    args["working_directory"] = "./calculator"

    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = {"Error": str(e)}

    if isinstance(function_result, Exception):
        function_result = {"Error": str(function_result)}

    return {"result": function_result}
