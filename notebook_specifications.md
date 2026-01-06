
# Building Enterprise AI Systems: Data Contracts for AI Readiness Assessment

## Introduction: Architecting the PE Org-AI-R Platform

**Persona:** Alex, a Senior Software Engineer at PE Org-AI-R Platform.
**Organization:** PE Org-AI-R Platform, a leading private equity firm specializing in identifying and nurturing AI-ready companies.

Alex's mission is to build the foundational architecture for a new AI Readiness Assessment system. This system will evaluate potential portfolio companies across critical dimensions, providing data-driven insights for investment and value creation strategies. In the world of enterprise AI, "AI that lives in notebooks dies in production." Alex understands that success hinges on robust system architecture, clear data contracts, and disciplined engineering practices, not just sophisticated models.

This notebook walks through Alex's initial steps to lay down the "platform skeleton" and define core data schemas using Pydantic, ensuring data integrity and setting the stage for future sprints. This is where "APIs and schemas act as contracts between teams and modules," a crucial step in preventing "data chaos" and "integration debt."

## 1. Setting Up the Project Environment and Structure

Alex begins by preparing the development environment and establishing a standardized directory structure. This structure is vital for managing complexity in a growing enterprise AI system, separating concerns, and aligning with industry best practices for monorepos.

### Installing Required Libraries

Alex ensures all necessary libraries, particularly `pydantic` for data schema definition and `faker` for synthetic data generation, are installed.

```python
!pip install pydantic~=2.0 faker~=20.0 python-dotenv~=1.0 # Pydantic v2 requires ~2.0, faker for synthetic data, dotenv for env vars
```

### Importing Required Dependencies

Alex imports the core modules needed for defining schemas, handling data types, and generating unique identifiers and synthetic data.

```python
import os
import shutil
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict
from uuid import uuid4

from pydantic import BaseModel, Field, ValidationError, model_validator
from faker import Faker
```

### Initializing the Monorepo Directory Structure

A well-defined project structure is the backbone of any maintainable software system. Alex creates the logical separation for APIs, services, schemas, and other components.

```python
# Function to create directories safely
def create_project_structure(base_path: str = "src/pe_orgair"):
    """
    Creates the foundational directory structure for the PE Org-AI-R Platform monorepo.
    """
    print(f"Creating project structure under: {base_path}")

    # Define core directories
    core_dirs = [
        f"{base_path}/api",
        f"{base_path}/services",
        f"{base_path}/schemas",
        f"{base_path}/db",
        f"{base_path}/pipelines",
        f"{base_path}/config",
        f"{base_path}/api/routes",
        f"{base_path}/services/scoring",
        f"{base_path}/services/extraction",
        f"{base_path}/services/retrieval",
        f"{base_path}/services/value_creation",
        f"{base_path}/services/monitoring",
        f"{base_path}/services/portfolio",
        f"{base_path}/schemas/v1",
        f"{base_path}/schemas/v1/exports", # For JSON schema exports
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "data/taxonomies",
        "data/sector_calibrations",
        "data/sample_companies",
        "docs/api",
        "docs/architecture",
        "scripts",
        "docker",
        "dags", # For Apache Airflow DAGs
    ]

    for d in core_dirs:
        os.makedirs(d, exist_ok=True)
        # print(f"  Created: {d}")

    # Initialize Python packages with __init__.py
    python_packages = [
        base_path,
        f"{base_path}/api",
        f"{base_path}/services",
        f"{base_path}/schemas",
        f"{base_path}/schemas/v1",
        f"{base_path}/config",
    ]
    for p in python_packages:
        init_file = os.path.join(p, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass # Create empty __init__.py
            # print(f"  Created: {init_file}")

    print("\nProject structure created successfully.")

# Execute the function to create the structure
project_root = "src/pe_orgair"
if os.path.exists("src"): # Clean up previous run for idempotency
    shutil.rmtree("src")
create_project_structure(project_root)

# Verify creation (optional, for demonstration)
print("\nVerifying key directories:")
print(f"Schema dir exists: {os.path.exists(f'{project_root}/schemas/v1')}")
print(f"API routes dir exists: {os.path.exists(f'{project_root}/api/routes')}")
```

