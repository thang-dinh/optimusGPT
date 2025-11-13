from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def solver_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


    # Define the prompt
    prompt = PromptTemplate(
        template="""
        You are an expert python coding agent. Using the gurobipy library, generate code to solve the following optimization problem.
        Include necessary imports and ensure the code is executable in a Python environment with gurobipy installed.
        Do not import any other libraries. Use comments to explain each step of the code.
        Do not include any additional text or explanations outside of the code.
        The code will be run exactly as provided so ensure it is complete and correct.
        Problem Statement: {structured_problem}
        Additional notes from previous attempts on similar problems: {notes}""",
        input_variables=["structured_problem", "notes"]
    )

    # Chain of runnables.
    chain = prompt | llm 
    # Return chain. Can be invoked with .invoke()
    return chain

