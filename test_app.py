
import os
import shutil
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
import json
from datetime import date
from decimal import Decimal

# Test 1: Introduction page and sidebar navigation
def test_introduction_page_and_navigation():
    """
    Tests that the introduction page loads correctly and that sidebar navigation
    updates the page content.
    """
    at = AppTest.from_file("app.py").run()

    # Verify initial state: Introduction page is displayed
    assert at.title[0].value == "QuLab: Week 1: Platform Foundation & Framework Architecture"
    assert at.header[0].value == "Introduction: Architecting the PE Org-AI-R Platform"
    assert at.selectbox("page_selector").value == "Introduction"

    # Navigate to "2. Defining Core Data Schemas" and verify
    at.selectbox("page_selector").set_value("2. Defining Core Data Schemas").run()
    assert at.header[0].value == "2. Defining Core Data Schemas with Pydantic"
    assert at.selectbox("page_selector").value == "2. Defining Core Data Schemas"

# Test 2: Project Environment Setup page
def test_project_environment_setup_page():
    """
    Tests the "1. Project Environment Setup" page, including project structure
    creation and verification. Mocks file system operations.
    """
    project_root = "src/pe_orgair"
    key_dirs = [
        f"{project_root}/schemas/v1",
        f"{project_root}/api/routes",
        f"{project_root}/services/scoring",
        f"{project_root}/schemas/v1/exports"
    ]

    # Patch create_project_structure, os.path.exists, and shutil.rmtree
    with patch('source.create_project_structure') as mock_create_structure, \
         patch('os.path.exists') as mock_path_exists, \
         patch('shutil.rmtree') as mock_rmtree:

        # Scenario 1: Simulate 'src' directory existing initially
        # mock_path_exists returns True for "src" and key_dirs after creation
        def path_exists_side_effect_initial_src(path):
            if path == "src":
                return True
            if any(kd in path for kd in key_dirs):
                return True
            return False
        mock_path_exists.side_effect = path_exists_side_effect_initial_src

        at = AppTest.from_file("app.py").run()
        at.selectbox("page_selector").set_value("1. Project Environment Setup").run()
        assert at.header[0].value == "1. Setting Up the Project Environment and Structure"

        # Click the "Create/Verify Project Structure" button
        at.button[0].click().run()

        # Verify that rmtree was called (due to initial 'src' existence) and then create_project_structure
        mock_rmtree.assert_called_once_with("src")
        mock_create_structure.assert_called_once_with(base_path=project_root)

        # Verify success message and detailed verification output
        assert at.success[0].value == "Project structure created successfully!"
        assert "All critical project directories are in place, demonstrating successful repository initialization." in at.success[0].value
        assert all(f"- ✅ `{d}` exists" in at.markdown[idx].value for idx, d in enumerate(key_dirs, start=6)) # Adjust index based on app content

        # Reset mocks for Scenario 2
        mock_create_structure.reset_mock()
        mock_rmtree.reset_mock()

        # Scenario 2: Simulate 'src' directory not existing initially
        # mock_path_exists returns False for "src" initially, then True for key_dirs after creation
        def path_exists_side_effect_no_initial_src(path):
            if any(kd in path for kd in key_dirs):
                return True
            return False
        mock_path_exists.side_effect = path_exists_side_effect_no_initial_src

        at_no_src = AppTest.from_file("app.py").run()
        at_no_src.selectbox("page_selector").set_value("1. Project Environment Setup").run()
        at_no_src.button[0].click().run()

        # Verify rmtree was NOT called and create_project_structure was called
        mock_rmtree.assert_not_called()
        mock_create_structure.assert_called_once_with(base_path=project_root)

        # Verify success message and detailed verification output
        assert at_no_src.success[0].value == "Project structure created successfully!"
        assert "All critical project directories are in place" in at_no_src.success[0].value


