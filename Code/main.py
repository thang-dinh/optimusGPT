import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
from agents.self_check_agent import self_check_chain
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
import os
import dotenv
from pathlib import Path


def main():
    # Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 0. Load environment variables from the repository Code/.env (or container /app/.env)
    dotenv_path = base / ".env"
    dotenv.load_dotenv(dotenv_path)

    # 1. User input
    file_path = base / "data" / "exmp_prbm.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    user_prompt = file_content

    csv_path = base / "data" / "example_tsp.csv"
    df = pd.read_csv(csv_path)

    # 2. LLM interprets problem
    structured_problem = interpreter_chain().invoke({"problem_statement": user_prompt})
    print("Structured problem:", structured_problem)

    # 3. Generate guropipy code to find solution
    solution = solver_chain().invoke({"formatted_problem": user_prompt})
    # Convert AImessage to string
    text_solution = getattr(solution, 'content', str(solution))
    sanitized_solution = PythonREPL.sanitize_input(text_solution)
    #output generated code to file in outputs/generated_code.py
    output_path = base / "output_code"
    with open(output_path / "generated_code.py", "w", encoding="utf-8") as code_file:
        code_file.write(sanitized_solution)
    #Confirm run with user input
    go_ahead = input("Do you want to execute this code? (yes/no): ")
    if go_ahead.lower() != 'yes':
        print("Execution cancelled by user.")
        return
    repl = PythonREPL()
    generated_code_output = repl.run(sanitized_solution, 10)
    print("Solution:", generated_code_output)
    # 4. Self-check the solution
    self_check = self_check_chain().invoke({
        "formatted_problem": user_prompt,
        "solution": generated_code_output
    })
    print("Self-check summary:", getattr(self_check, 'content', str(self_check)))
    


if __name__ == "__main__":
    main()
