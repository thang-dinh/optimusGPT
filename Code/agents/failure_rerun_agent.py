from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def failure_rerun_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the output schema
    class interpreter_output_schema(BaseModel):
        problem_consideration: str = Field(description="Was the code able to finish running? Did it produce an answer? If it did, does the answer seem like it aligns with the problem description.")
        explanation_of_failure: str = Field(description="Provide a detailed explanation of why the solution failed or was unsatisfactory.")
        actionable_instructions: str = Field(description="Outline the next steps to take in order to address the identified issues and move towards a satisfactory solution. This information will be provided to the solver code generator in a second attempt at solving the problem.")

    # Define parser in accordance with schema
    parser = JsonOutputParser(pydantic_object=interpreter_output_schema)

    llm_with_structured_output = llm.with_structured_output(interpreter_output_schema)

    # Define the prompt
    prompt = PromptTemplate(
        template="""
        You are an expert optimization assistant. An optimization problem has been solved with gurobipy code. It has been determined that this solution was either incorrect or unsatisfactory.
        You must determine what part of the process was flawed. First consider each piece of the solving process, and what major problems could have confounded the solution.
        Then consider if the problem was solvable, or if more information is needed to create a satisfactory response to the problem.
        Then provide actionable instructions to the solver code generator to help it create a better solution in a second attempt.

        {format_instructions}
        
        User Prompt: {user_prompt}
        Problem Interpretation and Context: {structured_problem}
        Code: {code}
        Code Output: {code_output}
        Notes created regarding the solution of similar problems in the past: {notes}""",
        input_variables=["user_prompt", "structured_problem", "code", "code_output", "notes"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain of runnables.
    chain = prompt | llm | parser
    # Return chain. Can be invoked with .invoke()
    return chain

