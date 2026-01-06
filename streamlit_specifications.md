
## 1. Application Overview

The **PE Org-AI-R Platform** is designed as a foundational UI shell for a private equity firm specializing in AI-ready companies. Its primary purpose is to provide an operational Minimum Viable Product (MVP) for AI-readiness scoring, enabling use cases such as company screening, due diligence, monitoring, and value creation. This application serves as a demonstration of robust system architecture and clear data contracts in an enterprise AI context, aligning with the persona of Alex, a Senior Software Engineer focused on building scalable and reliable AI systems.

The application's story flow unfolds as follows:
1.  **Dashboard Access**: Upon launching, the user (Alex) is presented with the "Portfolio Intelligence Dashboard," which offers a high-level overview of key AI-readiness metrics.
2.  **Company Selection**: Alex can select a target company from a dropdown list, simulating the process of evaluating different portfolio companies.
3.  **AI-Readiness Scoring**: Once a company is selected, the dashboard displays its "Org-AI-R," "V^R (Idiosyncratic)," "H^R (Systematic)," and "Risk Score" metrics. This allows Alex to quickly assess a company's AI maturity and potential. Explanations of the underlying formulas are provided to enhance understanding.
4.  **Supporting Evidence**: A dedicated section indicates where supporting evidence (e.g., from SEC filings, job data) would be displayed, emphasizing the data-driven nature of the platform.
5.  **Developer Tools**: Alex can navigate to a "Developer Tools (API Testing)" section via the sidebar. Here, they can test various API endpoints, such as `/health`, `/v1/companies`, and `/v1/scores/{company_id}`, to validate the integration and data contracts of the backend services. This is crucial for a developer persona to ensure the system's foundational components are working as expected.

This workflow demonstrates how Alex, as a software engineer, interacts with the system to both view critical business metrics and perform technical validation of the underlying API layer, ensuring the system's integrity and readiness for production.

## 2. Code Requirements

### Import Statement

```python
from source import *
import streamlit as st
```

### `st.session_state` Design

`st.session_state` is used to preserve user selections and application state across Streamlit reruns, providing a consistent user experience.

*   **Initialization**:
    ```python
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Portfolio Intelligence Dashboard"
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = "ACME Corp"
    if 'selected_api_endpoint' not in st.session_state:
        st.session_state.selected_api_endpoint = "/health"
    if 'api_test_result' not in st.session_state:
        st.session_state.api_test_result = None
    ```
*   **Update**:
    *   When the "Navigate" `st.selectbox` in the sidebar changes, `st.session_state.selected_page` is updated.
    *   When the "Select Company" `st.selectbox` on the dashboard changes, `st.session_state.selected_company` is updated.
    *   When the "Select Endpoint" `st.selectbox` in the "Developer Tools" section changes, `st.session_state.selected_api_endpoint` is updated, and `st.session_state.api_test_result` is reset to `None`.
    *   When the "Test Endpoint" `st.button` is clicked, `st.session_state.api_test_result` is updated with the mock JSON response.
*   **Read Across Pages (Conditional Rendering)**:
    *   `st.session_state.selected_page` determines which primary content block ("Portfolio Intelligence Dashboard" or "Developer Tools (API Testing)") is rendered.
    *   `st.session_state.selected_company` is used to pre-select the company in the `st.selectbox` and conceptually influence the displayed metrics (though metrics are static placeholders in this MVP).
    *   `st.session_state.selected_api_endpoint` is used to pre-select the API endpoint in the `st.selectbox` within the "Developer Tools" section.
    *   `st.session_state.api_test_result` is read to display the mock JSON response after an API test.

### UI Interactions and `source.py` Function Invocations

The Streamlit app primarily uses UI widgets and markdown to visualize data and simulate interactions. Direct invocations of complex `source.py` functions (like `create_project_structure` or `generate_synthetic_company`) are not required for the immediate display logic as per the MVP requirements specifying placeholder data. `source.py` provides the conceptual models (Pydantic schemas) which the UI implicitly relies on for understanding the data structures that would be exchanged with a real backend.

*   **Company Selection**: The `companies` list for `st.selectbox` is a placeholder list as specified in user requirements. If dynamic generation were needed, `source.py`'s `generate_synthetic_company` could be used to create `Company` objects, but this is not a requirement for the MVP dashboard display.
*   **API Endpoint Testing**: The `st.button("Test Endpoint")` interaction will update `st.session_state.api_test_result` with a mock JSON response. This mock response directly reflects the structure expected from `source.py`'s Pydantic schemas (e.g., a simplified `{"status": "ok", "endpoint": api_endpoint}` for health checks, or if expanded, could align with `Company` or `OrgAIRScore` models). No actual `source.py` function is *called* to generate this mock; it's a hardcoded response simulating a successful API interaction based on the defined contracts.

### Streamlit Application Structure (`app.py`)

