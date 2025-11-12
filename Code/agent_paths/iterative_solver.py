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

def path_initial(user_prompt: str, input_data: str = "") -> tuple[str, str]:
    # Use project root (/app inside container)
    project_root = Path(__file__).resolve().parent.parent

    # LLM interprets problem
    structured_problem = interpreter_chain().invoke({"problem_statement": user_prompt})
    print("Structured problem:", structured_problem)

    # Generate code
    solution = solver_chain().invoke({"formatted_problem": user_prompt})

    # Convert AI message to string and sanitize for REPL
    text_solution = getattr(solution, 'content', str(solution))
    sanitized_solution = PythonREPL.sanitize_input(text_solution)

    # Output generated code to project-root output_code/generated_code.py
    output_path = project_root / "output_code"
    output_path.mkdir(exist_ok=True)
    code_path = output_path / "generated_code.py"
    with open(code_path, "w", encoding="utf-8") as code_file:
        code_file.write(sanitized_solution)

    # Marker for agentic orchestration (logs)
    print(f"GENERATED_FILE::{code_path.name}")

    # Execute in REPL with 10 second timeout (kept as-is)
    repl = PythonREPL()
    generated_code_output = repl.run(sanitized_solution, 10)
    print("Solution:", generated_code_output)

    # Self-check the solution and return summary
    self_check = self_check_chain().invoke({
        "formatted_problem": user_prompt,
        "solution": generated_code_output
    })
    self_check_summary = getattr(self_check, 'content', str(self_check))

    return generated_code_output, self_check_summary

def path_subsequent(user_prompt: str, previous_code_solution: str, previous_self_analysis: str, user_feedback: str) -> tuple[str, str]:
    # Use project root (/app inside container)
    project_root = Path(__file__).resolve().parent.parent

    # Decide next step
    decision = decision_chain().invoke({
        "problem_statement": user_prompt,
        "previous_solution": previous_code_solution,
        "previous_self_analysis": previous_self_analysis,
        "user_feedback": user_feedback
    })
    print("Decision output:", decision)
    next_step = decision.next_step_definitive
    updated_prompt = user_prompt + "\nUser Feedback: " + user_feedback + decision.consideration

    if next_step == 1:
        print("Continuing from reinterpretation of the problem.")
        interpreted = interpreter_chain().invoke({"problem_statement": updated_prompt + decision.if_step_reinterpret})
        solution = solver_chain().invoke({"formatted_problem": getattr(interpreted, 'content', str(interpreted))})

        text_solution = getattr(solution, 'content', str(solution))
        sanitized_solution = PythonREPL.sanitize_input(text_solution)

        output_path = project_root / "output_code"
        output_path.mkdir(exist_ok=True)
        code_path = output_path / "generated_code_iteration_1.py"
        with open(code_path, "w", encoding="utf-8") as code_file:
            code_file.write(sanitized_solution)
        print(f"GENERATED_FILE::{code_path.name}")

        self_check_analysis = self_check_chain().invoke({
            "formatted_problem": user_prompt,
            "solution": text_solution
        })
        return text_solution, getattr(self_check_analysis, 'content', str(self_check_analysis))

    elif next_step == 2:
        print("Continuing from solution step with current context.")
        solution = solver_chain().invoke({"formatted_problem": updated_prompt + decision.if_step_solve})

        text_solution = getattr(solution, 'content', str(solution))
        sanitized_solution = PythonREPL.sanitize_input(text_solution)

        output_path = project_root / "output_code"
        output_path.mkdir(exist_ok=True)
        code_path = output_path / "generated_code_iteration_2.py"
        with open(code_path, "w", encoding="utf-8") as code_file:
            code_file.write(sanitized_solution)
        print(f"GENERATED_FILE::{code_path.name}")

        self_check_analysis = self_check_chain().invoke({
            "formatted_problem": user_prompt,
            "solution": text_solution
        })
        return text_solution, getattr(self_check_analysis, 'content', str(self_check_analysis))

    else:
        print("Requesting more information from user. Then reiterating solve step.")
        additional_info = input("Please provide additional information or context to help solve the problem:\n" + decision.if_step_request)
        user_feedback += "\n" + additional_info
        updated_prompt = user_prompt + "\nUser Feedback: " + user_feedback
        return path_subsequent(updated_prompt, previous_code_solution, previous_self_analysis, user_feedback)