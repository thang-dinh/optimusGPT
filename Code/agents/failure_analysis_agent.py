from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def verification_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the output schema
    class interpreter_output_schema(BaseModel):
        problem_consideration: str = Field(description="Was the code able to finish running? Did it produce an answer? If it did, does the answer seem like it aligns with the problem description.")
        output_succesful: bool = Field(description="Has a satisfactory answer been found? If yes, answer 'True', else output 'False'.")

    # Define parser in accordance with schema
    parser = JsonOutputParser(pydantic_object=interpreter_output_schema)

    llm_with_structured_output = llm.with_structured_output(interpreter_output_schema)

    # Define the prompt
    prompt = PromptTemplate(
        template="""
        You are an expert optimization assistant. An optimization problem has been solved with gurobipy code. Your task is to check the solution for correctness and completeness.
        If the problem has not been fully solved, identify if the problem lies in the problem interpretation, the approach the code took to solve the problem, or if there were errors in the code execution.
        Provide a concise summary of your findings.

        {format_instructions}
        
        Problem Statement: {formatted_problem}
        Problem Interpretation and Context: {structured_problem}
        Code: {code}
        Code Output: {solution}
        Notes created regarding the solution of similar problems in the past: {notes}""",
        input_variables=["formatted_problem", "structured_problem", "code", "solution", "notes"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain of runnables.
    chain = prompt | llm 
    # Return chain. Can be invoked with .invoke()
    return chain

