# Agent

A command-line AI coding agent powered by Google's Gemini models (specifically `gemini-2.5-flash`). This agent can assist with coding tasks by exploring the file system, reading and writing files, and executing Python code.

## Features

-   **Gemini-Powered**: Utilizes Google's generative AI for reasoning and code generation.
-   **Tool Use**: Capable of executing file system operations (list, read, write) and running Python scripts.
-   **Sandboxed Environment**: File operations are currently restricted to the `calculator/` directory relative to the project root for safety.
-   **CLI Interface**: Interact via command line arguments, file input, or standard input.
-   **Iterative Solving**: The agent operates in a loop (up to 20 iterations) to solve complex tasks step-by-step.

## Prerequisites

-   Python 3.12 or higher.
-   A Google Gemini API Key.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd agent
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

    *Note: `fastapi` and `uvicorn` are listed in `pyproject.toml`, but the core agent logic primarily relies on `google-genai` and `python-dotenv`.*

3.  **Configuration:**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

The main entry point is `main.py`. You can provide prompts in several ways:

**1. Direct Command Line Argument:**
```bash
python main.py "Write a python script to calculate the fibonacci sequence"
```

**2. From a File:**
```bash
python main.py --file prompt.txt
```

**3. Interactive / Standard Input:**
Run the script without arguments and type your prompt (press `Ctrl+D` or `Ctrl+Z` to submit):
```bash
python main.py
```

**Options:**
-   `--verbose`: Enable verbose output to see tool calls and detailed execution steps.

## Project Structure

-   `main.py`: The CLI entry point. Handles argument parsing and initialization.
-   `run_agent.py`: Contains the core agent logic, managing the conversation loop with the Gemini model and processing tool calls.
-   `functions/`: Contains the definitions and implementations of tools available to the agent (e.g., `get_file_content`, `write_file`).
-   `calculator/`: The default working directory for the agent's file operations. The agent "sees" this directory as its root.
-   `prompts.py`: Defines the system prompt and instructions for the AI.
-   `config.py`: Configuration constants (e.g., `MAX_CHARS`).

## Testing

The project includes basic test scripts (`test_*.py`) in the root directory to verify the functionality of individual tools.
```bash
python test_write_file.py
```
