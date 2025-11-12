import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
from agents.self_check_agent import self_check_chain
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
import os
import dotenv
from pathlib import Path
import workflows.optimus as optimus


def main():
    # Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 0. Load environment variables from the repository Code/.env (or container /app/.env)
    dotenv_path = base / ".env"
    dotenv.load_dotenv(dotenv_path)

    # 1. User input - currently static file read
    file_path = base / "data" / "example_scheduling.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    user_prompt = file_content
    generated_code_output = optimus.flow(user_prompt)



if __name__ == "__main__":
    main()