# Test 3: Defining Core Data Schemas page
def test_defining_core_data_schemas_page():
    """
    Tests that the "2. Defining Core Data Schemas" page displays enums,
    default weights, and JSON schemas for core Pydantic models.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("2. Defining Core Data Schemas").run()
    assert at.header[0].value == "2. Defining Core Data Schemas with Pydantic"

    # Verify presence of Enum displays
    assert "CompanyStatus" in at.markdown[2].value
    assert "OwnershipType" in at.markdown[3].value
    assert "DimensionName" in at.markdown[4].value
    assert len(at.json) >= 3 # Check for at least 3 JSON blocks (Enums + DEFAULT_WEIGHTS)

    # Verify DEFAULT_WEIGHTS display
    assert "Default Dimension Weights" in at.subheader[2].value
    assert json.loads(at.json[0].value) # The first json block should be default weights

    # Verify Core Pydantic Models Overview and presence of code blocks for schemas
    assert "Core Pydantic Models Overview" in at.subheader[3].value
    assert len(at.code) >= 3 # At least 3 code blocks for Company, DimensionScoreInput, SectorCalibration schemas


# Test 4: Enforcing Data Integrity - CompanyCreate Form
def test_company_create_form_valid_data():
    """
    Tests the CompanyCreate form with valid data, expecting a success message
    and correctly validated JSON output.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Fill the form with valid data
    at.text_input("company_name_input").set_value("Innovate AI Solutions").run()
    at.text_input("company_ticker_input").set_value("IAS").run()
    at.text_input("company_domain_input").set_value("innovateai.com").run()
    at.text_input("company_sector_id_input").set_value("tech_ai").run()
    # Dynamically find the index for "TARGET" (OwnershipType.TARGET.value)
    ownership_options = [o.value for o in at._script_info.module.source.OwnershipType]
    target_idx = ownership_options.index(at._script_info.module.source.OwnershipType.TARGET.value)
    at.selectbox("company_ownership_type_input").set_index(target_idx).run()
    at.number_input("company_ev_input").set_value(120000000.50).run()
    at.text_input("company_ev_currency_input").set_value("USD").run()
    at.date_input("company_ev_date_input").set_value(date(2025, 1, 15)).run()

    # Submit the form
    at.form_submit_button("company_create_form").click().run()

    # Verify success message and JSON output
    assert at.success[0].value == "CompanyCreate data is valid!"
    output_json = json.loads(at.json[3].value) # Assuming 3 JSONs before this are Enums/Weights
    assert output_json["name"] == "Innovate AI Solutions"
    assert output_json["enterprise_value"] == "120000000.50"
    assert output_json["ev_as_of_date"] == "2025-01-15"

def test_company_create_form_invalid_enterprise_value():
    """
    Tests the CompanyCreate form with an invalid (negative) enterprise value,
    expecting a validation error.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Fill with invalid enterprise_value
    at.text_input("company_name_input").set_value("Bad EV Company").run()
    at.text_input("company_sector_id_input").set_value("bad_sector").run()
    ownership_options = [o.value for o in at._script_info.module.source.OwnershipType]
    target_idx = ownership_options.index(at._script_info.module.source.OwnershipType.TARGET.value)
    at.selectbox("company_ownership_type_input").set_index(target_idx).run()
    at.number_input("company_ev_input").set_value(-100.00).run() # Invalid: must be >= 0

    at.form_submit_button("company_create_form").click().run()

    # Verify error message and validation details
    assert at.error[0].value == "Invalid CompanyCreate data."
    assert "Validation Error" in at.code[3].value
    assert "greater than or equal to 0" in at.code[3].value

def test_company_create_form_invalid_ev_currency_length():
    """
    Tests the CompanyCreate form with an invalid (too long) EV currency,
    expecting a validation error.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Fill with invalid ev_currency
    at.text_input("company_name_input").set_value("Bad Currency Company").run()
    at.text_input("company_sector_id_input").set_value("invalid_sector").run()
    ownership_options = [o.value for o in at._script_info.module.source.OwnershipType]
    target_idx = ownership_options.index(at._script_info.module.source.OwnershipType.TARGET.value)
    at.selectbox("company_ownership_type_input").set_index(target_idx).run()
    at.number_input("company_ev_input").set_value(500000.00).run()
    at.text_input("company_ev_currency_input").set_value("FOUR").run() # Invalid: max 3 chars

    at.form_submit_button("company_create_form").click().run()

    # Verify error message and validation details
    assert at.error[0].value == "Invalid CompanyCreate data."
    assert "Validation Error" in at.code[3].value
    assert "String should have at most 3 characters" in at.code[3].value

