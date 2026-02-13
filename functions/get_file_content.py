import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs= os.path.abspath(working_directory)
        
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if not os.path.isfile(target_file):
            return RuntimeError(f'Error: File not found or is not a regular file: "{file_path}"')
        
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs :
            return FileNotFoundError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description= f"Writes in a specified file relative to the working directory, returning the first {MAX_CHARS} characters. If a file exceeds the {MAX_CHARS} limit, the string: [...File 'file_path' truncated at {MAX_CHARS} characters] is added to the end of the returned data",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read relative to the working directory",
            ),
        },
    ),
)