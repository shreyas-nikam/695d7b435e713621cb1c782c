import streamlit as st
import pandas as pd
from datetime import date
from decimal import Decimal
import json
import os
import shutil

# Import business logic from source.py
from source import *

# 1. Page Configuration
st.set_page_config(
    page_title="QuLab: Week 1: Platform Foundation & Framework Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Sidebar Branding
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.sidebar.title("PE Org-AI-R Platform")
st.sidebar.markdown("---")

# 3. Session State Initialization
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
if 'page' not in st.session_state:
    st.session_state.page = "Introduction"

# 1. Project Environment Setup Page State
if 'project_structure_created' not in st.session_state:
    st.session_state.project_structure_created = False
if 'project_root_path' not in st.session_state:
    st.session_state.project_root_path = "src/pe_orgair"

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
if 'company_create_output' not in st.session_state: st.session_state.company_create_output = None

# DimensionScoreInput Form Inputs & Output
if 'dim_score_dimension' not in st.session_state: st.session_state.dim_score_dimension = DimensionName.DATA_INFRASTRUCTURE.value
if 'dim_score_score' not in st.session_state: st.session_state.dim_score_score = 85.50
if 'dim_score_confidence' not in st.session_state: st.session_state.dim_score_confidence = "high"
if 'dim_score_rationale' not in st.session_state: st.session_state.dim_score_rationale = "Strong data pipeline and governance policies observed."
if 'dim_score_evidence_ids' not in st.session_state: st.session_state.dim_score_evidence_ids = "ev_id_001,ev_id_002"
if 'dim_score_output' not in st.session_state: st.session_state.dim_score_output = None

# SectorCalibration Form Inputs & Output
if 'sector_cal_id' not in st.session_state: st.session_state.sector_cal_id = "tech_ai"
if 'sector_cal_name' not in st.session_state: st.session_state.sector_cal_name = "Technology & AI"
if 'sector_cal_h_r_baseline' not in st.session_state: st.session_state.sector_cal_h_r_baseline = 78.0
if 'sector_cal_h_r_ci_lower' not in st.session_state: st.session_state.sector_cal_h_r_ci_lower = 70.0
if 'sector_cal_h_r_ci_upper' not in st.session_state: st.session_state.sector_cal_h_r_ci_upper = 85.0
if 'sector_cal_effective_date' not in st.session_state: st.session_state.sector_cal_effective_date = date.today()
if 'sector_cal_weights_input' not in st.session_state: st.session_state.sector_cal_weights_input = json.dumps({dim.value: float(weight) for dim, weight in DEFAULT_WEIGHTS.items()}, indent=2)
if 'sector_cal_targets_input' not in st.session_state: st.session_state.sector_cal_targets_input = json.dumps({dim.value: 75.0 for dim in DimensionName}, indent=2)
if 'sector_cal_output' not in st.session_state: st.session_state.sector_cal_output = None

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

# 4. Application Title and Navigation
st.title("QuLab: Week 1: Platform Foundation & Framework Architecture")
st.divider()

page_options = [
    "Introduction",
    "1. Project Environment Setup",
    "2. Defining Core Data Schemas",
    "3. Enforcing Data Integrity",
    "4. Generating Formal Data Contracts",
    "5. Generating Synthetic Data"
]

# Sidebar Navigation
selected_page = st.sidebar.selectbox("Navigate to Section", page_options, key="page_selector")
# Update session state if changed via selector (or handle directly)
st.session_state.page = selected_page

st.sidebar.markdown("---")
st.sidebar.info("Persona: Alex, a Senior Software Engineer.\n\nMission: Architect the AI Readiness Assessment system for PE Org-AI-R Platform.")

# 5. Page Logic

# --- Page: Introduction ---
if st.session_state.page == "Introduction":
    st.header("Introduction: Architecting the PE Org-AI-R Platform")
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

# --- Page 1: Project Environment Setup ---
elif st.session_state.page == "1. Project Environment Setup":
    st.header("1. Setting Up the Project Environment and Structure")
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

# --- Page 2: Defining Core Data Schemas ---
elif st.session_state.page == "2. Defining Core Data Schemas":
    st.header("2. Defining Core Data Schemas with Pydantic")
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
    st.code(json.dumps(Company.model_json_schema(by_alias=True), indent=2), language="json")

    st.markdown(f"**`DimensionScoreInput` Model:** Defines the structure for submitting individual dimension scores, including score range validation and confidence levels.")
    st.code(json.dumps(DimensionScoreInput.model_json_schema(by_alias=True), indent=2), language="json")

    st.markdown(f"**`SectorCalibration` Model:** Captures sector-specific baselines and dimension weights. This model enforces a critical business rule: **the sum of dimension weights must be 1.0**, keeping scoring consistent across sectors and preventing misalignment between data science and operations.")
    st.code(json.dumps(SectorCalibration.model_json_schema(by_alias=True), indent=2), language="json")

    st.markdown(f"")
    st.success("These models define the unambiguous contracts that ensure data quality and integration across all PE Org-AI-R platform components.")

# --- Page 3: Enforcing Data Integrity ---
elif st.session_state.page == "3. Enforcing Data Integrity":
    st.header("3. Enforcing Data Integrity through Schema Validation")
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
            
            # Correctly handle selectbox index
            ownership_options = [o.value for o in OwnershipType]
            try:
                ownership_idx = ownership_options.index(st.session_state.company_create_ownership_type)
            except ValueError:
                ownership_idx = 0
            ownership_type = st.selectbox("Ownership Type", options=ownership_options, index=ownership_idx, key="company_ownership_type_input")
            
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
            dim_options = [d.value for d in DimensionName]
            try:
                dim_idx = dim_options.index(st.session_state.dim_score_dimension)
            except ValueError:
                dim_idx = 0
            dimension = st.selectbox("Dimension", options=dim_options, index=dim_idx, key="dim_score_dim_input")
            
            score = st.number_input("Score (0-100)", value=st.session_state.dim_score_score, min_value=0.0, max_value=100.0, format="%.2f", key="dim_score_score_input")
            
            conf_options = ["high", "medium", "low"]
            try:
                conf_idx = conf_options.index(st.session_state.dim_score_confidence)
            except ValueError:
                conf_idx = 0
            confidence_level = st.selectbox("Confidence Level", options=conf_options, index=conf_idx, key="dim_score_confidence_input")
            
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

# --- Page 4: Generating Formal Data Contracts ---
elif st.session_state.page == "4. Generating Formal Data Contracts":
    st.header("4. Generating Formal Data Contracts (JSON Schemas)")
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

# --- Page 5: Generating Synthetic Data ---
elif st.session_state.page == "5. Generating Synthetic Data":
    st.header("5. Generating Synthetic Data for Development and Testing")
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


# License
st.caption('''
---
## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
''')
