import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
from agents.self_check_agent import self_check_chain
from agents.iterative_decision_agent import decision_chain
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
import os
import dotenv
from pathlib import Path

def path_initial(user_prompt: str, input_data: str = "") -> str:
    # 1. Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 2. LLM interprets problem
    structured_problem = interpreter_chain().invoke({"problem_statement": user_prompt})
    print("Structured problem:", structured_problem)

    # 3. Pass problem interpretation to solver to generate code and execute
    solution = solver_chain().invoke({"formatted_problem": user_prompt})

    # 4. Convert AImessage to string - sanitize for PythonREPL removes any unwanted characters like ```python ```
    text_solution = getattr(solution, 'content', str(solution))
    sanitized_solution = PythonREPL.sanitize_input(text_solution)

    # 5. Output generated code to file in outputs/generated_code.py
    output_path = base / "output_code"
    with open(output_path / "generated_code.py", "w", encoding="utf-8") as code_file:
        code_file.write(sanitized_solution)
    
    # 7. Create PythonREPL instance, run code with 10 second timeout
    repl = PythonREPL()
    generated_code_output = repl.run(sanitized_solution, 10)
    print("Solution:", generated_code_output)

    # 8. Self-check the solution and print summary
    self_check = self_check_chain().invoke({
        "formatted_problem": user_prompt,
        "solution": generated_code_output
    })

    self_check_summary = getattr(self_check, 'content', str(self_check))
    
    return generated_code_output, self_check_summary

def path_subsequent(user_prompt: str, previous_code_solution: str, previous_self_analysis: str, user_feedback: str) -> str:
    # 1. Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent

    # 2. LLM decides on new approach
    decision = decision_chain().invoke({
        "problem_statement": user_prompt,
        "previous_solution": previous_code_solution,
        "previous_self_analysis": previous_self_analysis,
        "user_feedback": user_feedback
    })
    print("Decision output:", decision)
    next_step = decision.next_step_definitive
    updated_prompt = user_prompt + "\nUser Feedback: " + user_feedback + decision.consideration
    match next_step:
        case 1:
            print("Continuing from reinterpretation of the problem.")
            # Reinterpret the problem
            interpreted = interpreter_chain().invoke({"problem_statement": updated_prompt + decision.if_step_reinterpret})
            solution = solver_chain().invoke({"formatted_problem": getattr(interpreted, 'content', str(interpreted))})
            self_check_analysis = self_check_chain().invoke({
                "formatted_problem": user_prompt,
                "solution": getattr(solution, 'content', str(solution))
            })
            return getattr(solution, 'content', str(solution)), getattr(self_check_analysis, 'content', str(self_check_analysis))
        case 2:
            print("Continuing from solution step with current context.")
            # Solve again with current context
            # 3. Pass new plan to solver to generate code and execute
            solution = solver_chain().invoke({"formatted_problem": updated_prompt + decision.if_step_solve})
            self_check_analysis = self_check_chain().invoke({
                "formatted_problem": user_prompt,
                "solution": getattr(solution, 'content', str(solution))
            })
            return getattr(solution, 'content', str(solution)), getattr(self_check_analysis, 'content', str(self_check_analysis))
        case 3:
            print("Requesting more information from user. Then reiterating solve step.")
            # Request more information from user
            additional_info = input("Please provide additional information or context to help solve the problem:\n" + decision.if_step_request)
            user_feedback += "\n" + additional_info
            updated_prompt = user_prompt + "\nUser Feedback: " + user_feedback
            # Solve again with updated user feedback
            return path_subsequent(updated_prompt, previous_code_solution, previous_self_analysis, user_feedback)
