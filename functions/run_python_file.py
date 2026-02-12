import os, subprocess

def run_python_file(working_directory, file_path: str, args=None):
    try:
        working_dir_abs= os.path.abspath(working_directory)
            
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
                        
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs :
            raise FileNotFoundError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(target_file):
            raise FileNotFoundError(f'Error: "{file_path}" does not exist or is not a regular file')
        
        if not file_path.endswith(".py"):
            raise ValueError(f'Error: "{file_path}" is not a Python file')
        
        command = ["python", target_file]
        
        if args:
            command.extend(args)
            
        result = subprocess.run(command, timeout=30, capture_output=True, text=True)
        
        return_statement:str = ""
        
        if result.stdout:
            return_statement+= f"STDOUT:{result.stdout}\n"
        
        if result.stderr:
            return_statement+= f"STDERR:{result.stderr}\n"
            
        if result.returncode !=0 :
            return_statement += f"Process exited with code {result.returncode}\n"
        
        if not return_statement:
            return_statement += f"No output produced"
    
            
        return return_statement
    
    except Exception as e:
        return f"Error: executing Python file: {e}"