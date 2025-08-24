# AI Agent SQL Generator

## Visão do Projeto

Este projeto representa a **ideia inicial de um agente de IA** que muda a forma como interagimos com bancos de dados. O objetivo é criar um sistema que traduza perguntas em linguagem natural em consultas SQL.

## Conceito Central

### O que é?
Um agente de IA que:
- **Lê a documentação das tabelas** 
- **Gera scripts SQL** automaticamente baseados em perguntas em linguagem natural
- **Entende o contexto** e estrutura do banco de dados
- **Produz consultas otimizadas** sem necessidade de conhecimento técnico profundo

### Exemplo Prático
Em vez de escrever:
```sql
SELECT c.customer_id, SUM(s.total_amount) as total_compras
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id
ORDER BY total_compras ASC
LIMIT 1;
```

O usuário simplesmente pergunta: **"Qual o cliente que menos comprou?"**

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

#### 👥 **Sistema Multi-Agente**
- **Agente Principal**: Gera as consultas iniciais
- **Agente Validador**: Revisa a sintaxe e lógica das queries
- **Agente Otimizador**: Melhora performance das consultas
- **Agente Analista**: Interpreta e explica os resultados

#### 🧠 **Aprendizado Contínuo**
- Aprende com consultas anteriores
- Adapta-se ao padrão de uso do usuário
- Melhora a precisão baseada no feedback

## 🎨 Arquitetura Visionária

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interface     │    │   Agente        │    │   Banco de      │
│   Natural       │───▶│   Principal     │───▶│   Dados         │
│   Language      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agente        │    │   Agente        │    │   Agente        │
│   Validador     │◀───│   Otimizador    │───▶│   Analista      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 💡 Casos de Uso

### Para Analistas de Dados
- Consultas complexas sem escrever SQL
- Exploração rápida de dados
- Relatórios automáticos

### Para Desenvolvedores
- Prototipagem rápida de queries
- Validação de lógica de negócio
- Documentação automática de consultas

### Para Stakeholders
- Acesso direto aos dados sem intermediários
- Perguntas em linguagem natural
- Insights imediatos

## 🛠️ Tecnologias Atuais

- **Python**: Linguagem principal
- **Groq API**: Modelo de linguagem para geração de SQL
- **JSON**: Documentação de schema das tabelas
- **Environment Variables**: Configuração segura

## 🌟 Impacto Esperado

Este projeto tem o potencial de:
- **Democratizar o acesso a dados** para não-técnicos
- **Acelerar análises** de 80% do tempo atual
- **Reduzir erros** em consultas SQL
- **Padronizar** a forma de interagir com bancos de dados
- **Criar uma ponte** entre linguagem natural e dados estruturados
