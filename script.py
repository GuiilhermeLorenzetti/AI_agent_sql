import os 
from groq import Groq
import json
from dotenv import load_dotenv

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

question = "Qual o cliente que menos comprou?"

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
    
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Erro ao fazer a requisição para a API: {e}")
    exit(1)