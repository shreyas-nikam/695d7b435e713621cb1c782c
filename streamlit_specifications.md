
# Architecting the PE Org-AI-R Platform

## 1. Application Overview

This Streamlit application serves as an interactive guide for **Alex, a Senior Software Engineer at PE Org-AI-R Platform**, to establish the foundational architecture for an AI Readiness Assessment system. It focuses on the critical Week 1 tasks of defining system architecture, data contracts, and engineering practices, moving beyond mere model development to building production-ready AI.

The application guides Alex through a structured workflow, simulating the key engineering tasks:

1.  **Understanding the Vision**: The journey begins with an overview of the PE Org-AI-R Platform's mission and the overarching importance of robust engineering discipline for successfully deploying enterprise AI.
2.  **Setting up the Project Environment**: Alex will simulate the initialization of a standardized monorepo directory structure. This step highlights how a well-organized codebase is fundamental for managing complexity and adhering to industry best practices in large-scale AI projects.
3.  **Defining Core Data Schemas**: Through Pydantic models, Alex learns to define clear, unambiguous data contracts for key entities like companies, dimension scores, and sector calibrations. This section emphasizes schema as a critical tool for data integrity.
4.  **Enforcing Data Integrity**: Interactive forms demonstrate Pydantic's powerful validation capabilities. Alex can experiment with various inputs to see how the system automatically enforces data rules and surfaces validation errors, acting as a crucial guardrail against data quality issues.
5.  **Generating Formal Data Contracts**: The application showcases how to automatically generate machine-readable JSON Schemas directly from Pydantic models. This illustrates the principle of contract-first development, ensuring all downstream services and consumers have a universal, explicit data contract.
6.  **Generating Synthetic Data**: Finally, Alex explores how to generate realistic, schema-compliant synthetic data. This accelerates API development, UI prototyping, and early-stage feature testing, reducing reliance on potentially scarce or sensitive real-world data and avoiding "prototype purgatory."

Each step reinforces the principles of building scalable, maintainable, and reliable enterprise AI systems by prioritizing architecture, clear data contracts, and disciplined engineering practices, providing a hands-on experience of how to transition AI from notebooks to production.

## 2. Code Requirements

### Import Statements

The Streamlit application (`app.py`) will begin by importing necessary libraries and all required functions and classes directly from the `source.py` file, as specified.

```python
import streamlit as st
import pandas as pd
from datetime import date
from decimal import Decimal
import json
import os
import shutil # Used by create_project_structure within source.py

# Import all necessary components from the provided source.py
from source import (
    create_project_structure,
    CompanyStatus, OwnershipType, DimensionName,
    DEFAULT_WEIGHTS,
    CompanyBase, CompanyCreate, Company, CompanyDetail,
    DimensionScoreInput, DimensionScoreResult,
    SectorCalibration,
    generate_synthetic_company,
    generate_synthetic_dimension_score_input,
    generate_synthetic_sector_calibration,
    ValidationError # For catching Pydantic validation errors
)
```

### Streamlit Page Configuration

The application's initial layout and title are set using `st.set_page_config`.

```python
st.set_page_config(
    page_title="Architecting the PE Org-AI-R Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### `st.session_state` Design

The following `st.session_state` keys will be initialized at the start of the application. These keys are crucial for preserving state across user interactions and simulating a multi-page experience by storing user inputs, function outputs, and navigation choices.

```python
# Helper function to safely display JSON or plain text
def display_json_or_text(data):
    if data is None:
        return
    try:
        # Attempt to parse and display as pretty JSON
        st.json(json.loads(data))
    except (json.JSONDecodeError, TypeError):
        # If not valid JSON, display as a code block (for errors/raw text)
        st.code(data, language="text")

# Initialize session state variables
# Navigation
if 'page' not in st.session_state:
    st.session_state.page = "Introduction"

# 1. Project Environment Setup Page State
if 'project_structure_created' not in st.session_state:
    st.session_state.project_structure_created = False
if 'project_root_path' not in st.session_state:
    st.session_state.project_root_path = "src/pe_orgair" # Matches source.py default

