import pandas as pd
import requests
import streamlit as st

from api_client import (
    ask_ai,
    ask_documents,
    generate_report,
    get_customer_activity,
    get_operations_summary,
    get_report,
    get_shipment_delays,
    get_ticket_summary,
    list_documents,
    list_reports,
    upload_document,
)


st.set_page_config(
    page_title="AI Operations Copilot",
    page_icon="🤖",
    layout="wide",
)


def show_header():
    st.title("AI Operations Copilot")
    st.caption(
        "Enterprise-style AI assistant for operations analytics, support intelligence, documents, and reporting."
    )


def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), None
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to FastAPI backend. Make sure it is running on http://127.0.0.1:8000."
    except requests.exceptions.HTTPError as error:
        return None, f"Backend error: {error.response.text}"
    except Exception as error:
        return None, str(error)


def dashboard_page():
    st.header("Operations Dashboard")

    summary, error = safe_call(get_operations_summary)

    if error:
        st.error(error)
        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customers", summary["total_customers"])
    col2.metric("Shipments", summary["total_shipments"])
    col3.metric("Delayed Shipments", summary["delayed_shipments"])
    col4.metric("Delay Rate", f'{summary["delay_rate_percent"]}%')

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Support Tickets", summary["total_support_tickets"])
    col6.metric("Open Tickets", summary["open_tickets"])
    col7.metric("High Priority", summary["high_priority_tickets"])
    col8.metric("SLA Breach Rate", f'{summary["sla_breach_rate_percent"]}%')

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Shipment Delay Reasons")
        delay_data, error = safe_call(get_shipment_delays)

        if error:
            st.warning(error)
        else:
            df_reasons = pd.DataFrame(delay_data["top_delay_reasons"])
            if not df_reasons.empty:
                st.bar_chart(df_reasons.set_index("delay_reason")["count"])
                st.dataframe(df_reasons, use_container_width=True)
            else:
                st.info("No delayed shipments found.")

    with right:
        st.subheader("Ticket Categories")
        ticket_data, error = safe_call(get_ticket_summary)

        if error:
            st.warning(error)
        else:
            df_categories = pd.DataFrame(ticket_data["tickets_by_category"])
            if not df_categories.empty:
                st.bar_chart(df_categories.set_index("category")["count"])
                st.dataframe(df_categories, use_container_width=True)
            else:
                st.info("No tickets found.")

    st.divider()

    st.subheader("Most Active Customers")
    customer_data, error = safe_call(get_customer_activity, 10)

    if error:
        st.warning(error)
    else:
        df_customers = pd.DataFrame(customer_data["customers"])
        st.dataframe(df_customers, use_container_width=True)


def chat_page():
    st.header("AI Chat Assistant")
    st.caption("Ask operational questions. The agent can use analytics, documents, and report tools.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant"):
            st.write(item["answer"])

            if item.get("tools_used"):
                st.caption(f"Tools used: {', '.join(item['tools_used'])}")

    question = st.chat_input("Ask something like: Why are shipments delayed this week?")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result, error = safe_call(ask_ai, question)

            if error:
                st.error(error)
                return

            st.write(result["answer"])

            if result.get("tools_used"):
                st.caption(f"Tools used: {', '.join(result['tools_used'])}")

            with st.expander("Debug: Tool Outputs"):
                st.json(result.get("tool_outputs", []))

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": result["answer"],
                "tools_used": result.get("tools_used", []),
            }
        )


def documents_page():
    st.header("Document Intelligence")
    st.caption("Upload PDF documents and ask questions using RAG.")

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
    )

    if uploaded_file and st.button("Upload and Process Document"):
        with st.spinner("Uploading, extracting text, chunking, and embedding..."):
            result, error = safe_call(upload_document, uploaded_file)

        if error:
            st.error(error)
        else:
            st.success("Document processed successfully.")
            st.json(result)

    st.divider()

    st.subheader("Uploaded Documents")

    documents, error = safe_call(list_documents)

    if error:
        st.warning(error)
    else:
        if documents:
            st.dataframe(pd.DataFrame(documents), use_container_width=True)
        else:
            st.info("No documents uploaded yet.")

    st.divider()

    st.subheader("Ask a Document Question")

    question = st.text_input(
        "Question",
        placeholder="Example: What does the policy say about escalation?",
    )

    top_k = st.slider("Number of chunks to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Ask Documents"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching documents and generating answer..."):
                result, error = safe_call(ask_documents, question, top_k)

            if error:
                st.error(error)
            else:
                st.subheader("Answer")
                st.write(result["answer"])

                with st.expander("Retrieved Chunks"):
                    st.json(result["retrieved_chunks"])


def reports_page():
    st.header("Reports")
    st.caption("Generate and view AI-written operations reports.")

    st.subheader("Generate New Report")

    report_type = st.text_input(
        "Report Type",
        value="Weekly Operations Report",
    )

    generated_by = st.text_input(
        "Generated By",
        value="streamlit_user",
    )

    if st.button("Generate Report"):
        with st.spinner("Generating AI report..."):
            result, error = safe_call(generate_report, report_type, generated_by)

        if error:
            st.error(error)
        else:
            st.success(f"Report generated. ID: {result['id']}")
            st.markdown(result["content"])

            with st.expander("Analytics Context Used"):
                st.json(result["context_preview"])

    st.divider()

    st.subheader("Report History")

    reports, error = safe_call(list_reports, 50)

    if error:
        st.warning(error)
        return

    if not reports:
        st.info("No reports generated yet.")
        return

    df_reports = pd.DataFrame(reports)
    st.dataframe(df_reports, use_container_width=True)

    report_ids = [report["id"] for report in reports]
    selected_id = st.selectbox("Select report to view", report_ids)

    if st.button("View Selected Report"):
        report, error = safe_call(get_report, selected_id)

        if error:
            st.error(error)
        else:
            st.subheader(report["title"])
            st.caption(f"Generated by {report['generated_by']} on {report['created_at']}")
            st.markdown(report["content"])


def main():
    show_header()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Chat",
            "Documents",
            "Reports",
        ],
    )

    if page == "Dashboard":
        dashboard_page()

    elif page == "AI Chat":
        chat_page()

    elif page == "Documents":
        documents_page()

    elif page == "Reports":
        reports_page()


if __name__ == "__main__":
    main()