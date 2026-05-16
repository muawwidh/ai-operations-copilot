# API Design

This document describes the API design of AI Operations Copilot.

The backend is built with FastAPI and exposes REST APIs for health checks, analytics, AI chat, document intelligence, and report generation.

Base URL for local development:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 1. API Groups

The API is organized into the following groups:

```text
1. Health
2. Analytics
3. AI Chat
4. Documents
5. Reports
```

---

## 2. Health API

### GET `/api/health`

Checks whether the backend service is running.

#### Request

No request body required.

#### Example URL

```text
GET http://127.0.0.1:8000/api/health
```

#### Example Response

```json
{
  "status": "ok",
  "service": "AI Operations Copilot",
  "version": "0.1.0"
}
```

#### Purpose

This endpoint confirms that the FastAPI backend is available.

---

## 3. Analytics APIs

Analytics APIs provide structured business insights from the PostgreSQL database.

---

### GET `/api/analytics/operations-summary`

Returns high-level operations KPIs.

#### Example URL

```text
GET http://127.0.0.1:8000/api/analytics/operations-summary
```

#### Example Response

```json
{
  "total_customers": 100,
  "total_shipments": 1000,
  "delayed_shipments": 269,
  "delay_rate_percent": 26.9,
  "total_support_tickets": 300,
  "open_tickets": 143,
  "high_priority_tickets": 150,
  "sla_breached_tickets": 82,
  "sla_breach_rate_percent": 27.33
}
```

#### Purpose

This endpoint provides an executive-level view of operational performance.

---

### GET `/api/analytics/shipment-delays`

Returns shipment delay analysis.

#### Example URL

```text
GET http://127.0.0.1:8000/api/analytics/shipment-delays
```

#### Example Response

```json
{
  "total_shipments": 1000,
  "delayed_shipments": 269,
  "delay_rate_percent": 26.9,
  "top_delay_reasons": [
    {
      "delay_reason": "Customs Clearance",
      "count": 55,
      "average_delay_days": 3.8
    }
  ],
  "carrier_delay_summary": [
    {
      "carrier": "Aramex",
      "delayed_count": 62,
      "average_delay_days": 4.1
    }
  ],
  "top_delayed_destinations": [
    {
      "destination_city": "Riyadh",
      "delayed_count": 35,
      "average_delay_days": 3.9
    }
  ]
}
```

#### Purpose

This endpoint identifies shipment delay patterns by reason, carrier, and destination.

---

### GET `/api/analytics/ticket-summary`

Returns support ticket and SLA analysis.

#### Example URL

```text
GET http://127.0.0.1:8000/api/analytics/ticket-summary
```

#### Example Response

```json
{
  "total_tickets": 300,
  "sla_breached_tickets": 82,
  "sla_breach_rate_percent": 27.33,
  "high_priority_open_tickets": 25,
  "tickets_by_priority": [
    {
      "priority": "High",
      "count": 80
    }
  ],
  "tickets_by_status": [
    {
      "status": "Open",
      "count": 70
    }
  ],
  "tickets_by_category": [
    {
      "category": "Delivery",
      "count": 90
    }
  ]
}
```

#### Purpose

This endpoint helps support managers understand ticket volume, SLA risk, workload, and issue categories.

---

### GET `/api/analytics/customer-activity`

Returns the most active customers based on shipment count, ticket count, and activity score.

#### Query Parameters

| Parameter | Type    | Required | Description                                   |
| --------- | ------- | -------- | --------------------------------------------- |
| limit     | integer | No       | Number of customers to return. Default is 10. |

#### Example URL

```text
GET http://127.0.0.1:8000/api/analytics/customer-activity?limit=10
```

#### Example Response

```json
{
  "limit": 10,
  "customers": [
    {
      "customer_code": "CUST-0001",
      "customer_name": "Example Trading LLC",
      "customer_tier": "Enterprise",
      "account_status": "Active",
      "shipment_count": 35,
      "ticket_count": 8,
      "activity_score": 59
    }
  ]
}
```

#### Purpose

This endpoint identifies high-activity customers who may require account management attention.

---

## 4. AI Chat API

The AI Chat API allows users to ask natural language business questions.

---

### POST `/api/chat/ask`

Receives a user question and returns an AI-generated answer.

The AI agent can select from approved backend tools such as analytics, document search, and report generation.

#### Example URL

```text
POST http://127.0.0.1:8000/api/chat/ask
```

#### Request Body

```json
{
  "question": "Why are shipments delayed this week?"
}
```

#### Example Response

```json
{
  "interaction_id": 1,
  "question": "Why are shipments delayed this week?",
  "answer": "Shipments are mainly delayed due to customs clearance and carrier capacity issues...",
  "tools_used": [
    "get_shipment_delay_summary"
  ],
  "source_type": "database",
  "tool_outputs": [
    {
      "tool_name": "get_shipment_delay_summary",
      "arguments": {},
      "result": {
        "total_shipments": 1000,
        "delayed_shipments": 269,
        "delay_rate_percent": 26.9
      }
    }
  ]
}
```

#### Purpose

This endpoint is the main conversational AI interface of the system.

---

## 5. Documents APIs

Document APIs support PDF upload, document listing, and document question answering.

---

### POST `/api/documents/upload`