# 3. Enforcing Data Integrity Page Forms and Outputs
# CompanyCreate Form Inputs & Output
if 'company_create_name' not in st.session_state: st.session_state.company_create_name = "InnovateAI Solutions"
if 'company_create_ticker' not in st.session_state: st.session_state.company_create_ticker = "IAS"
if 'company_create_domain' not in st.session_state: st.session_state.company_create_domain = "innovateai.com"
if 'company_create_sector_id' not in st.session_state: st.session_state.company_create_sector_id = "tech_ai"
if 'company_create_ev' not in st.session_state: st.session_state.company_create_ev = 120000000.50
if 'company_create_ev_currency' not in st.session_state: st.session_state.company_create_ev_currency = "USD"
if 'company_create_ev_as_of_date' not in st.session_state: st.session_state.company_create_ev_as_of_date = date.today()
if 'company_create_ownership_type' not in st.session_state: st.session_state.company_create_ownership_type = OwnershipType.TARGET.value
if 'company_create_output' not in st.session_state: st.session_state.company_create_output = None # Stores result (JSON string) or error message (string)

# DimensionScoreInput Form Inputs & Output
if 'dim_score_dimension' not in st.session_state: st.session_state.dim_score_dimension = DimensionName.DATA_INFRASTRUCTURE.value
if 'dim_score_score' not in st.session_state: st.session_state.dim_score_score = 85.50
if 'dim_score_confidence' not in st.session_state: st.session_state.dim_score_confidence = "high"
if 'dim_score_rationale' not in st.session_state: st.session_state.dim_score_rationale = "Strong data pipeline and governance policies observed."
if 'dim_score_evidence_ids' not in st.session_state: st.session_state.dim_score_evidence_ids = "ev_id_001,ev_id_002"
if 'dim_score_output' not in st.session_state: st.session_state.dim_score_output = None # Stores result (JSON string) or error message (string)

# SectorCalibration Form Inputs & Output
if 'sector_cal_id' not in st.session_state: st.session_state.sector_cal_id = "tech_ai"
if 'sector_cal_name' not in st.session_state: st.session_state.sector_cal_name = "Technology & AI"
if 'sector_cal_h_r_baseline' not in st.session_state: st.session_state.sector_cal_h_r_baseline = 78.0
if 'sector_cal_h_r_ci_lower' not in st.session_state: st.session_state.sector_cal_h_r_ci_lower = 70.0
if 'sector_cal_h_r_ci_upper' not in st.session_state: st.session_state.sector_cal_h_r_ci_upper = 85.0
if 'sector_cal_effective_date' not in st.session_state: st.session_state.sector_cal_effective_date = date.today()
if 'sector_cal_weights_input' not in st.session_state: st.session_state.sector_cal_weights_input = json.dumps({dim.value: float(weight) for dim, weight in DEFAULT_WEIGHTS.items()}, indent=2) # Editable JSON string
if 'sector_cal_targets_input' not in st.session_state: st.session_state.sector_cal_targets_input = json.dumps({dim.value: 75.0 for dim in DimensionName}, indent=2) # Editable JSON string
if 'sector_cal_output' not in st.session_state: st.session_state.sector_cal_output = None # Stores result (JSON string) or error message (string)

# 4. Generating Formal Data Contracts Page State
if 'json_schema_company' not in st.session_state: st.session_state.json_schema_company = None
if 'json_schema_dimension_score_input' not in st.session_state: st.session_state.json_schema_dimension_score_input = None
if 'json_schema_sector_calibration' not in st.session_state: st.session_state.json_schema_sector_calibration = None

# 5. Generating Synthetic Data Page State
if 'synth_data_sector_id' not in st.session_state: st.session_state.synth_data_sector_id = "software_dev"
if 'synth_data_sector_name' not in st.session_state: st.session_state.synth_data_sector_name = "Software Development"
if 'synthetic_company_data' not in st.session_state: st.session_state.synthetic_company_data = None
if 'synthetic_score_input_data' not in st.session_state: st.session_state.synthetic_score_input_data = None
if 'synthetic_sector_calibration_data' not in st.session_state: st.session_state.synthetic_sector_calibration_data = None
```

### Application Structure and Flow

The application simulates a multi-page experience using a `st.selectbox` in the sidebar for navigation. Each selected option conditionally renders a different section of the `app.py` file.

#### Sidebar Navigation

```python
st.sidebar.title("PE Org-AI-R Platform")
st.sidebar.markdown("---")
page_options = [
    "Introduction",
    "1. Project Environment Setup",
    "2. Defining Core Data Schemas",
    "3. Enforcing Data Integrity",
    "4. Generating Formal Data Contracts",
    "5. Generating Synthetic Data"
]
selected_page = st.sidebar.selectbox("Navigate to Section", page_options, key="page")

