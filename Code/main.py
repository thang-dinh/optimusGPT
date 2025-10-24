import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
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
    out_path = base / "output_code" / "generated_code.py"
    # ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as file:
        # solver_chain() result may expose content attribute
        file.write(getattr(solution, 'content', str(solution)))

    ## 4. Visualization
    # visualize_tour(df, solution["order"])


if __name__ == "__main__":
    main()
