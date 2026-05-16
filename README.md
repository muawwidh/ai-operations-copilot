# AI Operations Copilot

AI Operations Copilot is a full-stack AI-powered business operations assistant designed for logistics, support, analytics, document intelligence, and management reporting.

The system acts as an AI operations analyst inside an organization. It can analyze structured operational data, answer business questions, retrieve knowledge from uploaded PDF documents, generate management reports, and use agent-style tool calling to select the correct backend capability.

---

## 1. Project Overview

Organizations often manage operational data across multiple systems such as shipment platforms, support ticketing tools, customer databases, internal reports, and policy documents. Business users need timely answers, but they often depend on analysts, developers, or manual reporting cycles.

AI Operations Copilot addresses this by providing an intelligent assistant that can:

- Analyze operational KPIs
- Explain shipment delays
- Summarize support ticket and SLA risks
- Identify high-activity customers
- Answer questions from uploaded documents
- Generate management reports
- Use backend tools through AI agent tool calling

The platform is built using FastAPI, PostgreSQL, OpenAI, ChromaDB, Streamlit, and Docker.

---

## 2. Main Capabilities

### Operations Analytics

The system provides analytics APIs and dashboard views for:

- Total customers
- Total shipments
- Delayed shipments
- Delay rate
- Support tickets
- Open tickets
- High-priority tickets
- SLA breach rate
- Shipment delay reasons
- Carrier delay summary
- Ticket categories
- Customer activity

### AI Chat Assistant

The AI chat assistant allows users to ask business questions such as:

- Why are shipments delayed this week?
- Summarize the support ticket situation.
- Which customers are most active?
- Generate a weekly operations report.
- What does the uploaded document say about escalation?

The assistant uses tool calling to decide which backend function should be used for each question.

### Document Intelligence / RAG

The system supports PDF-based document intelligence.

It can:

- Upload PDF documents
- Extract readable text from PDFs
- Split extracted content into chunks
- Generate embeddings
- Store vectors in ChromaDB
- Retrieve relevant chunks
- Answer questions using retrieved document context

### AI Report Generation

The system generates AI-written business reports using analytics context from the database.

Generated reports are saved in PostgreSQL and can be viewed later from the frontend or API.

### Streamlit Frontend

The frontend is built with Streamlit and includes:

- Dashboard page
- AI Chat page
- Documents page
- Reports page

### Dockerized Runtime

Docker Compose runs the complete application stack:

- PostgreSQL database
- FastAPI backend
- Streamlit frontend

This provides a consistent runtime environment for development, demonstration, and deployment preparation.

---

## 3. Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- OpenAI API
- ChromaDB
- pypdf

### Frontend

- Streamlit
- Pandas
- Requests

### Database

- PostgreSQL

### AI / RAG

- OpenAI Chat Model
- OpenAI Embeddings
- ChromaDB Vector Store
- Prompt Engineering
- Agent Tool Calling
- Retrieval-Augmented Generation

### DevOps

- Docker
- Docker Compose
- GitHub

---

## 4. System Architecture

```text
Streamlit Frontend
        |
        v
FastAPI Backend
        |
        +---------------- PostgreSQL
        |                    |
        |                    +-- customers
        |                    +-- shipments
        |                    +-- support_tickets
        |                    +-- documents
        |                    +-- document_chunks
        |                    +-- reports
        |                    +-- ai_interactions
        |                    +-- system_logs
        |
        +---------------- AI Layer
        |                    |
        |                    +-- OpenAI Chat Model
        |                    +-- Prompt Templates
        |                    +-- Agent Tool Calling
        |
        +---------------- RAG Layer
                             |
                             +-- PDF Text Extraction
                             +-- Text Chunking
                             +-- Embeddings
                             +-- ChromaDB
                             +-- Document Q&A
```

---

## 5. Project Folder Structure