```python
# --- Page Configuration ---
st.set_page_config(
    page_title="PE Org-AI-R Platform",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Session State Initialization ---
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Portfolio Intelligence Dashboard"
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "ACME Corp"
if 'selected_api_endpoint' not in st.session_state:
    st.session_state.selected_api_endpoint = "/health"
if 'api_test_result' not in st.session_state:
    st.session_state.api_test_result = None

# --- Sidebar Navigation ---
st.sidebar.title("PE Org-AI-R Platform")
st.sidebar.markdown("---")

# Simulate multi-page experience with conditional rendering
page_options = ["Portfolio Intelligence Dashboard", "Developer Tools (API Testing)"]
selected_page_ui = st.sidebar.selectbox(
    "Navigate",
    page_options,
    index=page_options.index(st.session_state.selected_page)
)

if selected_page_ui != st.session_state.selected_page:
    st.session_state.selected_page = selected_page_ui
    # Reset API test result if navigating away from or to Developer Tools
    if st.session_state.selected_page == "Developer Tools (API Testing)":
        st.session_state.api_test_result = None
    else:
        st.session_state.api_test_result = None # Clear for other pages too

# --- Main Content Area ---
if st.session_state.selected_page == "Portfolio Intelligence Dashboard":
    st.title("Portfolio Intelligence Dashboard")

    st.markdown(
        f"""
        Welcome to the PE Org-AI-R Platform. This system enables:

        - **Screening**: Rapid AI-readiness assessment of target companies
        - **Due Diligence**: Comprehensive scoring across 7 dimensions
        - **Monitoring**: Portfolio-level AI capability tracking
        - **Value Creation**: EBITDA attribution and 100-day planning
        """
    )

    st.subheader("Company Selection")
    companies = ["ACME Corp", "TechStart Inc", "DataFlow Ltd"]
    selected_company_ui = st.selectbox(
        "Select Company",
        companies,
        key="company_selector", # Unique key for this widget
        index=companies.index(st.session_state.selected_company),
        on_change=lambda: st.session_state.update(selected_company=st.session_state.company_selector)
    )

    st.subheader("AI-Readiness Score")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Org-AI-R", "67.3", "+2.1")
    with col2:
        st.metric("V^R (Idiosyncratic)", "72.5", "+1.8")
    with col3:
        st.metric("H^R (Systematic)", "75.0", "0")
    with col4:
        st.metric("Risk Score", "2.3", "-0.2")

    st.markdown(r"$$ \text{Org-AI-R} = w_1 S_1 + w_2 S_2 + \dots + w_7 S_7 $$")
    st.markdown(r"where $\text{Org-AI-R}$ is the overall AI-Readiness score, $w_i$ are dimension weights, and $S_i$ are individual dimension scores.")

    st.markdown(r"$$ V^R = \frac{\text{Company Score}}{\text{Sector Benchmark}} \times 100 $$")
    st.markdown(r"where $V^R$ represents idiosyncratic readiness, comparing a company's performance against its sector benchmark.")

    st.markdown(r"$$ H^R = \text{Systematic Opportunity Baseline} $$")
    st.markdown(r"where $H^R$ reflects the systematic opportunity for AI adoption within the company's sector, based on calibration data.")

    st.subheader("Supporting Evidence")
    st.info("Evidence panel will display citations from SEC filings and job data.")

elif st.session_state.selected_page == "Developer Tools (API Testing)":
    st.title("Developer Tools")
    st.markdown(f"This section allows you to test the underlying API endpoints for the PE Org-AI-R platform.")
    st.markdown(f"As a Software Developer or Data Engineer, you can validate the API contracts directly here.")

    st.markdown("### API Endpoint Testing")
    api_endpoints = ["/health", "/v1/companies", "/v1/scores/{company_id}"]
    selected_endpoint_ui = st.selectbox(
        "Select Endpoint",
        api_endpoints,
        key="api_endpoint_selector", # Unique key for this widget
        index=api_endpoints.index(st.session_state.selected_api_endpoint),
        on_change=lambda: st.session_state.update(selected_api_endpoint=st.session_state.api_endpoint_selector, api_test_result=None)
    )

    if st.button("Test Endpoint"):
        # Mock JSON response as per user requirements
        mock_response = {"status": "ok", "endpoint": st.session_state.selected_api_endpoint}
        st.session_state.api_test_result = mock_response
        st.markdown(f"```python\n# Simulating API call to: {st.session_state.selected_api_endpoint}\n# No actual API call is made in this Streamlit shell.\n```")
        st.markdown(f"Mocking a successful API response based on defined data contracts.")

    if st.session_state.api_test_result:
        st.json(st.session_state.api_test_result)
        st.markdown(f"This JSON response validates the structure and data types that would be expected from the backend API, which are formalized by Pydantic schemas like `Company` or `DimensionScoreInput` from `source.py`.")
```
