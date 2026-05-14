AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_operations_summary",
            "description": "Get a high-level operations KPI summary including customers, shipments, delays, tickets, and SLA breaches.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_shipment_delay_summary",
            "description": "Analyze shipment delays including delay rate, top delay reasons, carrier delay summary, and delayed destinations.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_summary",
            "description": "Analyze support tickets including priorities, statuses, categories, SLA breaches, and open high-priority tickets.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_activity",
            "description": "Find the most active customers based on shipments, tickets, customer tier, account status, and activity score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of customers to return.",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50,
                    }
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search uploaded PDF documents and retrieve relevant document chunks for answering policy, SOP, or knowledge questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The user question to search against uploaded document content.",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of relevant chunks to retrieve.",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_operations_report",
            "description": "Generate and save an AI-written operations report using current analytics data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_type": {
                        "type": "string",
                        "description": "Type of report to generate.",
                        "default": "Weekly Operations Report",
                    },
                    "generated_by": {
                        "type": "string",
                        "description": "Name of the user or system generating the report.",
                        "default": "agent",
                    },
                },
                "additionalProperties": False,
            },
        },
    },
]