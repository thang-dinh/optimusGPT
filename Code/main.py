import pandas as pd
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
    while (True):
        working_memory, analysis = optimus.flow(user_prompt)
        print("Working memory:", str(working_memory))
        print("Analysis:", analysis)
        if(analysis['output_succesful']):
            print("Process completed successfully.")
            break
        else:
            print("The solution was not satisfactory. Please provide additional information or context to help improve the solution.")
            user_prompt_addition = input("Enter additional information or context if requested: ")
        user_prompt = user_prompt + "\nAdditional Information: " + user_prompt_addition


if __name__ == "__main__":
    main()