st.sidebar.markdown("---")
st.sidebar.info("Persona: Alex, a Senior Software Engineer.\n\nMission: Architect the AI Readiness Assessment system for PE Org-AI-R Platform.")
```

#### Page Content (Conditional Rendering Logic)

##### **Page: Introduction**

*   **Purpose**: Provides the user (Alex) with a high-level overview of the PE Org-AI-R platform's mission and the critical engineering principles for enterprise AI.
*   **Markdown**:
    ```python
    if st.session_state.page == "Introduction":
        st.title("Introduction: Architecting the PE Org-AI-R Platform")
        st.markdown(f"As Alex, a Senior Software Engineer at PE Org-AI-R Platform, your mission is to build the foundational architecture for a new AI Readiness Assessment system. This system will evaluate potential portfolio companies across critical dimensions, providing data-driven insights for investment and value creation strategies.")
        st.markdown(f"")
        st.markdown(f"In the world of enterprise AI, it's often said: **\"AI that lives in notebooks dies in production.\"** This platform's success hinges on robust system architecture, clear data contracts, and disciplined engineering practices, not just sophisticated models.")
        st.markdown(f"")
        st.markdown(f"This application guides you through the initial steps to lay down the platform skeleton and define core data schemas using Pydantic, ensuring data integrity and setting the stage for future sprints. This is where APIs and schemas act as contracts between teams and modules, a crucial step in preventing data chaos and integration debt.")
        st.markdown(f"")
        st.subheader("Core Objectives for Week 1: Platform Foundation")
        st.markdown(f"- Initialize a monorepo with CI/CD capabilities.")
        st.markdown(f"- Define core Pydantic models for data structures.")
        st.markdown(f"- Scaffold a FastAPI application with stub routes for companies, scores, and health.")
        st.markdown(f"- Implement a basic Streamlit application (`src/ui/app.py`) to serve as a UI shell.")
        st.markdown(f"- Ensure the Streamlit application can be run locally via `streamlit run src/ui/app.py`.")
        st.markdown(f"")
        st.info("Use the sidebar navigation to proceed through Alex's architectural journey.")
    ```

##### **Page: 1. Project Environment Setup**

*   **Purpose**: Guides Alex through setting up the foundational monorepo structure, emphasizing its role in managing complexity and adhering to best practices.
*   **Markdown**: `## 1. Setting Up the Project Environment and Structure`
*   **Widgets**: `st.button` to trigger structure creation/verification, `st.markdown` and `st.success`/`st.warning`/`st.error` for feedback.
*   **Function Invocation**:
    *   `create_project_structure(base_path=st.session_state.project_root_path)`: Called to (re)create the directory structure.
    *   `os.path.exists()`: Used to verify the existence of key directories.
    *   `shutil.rmtree("src")`: Called to simulate the idempotent cleanup from the original notebook's project setup.
*   **Session State Update**: `st.session_state.project_structure_created` is set to `True` on successful creation.
*   **Session State Read**: `st.session_state.project_structure_created` is read to show appropriate messages and verification.

```python
elif st.session_state.page == "1. Project Environment Setup":
    st.title("1. Setting Up the Project Environment and Structure")
    st.markdown(f"Alex begins by preparing the development environment and establishing a standardized directory structure. This structure is vital for managing complexity in a growing enterprise AI system, separating concerns, and aligning with industry best practices for monorepos.")
    st.markdown(f"")

    project_root = st.session_state.project_root_path

    st.subheader("Action: Initialize Project Structure")
    st.markdown(f"Click the button below to simulate the creation of the foundational directory structure for the PE Org-AI-R Platform monorepo under `{project_root}`. The original notebook logic includes cleaning up any existing `src` directory to ensure idempotency for a fresh setup.")

    if st.button("Create/Verify Project Structure"):
        try:
            # Replicate the notebook's idempotent behavior: remove 'src' if it exists.
            if os.path.exists("src"):
                st.info(f"Existing 'src' directory found. Removing for a clean setup...")
                shutil.rmtree("src")
                st.session_state.project_structure_created = False # Reset state after cleanup

            create_project_structure(base_path=project_root)
            st.session_state.project_structure_created = True
            st.success("Project structure created successfully!")
        except Exception as e:
            st.error(f"Error creating project structure: {e}")

    # Display verification status
    if st.session_state.project_structure_created or os.path.exists(project_root):
        st.subheader("Verification of Key Directories:")
        key_dirs = [
            f"{project_root}/schemas/v1",
            f"{project_root}/api/routes",
            f"{project_root}/services/scoring",
            f"{project_root}/schemas/v1/exports"
        ]
        all_exist = True
        for d in key_dirs:
            exists = os.path.exists(d)
            status_icon = "✅" if exists else "❌"
            st.markdown(f"- {status_icon} `{d}` exists")
            if not exists:
                all_exist = False
        if all_exist:
            st.success("All critical project directories are in place, demonstrating successful repository initialization.")
        else:
            st.warning("Some critical directories are missing. Please try recreating the structure.")
    else:
        st.info("Project structure not yet verified or created. Click the button above to begin.")

    st.markdown(f"")
    st.markdown(f"Alex has now established the fundamental folder structure for the PE Org-AI-R platform. This adheres to the **separation of concerns** principle, which prevents failures in large systems by organizing code into distinct, manageable parts. This systematic initialization reduces technical debt from the outset, ensuring future development can proceed efficiently.")
```