### Explanation of Execution
Alex has now established the fundamental folder structure for the PE Org-AI-R platform. This adheres to the "separation of concerns" principle, which prevents failures in large systems by organizing code into distinct, manageable parts. This systematic initialization reduces "technical debt" from the outset, ensuring future development can proceed efficiently.

## 2. Defining Core Data Schemas with Pydantic

Alex moves on to defining the core data structures that will represent the entities within the AI Readiness Assessment system. Pydantic models are chosen for their ability to define clear data "contracts" (schemas) with built-in validation, which is critical for ensuring data quality across different system components and preventing "prototype purgatory."

```python
# Enums from the provided content
class CompanyStatus(str, Enum):
    """Possible statuses for a company."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ACQUIRED = "acquired"
    EXITED = "exited"

class OwnershipType(str, Enum):
    """Types of ownership for a company."""
    PORTFOLIO = "portfolio"
    TARGET = "target"
    EXITED = "exited"
    BENCHMARK = "benchmark"

class DimensionName(str, Enum):
    """Seven validated dimensions of AI readiness."""
    DATA_INFRASTRUCTURE = "data_infrastructure"
    AI_GOVERNANCE = "ai_governance"
    TECHNOLOGY_STACK = "technology_stack"
    TALENT = "talent"
    LEADERSHIP = "leadership"
    USE_CASE_PORTFOLIO = "use_case_portfolio"
    CULTURE = "culture"

# Default dimension weights (can be overridden by sector)
DEFAULT_WEIGHTS: Dict[DimensionName, Decimal] = {
    DimensionName.DATA_INFRASTRUCTURE: Decimal("0.25"),
    DimensionName.AI_GOVERNANCE: Decimal("0.20"),
    DimensionName.TECHNOLOGY_STACK: Decimal("0.15"),
    DimensionName.TALENT: Decimal("0.15"),
    DimensionName.LEADERSHIP: Decimal("0.10"),
    DimensionName.USE_CASE_PORTFOLIO: Decimal("0.10"),
    DimensionName.CULTURE: Decimal("0.05"),
}

# Company-related schemas
class CompanyBase(BaseModel):
    """Base company model, defining common fields."""
    name: str = Field(..., min_length=1, max_length=200)
    ticker: Optional[str] = Field(None, max_length=20)
    domain: Optional[str] = Field(None, max_length=200)
    cik: Optional[str] = Field(None, max_length=20)
    sector_id: str = Field(..., description="Reference to sector calibration")
    sub_sector_id: Optional[str] = None

class CompanyCreate(CompanyBase):
    """Schema for creating a company, including optional initial financial details."""
    enterprise_value: Optional[Decimal] = Field(None, ge=0)
    ev_currency: str = Field(default="USD", max_length=3)
    ev_as_of_date: Optional[date] = None
    ownership_type: OwnershipType = OwnershipType.TARGET
    fund_id: Optional[str] = None

class Company(CompanyBase):
    """Full company model with all fields, including system-generated ones."""
    company_id: str = Field(default_factory=lambda: str(uuid4()))
    enterprise_value: Optional[Decimal] = Field(None, ge=0) # Redundant but kept from source
    ev_currency: str = Field("USD", max_length=3) # Redundant but kept from source
    ev_as_of_date: Optional[date] = None # Redundant but kept from source
    status: CompanyStatus = CompanyStatus.ACTIVE
    ownership_type: Optional[OwnershipType] = None # Optional here to allow for updates to existing
    fund_id: Optional[str] = None # Optional here to allow for updates to existing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True # Allow creating model instances from ORM objects

class CompanyDetail(Company):
    """Company with related data for detail view."""
    sector_name: Optional[str] = None
    current_org_air: Optional[Decimal] = None
    last_scored_at: Optional[datetime] = None
    document_count: int = 0
    job_signal_count: int = 0

# Dimension and scoring schemas
class DimensionScoreInput(BaseModel):
    """Input for a single dimension score, subject to validation."""
    dimension: DimensionName
    score: Decimal = Field(..., ge=0, le=100)
    confidence_level: Optional[str] = Field(
        default="medium", pattern="^(high|medium|low)$"
    )
    rationale: Optional[str] = Field(None, max_length=1000)
    evidence_chunk_ids: List[str] = Field(default_factory=list)

    @model_validator(mode='before')
    @classmethod
    def round_score(cls, values):
        if isinstance(values, dict) and 'score' in values and isinstance(values['score'], (float, Decimal)):
            values['score'] = Decimal(values['score']).quantize(Decimal("0.01"))
        return values

class DimensionScoreResult(BaseModel):
    """Stored dimension score with metadata for historical tracking."""
    score_id: str = Field(default_factory=lambda: str(uuid4()))
    company_id: str
    assessment_id: str = Field(default_factory=lambda: str(uuid4()))
    dimension: DimensionName
    score: Decimal = Field(..., ge=0, le=100)
    weight: Decimal = Field(..., ge=0, le=1) # Dimension weights
    confidence_level: str
    assessor_id: Optional[str] = None
    assessment_method: str
    assessment_date: date
    evidence_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SectorCalibration(BaseModel):
    """Sector calibration data including Human-Readiness (H^R) and dimension weights."""
    sector_id: str
    sector_name: str
    h_r_baseline: Decimal = Field(..., ge=0, le=100, description="Systematic Opportunity (H^R) baseline score")
    h_r_ci_lower: Optional[Decimal] = Field(None, ge=0, le=100, description="Lower bound of H^R confidence interval")
    h_r_ci_upper: Optional[Decimal] = Field(None, ge=0, le=100, description="Upper bound of H^R confidence interval")
    weights: Dict[DimensionName, Decimal] = Field(..., description="Weights for each dimension, must sum to 1.0")
    targets: Dict[DimensionName, Decimal] = Field(..., description="Sector targets (75th percentile benchmarks)")
    effective_date: date

    @model_validator(mode='after')
    def validate_weights_sum(self) -> 'SectorCalibration':
        """
        Ensures that the sum of dimension weights equals 1.0.
        This is a critical business rule for consistent scoring.
        """
        total_weights = sum(self.weights.values())
        # Check if total_weights is approximately 1.0 to account for floating-point inaccuracies
        if abs(total_weights - Decimal("1.0")) > Decimal("0.001"):
            raise ValueError(f"Dimension weights must sum to 1.0, got {total_weights}")
        return self

    class Config:
        from_attributes = True

print("Pydantic models for PE Org-AI-R Platform defined.")
print("\nDEFAULT_WEIGHTS for dimensions:")
for dim, weight in DEFAULT_WEIGHTS.items():
    print(f"  - {dim.value}: {weight}")
```

