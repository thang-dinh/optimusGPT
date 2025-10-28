from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def decision_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the output schema
    class interpreter_output_schema(BaseModel):
        plan: str = Field(description="Description of the new approach to solve the problem")
        consideration: str = Field(description="Considerations based on previous attempts and user feedback to pass along to the solver or interpreter as needed.")
        next_step: str = Field(description="The immediate next step to take in the solution process. Which could be reinterpreting the problem with the new information, solving again with current context, or requesting more information.")
        next_step_definitive: int = Field(description="A definitive step number to take next: 1 for reinterpret problem, 2 for solve again, 3 for request more information.")
        if_step_reinterpret: str = Field(description="Instructions on how to reinterpret the problem if that is the next step. Otherwise leave empty.")
        if_step_solve: str = Field(description="Instructions on how to solve again with current context if that is the next step. Otherwise leave empty.")
        if_step_request: str = Field(description="If requesting more information, specify what information you feel you are lacking, then ask for the specific information needed. Otherwise leave empty.")
        notes: str = Field(description="Any additional notes or assumptions to pass along to further iterations if needed.")

    # Define parser in accordance with schema
    parser = JsonOutputParser(pydantic_object=interpreter_output_schema)

    llm_with_structured_output = llm.with_structured_output(interpreter_output_schema)
    # Define the prompt
    prompt = PromptTemplate(
        template="""You are an expert optimization assistant. A part of a program that helps users solve optimization problems.
        Previous iterations have failed to find satisfactory solutions. Based on the problem statement, previous solution attempts, and user feedback, plan a new approach to solve the problem.

        {format_instructions}

        Original Problem Statement: {problem_statement}
        Previous Solution Attempt: {previous_code_solution}
        Previous Analysis: {previous_self_analysis}
        User Feedback: {user_feedback}""",
        input_variables=["problem_statement", "previous_code_solution", "previous_self_analysis", "user_feedback"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain of runnables.
    chain = prompt | llm | parser
    # Return chain. Can be invoked with .invoke()
    return chain