##### **Page: 2. Defining Core Data Schemas**

*   **Purpose**: Demonstrates how Pydantic models define robust data contracts, providing an overview of key enums and data structures.
*   **Markdown**: `## 2. Defining Core Data Schemas with Pydantic`
*   **Widgets**: `st.json` to display enum values and default weights, `st.code` to show JSON schemas of the models. `st.markdown` for explanations.
*   **Function Invocation**: None directly from user interaction, as Pydantic models are defined upon `source.py` import. We use `model_json_schema()` to display their structure.
*   **Session State Update**: N/A on this page.
*   **Session State Read**: N/A on this page.

```python
elif st.session_state.page == "2. Defining Core Data Schemas":
    st.title("2. Defining Core Data Schemas with Pydantic")
    st.markdown(f"Alex moves on to defining the core data structures that will represent the entities within the AI Readiness Assessment system. Pydantic models are chosen for their ability to define clear data contracts (schemas) with built-in validation, which is critical for ensuring data quality across different system components and preventing **prototype purgatory**.")
    st.markdown(f"")

    st.subheader("Pydantic Enums: Standardizing Categorical Data")
    st.markdown(f"Enums provide a way to define a set of named constant values, ensuring consistency and preventing typos across the codebase.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**`CompanyStatus`**")
        st.json({s.name: s.value for s in CompanyStatus})
    with col2:
        st.markdown(f"**`OwnershipType`**")
        st.json({o.name: o.value for o in OwnershipType})
    with col3:
        st.markdown(f"**`DimensionName`** (7 AI Readiness Dimensions)")
        st.json({d.name: d.value for d in DimensionName})

    st.subheader("Default Dimension Weights")
    st.markdown(f"These weights represent the default importance of each AI readiness dimension, which can be overridden by specific sector calibrations. A crucial invariant is that the sum of these weights must be 1.0.")
    st.markdown(r"$$ \sum_{d \in \text{DimensionName}} W_d = 1.0 $$")
    st.markdown(r"where $W_d$ is the weight assigned to dimension $d$.")
    st.json({dim.value: float(weight) for dim, weight in DEFAULT_WEIGHTS.items()})

    st.subheader("Core Pydantic Models Overview")
    st.markdown(f"Below are summaries of the key Pydantic models defined in `source.py` that establish the data contracts for our platform. Each `BaseModel` specifies expected data types, required fields, and validation rules.")

    st.markdown(f"**`Company` Model:** Defines the full structure for companies within the system, including system-generated fields like `company_id` and timestamps.")
    st.code(json.dumps(Company.model_json_schema(by_alias=True, indent=2)), language="json")

    st.markdown(f"**`DimensionScoreInput` Model:** Defines the structure for submitting individual dimension scores, including score range validation and confidence levels.")
    st.code(json.dumps(DimensionScoreInput.model_json_schema(by_alias=True, indent=2)), language="json")

    st.markdown(f"**`SectorCalibration` Model:** Captures sector-specific baselines and dimension weights. This model enforces a critical business rule: **the sum of dimension weights must be 1.0**, keeping scoring consistent across sectors and preventing misalignment between data science and operations.")
    st.code(json.dumps(SectorCalibration.model_json_schema(by_alias=True, indent=2)), language="json")

    st.markdown(f"")
    st.success("These models define the unambiguous contracts that ensure data quality and integration across all PE Org-AI-R platform components.")
```

##### **Page: 3. Enforcing Data Integrity**