### Explanation of Execution
Alex has now meticulously defined the data blueprints for the AI Readiness system. Each `BaseModel` specifies the expected data types, required fields, and intricate validation rules using `Field` parameters like `min_length`, `max_length`, `ge` (greater than or equal to), `le` (less than or equal to), and `pattern`. The `DimensionName` `Enum` ensures that all dimensions are consistently named, preventing "data chaos" from inconsistent spellings. The `SectorCalibration` model includes a `@model_validator` to enforce a critical business rule: **the sum of dimension weights must be 1.0**. This is mathematically represented as:

$$
\sum_{i=1}^{N} w_i = 1.0
$$

where $w_i$ is the weight for the $i$-th `DimensionName`, and $N$ is the total number of dimensions. This validation ensures that the scoring mechanism remains consistent and fair across different sectors. This explicit contract helps avoid "misalignment between data science and operations" by setting clear expectations for data input.

## 3. Enforcing Data Integrity through Schema Validation

A key benefit of Pydantic is its automatic data validation, which is paramount for an enterprise AI system. Alex demonstrates how this prevents invalid or malformed data from corrupting the system, which is a common cause of "AI failure."

### 3.1 Valid Data Instantiation

Alex first shows how to create model instances with valid data, demonstrating successful adherence to the defined schemas.

