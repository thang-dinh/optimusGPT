from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def interpreter_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the output schema
    class interpreter_output_schema(BaseModel):
        objective: str = Field(description="The optimization objective")
        variables: str = Field(description="The decision variables")
        constraints: str = Field(description="The key constraints")
        notes: str = Field(description="Any additional notes or assumptions")

    # Define parser in accordance with schema
    parser = JsonOutputParser(pydantic_object=interpreter_output_schema)

    llm_with_structured_output = llm.with_structured_output(interpreter_output_schema)
    # Define the prompt
    prompt = PromptTemplate(
        template="""You are an expert optimization assistant. Given a user request and a dataset preview, extract: 
        1. The objective (e.g., minimize total distance) 
        2. The decision variable
        3. The key constraints (visit each node once, return to start)
        4. Any additional notes or assumptions.

        {format_instructions}

        Problem Statement: {problem_statement}""",
        input_variables=["problem_statement"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain of runnables.
    chain = prompt | llm | parser
    # Return chain. Can be invoked with .invoke()
    return chain

