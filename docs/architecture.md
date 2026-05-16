# System Architecture

AI Operations Copilot is designed as a modular full-stack AI operations platform. The architecture separates the frontend, backend API, database, AI services, document intelligence pipeline, and deployment layer.

The purpose of this architecture is to make the system maintainable, extensible, testable, and deployment-ready.

---

## 1. Architecture Overview

```text
User
 |
 v
Streamlit Frontend
 |
 v
FastAPI Backend
 |
 +---------------- PostgreSQL Database
 |
 +---------------- OpenAI AI Services
 |
 +---------------- ChromaDB Vector Store
 |
 +---------------- File Upload Storage
```

The user interacts with the Streamlit frontend. The frontend sends API requests to the FastAPI backend. The backend communicates with PostgreSQL for structured data, OpenAI for AI responses and embeddings, and ChromaDB for document vector search.

---

## 2. Main Architecture Layers

The system is divided into six main layers:

```text
1. Frontend Layer
2. API Layer
3. Service Layer
4. Data Layer
5. AI and RAG Layer
6. DevOps Layer
```

---

## 3. Frontend Layer

The frontend is built using Streamlit.

The frontend provides an operational interface for:

- Dashboard analytics
- AI chat assistant
- Document upload
- Document question answering
- Report generation
- Report history

The frontend does not directly access the database. It communicates only with the FastAPI backend through REST APIs.

Frontend location:

```text
frontend/streamlit_app/
```

Main files:

```text
app.py
api_client.py
requirements.txt
Dockerfile
```

---

## 4. API Layer

The backend API is built using FastAPI.

The API layer exposes endpoints for:

- Health check
- Analytics
- AI chat
- Documents
- Reports

Backend location:

```text
backend/app/
```

Main API files:

```text
backend/app/api/routes_health.py
backend/app/api/routes_analytics.py
backend/app/api/routes_chat.py
backend/app/api/routes_documents.py
backend/app/api/routes_reports.py
```

The API layer receives user requests, validates inputs, calls service functions, and returns structured responses.

---

## 5. Service Layer

The service layer contains the main business logic.

Main service files:

```text
backend/app/services/analytics_service.py
backend/app/services/chat_service.py
backend/app/services/document_service.py
backend/app/services/report_service.py
```

Responsibilities:

- Calculate operations KPIs
- Analyze shipment delays
- Analyze support tickets
- Identify customer activity
- Process uploaded documents
- Retrieve relevant document chunks
- Generate AI reports
- Save AI interactions

The service layer keeps business logic separate from API route files.

---

## 6. Data Layer

The data layer is based on PostgreSQL and SQLAlchemy.

PostgreSQL stores structured business data such as:

- Customers
- Shipments
- Support tickets
- Uploaded documents
- Document chunks
- Generated reports
- AI interactions
- System logs

Database models are located in:

```text
backend/app/models/
```

Main models:

```text
customer.py
shipment.py
support_ticket.py
document.py
document_chunk.py
report.py
ai_interaction.py
system_log.py
```

The database connection is configured in:

```text
backend/app/database.py
```

Environment configuration is handled in:

```text
backend/app/config.py
```

---

## 7. AI Layer

The AI layer uses OpenAI models for:

- Natural language response generation
- Business analysis explanations
- Report writing
- Document question answering
- Agent tool calling
- Embedding generation

AI-related files are located in:

```text
backend/app/ai/
```

Main files:

```text
llm_client.py
embeddings.py
prompts.py
tool_schemas.py
agent.py
```

---

## 8. Agent Tool Calling

The agent tool calling layer allows the AI assistant to choose backend tools automatically.

Available tools include:

- get_operations_summary
- get_shipment_delay_summary
- get_ticket_summary
- get_customer_activity
- search_documents
- generate_operations_report

The model does not directly access the database. It requests approved tools, the backend executes those tools safely, and the tool result is passed back to the model for final response generation.

This approach is more controlled and enterprise-friendly than unrestricted database access.

---

## 9. RAG / Document Intelligence Layer

The RAG layer allows the system to answer questions from uploaded PDF documents.

The document pipeline is:

```text
Upload PDF
  |
  v
Save file locally
  |
  v
Extract text using pypdf
  |
  v
Split text into chunks
  |
  v
Save chunk metadata in PostgreSQL
  |
  v
Generate embeddings using OpenAI
  |
  v
Store vectors in ChromaDB
  |
  v
Retrieve relevant chunks
  |
  v
Generate answer using LLM
```

Main files:

```text
backend/app/services/document_service.py
backend/app/utils/pdf_reader.py
backend/app/utils/text_splitter.py
backend/app/ai/embeddings.py
```

ChromaDB stores vector embeddings for semantic search.

PostgreSQL stores document and chunk metadata for traceability.

---

## 10. Report Generation Layer

The report generation layer uses analytics data and AI writing to generate management reports.

Report flow:

```text
User requests report
  |
  v
Backend collects analytics context
  |
  v
Prompt is created
  |
  v
OpenAI generates report
  |
  v
Report is saved in PostgreSQL
  |
  v
Frontend/API displays report
```

Main files:

```text
backend/app/services/report_service.py
backend/app/api/routes_reports.py
backend/app/models/report.py
```

Reports can be generated from the Reports page or through AI chat.

---

## 11. DevOps Layer

Docker Compose is used to run the full system.

Services:

```text
postgres
backend
frontend
```

Main file:

```text
docker-compose.yml
```

Backend Dockerfile:

```text
backend/Dockerfile
```

Frontend Dockerfile:

```text
frontend/streamlit_app/Dockerfile
```

Docker Compose starts:

- PostgreSQL on port 5432
- FastAPI backend on port 8000
- Streamlit frontend on port 8501

---

## 12. Runtime Ports

```text
PostgreSQL: 5432
FastAPI Backend: 8000
Streamlit Frontend: 8501
```

Application URLs:

```text
Backend Health:
http://127.0.0.1:8000/api/health

Backend Swagger:
http://127.0.0.1:8000/docs

Frontend:
http://127.0.0.1:8501
```

---

## 13. Data Flow: Dashboard

```text
User opens Dashboard
  |
  v
Streamlit calls FastAPI analytics endpoints
  |
  v
FastAPI calls analytics_service.py
  |
  v
SQLAlchemy queries PostgreSQL
  |
  v
Analytics JSON returned to frontend
  |
  v
Streamlit displays metrics and charts
```

---

## 14. Data Flow: AI Chat

```text
User asks question
  |
  v
Streamlit sends question to /api/chat/ask
  |
  v
FastAPI calls chat_service.py
  |
  v
Agent decides which tool to use
  |
  v
Backend executes selected tool
  |
  v
Tool result sent back to LLM
  |
  v
LLM generates final answer
  |
  v
Answer saved in ai_interactions table
  |
  v
Frontend displays response
```

---

## 15. Data Flow: Document Q&A

```text
User uploads PDF
  |
  v
Backend extracts text
  |
  v
Text is split into chunks
  |
  v
Chunks saved in PostgreSQL
  |
  v
Embeddings saved in ChromaDB
  |
  v
User asks question
  |
  v
Question is embedded
  |
  v
Relevant chunks retrieved
  |
  v
LLM answers using document context
```

---

## 16. Architecture Summary

This architecture separates responsibilities clearly.

- Frontend handles user interaction.
- Backend handles APIs and business logic.
- PostgreSQL handles structured data.
- ChromaDB handles vector search.
- OpenAI handles language understanding and generation.
- Docker handles consistent runtime setup.

The result is a maintainable architecture that can evolve from an MVP into a larger enterprise AI operations platform.