```python
print("--- Valid Data Instantiation ---")

# Example 1: Valid DimensionScoreInput
valid_score_input = DimensionScoreInput(
    dimension=DimensionName.DATA_INFRASTRUCTURE,
    score=Decimal("85.50"),
    confidence_level="high",
    rationale="Strong data pipeline and governance policies observed.",
    evidence_chunk_ids=["ev_id_001", "ev_id_002"]
)
print(f"\nSuccessfully created valid DimensionScoreInput:\n{valid_score_input.model_dump_json(indent=2)}")

# Example 2: Valid CompanyCreate
valid_company_create = CompanyCreate(
    name="InnovateAI Solutions",
    ticker="IAS",
    domain="innovateai.com",
    sector_id="tech_ai",
    enterprise_value=Decimal("120000000.50"),
    ev_currency="USD",
    ev_as_of_date=date(2023, 11, 15),
    ownership_type=OwnershipType.TARGET
)
print(f"\nSuccessfully created valid CompanyCreate:\n{valid_company_create.model_dump_json(indent=2)}")

# Example 3: Valid SectorCalibration with DEFAULT_WEIGHTS
valid_sector_calibration = SectorCalibration(
    sector_id="tech_ai",
    sector_name="Technology & AI",
    h_r_baseline=Decimal("78.0"),
    h_r_ci_lower=Decimal("70.0"),
    h_r_ci_upper=Decimal("85.0"),
    weights=DEFAULT_WEIGHTS,
    targets={dim: Decimal("75.0") for dim in DimensionName},
    effective_date=date(2024, 1, 1)
)
print(f"\nSuccessfully created valid SectorCalibration:\n{valid_sector_calibration.model_dump_json(indent=2)}")
```

### Explanation of Execution
These examples demonstrate Pydantic's seamless validation. Alex can confidently use these models as "inputs" to other parts of the system, knowing that the data adheres to the specified structure and constraints. This is a direct application of using "APIs and schemas as contracts" to ensure internal consistency and reliability. The `score` field is automatically rounded to two decimal places as specified by the `round_score` validator, demonstrating automated data cleaning.

### 3.2 Demonstrating Validation Errors

Now, Alex intentionally introduces invalid data to showcase Pydantic's error handling. This is critical for robust system design, as it ensures that "brittle orchestration" and data-related bugs are caught early.

```python
print("\n--- Demonstrating Validation Errors ---")

# Invalid DimensionScoreInput: Score out of bounds
try:
    invalid_score_input_score = DimensionScoreInput(
        dimension=DimensionName.TALENT,
        score=Decimal("101.0"), # Invalid: score > 100
        confidence_level="medium"
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for invalid score:\n{e}")
    # Alex checks for specific error detail to confirm the validation rule
    assert "less than or equal to 100" in str(e)

# Invalid DimensionScoreInput: Invalid confidence_level pattern
try:
    invalid_score_input_confidence = DimensionScoreInput(
        dimension=DimensionName.LEADERSHIP,
        score=Decimal("65.0"),
        confidence_level="very_high" # Invalid: does not match pattern
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for invalid confidence_level:\n{e}")
    assert "string does not match regex" in str(e)

# Invalid SectorCalibration: Weights do not sum to 1.0
bad_weights = {dim: Decimal("0.10") for dim in DimensionName} # Sums to 0.70 (7 dimensions * 0.10)
try:
    invalid_sector_calibration_weights = SectorCalibration(
        sector_id="finance",
        sector_name="Financial Services",
        h_r_baseline=Decimal("60.0"),
        weights=bad_weights, # Invalid: sum != 1.0
        targets={dim: Decimal("65.0") for dim in DimensionName},
        effective_date=date(2024, 1, 1)
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for weights sum:\n{e}")
    assert "Dimension weights must sum to 1.0" in str(e)

# Invalid SectorCalibration: h_r_baseline out of bounds
try:
    invalid_sector_calibration_baseline = SectorCalibration(
        sector_id="healthcare",
        sector_name="Healthcare",
        h_r_baseline=Decimal("105.0"), # Invalid: baseline > 100
        weights=DEFAULT_WEIGHTS,
        targets={dim: Decimal("70.0") for dim in DimensionName},
        effective_date=date(2024, 1, 1)
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for h_r_baseline:\n{e}")
    assert "less than or equal to 100" in str(e)
```

