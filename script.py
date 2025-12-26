import os, json, re
from groq import Groq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Check if API key is defined
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check if .env file exists and contains GROQ_API_KEY")

# Check if model is defined, otherwise use default
model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

# Initialize Groq client
cliente = Groq(api_key=api_key)

# Load table documentation
try:
    with open("table_documentation.json", "r", encoding="utf-8") as f:
        table_documentation = json.load(f)
except FileNotFoundError:
    print("Error: table_documentation.json file not found")
    exit(1)
except json.JSONDecodeError:
    print("Error: table_documentation.json has invalid format")
    exit(1)

# Ask user
question = input("Enter your question about the data: ")

# The state that will be shared between agents
class AgentState(TypedDict):
    question: str
    table_documentation: str
    sql_query: str
    validation_result: str
    
def generate_sql_query(state: AgentState):
    print("---SQL Generation Agent---")
    question = state["question"]
    table_documentation = state["table_documentation"]

    message = [
        { 
            "role": "system",
            "content": "You are an assistant that generates SQL queries based on the provided table schema. Do not invent columns or tables that are not in the schema."
        },
        {
            "role": "user",
            "content": f"available tables: {table_documentation} \n\nQuestion:{question}\n\nGenerate only the SQL, without any other text."
        }
    ]  

    try:
        response = cliente.chat.completions.create(
            model=model_name,
            messages=message,
            temperature=0.0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        sql_query = response.choices[0].message.content.strip()
        print(f"Generated SQL: {sql_query}")
        return {"sql_query": sql_query}
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return {"sql_query": "Generation Error"}

def validate_sql(state: AgentState):
    print("\n--- SQL Validation Agent ---")
    sql_query = state["sql_query"]
    table_documentation = state["table_documentation"]

    if "Generation Error" in sql_query:
        print("Validation failed: SQL generation error.")
        return {"validation_result": "invalid"}

    validation_prompt = (
        f"Consider the following table schema: {table_documentation}. "
        f"The following SQL query was generated: '{sql_query}'. "
        "Validate this query. If it is valid and uses only tables and columns existing in the schema and does not contain commands like 'drop', 'create', 'alter', 'truncate', 'insert', 'update', 'delete', answer 'valid'. "
        "If it is invalid (e.g., incorrect syntax, non-existent table/column, disallowed commands), answer 'invalid'. "
        "Generate only the word 'valid' or 'invalid', without any other text."
    )
    
    message = [
        {"role": "user", "content": validation_prompt}
    ]

    try:
        response = cliente.chat.completions.create(
            model=model_name,
            messages=message,
            temperature=0.0,
            max_tokens=100,
        )
        validation_response = response.choices[0].message.content.strip().lower()
        
        if "valid" in validation_response:
            print("Validation result: Valid.")
            return {"validation_result": "valid"}
        else:
            print("Validation result: Invalid.")
            return {"validation_result": "invalid"}
    except Exception as e:
        print(f"Error validating SQL: {e}")
        return {"validation_result": "invalid"}
    
def should_continue(state: AgentState):
    if state["validation_result"] == "valid":
        print("\nSQL validated successfully. End of process.")
        return {"next": "end"}
    else:
        print("\nInvalid SQL. Trying to generate again...")
        return {"next": "regenerate"}

# Building the graph
builder = StateGraph(AgentState)

builder.add_node("generate_sql", generate_sql_query)
builder.add_node("validate_sql", validate_sql)
builder.add_node("should_continue", should_continue)

builder.add_edge(START, "generate_sql")
builder.add_edge("generate_sql", "validate_sql")
builder.add_edge("validate_sql", "should_continue")

# Configuring exit conditions
builder.add_conditional_edges(
    "should_continue",
    lambda x: x["next"],
    {
        "end": END,
        "regenerate": "generate_sql"
    }
)

# Compiling the graph
graph = builder.compile()

# Executing the graph
if __name__ == "__main__":
    initial_state = {
        "question": question,
        "table_documentation": json.dumps(table_documentation, ensure_ascii=False),
        "sql_query": "",
        "validation_result": ""
    }
    
    result = graph.invoke(initial_state)
    print(f"\nFinal SQL: {result['sql_query']}")