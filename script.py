import os, json, re
from groq import Groq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se a API key está definida
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada. Verifique se o arquivo .env existe e contém a variável GROQ_API_KEY")

# Verifica se o modelo está definido, senão usa um padrão
model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

# Inicializa o cliente Groq
cliente = Groq(api_key=api_key)

# Carrega a documentação das tabelas
try:
    with open("table_documentation.json", "r", encoding="utf-8") as f:
        table_documentation = json.load(f)
except FileNotFoundError:
    print("Erro: arquivo table_documentation.json não encontrado")
    exit(1)
except json.JSONDecodeError:
    print("Erro: arquivo table_documentation.json com formato inválido")
    exit(1)

# Pergunta ao usuário
question = input("Digite sua pergunta sobre os dados: ")

# O estado que será compartilhado entre os agentes 
class AgentState(TypedDict):
    question: str
    table_documentation: str
    sql_query: str
    validation_result: str
    
def generate_sql_query(state: AgentState):
    print("---Agente de Geração de SQL---")
    question = state["question"]
    table_documentation = state["table_documentation"]

    message = [
        { 
            "role": "system",
            "content": "Você é um assistente que gera consultas SQL baseadas no schema de tabelas fornecido. Não invente colunas ou tabelas que não estão no schema."
        },
        {
            "role": "user",
            "content": f"tabelas disponiveis: {table_documentation} \n\nPergunta:{question}\n\nGere apenas o SQL, sem nenhum outro texto."
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
        print(f"SQL gerado: {sql_query}")
        return {"sql_query": sql_query}
    except Exception as e:
        print(f"Erro ao gerar SQL: {e}")
        return {"sql_query": "Erro na geração"}

def validate_sql(state: AgentState):
    print("\n--- Agente Validador de SQL ---")
    sql_query = state["sql_query"]
    table_documentation = state["table_documentation"]

    if "Erro na geração" in sql_query:
        print("Validação falhou: Erro na geração do SQL.")
        return {"validation_result": "invalid"}

    validation_prompt = (
        f"Considere o seguinte schema de tabelas: {table_documentation}. "
        f"A seguinte consulta SQL foi gerada: '{sql_query}'. "
        "Valide esta consulta. Se ela for válida e utilizar apenas tabelas e colunas que existem no schema e se não existem comandos como 'drop', 'create', 'alter', 'truncate', 'insert', 'update', 'delete', responda 'válido'. "
        "Se for inválida (ex: sintaxe incorreta, tabela/coluna inexistente, comandos não permitidos), responda 'inválido'. "
        "Gere apenas a palavra 'válido' ou 'inválido', sem nenhum outro texto."
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
        
        if "válido" in validation_response:
            print("Resultado da validação: Válido.")
            return {"validation_result": "valid"}
        else:
            print("Resultado da validação: Inválido.")
            return {"validation_result": "invalid"}
    except Exception as e:
        print(f"Erro ao validar SQL: {e}")
        return {"validation_result": "invalid"}
    
def should_continue(state: AgentState):
    if state["validation_result"] == "valid":
        print("\nSQL validado com sucesso. Fim do processo.")
        return {"next": "end"}
    else:
        print("\nSQL inválido. Tentando gerar novamente...")
        return {"next": "regenerate"}

# Construindo o grafo 
builder = StateGraph(AgentState)

builder.add_node("generate_sql", generate_sql_query)
builder.add_node("validate_sql", validate_sql)
builder.add_node("should_continue", should_continue)

builder.add_edge(START, "generate_sql")
builder.add_edge("generate_sql", "validate_sql")
builder.add_edge("validate_sql", "should_continue")

# Configurando as condições de saída
builder.add_conditional_edges(
    "should_continue",
    lambda x: x["next"],
    {
        "end": END,
        "regenerate": "generate_sql"
    }
)

# Compilando o grafo
graph = builder.compile()

# Executando o grafo
if __name__ == "__main__":
    initial_state = {
        "question": question,
        "table_documentation": json.dumps(table_documentation, ensure_ascii=False),
        "sql_query": "",
        "validation_result": ""
    }
    
    result = graph.invoke(initial_state)
    print(f"\nSQL Final: {result['sql_query']}")