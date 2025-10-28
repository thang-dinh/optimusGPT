import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
from agents.self_check_agent import self_check_chain
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
import os
import dotenv
from pathlib import Path
import Code.agent_paths.iterative_solver as iterative_solver



def main():
    # Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 0. Load environment variables from the repository Code/.env (or container /app/.env)
    dotenv_path = base / ".env"
    dotenv.load_dotenv(dotenv_path)

    # 1. User input - currently static file read
    file_path = base / "data" / "exmp_prbm.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    user_prompt = file_content

    generated_code_output, self_check_summary = iterative_solver.path_initial(user_prompt)

    another = input("Do you want to run another iteration? (yes/no): ")
    if another.lower() == 'yes':
        additional_context = input("Please provide missing context or feedback for the next iteration:\n")
        generated_code_output, self_check_summary = iterative_solver.path_subsequent(user_prompt, generated_code_output, additional_context)
    



if __name__ == "__main__":
    main()