### Explanation of Execution
By demonstrating how `ValidationError` exceptions are raised, Alex confirms that Pydantic effectively acts as a gatekeeper for data quality. This proactive approach helps prevent "ML technical debt" that arises from inconsistent or invalid inputs further down the pipeline. When an analyst tries to input a score of `101.0`, or define sector weights that don't add up to 1.0, the system immediately flags the issue, guiding the user to correct the data. This ensures that the system's "inputs" are always reliable.

## 4. Generating Formal Data Contracts (JSON Schemas)

Alex recognizes that sharing data structures across different services, frontend applications, and external partners requires a universally understood format. Generating JSON Schema from Pydantic models provides formal, language-agnostic "contracts" that empower "contract-first development."

```python
print("--- Generating JSON Schemas ---")

# Generate JSON Schema for Company model
company_json_schema = Company.model_json_schema()
print("\nJSON Schema for Company:\n")
print(company_json_schema.model_dump_json(indent=2))

# Generate JSON Schema for DimensionScoreInput model
dimension_score_input_json_schema = DimensionScoreInput.model_json_schema()
print("\nJSON Schema for DimensionScoreInput:\n")
print(dimension_score_input_json_schema.model_dump_json(indent=2))

# Generate JSON Schema for SectorCalibration model
sector_calibration_json_schema = SectorCalibration.model_json_schema()
print("\nJSON Schema for SectorCalibration:\n")
print(sector_calibration_json_schema.model_dump_json(indent=2))

# Save a schema to the designated exports directory
schema_export_path = f"{project_root}/schemas/v1/exports/company_v1.json"
with open(schema_export_path, "w") as f:
    f.write(company_json_schema.model_dump_json(indent=2))
print(f"\nJSON Schema for Company exported to: {schema_export_path}")
```

### Explanation of Execution
Alex has now generated a standardized, machine-readable JSON Schema for each critical entity. This output explicitly defines the structure, data types, and validation rules in a format that any programming language or system can interpret. For instance, a frontend developer can use the `company_json_schema` to dynamically generate forms or validate user input client-side, ensuring alignment with the backend API. This proactive step reinforces the idea of "APIs and schemas as contracts," minimizing miscommunication and integration issues across teams, a common pitfall leading to "data chaos."

## 5. Generating Synthetic Data for Development and Testing

Before real data pipelines are fully operational, Alex needs to provide realistic, yet synthetic, data for testing various components like API endpoints, UI dashboards, and initial service logic. This synthetic data must rigorously adhere to the defined Pydantic schemas.

