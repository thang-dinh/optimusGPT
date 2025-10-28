from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def self_check_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


    # Define the prompt
    prompt = PromptTemplate(
        template="""
        You are an expert optimization agent. Given the following optimization problem and its solution, generate a concise summary of the solution approach and key results.
        In your summary, verify the solution's correctness and highlight any assumptions made.
        Include any relevant metrics or performance indicators, and discuss potential implications or applications of the solution such as trade-offs, scalability, or real-world impact.
        Keep discussion concise and overall report as short as possible. If there are no relevant considerations for the user, simply state "No additional considerations."
        
        Problem Statement: {formatted_problem}
        Solution: {solution}""",
        input_variables=["formatted_problem", "solution"]
    )

    # Chain of runnables.
    chain = prompt | llm 
    # Return chain. Can be invoked with .invoke()
    return chain