*   **Purpose**: Allows Alex to interactively test Pydantic's validation rules using forms, demonstrating how schemas act as guardrails.
*   **Markdown**: `## 3. Enforcing Data Integrity through Schema Validation`
*   **Widgets**: `st.form` containing `st.text_input`, `st.number_input`, `st.selectbox`, `st.date_input`, `st.text_area` for each model (`CompanyCreate`, `DimensionScoreInput`, `SectorCalibration`). `st.form_submit_button` to trigger validation. Output displayed via `display_json_or_text`.
*   **Function Invocation**: `CompanyCreate(**data)`, `DimensionScoreInput(**data)`, `SectorCalibration(**data)`. These calls are wrapped in `try-except ValidationError` blocks.
*   **Session State Update**: The validated model's JSON string or the `ValidationError` message is stored in `st.session_state.company_create_output`, `st.session_state.dim_score_output`, or `st.session_state.sector_cal_output`.
*   **Session State Read**: The stored outputs are read and displayed to the user.

```python
elif st.session_state.page == "3. Enforcing Data Integrity":
    st.title("3. Enforcing Data Integrity through Schema Validation")
    st.markdown(f"Pydantic provides strong automatic validation to prevent invalid or malformed data from entering the system. Alex can use this to ensure that all data flowing through the platform adheres to the defined contracts, catching errors early and preventing brittle orchestration.")
    st.markdown(f"")

    st.subheader("Interactive Data Validation Examples")
    st.markdown(f"Experiment with the forms below to see Pydantic's validation in action. Try entering both valid and invalid data (e.g., scores outside 0-100, or weights that don't sum to 1.0) to observe how it enforces data integrity.")

    # --- CompanyCreate Validation Form ---
    st.markdown(f"### Validate `CompanyCreate` Model")
    with st.form("company_create_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Company Name", value=st.session_state.company_create_name, key="company_name_input")
            ticker = st.text_input("Ticker (Optional)", value=st.session_state.company_create_ticker, key="company_ticker_input")
            domain = st.text_input("Domain (Optional)", value=st.session_state.company_create_domain, key="company_domain_input")
            sector_id = st.text_input("Sector ID", value=st.session_state.company_create_sector_id, key="company_sector_id_input")
            ownership_type = st.selectbox("Ownership Type", options=[o.value for o in OwnershipType], index=[o.value for o in OwnershipType].index(st.session_state.company_create_ownership_type), key="company_ownership_type_input")
        with col2:
            enterprise_value = st.number_input("Enterprise Value (Optional, >=0)", value=st.session_state.company_create_ev, min_value=0.0, format="%.2f", key="company_ev_input")
            ev_currency = st.text_input("EV Currency (max 3 chars)", value=st.session_state.company_create_ev_currency, max_chars=3, key="company_ev_currency_input")
            ev_as_of_date = st.date_input("EV As Of Date (Optional)", value=st.session_state.company_create_ev_as_of_date, key="company_ev_date_input")

        submitted_company = st.form_submit_button("Validate CompanyCreate")
        if submitted_company:
            try:
                company_data = {
                    "name": name,
                    "ticker": ticker if ticker else None,
                    "domain": domain if domain else None,
                    "sector_id": sector_id,
                    "enterprise_value": Decimal(str(enterprise_value)) if enterprise_value is not None else None,
                    "ev_currency": ev_currency,
                    "ev_as_of_date": ev_as_of_date,
                    "ownership_type": ownership_type
                }
                valid_company = CompanyCreate(**company_data)
                st.session_state.company_create_output = valid_company.model_dump_json(indent=2)
                st.success("CompanyCreate data is valid!")
            except ValidationError as e:
                st.session_state.company_create_output = f"Validation Error:\n{e}"
                st.error("Invalid CompanyCreate data.")
            except Exception as e:
                st.session_state.company_create_output = f"An unexpected error occurred: {e}"
                st.error("An unexpected error occurred.")
    display_json_or_text(st.session_state.company_create_output)
    st.markdown(f"---")

    # --- DimensionScoreInput Validation Form ---
    st.markdown(f"### Validate `DimensionScoreInput` Model")
    with st.form("dim_score_form"):
        col1, col2 = st.columns(2)
        with col1:
            dimension = st.selectbox("Dimension", options=[d.value for d in DimensionName], index=[d.value for d in DimensionName].index(st.session_state.dim_score_dimension), key="dim_score_dim_input")
            score = st.number_input("Score (0-100)", value=st.session_state.dim_score_score, min_value=0.0, max_value=100.0, format="%.2f", key="dim_score_score_input")
            confidence_level = st.selectbox("Confidence Level", options=["high", "medium", "low"], index=["high", "medium", "low"].index(st.session_state.dim_score_confidence), key="dim_score_confidence_input")
        with col2:
            rationale = st.text_area("Rationale (Optional, max 1000 chars)", value=st.session_state.dim_score_rationale, max_chars=1000, key="dim_score_rationale_input")
            evidence_chunk_ids_str = st.text_input("Evidence Chunk IDs (comma-separated)", value=st.session_state.dim_score_evidence_ids, key="dim_score_evidence_input")

        submitted_score = st.form_submit_button("Validate DimensionScoreInput")
        if submitted_score:
            try:
                evidence_ids = [e.strip() for e in evidence_chunk_ids_str.split(',') if e.strip()] if evidence_chunk_ids_str else []
                score_data = {
                    "dimension": dimension,
                    "score": Decimal(str(score)),
                    "confidence_level": confidence_level,
                    "rationale": rationale if rationale else None,
                    "evidence_chunk_ids": evidence_ids
                }
                valid_score = DimensionScoreInput(**score_data)
                st.session_state.dim_score_output = valid_score.model_dump_json(indent=2)
                st.success("DimensionScoreInput data is valid!")
            except ValidationError as e:
                st.session_state.dim_score_output = f"Validation Error:\n{e}"
                st.error("Invalid DimensionScoreInput data.")
            except Exception as e:
                st.session_state.dim_score_output = f"An unexpected error occurred: {e}"
                st.error("An unexpected error occurred.")
    display_json_or_text(st.session_state.dim_score_output)
    st.markdown(f"---")

    # --- SectorCalibration Validation Form ---
    st.markdown(f"### Validate `SectorCalibration` Model")
    with st.form("sector_cal_form"):
        col1, col2 = st.columns(2)
        with col1:
            sector_id = st.text_input("Sector ID", value=st.session_state.sector_cal_id, key="sector_cal_id_input")
            sector_name = st.text_input("Sector Name", value=st.session_state.sector_cal_name, key="sector_cal_name_input")
            h_r_baseline = st.number_input("H^R Baseline (0-100)", value=st.session_state.sector_cal_h_r_baseline, min_value=0.0, max_value=100.0, format="%.2f", key="sector_cal_baseline_input")
            h_r_ci_lower = st.number_input("H^R CI Lower (Optional, 0-100)", value=st.session_state.sector_cal_h_r_ci_lower, min_value=0.0, max_value=100.0, format="%.2f", key="sector_cal_ci_lower_input")
            h_r_ci_upper = st.number_input("H^R CI Upper (Optional, 0-100)", value=st.session_state.sector_cal_h_r_ci_upper, min_value=0.0, max_value=100.0, format="%.2f", key="sector_cal_ci_upper_input")
        with col2:
            effective_date = st.date_input("Effective Date", value=st.session_state.sector_cal_effective_date, key="sector_cal_date_input")
            st.markdown(f"**Dimension Weights (JSON):** Must sum to 1.0. (e.g., use `DEFAULT_WEIGHTS` from `source.py`)")
            weights_input_str = st.text_area("Weights (JSON)", value=st.session_state.sector_cal_weights_input, height=150, key="sector_cal_weights_input_area")
            st.markdown(f"**Dimension Targets (JSON):**")
            targets_input_str = st.text_area("Targets (JSON)", value=st.session_state.sector_cal_targets_input, height=150, key="sector_cal_targets_input_area")

        submitted_sector_cal = st.form_submit_button("Validate SectorCalibration")
        if submitted_sector_cal:
            try:
                weights_dict = json.loads(weights_input_str)
                targets_dict = json.loads(targets_input_str)
                # Convert string keys to DimensionName enum and values to Decimal
                weights_enum_keys = {DimensionName(k): Decimal(str(v)) for k, v in weights_dict.items()}
                targets_enum_keys = {DimensionName(k): Decimal(str(v)) for k, v in targets_dict.items()}

                sector_cal_data = {
                    "sector_id": sector_id,
                    "sector_name": sector_name,
                    "h_r_baseline": Decimal(str(h_r_baseline)),
                    "h_r_ci_lower": Decimal(str(h_r_ci_lower)) if h_r_ci_lower is not None else None,
                    "h_r_ci_upper": Decimal(str(h_r_ci_upper)) if h_r_ci_upper is not None else None,
                    "weights": weights_enum_keys,
                    "targets": targets_enum_keys,
                    "effective_date": effective_date
                }
                valid_sector_cal = SectorCalibration(**sector_cal_data)
                st.session_state.sector_cal_output = valid_sector_cal.model_dump_json(indent=2)
                st.success("SectorCalibration data is valid!")
            except ValidationError as e:
                st.session_state.sector_cal_output = f"Validation Error:\n{e}"
                st.error("Invalid SectorCalibration data.")
            except json.JSONDecodeError as e:
                st.session_state.sector_cal_output = f"JSON parsing error in weights or targets: {e}. Please ensure valid JSON format."
                st.error("Invalid JSON format for weights or targets.")
            except ValueError as e: # Catch enum conversion errors or other value issues
                st.session_state.sector_cal_output = f"Value Error: {e}. Ensure DimensionName keys are correct and values are numeric."
                st.error("A value error occurred, check dimension names or data types.")
            except Exception as e:
                st.session_state.sector_cal_output = f"An unexpected error occurred: {e}"
                st.error("An unexpected error occurred.")
    display_json_or_text(st.session_state.sector_cal_output)

    st.markdown(f"")
    st.markdown(f"By explicitly surfacing validation errors, the schemas act as strong guardrails against data issues that often lead to brittle orchestration and **ML technical debt**.")
```

