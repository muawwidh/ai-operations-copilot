# Database Schema

This document explains the database schema used in AI Operations Copilot.

The system uses PostgreSQL as the main relational database. SQLAlchemy is used as the ORM layer in the FastAPI backend.

The database stores structured business data, document metadata, generated reports, and AI interaction history.

---

## 1. Database Overview

Database name:

```text
ai_operations_copilot
```

Main tables:

```text
customers
shipments
support_tickets
documents
document_chunks
reports
ai_interactions
system_logs
```

---

## 2. Entity Relationship Overview

```text
customers
   |
   +---- shipments
   |
   +---- support_tickets

documents
   |
   +---- document_chunks

reports

ai_interactions

system_logs
```

A customer can have many shipments.

A customer can have many support tickets.

A document can have many document chunks.

Reports, AI interactions, and system logs are independent tracking tables.

---

## 3. customers Table

The `customers` table stores customer master data.

### Purpose

This table represents companies or clients using the operations/logistics service.

### Main Fields

| Field          | Type     | Description                                         |
| -------------- | -------- | --------------------------------------------------- |
| id             | Integer  | Primary key                                         |
| customer_code  | String   | Unique customer code                                |
| customer_name  | String   | Customer/company name                               |
| industry       | String   | Customer industry                                   |
| country        | String   | Customer country                                    |
| city           | String   | Customer city                                       |
| customer_tier  | String   | Customer tier such as Standard, Premium, Enterprise |
| account_status | String   | Active, At Risk, or Inactive                        |
| created_at     | DateTime | Record creation timestamp                           |

### Relationships

```text
customers.id → shipments.customer_id
customers.id → support_tickets.customer_id
```

### Example Use

This table is used to calculate customer activity and identify high-value or high-activity customers.

---

## 4. shipments Table

The `shipments` table stores shipment and delivery records.

### Purpose

This table represents shipment operations and delivery performance.

### Main Fields

| Field                 | Type     | Description                                        |
| --------------------- | -------- | -------------------------------------------------- |
| id                    | Integer  | Primary key                                        |
| shipment_code         | String   | Unique shipment code                               |
| customer_id           | Integer  | Foreign key to customers                           |
| origin_city           | String   | Shipment origin city                               |
| destination_city      | String   | Shipment destination city                          |
| carrier               | String   | Carrier or logistics provider                      |
| shipment_status       | String   | Created, In Transit, Delivered, Delayed, Cancelled |
| priority              | String   | Low, Normal, High, Critical                        |
| planned_delivery_date | Date     | Planned delivery date                              |
| actual_delivery_date  | Date     | Actual delivery date                               |
| delay_days            | Integer  | Number of delay days                               |
| delay_reason          | String   | Reason for delay                                   |
| shipping_cost         | Numeric  | Shipping cost                                      |
| created_at            | DateTime | Record creation timestamp                          |

### Relationships

```text
shipments.customer_id → customers.id
```

### Example Use

This table is used for:

- Delay rate calculation
- Top delay reasons
- Carrier performance analysis
- Delayed destination analysis
- Operations summary metrics

---

## 5. support_tickets Table

The `support_tickets` table stores customer support and service tickets.

### Purpose

This table represents customer complaints, service issues, SLA risks, and support workload.

### Main Fields

| Field        | Type     | Description                                    |
| ------------ | -------- | ---------------------------------------------- |
| id           | Integer  | Primary key                                    |
| ticket_code  | String   | Unique ticket code                             |
| customer_id  | Integer  | Foreign key to customers                       |
| subject      | String   | Ticket subject                                 |
| description  | Text     | Ticket details                                 |
| priority     | String   | Low, Medium, High, Critical                    |
| status       | String   | Open, In Progress, Resolved, Closed            |
| category     | String   | Delivery, Billing, Technical, Account, Product |
| created_at   | DateTime | Ticket creation timestamp                      |
| resolved_at  | DateTime | Resolution timestamp                           |
| sla_due_at   | DateTime | SLA due timestamp                              |
| sla_breached | Boolean  | Whether SLA was breached                       |
| sentiment    | String   | Positive, Neutral, Negative                    |

### Relationships

```text
support_tickets.customer_id → customers.id
```

### Example Use

This table is used for:

- SLA breach analysis
- Ticket category analysis
- Priority distribution
- Open ticket monitoring
- Customer activity scoring

---

## 6. documents Table

The `documents` table stores uploaded document metadata.

### Purpose

This table tracks PDF documents uploaded for document intelligence and RAG.

### Main Fields