Uploads a PDF document, extracts text, splits it into chunks, creates embeddings, stores metadata in PostgreSQL, and stores vectors in ChromaDB.

#### Request Type

Multipart form data.

#### Field

| Field | Type     | Required | Description            |
| ----- | -------- | -------- | ---------------------- |
| file  | PDF file | Yes      | PDF document to upload |

#### Example Response

```json
{
  "id": 1,
  "file_name": "operations_policy.pdf",
  "file_type": "pdf",
  "processed_status": "Processed",
  "chunks_created": 8,
  "uploaded_at": "2026-05-16T10:30:00"
}
```

#### Purpose

This endpoint prepares uploaded documents for retrieval-augmented generation.

---

### GET `/api/documents`

Returns a list of uploaded documents.

#### Example URL

```text
GET http://127.0.0.1:8000/api/documents
```

#### Example Response

```json
[
  {
    "id": 1,
    "file_name": "operations_policy.pdf",
    "file_type": "pdf",
    "processed_status": "Processed",
    "uploaded_at": "2026-05-16T10:30:00"
  }
]
```

#### Purpose

This endpoint allows the frontend to display uploaded document history.

---

### POST `/api/documents/ask`

Asks a question against uploaded documents using RAG.

#### Example URL

```text
POST http://127.0.0.1:8000/api/documents/ask
```

#### Request Body

```json
{
  "question": "What does the document say about escalation?",
  "top_k": 5
}
```

#### Example Response

```json
{
  "question": "What does the document say about escalation?",
  "answer": "According to the retrieved document context, high-priority issues should be escalated...",
  "retrieved_chunks": [
    {
      "text": "Escalation rules for high-priority operational cases...",
      "metadata": {
        "document_id": 1,
        "chunk_id": 3,
        "file_name": "operations_policy.pdf",
        "chunk_index": 2
      },
      "distance": 0.23
    }
  ]
}
```

#### Purpose

This endpoint allows users to ask questions from uploaded PDF documents.

---

## 6. Reports APIs

Reports APIs support AI-generated business reports.

---

### POST `/api/reports/generate`

Generates and saves an AI-written operations report.

#### Example URL

```text
POST http://127.0.0.1:8000/api/reports/generate
```

#### Request Body

```json
{
  "report_type": "Weekly Operations Report",
  "generated_by": "operations_manager"
}
```

#### Example Response

```json
{
  "id": 1,
  "report_type": "Weekly Operations Report",
  "title": "Weekly Operations Report",
  "content": "# Weekly Operations Report\n\n## Executive Summary\n...",
  "generated_by": "operations_manager",
  "created_at": "2026-05-16T10:45:00",
  "context_preview": {
    "operations_summary": {},
    "shipment_delay_summary": {},
    "ticket_summary": {},
    "customer_activity": {}
  }
}
```

#### Purpose

This endpoint generates management reports using current analytics context.

---

### GET `/api/reports`

Returns report history.

#### Query Parameters

| Parameter | Type    | Required | Description                                 |
| --------- | ------- | -------- | ------------------------------------------- |
| limit     | integer | No       | Number of reports to return. Default is 20. |

#### Example URL

```text
GET http://127.0.0.1:8000/api/reports?limit=20
```

#### Example Response

```json
[
  {
    "id": 1,
    "report_type": "Weekly Operations Report",
    "title": "Weekly Operations Report",
    "generated_by": "operations_manager",
    "created_at": "2026-05-16T10:45:00"
  }
]
```

#### Purpose

This endpoint allows users to view previously generated reports.

---

### GET `/api/reports/{report_id}`

Returns one report by ID.

#### Example URL

```text
GET http://127.0.0.1:8000/api/reports/1
```

#### Example Response

```json
{
  "id": 1,
  "report_type": "Weekly Operations Report",
  "title": "Weekly Operations Report",
  "content": "# Weekly Operations Report\n\n## Executive Summary\n...",
  "generated_by": "operations_manager",
  "created_at": "2026-05-16T10:45:00"
}
```

#### Purpose

This endpoint allows users to view the full content of a selected report.

---

## 7. AI Agent Tools

The AI chat agent can use the following tools:

```text
get_operations_summary
get_shipment_delay_summary
get_ticket_summary
get_customer_activity
search_documents
generate_operations_report
```

The model does not directly access the database. It requests approved tools, and the backend executes those tools safely.

---

## 8. Source Types

AI interactions can have different source types:

```text
general
database
document
mixed
```

Meaning:

- general: no specific backend tool was used
- database: analytics or structured data tool was used
- document: document retrieval was used
- mixed: both document and database tools were used

---

## 9. Error Handling

Common API error scenarios include:

- Backend service not running
- Missing OpenAI API key
- Database connection failure
- Invalid PDF file
- No readable text in PDF
- Empty database
- ChromaDB retrieval issue
- Invalid report ID

The API returns structured HTTP errors through FastAPI.

---

## 10. API Design Summary

The API design follows a modular approach:

- Routes receive and validate requests.
- Services handle business logic.
- Models represent database tables.
- The AI layer handles prompts, LLM calls, embeddings, and tool calling.
- The frontend communicates with the backend only through REST APIs.

This structure makes the system easier to test, maintain, integrate, and expand.