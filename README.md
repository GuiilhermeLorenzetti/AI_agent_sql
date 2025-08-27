# AI Agent SQL Generator

## Visão do Projeto

Este projeto implementa um **agente de IA inteligente** que traduz perguntas em linguagem natural em consultas SQL usando um sistema multi-agente baseado em LangGraph. O sistema gera e valida consultas SQL automaticamente.

## 🚀 Funcionalidades Implementadas

### Exemplo Prático
Em vez de escrever:
```sql
SELECT c.customer_name, SUM(s.total_amount) as total_compras
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_compras ASC
LIMIT 1;

O usuário simplesmente pergunta: **"Qual o cliente que menos comprou?"**

### O que é?
Um agente de IA que:
- **Lê a documentação das tabelas** 
- **Gera scripts SQL** automaticamente baseados em perguntas em linguagem natural
- **Entende o contexto** e estrutura do banco de dados
- **Produz consultas otimizadas** sem necessidade de conhecimento técnico profundo

### ✅ **Interface Interativa**
- **Input Dinâmico**: O usuário digita perguntas em tempo real
- **Output Limpo**: Exibe apenas o SQL final gerado
- **Validação Automática**: Garante que apenas SQL válido seja retornado

### ✅ **Documentação de Schema**
- **JSON Estruturado**: Schema das tabelas em formato legível
- **Validação de Tabelas**: Verifica existência de colunas e tabelas
- **Prevenção de Comandos Perigosos**: Bloqueia DROP, CREATE, DELETE, etc.

## 🏗️ Arquitetura Atual

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input         │    │   Agente        │    │   Validação     │
│   Usuário       │───▶│   Gerador       │───▶│   SQL           │
│   (Pergunta)    │    │   (Groq API)    │    │   (Groq API)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Output        │    │   Decisão       │    │   Loop          │
│   (SQL Final)   │◀───│   Continuar?    │◀───│   Regenerar     │
│                 │    │   (LangGraph)   │    │   se Inválido   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔮 Roadmap e Evolução

### Fase Atual (MVP)
- ✅ Leitura de documentação de tabelas via JSON
- ✅ Geração de SQL via API Groq
- ✅ Processamento de perguntas em linguagem natural

### Próximas Fases

#### 🔄 **Auto-Descoberta de Schema**
- O agente conecta diretamente ao banco de dados
- Lê automaticamente a estrutura das tabelas
- Identifica relacionamentos e constraints
- Atualiza a documentação em tempo real

#### 🤖 **Execução Automática**
- Executa as consultas geradas automaticamente
- Retorna resultados formatados
- Trata erros e otimiza queries quando necessário

## 🌟 Impacto Esperado

Este projeto tem o potencial de:
- **Democratizar o acesso a dados** para não-técnicos
- **Acelerar análises** 
- **Reduzir erros** em consultas SQL
- **Padronizar** a forma de interagir com bancos de dados
- **Criar uma ponte** entre linguagem natural e dados estruturados
