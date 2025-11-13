import pandas as pd
import os
import dotenv
from pathlib import Path
import workflows.optimus as optimus
import json
import agents.chat_rerun_agent as chat_rerun_chain


def main():
    # Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 0. Load environment variables from the repository Code/.env (or container /app/.env)
    dotenv_path = base / ".env"
    dotenv.load_dotenv(dotenv_path)

    # 1. User input - currently static file read
    file_path = base / "data" / "example_problems" / "example_scheduling.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    user_prompt = file_content
    chat_history = ""
    while (True):
        working_memory, analysis = optimus.flow(user_prompt)
        print(", ".join(f"{key}: {value}" for key, value in analysis.items()))
        # Allow user to 
        user_input = input("Now you can exit, or choose to discuss further with the AI. Type 'exit' to quit at anytime, or enter your follow-up prompt: ")
        if(user_input.lower() == 'exit'):
            break
        else:
            while(True):
                chat_history = chat_history + "\nHuman: " + user_input 
                chat_response = chat_rerun_chain.chat_rerun_chain().invoke({
                    "memory": json.dumps(working_memory),
                    "evaluation": json.dumps(analysis),
                    "chat_history": user_input
                })
                chat_history = chat_history + "\nAI: " + getattr(chat_response, 'content', str(chat_response))
                print("AI Response:", getattr(chat_response, 'content', str(chat_response)))
                user_input = input("Type 'exit' to stop the discussion, or 'plan' to generate a new plan based off of your discussion, or enter your next prompt: ")
                if(user_input.lower() == 'exit'):
                    break
                elif(user_input.lower() == 'plan'):
                    chat_response = chat_rerun_chain.chat_rerun_chain().invoke({
                    "memory": json.dumps(working_memory),
                    "evaluation": json.dumps(analysis),
                    "chat_history": user_input
                    })
                    print("AI Plan Response:", getattr(chat_response, 'content', str(chat_response)))
                    user_input = input("Type 'exit' to stop the discussion, or 'continue' to keep discussing. Otherwise the plan will be used to generate a new solution: ")
                    if(user_input.lower() == 'exit'):
                        break
                    elif(user_input.lower() == 'continue'):
                        continue
                    else:
                        user_prompt = user_prompt + getattr(chat_response, 'content', str(chat_response))
                        break
                

if __name__ == "__main__":
    main()