##### **Page: 4. Generating Formal Data Contracts**

*   **Purpose**: Illustrates contract-first development by showing how Pydantic models can be converted into universal JSON Schemas.
*   **Markdown**: `## 4. Generating Formal Data Contracts (JSON Schemas)`
*   **Widgets**: `st.button` to trigger schema generation, `st.json` to display the generated schemas.
*   **Function Invocation**: `Company.model_json_schema()`, `DimensionScoreInput.model_json_schema()`, `SectorCalibration.model_json_schema()`.
*   **Session State Update**: The generated JSON schema dictionaries are stored in `st.session_state.json_schema_company`, `st.session_state.json_schema_dimension_score_input`, and `st.session_state.json_schema_sector_calibration`.
*   **Session State Read**: The stored JSON schemas are read and displayed.

```python
elif st.session_state.page == "4. Generating Formal Data Contracts":
    st.title("4. Generating Formal Data Contracts (JSON Schemas)")
    st.markdown(f"Sharing data structures across services and teams requires a universal contract. JSON Schema, generated directly from our Pydantic models, enables **contract-first development**. This ensures that all components, whether frontend, backend, or partner systems, agree on the exact structure and validation rules for data.")
    st.markdown(f"")

    st.subheader("Generate JSON Schemas from Pydantic Models")
    st.markdown(f"Click the buttons below to generate and display the formal JSON Schemas for our core data models. These schemas are machine-readable and language-agnostic, making them ideal for cross-team communication and automated tooling.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Generate `Company` JSON Schema"):
            st.session_state.json_schema_company = Company.model_json_schema()
            st.success("Company JSON Schema generated!")
        if st.session_state.json_schema_company:
            st.markdown(f"**JSON Schema for `Company`:**")
            st.json(st.session_state.json_schema_company)

    with col2:
        if st.button("Generate `DimensionScoreInput` JSON Schema"):
            st.session_state.json_schema_dimension_score_input = DimensionScoreInput.model_json_schema()
            st.success("DimensionScoreInput JSON Schema generated!")
        if st.session_state.json_schema_dimension_score_input:
            st.markdown(f"**JSON Schema for `DimensionScoreInput`:**")
            st.json(st.session_state.json_schema_dimension_score_input)

    with col3:
        if st.button("Generate `SectorCalibration` JSON Schema"):
            st.session_state.json_schema_sector_calibration = SectorCalibration.model_json_schema()
            st.success("SectorCalibration JSON Schema generated!")
        if st.session_state.json_schema_sector_calibration:
            st.markdown(f"**JSON Schema for `SectorCalibration`:**")
            st.json(st.session_state.json_schema_sector_calibration)

    st.markdown(f"")
    st.markdown(f"These machine-readable schemas define structure, data types, and validation rules in a language-agnostic format that downstream consumers (frontends, services, partners) can use for generation and validation. Alex can now confidently share these contracts knowing they enforce strict data integrity.")
    st.info(f"In a real project, these schemas would typically be exported to a designated directory like `{st.session_state.project_root_path}/schemas/v1/exports/` for version control and automated distribution, forming part of a continuous integration pipeline.")
```