```python
fake = Faker()

def generate_synthetic_company(sector_id: str) -> Company:
    """Generates a synthetic Company instance."""
    return Company(
        name=fake.company(),
        ticker=fake.bothify(text='???###').upper(),
        domain=fake.domain_name(),
        cik=fake.lexify(text='?????????'),
        sector_id=sector_id,
        sub_sector_id=fake.word() if fake.boolean(chance_of_getting_true=30) else None,
        enterprise_value=Decimal(fake.random_int(min=1_000_000, max=10_000_000_000)),
        ev_currency=fake.currency_code(),
        ev_as_of_date=fake.date_between(start_date='-2y', end_date='today'),
        ownership_type=fake.random_element(list(OwnershipType)),
        fund_id=fake.uuid4() if fake.boolean(chance_of_getting_true=50) else None,
        status=fake.random_element(list(CompanyStatus)),
        created_at=fake.date_time_between(start_date='-5y', end_date='-1y'),
        updated_at=fake.date_time_between(start_date='-1y', end_date='now')
    )

def generate_synthetic_dimension_score_input(company_id: str) -> DimensionScoreInput:
    """Generates a synthetic DimensionScoreInput instance."""
    return DimensionScoreInput(
        dimension=fake.random_element(list(DimensionName)),
        score=Decimal(fake.pyfloat(min_value=0, max_value=100, right_digits=2)),
        confidence_level=fake.random_element(["high", "medium", "low"]),
        rationale=fake.sentence(nb_words=10) if fake.boolean(chance_of_getting_true=70) else None,
        evidence_chunk_ids=[fake.uuid4() for _ in range(fake.random_int(min=0, max=3))]
    )

def generate_synthetic_sector_calibration(sector_id: str, sector_name: str) -> SectorCalibration:
    """Generates a synthetic SectorCalibration instance."""
    # Ensure weights sum to 1.0 (distribute 1.0 across dimensions)
    weights_values = [Decimal(fake.pyfloat(min_value=0.01, max_value=0.30, right_digits=2)) for _ in DimensionName]
    total_raw_weights = sum(weights_values)
    normalized_weights = {
        dim: (val / total_raw_weights).quantize(Decimal("0.01")) for dim, val in zip(DimensionName, weights_values)
    }
    # Adjust last weight to ensure sum is exactly 1.0 due to rounding
    current_sum = sum(normalized_weights.values())
    if current_sum != Decimal("1.0"):
        last_dim = list(DimensionName)[-1]
        normalized_weights[last_dim] += (Decimal("1.0") - current_sum)
        normalized_weights[last_dim] = normalized_weights[last_dim].quantize(Decimal("0.01"))
        if normalized_weights[last_dim] < Decimal("0.01"): # Prevent negative or too small weights
            normalized_weights[last_dim] = Decimal("0.01") # Set a minimum
            # Re-normalize if necessary, simple approach for demo
            # In a real system, a more robust normalization would be used.
            # For this demo, assuming the initial distribution allows for adjustment.

    return SectorCalibration(
        sector_id=sector_id,
        sector_name=sector_name,
        h_r_baseline=Decimal(fake.pyfloat(min_value=50, max_value=90, right_digits=2)),
        h_r_ci_lower=Decimal(fake.pyfloat(min_value=45, max_value=80, right_digits=2)) if fake.boolean(chance_of_getting_true=70) else None,
        h_r_ci_upper=Decimal(fake.pyfloat(min_value=60, max_value=95, right_digits=2)) if fake.boolean(chance_of_getting_true=70) else None,
        weights=normalized_weights,
        targets={dim: Decimal(fake.pyfloat(min_value=60, max_value=85, right_digits=2)) for dim in DimensionName},
        effective_date=fake.date_between(start_date='-1y', end_date='today')
    )

# Generate and display example synthetic data
print("--- Generating Synthetic Data ---")

# Synthetic Company
synth_company = generate_synthetic_company(sector_id="software_dev")
print(f"\nSynthetic Company:\n{synth_company.model_dump_json(indent=2)}")

# Synthetic DimensionScoreInput
synth_score_input = generate_synthetic_dimension_score_input(company_id=synth_company.company_id)
print(f"\nSynthetic DimensionScoreInput:\n{synth_score_input.model_dump_json(indent=2)}")

# Synthetic SectorCalibration
synth_sector_calibration = generate_synthetic_sector_calibration(sector_id="software_dev", sector_name="Software Development")
print(f"\nSynthetic SectorCalibration:\n{synth_sector_calibration.model_dump_json(indent=2)}")
```

### Explanation of Execution
Alex has successfully generated structured synthetic data that strictly conforms to the defined Pydantic schemas. This synthetic data provides a critical resource for various downstream activities, such as:
- **API Development:** Developers can use this data to mock API responses or populate request bodies during endpoint testing, preventing "broken initial scaffolding."
- **UI Prototyping:** Frontend engineers can use these JSON structures to build and test UI components (e.g., in Streamlit), allowing them to visualize how company profiles and AI readiness scores would appear without needing a fully functional backend.
- **Early Stage Feature Development:** Data engineers can use this data to test initial data processing pipelines or database interactions.

By having readily available, schema-validated synthetic data, Alex ensures that development can proceed quickly and efficiently, preventing "prototype purgatory" and accelerating the path to an operational MVP.