```text
ai-operations-copilot/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── seed/
│   │   ├── services/
│   │   └── utils/
│   ├── scripts/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   └── streamlit_app/
│       ├── app.py
│       ├── api_client.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── docs/
│   ├── architecture.md
│   ├── api-design.md
│   ├── database-schema.md
│   ├── demo-guide.md
│   └── future-roadmap.md
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## 6. Environment Configuration

Create a root-level `.env` file:

```bash
cp .env.example .env
```

Set the required environment variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The `.env` file must not be committed to source control.

---

## 7. Run with Docker Compose

Build and start all services:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up --build -d
```

Verify running containers:

```bash
docker ps
```

Expected services:

```text
ai_operations_postgres
ai_operations_backend
ai_operations_frontend
```

Application URLs:

```text
Backend Swagger: http://127.0.0.1:8000/docs
Backend Health:  http://127.0.0.1:8000/api/health
Frontend:        http://127.0.0.1:8501
```

---

## 8. Database Initialization

Create database tables:

```bash
docker compose exec backend python scripts/create_tables.py
```

Seed operational data:

```bash
docker compose exec backend python app/seed/seed_database.py
```

Verify analytics output:

```text
GET /api/analytics/operations-summary
```

---

## 9. Local Development Setup

Start PostgreSQL through Docker:

```bash
docker compose up -d postgres
```

Start the backend:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Start the Streamlit frontend in a separate terminal:

```bash
cd frontend/streamlit_app
source .venv/bin/activate
streamlit run app.py
```

---

## 10. Main API Endpoints

### Health

```text
GET /api/health
```

### Analytics

```text
GET /api/analytics/operations-summary
GET /api/analytics/shipment-delays
GET /api/analytics/ticket-summary
GET /api/analytics/customer-activity
```

### AI Chat

```text
POST /api/chat/ask
```

### Documents

```text
POST /api/documents/upload
GET  /api/documents
POST /api/documents/ask
```

### Reports

```text
POST /api/reports/generate
GET  /api/reports
GET  /api/reports/{report_id}
```

---

## 11. Example AI Questions

```text
Why are shipments delayed this week?
```

```text
Summarize the support ticket situation and SLA risks.
```

```text
Which customers are most active?
```

```text
Give me a high-level operations performance overview.
```

```text
Generate a weekly operations report for management.
```

```text
According to the uploaded document, what are the main rules?
```

---

## 12. Dockerization Strategy

Dockerization packages the backend, frontend, database connection setup, dependencies, environment configuration, and runtime behavior into a consistent environment.

This is valuable because the application has multiple services that must run together:

- PostgreSQL database
- FastAPI backend
- Streamlit frontend
- ChromaDB persistence
- File upload storage
- OpenAI configuration

Docker Compose allows the complete application stack to start with a single command:

```bash
docker compose up --build
```

Docker is especially useful when the project needs to be shared, demonstrated, deployed, or reproduced on another machine.

---

## 13. Current Project Status

Completed:

- FastAPI backend foundation
- PostgreSQL database setup
- SQLAlchemy data models
- Synthetic data generation
- Analytics APIs
- AI chat endpoint
- AI agent tool calling
- PDF document upload
- PDF text extraction
- Document chunking
- Embedding generation
- ChromaDB vector storage
- Document Q&A
- AI report generation
- Report history
- Streamlit frontend
- Docker Compose setup

---

## 14. Future Improvements

Planned improvements:

- Authentication
- Role-based access control
- React or Next.js frontend
- Report export to PDF and DOCX
- Scheduled weekly reports
- Email report delivery
- Advanced LangGraph workflows
- Cloud deployment
- ERP, CRM, ticketing, and logistics integrations
- Monitoring and logging dashboard
- Admin dashboard
- Audit dashboard

---

## 15. Portfolio Summary

AI Operations Copilot demonstrates how modern AI can be integrated into enterprise operations. It combines backend APIs, structured data analytics, document intelligence, RAG, AI tool calling, report generation, frontend dashboards, and Docker-based deployment.

The project shows practical experience in full-stack development, AI integration, business analytics, system design, and production-style application architecture.