##### **Page: 5. Generating Synthetic Data**

*   **Purpose**: Shows Alex how to generate schema-compliant synthetic data for accelerating development and testing without real-world data.
*   **Markdown**: `## 5. Generating Synthetic Data for Development and Testing`
*   **Widgets**: `st.text_input` for `sector_id` and `sector_name` parameters. `st.button` for generating each type of synthetic data. `st.json` to display the generated data.
*   **Function Invocation**: `generate_synthetic_company(sector_id=...)`, `generate_synthetic_dimension_score_input(company_id=...)`, `generate_synthetic_sector_calibration(sector_id=..., sector_name=...)`.
*   **Session State Update**: The JSON string representation of generated models is stored in `st.session_state.synthetic_company_data`, `st.session_state.synthetic_score_input_data`, and `st.session_state.synthetic_sector_calibration_data`.
*   **Session State Read**: The stored synthetic data is read and displayed. A dynamically generated `company_id` from the synthetic company is used for the synthetic dimension score input.

```python
elif st.session_state.page == "5. Generating Synthetic Data":
    st.title("5. Generating Synthetic Data for Development and Testing")
    st.markdown(f"Before real pipelines are ready, Alex uses synthetic data that rigorously adheres to the defined schemas. This accelerates API development, UI prototyping, and early-stage feature work while avoiding **prototype purgatory**.")
    st.markdown(f"")

    st.subheader("Interactive Synthetic Data Generation")
    st.markdown(f"Use the controls below to generate synthetic data instances for Company, Dimension Scores, and Sector Calibrations. Observe how the generated data conforms to the Pydantic schemas, ready for use in development and testing environments.")

    col1, col2 = st.columns(2)
    with col1:
        synth_sector_id = st.text_input("Sector ID for Synthetic Data", value=st.session_state.synth_data_sector_id, key="synth_sector_id_input")
    with col2:
        synth_sector_name = st.text_input("Sector Name for Synthetic Data", value=st.session_state.synth_data_sector_name, key="synth_sector_name_input")

    st.markdown(f"---")

    # --- Generate Synthetic Company ---
    st.markdown(f"### Generate Synthetic `Company`")
    if st.button("Generate Company"):
        synth_company = generate_synthetic_company(sector_id=synth_sector_id)
        st.session_state.synthetic_company_data = synth_company.model_dump_json(indent=2)
        st.success("Synthetic Company generated!")
    if st.session_state.synthetic_company_data:
        st.json(json.loads(st.session_state.synthetic_company_data))
    st.markdown(f"---")

    # --- Generate Synthetic DimensionScoreInput ---
    st.markdown(f"### Generate Synthetic `DimensionScoreInput`")
    company_id_for_score = "synth-company-id-placeholder" # Default if no company generated yet
    if st.session_state.synthetic_company_data:
        # Extract company_id from the last generated synthetic company if available
        try:
            temp_company = Company.model_validate_json(st.session_state.synthetic_company_data)
            company_id_for_score = temp_company.company_id
            st.info(f"Using dynamically generated Company ID: `{company_id_for_score}` for Dimension Score Input.")
        except Exception:
            st.warning("Could not extract company_id from previously generated synthetic company. Using placeholder.")

    if st.button("Generate Dimension Score Input"):
        synth_score_input = generate_synthetic_dimension_score_input(company_id=company_id_for_score)
        st.session_state.synthetic_score_input_data = synth_score_input.model_dump_json(indent=2)
        st.success("Synthetic DimensionScoreInput generated!")
    if st.session_state.synthetic_score_input_data:
        st.json(json.loads(st.session_state.synthetic_score_input_data))
    st.markdown(f"---")

    # --- Generate Synthetic SectorCalibration ---
    st.markdown(f"### Generate Synthetic `SectorCalibration`")
    if st.button("Generate Sector Calibration"):
        synth_sector_calibration = generate_synthetic_sector_calibration(sector_id=synth_sector_id, sector_name=synth_sector_name)
        st.session_state.synthetic_sector_calibration_data = synth_sector_calibration.model_dump_json(indent=2)
        st.success("Synthetic SectorCalibration generated!")
    if st.session_state.synthetic_sector_calibration_data:
        st.json(json.loads(st.session_state.synthetic_sector_calibration_data))

    st.markdown(f"")
    st.markdown(f"This concludes Alex's foundational architectural sprint. With a robust directory structure, clear data contracts enforced by Pydantic, formal JSON schemas, and synthetic data for development, the PE Org-AI-R platform is now well-positioned for future sprints and the integration of advanced AI capabilities.")
```
