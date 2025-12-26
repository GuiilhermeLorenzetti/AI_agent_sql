# AI Agent SQL Generator

## Project Vision

This project represents the **initial idea of an AI agent** that revolutionizes how we interact with databases. The goal is to create a system that translates natural language questions into SQL queries.

## Core Concept

### What is it?
An AI agent that:
- **Reads table documentation**
- **Generates SQL scripts** automatically based on natural language questions
- **Understands the context** and structure of the database
- **Produces optimized queries** without the need for deep technical knowledge

### Practical Example
Instead of writing:
```sql
SELECT c.customer_id, SUM(s.total_amount) as total_purchases
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id
ORDER BY total_purchases ASC
LIMIT 1;
```

The user simply asks: **"Which customer bought the least?"**

### What is it?
An AI agent that:
- **Reads table documentation**
- **Generates SQL scripts** automatically based on natural language questions
- **Understands the context** and structure of the database
- **Produces optimized queries** without the need for deep technical knowledge

### ✅ **Interactive Interface**
- **Dynamic Input**: User types questions in real-time
- **Clean Output**: Displays only the final generated SQL
- **Automatic Validation**: Ensures only valid SQL is returned

### ✅ **Schema Documentation**
- **Structured JSON**: Table schema in readable format
- **Table Validation**: Verifies existence of columns and tables
- **Dangerous Command Prevention**: Blocks DROP, CREATE, DELETE, etc.

## 🏗️ Current Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input         │    │   Agent         │    │   Validation    │
│   User          │───▶│   Generator     │───▶│   SQL           │
│   (Question)    │    │   (Groq API)    │    │   (Groq API)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Output        │    │   Decision      │    │   Loop          │
│   (Final SQL)   │◀───│   Continue?     │◀───│   Regenerate    │
│                 │    │   (LangGraph)   │    │   if Invalid    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔮 Roadmap and Evolution

### Current Phase (MVP)
- ✅ Reading table documentation via JSON
- ✅ SQL generation via Groq API
- ✅ Natural language processing of questions

### Next Phases

#### 🔄 **Schema Auto-Discovery**
- Agent connects directly to the database
- Automatically reads table structure
- Identifies relationships and constraints
- Updates documentation in real-time

#### 🤖 **Automatic Execution**
- Executes generated queries automatically
- Returns formatted results
- Handles errors and optimizes queries when necessary

## 🌟 Expected Impact

This project has the potential to:
- **Democratize data access** for non-technical users
- **Accelerate analysis**
- **Reduce errors** in SQL queries
- **Standardize** how we interact with databases
- **Bridge the gap** between natural language and structured data
