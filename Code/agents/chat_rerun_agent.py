from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
from pydantic import BaseModel, Field

def chat_rerun_chain():
    # Create the LLM instance
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define the prompt
    prompt = PromptTemplate(
        template="""You are an expert optimization assistant. An optimization problem has been solved with gurobipy code. 
        You will be 

        Memory of the problem solving attempts so far: {memory}
        Evaluation of the previous attempts: {evaluation}
        Human input regarding the problem: {user_input}""",
        input_variables=["memory", "evaluation", "user_input"],
    )

    # Chain of runnables.
    chain = prompt | llm 
    # Return chain. Can be invoked with .invoke()
    return chain