# Test 5: Enforcing Data Integrity - DimensionScoreInput Form
def test_dimension_score_input_form_valid_data():
    """
    Tests the DimensionScoreInput form with valid data, expecting a success message
    and correctly validated JSON output.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Fill the form with valid data
    dimension_options = [d.value for d in at._script_info.module.source.DimensionName]
    data_infra_idx = dimension_options.index(at._script_info.module.source.DimensionName.DATA_INFRASTRUCTURE.value)
    at.selectbox("dim_score_dim_input").set_index(data_infra_idx).run()
    at.number_input("dim_score_score_input").set_value(85.50).run()
    at.selectbox("dim_score_confidence_input").set_value("high").run()
    at.text_area("dim_score_rationale_input").set_value("Strong data pipeline and governance policies observed.").run()
    at.text_input("dim_score_evidence_input").set_value("ev_id_001, ev_id_002").run()

    # Submit the form
    at.form_submit_button("dim_score_form").click().run()

    # Verify success message and JSON output
    assert at.success[0].value == "DimensionScoreInput data is valid!"
    output_json = json.loads(at.json[4].value) # Adjusted index for previous forms
    assert output_json["dimension"] == "data_infrastructure"
    assert output_json["score"] == "85.50"
    assert "ev_id_001" in output_json["evidence_chunk_ids"]


def test_dimension_score_input_form_invalid_score():
    """
    Tests the DimensionScoreInput form with an invalid score (out of 0-100 range),
    expecting a validation error.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Fill with invalid score
    dimension_options = [d.value for d in at._script_info.module.source.DimensionName]
    ml_ops_idx = dimension_options.index(at._script_info.module.source.DimensionName.ML_OPS.value)
    at.selectbox("dim_score_dim_input").set_index(ml_ops_idx).run()
    at.number_input("dim_score_score_input").set_value(100.01).run() # Invalid: > 100
    at.selectbox("dim_score_confidence_input").set_value("low").run()

    at.form_submit_button("dim_score_form").click().run()

    # Verify error message and validation details
    assert at.error[0].value == "Invalid DimensionScoreInput data."
    assert "Validation Error" in at.code[4].value
    assert "less than or equal to 100" in at.code[4].value

# Test 6: Enforcing Data Integrity - SectorCalibration Form
def test_sector_calibration_form_valid_data():
    """
    Tests the SectorCalibration form with valid data (weights sum to 1.0),
    expecting a success message and correctly validated JSON output.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Get valid default weights and targets from the app's source module
    source_module = at._script_info.module.source
    valid_weights = {dim.value: float(weight) for dim, weight in source_module.DEFAULT_WEIGHTS.items()}
    valid_targets = {dim.value: 75.0 for dim in source_module.DimensionName}

    # Fill the form with valid data
    at.text_input("sector_cal_id_input").set_value("tech_ai").run()
    at.text_input("sector_cal_name_input").set_value("Technology & AI").run()
    at.number_input("sector_cal_baseline_input").set_value(78.0).run()
    at.number_input("sector_cal_ci_lower_input").set_value(70.0).run()
    at.number_input("sector_cal_ci_upper_input").set_value(85.0).run()
    at.date_input("sector_cal_date_input").set_value(date(2024, 1, 1)).run()
    at.text_area("sector_cal_weights_input_area").set_value(json.dumps(valid_weights, indent=2)).run()
    at.text_area("sector_cal_targets_input_area").set_value(json.dumps(valid_targets, indent=2)).run()

    # Submit the form
    at.form_submit_button("sector_cal_form").click().run()

    # Verify success message and JSON output
    assert at.success[0].value == "SectorCalibration data is valid!"
    output_json = json.loads(at.json[5].value) # Adjusted index for previous forms
    assert output_json["sector_id"] == "tech_ai"
    assert output_json["h_r_baseline"] == "78.00"
    # Verify weights sum approximately to 1.0
    assert abs(sum(Decimal(v) for v in output_json["weights"].values()) - 1.0) < 1e-9


def test_sector_calibration_form_invalid_weights_sum():
    """
    Tests the SectorCalibration form with weights that do not sum to 1.0,
    expecting a validation error.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    # Define invalid weights (sum not 1.0)
    invalid_weights = {
        "data_infrastructure": 0.5,
        "ml_ops": 0.3,
        "ai_strategy": 0.3, # Sums to 1.1
        "talent_and_culture": 0.0,
        "governance_and_ethics": 0.0,
        "innovation_and_research": 0.0,
        "business_integration": 0.0
    }
    source_module = at._script_info.module.source
    valid_targets = {dim.value: 75.0 for dim in source_module.DimensionName}

    # Fill with invalid weights
    at.text_input("sector_cal_id_input").set_value("invalid_weights_sector").run()
    at.text_input("sector_cal_name_input").set_value("Invalid Weights Sector").run()
    at.number_input("sector_cal_baseline_input").set_value(70.0).run()
    at.text_area("sector_cal_weights_input_area").set_value(json.dumps(invalid_weights, indent=2)).run()
    at.text_area("sector_cal_targets_input_area").set_value(json.dumps(valid_targets, indent=2)).run()

    at.form_submit_button("sector_cal_form").click().run()

    # Verify error message and validation details
    assert at.error[0].value == "Invalid SectorCalibration data."
    assert "Validation Error" in at.code[5].value
    assert "sum of weights must be approximately 1.0" in at.code[5].value

