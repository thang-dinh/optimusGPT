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
        seen_catagory: bool = Field(description="Whether the problem fits into an already seen catagory. 'True' if it has. 'False' otherwise")
        problem_catagory: str = Field(description="The catagory of optimization problem. Only the name of the catagory, to be made a file name, or used to access an existing file.")
        objective: str = Field(description="The optimization objective")
        variables: str = Field(description="The decision variables")
        constraints: str = Field(description="The key constraints")
        extra_info: str = Field(description="Any additional notes or assumptions")

    # Define parser in accordance with schema
    parser = JsonOutputParser(pydantic_object=interpreter_output_schema)

    llm_with_structured_output = llm.with_structured_output(interpreter_output_schema)
    # Define the prompt
    prompt = PromptTemplate(
        template="""You are an expert optimization assistant. Given a user optimization problem extract: 
        1. Whether the problem fits into an already seen catagory of optimization problems.
        2. If the problem fits into a known catagory, specify which catagory. Otherwise state the name of the new catagory. The catagory should be as broad as possible, ex. Scheduling, Traveling Salesman Problem, Investing.
        3. The objective (E.g. minimize cost, maximize profit, create schedule, etc.)
        4. The variables involved
        5. The key constraints
        6. Any additional information needed to properly define the optimization problem.

        {format_instructions}

        Problem Statement: {problem_statement}
        Problem catagories already seen: {problem_catagories}""",
        input_variables=["problem_statement", "problem_catagories"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain of runnables.
    chain = prompt | llm | parser
    # Return chain. Can be invoked with .invoke()
    return chain