| Field            | Type     | Description                   |
| ---------------- | -------- | ----------------------------- |
| id               | Integer  | Primary key                   |
| file_name        | String   | Original uploaded file name   |
| file_type        | String   | File type, currently PDF      |
| file_path        | String   | Local storage path            |
| processed_status | String   | Pending, Processed, or Failed |
| uploaded_at      | DateTime | Upload timestamp              |

### Relationships

```text
documents.id → document_chunks.document_id
```

### Example Use

This table is used to display uploaded document history and processing status.

---

## 7. document_chunks Table

The `document_chunks` table stores extracted document text chunks.

### Purpose

This table stores chunk-level document text metadata. The actual vectors are stored in ChromaDB.

### Main Fields

| Field             | Type     | Description                    |
| ----------------- | -------- | ------------------------------ |
| id                | Integer  | Primary key                    |
| document_id       | Integer  | Foreign key to documents       |
| chunk_index       | Integer  | Order of chunk in the document |
| chunk_text        | Text     | Extracted text chunk           |
| chroma_collection | String   | ChromaDB collection name       |
| created_at        | DateTime | Chunk creation timestamp       |

### Relationships

```text
document_chunks.document_id → documents.id
```

### Example Use

This table supports traceability between uploaded documents, text chunks, and retrieved RAG context.

---

## 8. reports Table

The `reports` table stores AI-generated business reports.

### Purpose

This table saves generated reports so users can view report history.

### Main Fields

| Field        | Type     | Description                             |
| ------------ | -------- | --------------------------------------- |
| id           | Integer  | Primary key                             |
| report_type  | String   | Type of report                          |
| title        | String   | Report title                            |
| content      | Text     | AI-generated report content in Markdown |
| generated_by | String   | User/system that generated the report   |
| created_at   | DateTime | Report generation timestamp             |

### Example Use

This table is used by the Reports page to show report history and report details.

---

## 9. ai_interactions Table

The `ai_interactions` table stores AI chat history.

### Purpose

This table records user questions, AI responses, tools used, and source type.

### Main Fields

| Field         | Type     | Description                           |
| ------------- | -------- | ------------------------------------- |
| id            | Integer  | Primary key                           |
| user_question | Text     | User question                         |
| ai_response   | Text     | AI-generated answer                   |
| tools_used    | String   | Backend tools used by the agent       |
| source_type   | String   | general, database, document, or mixed |
| created_at    | DateTime | Interaction timestamp                 |

### Example Use

This table is useful for audit history, debugging, analytics, and future conversation tracking.

---

## 10. system_logs Table

The `system_logs` table stores backend system log records.

### Purpose

This table can be used for application monitoring and troubleshooting.

### Main Fields

| Field       | Type     | Description            |
| ----------- | -------- | ---------------------- |
| id          | Integer  | Primary key            |
| log_level   | String   | INFO, WARNING, ERROR   |
| module_name | String   | Module or service name |
| message     | Text     | Log message            |
| created_at  | DateTime | Log timestamp          |

### Example Use

This table can later support an admin dashboard or monitoring page.

---

## 11. Main Relationships

### Customer to Shipments

```text
One customer can have many shipments.
```

```text
customers.id = shipments.customer_id
```

### Customer to Support Tickets

```text
One customer can have many support tickets.
```

```text
customers.id = support_tickets.customer_id
```

### Document to Document Chunks

```text
One document can have many chunks.
```

```text
documents.id = document_chunks.document_id
```

---

## 12. Data Generation

Synthetic operational data is generated for:

- Customers
- Shipments
- Support tickets

Seed scripts are located in:

```text
backend/app/seed/
```

Main seed file:

```text
backend/app/seed/seed_database.py
```

Run seed inside Docker:

```bash
docker compose exec backend python app/seed/seed_database.py
```

Run seed manually:

```bash
cd backend
source .venv/bin/activate
python app/seed/seed_database.py
```

---

## 13. Database Creation

Tables are created using:

```text
backend/scripts/create_tables.py
```

Run inside Docker:

```bash
docker compose exec backend python scripts/create_tables.py
```

Run manually:

```bash
cd backend
source .venv/bin/activate
python scripts/create_tables.py
```

---

## 14. Database Design Summary

The schema is designed to support:

- Operations analytics
- Shipment performance monitoring
- Support ticket analysis
- Customer activity scoring
- Document intelligence
- AI report generation
- AI interaction logging
- Future audit and monitoring features

The schema is designed for an MVP while remaining extensible for enterprise integrations, audit tracking, reporting, and advanced analytics.