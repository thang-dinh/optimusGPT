import pandas as pd
from agents.interpreter_agent import interpreter_chain
from agents.solver_agent import solver_chain
from agents.verify_agent import verification_chain
from agents.result_summary_agent import result_summary_chain
from agents.failure_analysis_agent import failure_analysis_chain
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
import os
import dotenv
from pathlib import Path
import json

def flow(user_prompt: str) -> tuple[dict, str]:
    # Base directory where this file lives (Code/)
    base = Path(__file__).resolve().parent.parent

    #Store prompt in memory
    working_memory = {"original_prompt": user_prompt}

    # LLM interprets problem
    catagories = os.listdir(base / "data" / "problem_catagories")
    structured_problem = interpreter_chain().invoke({"problem_statement": user_prompt, "problem_catagories": str(catagories)})
    str_structured_problem = getattr(structured_problem, 'content', str(structured_problem))
    print("Structured problem:", str_structured_problem)

    if(structured_problem['seen_catagory']):  
        with open(base / "data" / "notes_by_catagory" / structured_problem['problem_catagory'], "r", encoding="utf-8") as notes:
            working_memory["existing_notes"] = notes.read()

    #Store interpretation json in memory
    working_memory["interpretation"] = structured_problem

    # Pass problem interpretation to solver to generate code along with notes 
    solution = solver_chain().invoke({"formatted_problem": str_structured_problem, "notes": working_memory["existing_notes"]})
    
    # Convert AImessage to string - sanitize for PythonREPL removes any unwanted characters like ```python ```
    unsanitized_code = getattr(solution, 'content', str(solution))
    sanitized_code = PythonREPL.sanitize_input(unsanitized_code)

    # Output generated code to file in outputs/generated_code.py
    working_memory["code_solution": sanitized_code]
    
    # Create PythonREPL instance, run code with 30 second timeout
    repl = PythonREPL()
    generated_code_output = repl.run(sanitized_code, 30)
    print("Solution:", generated_code_output)
    working_memory["code_output"] = generated_code_output

    # Self-check the solution and print summary
    self_check = verification_chain().invoke({
        "user_prompt": user_prompt,
        "structured_problem": str_structured_problem,
        "code": sanitized_code,
        "code_output": generated_code_output,
        "notes": working_memory["existing_notes"]
    })

    #Next steps to implement: if code succesful, summarize results for the user, and return all steps.
    # If code failed, failure analysis, determine where the problem was, either ask for more information, or create notes regarding specific problem, and try again

    if(self_check["output_succesful"]):
        summary = result_summary_chain.invoke()# NEeds parameters
        return getattr(summary, 'content', str(summary))
    else:
        evaluation = failure_analysis_chain.invoke({
            "user_prompt": user_prompt,
            "structured_problem": str_structured_problem,
            "code": sanitized_code,
            "code_output": generated_code_output,
            "notes": working_memory["existing_notes"]
        })
        #write notes to file for future use
        if("notes_for_future" in evaluation):
            notes_filename = structured_problem['problem_catagory']
            with open(base / "data" / "notes_by_catagory" / notes_filename, "a", encoding="utf-8") as notes_file:
                notes_file.write("\n")
                notes_file.write(evaluation["notes_for_future"])
        return (working_memory, getattr(evaluation, 'content', str(evaluation)))