def test_sector_calibration_form_invalid_json_weights():
    """
    Tests the SectorCalibration form with malformed JSON for weights,
    expecting a JSON parsing error.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("3. Enforcing Data Integrity").run()

    malformed_json_weights = "{'data_infrastructure': 0.5," # Invalid JSON format (single quotes, missing brace)
    source_module = at._script_info.module.source
    valid_targets = {dim.value: 75.0 for dim in source_module.DimensionName}

    # Fill with malformed JSON
    at.text_input("sector_cal_id_input").set_value("malformed_json_sector").run()
    at.text_area("sector_cal_weights_input_area").set_value(malformed_json_weights).run()
    at.text_area("sector_cal_targets_input_area").set_value(json.dumps(valid_targets, indent=2)).run()

    at.form_submit_button("sector_cal_form").click().run()

    # Verify error message for JSON parsing
    assert at.error[0].value == "Invalid JSON format for weights or targets."
    assert "JSON parsing error in weights or targets" in at.code[5].value


# Test 7: Generating Formal Data Contracts page
def test_generating_formal_data_contracts_page():
    """
    Tests the "4. Generating Formal Data Contracts" page, verifying that
    JSON schemas can be generated and displayed for core models.
    """
    at = AppTest.from_file("app.py").run()
    at.selectbox("page_selector").set_value("4. Generating Formal Data Contracts").run()
    assert at.header[0].value == "4. Generating Formal Data Contracts (JSON Schemas)"

    # Generate Company JSON Schema
    at.button[0].click().run()
    assert at.success[0].value == "Company JSON Schema generated!"
    assert at.session_state.json_schema_company is not None
    assert "title" in at.json[0].value and "Company" in at.json[0].value

    # Generate DimensionScoreInput JSON Schema
    at.button[1].click().run()
    assert at.success[1].value == "DimensionScoreInput JSON Schema generated!"
    assert at.session_state.json_schema_dimension_score_input is not None
    assert "title" in at.json[1].value and "DimensionScoreInput" in at.json[1].value

    # Generate SectorCalibration JSON Schema
    at.button[2].click().run()
    assert at.success[2].value == "SectorCalibration JSON Schema generated!"
    assert at.session_state.json_schema_sector_calibration is not None
    assert "title" in at.json[2].value and "SectorCalibration" in at.json[2].value


# Test 8: Generating Synthetic Data page
def test_generating_synthetic_data_page():
    """
    Tests the "5. Generating Synthetic Data" page, verifying that synthetic data
    can be generated for Company, DimensionScoreInput, and SectorCalibration.
    Mocks the synthetic data generation functions from source.py.
    """
    # Mock synthetic data generation functions to return predictable results
    with patch('source.generate_synthetic_company') as mock_gen_company, \
         patch('source.generate_synthetic_dimension_score_input') as mock_gen_score, \
         patch('source.generate_synthetic_sector_calibration') as mock_gen_sector_cal:

        # Define a mock Pydantic model with model_dump_json method
        class MockPydanticModel:
            def __init__(self, data):
                self._data = data
            def model_dump_json(self, indent=2):
                return json.dumps(self._data, indent=indent)
            @property
            def company_id(self): # Required for passing company_id to generate_synthetic_dimension_score_input
                return self._data.get("company_id")

        # Define mock data for each synthetic generation function
        mock_company_data = {
            "company_id": "synth-comp-123", "name": "Synthetic Company One", "sector_id": "game_dev",
            "ownership_type": "target_company", "status": "active",
            "created_at": "2023-01-01T00:00:00+00:00", "updated_at": "2023-01-01T00:00:00+00:00"
        }
        mock_score_data = {
            "score_id": "synth-score-456", "company_id": "synth-comp-123", "dimension": "ai_strategy",
            "score": "75.00", "confidence_level": "medium",
            "created_at": "2023-01-01T00:00:00+00:00", "updated_at": "2023-01-01T00:00:00+00:00"
        }
        mock_sector_cal_data = {
            "sector_calibration_id": "synth-sector-cal-789", "sector_id": "game_dev",
            "sector_name": "Game Development", "h_r_baseline": "78.00",
            "weights": {"data_infrastructure": "0.20", "ml_ops": "0.20", "ai_strategy": "0.20",
                        "talent_and_culture": "0.10", "governance_and_ethics": "0.10",
                        "innovation_and_research": "0.10", "business_integration": "0.10"},
            "targets": {"data_infrastructure": "80.00", "ml_ops": "75.00", "ai_strategy": "70.00",
                        "talent_and_culture": "70.00", "governance_and_ethics": "85.00",
                        "innovation_and_research": "70.00", "business_integration": "70.00"},
            "effective_date": "2023-01-01",
            "created_at": "2023-01-01T00:00:00+00:00", "updated_at": "2023-01-01T00:00:00+00:00"
        }

        mock_gen_company.return_value = MockPydanticModel(mock_company_data)
        mock_gen_score.return_value = MockPydanticModel(mock_score_data)
        mock_gen_sector_cal.return_value = MockPydanticModel(mock_sector_cal_data)

        at = AppTest.from_file("app.py").run()
        at.selectbox("page_selector").set_value("5. Generating Synthetic Data").run()
        assert at.header[0].value == "5. Generating Synthetic Data for Development and Testing"

        # Change sector ID/name inputs for generation parameters
        at.text_input("synth_sector_id_input").set_value("game_dev").run()
        at.text_input("synth_sector_name_input").set_value("Game Development").run()

        # Generate Synthetic Company
        at.button[0].click().run() # The "Generate Company" button
        mock_gen_company.assert_called_once_with(sector_id="game_dev")
        assert at.success[0].value == "Synthetic Company generated!"
        assert json.loads(at.json[0].value)["company_id"] == "synth-comp-123"
        assert at.session_state.synthetic_company_data is not None

        # Generate Synthetic DimensionScoreInput
        at.button[1].click().run() # The "Generate Dimension Score Input" button
        # The app passes company_id_for_score, which is taken from session_state.synthetic_company_data
        mock_gen_score.assert_called_once_with(company_id="synth-comp-123")
        assert at.success[1].value == "Synthetic DimensionScoreInput generated!"
        assert json.loads(at.json[1].value)["company_id"] == "synth-comp-123"
        assert at.session_state.synthetic_score_input_data is not None

        # Generate Synthetic SectorCalibration
        at.button[2].click().run() # The "Generate Sector Calibration" button
        mock_gen_sector_cal.assert_called_once_with(sector_id="game_dev", sector_name="Game Development")
        assert at.success[2].value == "Synthetic SectorCalibration generated!"
        assert json.loads(at.json[2].value)["sector_id"] == "game_dev"
        assert at.session_state.synthetic_sector_calibration_data is not None
