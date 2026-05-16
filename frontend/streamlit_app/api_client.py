import os

import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_operations_summary():
    response = requests.get(f"{API_BASE_URL}/api/analytics/operations-summary")
    response.raise_for_status()
    return response.json()


def get_shipment_delays():
    response = requests.get(f"{API_BASE_URL}/api/analytics/shipment-delays")
    response.raise_for_status()
    return response.json()


def get_ticket_summary():
    response = requests.get(f"{API_BASE_URL}/api/analytics/ticket-summary")
    response.raise_for_status()
    return response.json()


def get_customer_activity(limit: int = 10):
    response = requests.get(
        f"{API_BASE_URL}/api/analytics/customer-activity",
        params={"limit": limit},
    )
    response.raise_for_status()
    return response.json()


def ask_ai(question: str):
    response = requests.post(
        f"{API_BASE_URL}/api/chat/ask",
        json={"question": question},
    )
    response.raise_for_status()
    return response.json()


def upload_document(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/api/documents/upload",
        files=files,
    )
    response.raise_for_status()
    return response.json()


def list_documents():
    response = requests.get(f"{API_BASE_URL}/api/documents")
    response.raise_for_status()
    return response.json()


def ask_documents(question: str, top_k: int = 5):
    response = requests.post(
        f"{API_BASE_URL}/api/documents/ask",
        json={
            "question": question,
            "top_k": top_k,
        },
    )
    response.raise_for_status()
    return response.json()


def generate_report(
    report_type: str = "Weekly Operations Report",
    generated_by: str = "streamlit_user",
):
    response = requests.post(
        f"{API_BASE_URL}/api/reports/generate",
        json={
            "report_type": report_type,
            "generated_by": generated_by,
        },
    )
    response.raise_for_status()
    return response.json()


def list_reports(limit: int = 20):
    response = requests.get(
        f"{API_BASE_URL}/api/reports",
        params={"limit": limit},
    )
    response.raise_for_status()
    return response.json()


def get_report(report_id: int):
    response = requests.get(f"{API_BASE_URL}/api/reports/{report_id}")
    response.raise_for_status()
    return response.json()