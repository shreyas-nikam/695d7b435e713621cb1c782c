import os
import shutil
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Literal
from uuid import uuid4
import json

from pydantic import BaseModel, Field, ValidationError, model_validator
from faker import Faker
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
        f"{base_path}/schemas/v1/exports",  # For JSON schema exports
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
        "dags",  # For Apache Airflow DAGs
    ]

    for d in core_dirs:
        os.makedirs(d, exist_ok=True)

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
                f.write("# Package init\n")

    print("\nProject structure created successfully.")


# Execute the function to create the structure
project_root = "src/pe_orgair"
if os.path.exists("src"):  # Clean up previous run for idempotency
    shutil.rmtree("src")
create_project_structure(project_root)

# Verify creation (optional, for demonstration)
print("\nVerifying key directories:")
print(f"Schema dir exists: {os.path.exists(f'{project_root}/schemas/v1')}")
print(f"API routes dir exists: {os.path.exists(f'{project_root}/api/routes')}")
# Enums


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
    enterprise_value: Optional[Decimal] = Field(None, ge=0)
    ev_currency: str = Field("USD", max_length=3)
    ev_as_of_date: Optional[date] = None
    status: CompanyStatus = CompanyStatus.ACTIVE
    ownership_type: Optional[OwnershipType] = None
    fund_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


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
    confidence_level: Literal["high", "medium", "low"] = "medium"
    rationale: Optional[str] = Field(None, max_length=1000)
    evidence_chunk_ids: List[str] = Field(default_factory=list)

    @model_validator(mode='before')
    @classmethod
    def round_score(cls, values):
        if isinstance(values, dict) and 'score' in values and isinstance(values['score'], (float, Decimal)):
            values['score'] = Decimal(
                values['score']).quantize(Decimal("0.01"))
        return values


class DimensionScoreResult(BaseModel):
    """Stored dimension score with metadata for historical tracking."""
    score_id: str = Field(default_factory=lambda: str(uuid4()))
    company_id: str
    assessment_id: str = Field(default_factory=lambda: str(uuid4()))
    dimension: DimensionName
    score: Decimal = Field(..., ge=0, le=100)
    weight: Decimal = Field(..., ge=0, le=1)
    confidence_level: str
    assessor_id: Optional[str] = None
    assessment_method: str
    assessment_date: date
    evidence_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SectorCalibration(BaseModel):
    """Sector calibration including H^R and dimension weights."""
    sector_id: str
    sector_name: str
    h_r_baseline: Decimal = Field(..., ge=0, le=100,
                                  description="Systematic Opportunity (H^R) baseline score")
    h_r_ci_lower: Optional[Decimal] = Field(
        None, ge=0, le=100, description="Lower bound of H^R CI")
    h_r_ci_upper: Optional[Decimal] = Field(
        None, ge=0, le=100, description="Upper bound of H^R CI")
    weights: Dict[DimensionName, Decimal] = Field(
        ..., description="Weights for each dimension, must sum to 1.0")
    targets: Dict[DimensionName,
                  Decimal] = Field(..., description="Sector targets (benchmarks)")
    effective_date: date

    @model_validator(mode='after')
    def validate_weights_sum(self) -> 'SectorCalibration':
        total_weights = sum(self.weights.values())
        if abs(total_weights - Decimal("1.0")) > Decimal("0.001"):
            raise ValueError(
                f"Dimension weights must sum to 1.0, got {total_weights}")
        return self

    class Config:
        from_attributes = True


print("Pydantic models for PE Org-AI-R Platform defined.")
print("\nDEFAULT_WEIGHTS for dimensions:")
for dim, weight in DEFAULT_WEIGHTS.items():
    print(f"  - {dim.value}: {weight}")
print("--- Valid Data Instantiation ---")

# Example 1: Valid DimensionScoreInput
valid_score_input = DimensionScoreInput(
    dimension=DimensionName.DATA_INFRASTRUCTURE,
    score=Decimal("85.50"),
    confidence_level="high",
    rationale="Strong data pipeline and governance policies observed.",
    evidence_chunk_ids=["ev_id_001", "ev_id_002"],
)
print(
    f"\nSuccessfully created valid DimensionScoreInput:\n{valid_score_input.model_dump_json(indent=2)}")

# Example 2: Valid CompanyCreate
valid_company_create = CompanyCreate(
    name="InnovateAI Solutions",
    ticker="IAS",
    domain="innovateai.com",
    sector_id="tech_ai",
    enterprise_value=Decimal("120000000.50"),
    ev_currency="USD",
    ev_as_of_date=date(2023, 11, 15),
    ownership_type=OwnershipType.TARGET,
)
print(
    f"\nSuccessfully created valid CompanyCreate:\n{valid_company_create.model_dump_json(indent=2)}")

# Example 3: Valid SectorCalibration with DEFAULT_WEIGHTS
valid_sector_calibration = SectorCalibration(
    sector_id="tech_ai",
    sector_name="Technology & AI",
    h_r_baseline=Decimal("78.0"),
    h_r_ci_lower=Decimal("70.0"),
    h_r_ci_upper=Decimal("85.0"),
    weights=DEFAULT_WEIGHTS,
    targets={dim: Decimal("75.0") for dim in DimensionName},
    effective_date=date(2024, 1, 1),
)
print(
    f"\nSuccessfully created valid SectorCalibration:\n{valid_sector_calibration.model_dump_json(indent=2)}")
print("\n--- Demonstrating Validation Errors ---")

# Invalid DimensionScoreInput: Score out of bounds
try:
    invalid_score_input_score = DimensionScoreInput(
        dimension=DimensionName.TALENT,
        score=Decimal("101.0"),  # Invalid: score > 100
        confidence_level="medium",
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for invalid score:\n{e}")
    assert "less than or equal to 100" in str(e)

# Invalid DimensionScoreInput: Invalid confidence_level (Literal constraint)
try:
    invalid_score_input_confidence = DimensionScoreInput(
        dimension=DimensionName.LEADERSHIP,
        score=Decimal("65.0"),
        confidence_level="very_high",  # Invalid: not in allowed set
    )
except ValidationError as e:
    print(
        f"\nCaught expected ValidationError for invalid confidence_level:\n{e}")
    # Pydantic v2 literal error messages are more direct
    assert "Input should be 'high', 'medium' or 'low'" in str(e)

# Invalid SectorCalibration: Weights do not sum to 1.0
bad_weights = {dim: Decimal("0.10") for dim in DimensionName}  # Sums to 0.70
try:
    invalid_sector_calibration_weights = SectorCalibration(
        sector_id="finance",
        sector_name="Financial Services",
        h_r_baseline=Decimal("60.0"),
        weights=bad_weights,  # Invalid: sum != 1.0
        targets={dim: Decimal("65.0") for dim in DimensionName},
        effective_date=date(2024, 1, 1),
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for weights sum:\n{e}")
    assert "Dimension weights must sum to 1.0" in str(e)

# Invalid SectorCalibration: h_r_baseline out of bounds
try:
    invalid_sector_calibration_baseline = SectorCalibration(
        sector_id="healthcare",
        sector_name="Healthcare",
        h_r_baseline=Decimal("105.0"),  # Invalid: baseline > 100
        weights=DEFAULT_WEIGHTS,
        targets={dim: Decimal("70.0") for dim in DimensionName},
        effective_date=date(2024, 1, 1),
    )
except ValidationError as e:
    print(f"\nCaught expected ValidationError for h_r_baseline:\n{e}")
    assert "less than or equal to 100" in str(e)
print("--- Generating JSON Schemas ---")

# Generate JSON Schema for Company model
company_json_schema = Company.model_json_schema()
print("\nJSON Schema for Company:\n")
print(json.dumps(company_json_schema, indent=2))

# Generate JSON Schema for DimensionScoreInput model
dimension_score_input_json_schema = DimensionScoreInput.model_json_schema()
print("\nJSON Schema for DimensionScoreInput:\n")
print(json.dumps(dimension_score_input_json_schema, indent=2))

# Generate JSON Schema for SectorCalibration model
sector_calibration_json_schema = SectorCalibration.model_json_schema()
print("\nJSON Schema for SectorCalibration:\n")
print(json.dumps(sector_calibration_json_schema, indent=2))

# Save a schema to the designated exports directory
schema_export_path = f"{project_root}/schemas/v1/exports/company_v1.json"
with open(schema_export_path, "w") as f:
    f.write(json.dumps(company_json_schema, indent=2))
print(f"\nJSON Schema for Company exported to: {schema_export_path}")
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
        enterprise_value=Decimal(fake.random_int(
            min=1_000_000, max=10_000_000_000)),
        ev_currency=fake.currency_code(),
        ev_as_of_date=fake.date_between(start_date='-2y', end_date='today'),
        ownership_type=fake.random_element(list(OwnershipType)),
        fund_id=fake.uuid4() if fake.boolean(chance_of_getting_true=50) else None,
        status=fake.random_element(list(CompanyStatus)),
        created_at=fake.date_time_between(start_date='-5y', end_date='-1y'),
        updated_at=fake.date_time_between(start_date='-1y', end_date='now'),
    )


def generate_synthetic_dimension_score_input(company_id: str) -> DimensionScoreInput:
    """Generates a synthetic DimensionScoreInput instance."""
    return DimensionScoreInput(
        dimension=fake.random_element(list(DimensionName)),
        score=Decimal(
            str(fake.pyfloat(min_value=0, max_value=100, right_digits=2))),
        confidence_level=fake.random_element(["high", "medium", "low"]),
        rationale=fake.sentence(nb_words=10) if fake.boolean(
            chance_of_getting_true=70) else None,
        evidence_chunk_ids=[fake.uuid4()
                            for _ in range(fake.random_int(min=0, max=3))],
    )


def generate_synthetic_sector_calibration(sector_id: str, sector_name: str) -> SectorCalibration:
    """Generates a synthetic SectorCalibration instance with weights summing to 1.0."""
    dims = list(DimensionName)
    n = len(dims)
    # Create positive random raw weights
    raw = [Decimal(str(fake.pyfloat(min_value=0.1, max_value=1.0, right_digits=6)))
           for _ in range(n)]
    total = sum(raw)
    normalized = [w / total for w in raw]
    # Force exact sum to 1.0 by adjusting the last value
    adjusted = normalized[:-1]
    last = Decimal("1.0") - sum(adjusted)
    adjusted.append(last)
    weights = {dim: val for dim, val in zip(dims, adjusted)}

    return SectorCalibration(
        sector_id=sector_id,
        sector_name=sector_name,
        h_r_baseline=Decimal(
            str(fake.pyfloat(min_value=50, max_value=90, right_digits=2))),
        h_r_ci_lower=Decimal(str(fake.pyfloat(min_value=45, max_value=80, right_digits=2))) if fake.boolean(
            chance_of_getting_true=70) else None,
        h_r_ci_upper=Decimal(str(fake.pyfloat(min_value=60, max_value=95, right_digits=2))) if fake.boolean(
            chance_of_getting_true=70) else None,
        weights=weights,
        targets={dim: Decimal(
            str(fake.pyfloat(min_value=60, max_value=85, right_digits=2))) for dim in dims},
        effective_date=fake.date_between(start_date='-1y', end_date='today'),
    )


# Generate and display example synthetic data
print("--- Generating Synthetic Data ---")

# Synthetic Company
synth_company = generate_synthetic_company(sector_id="software_dev")
print(f"\nSynthetic Company:\n{synth_company.model_dump_json(indent=2)}")

# Synthetic DimensionScoreInput
synth_score_input = generate_synthetic_dimension_score_input(
    company_id=synth_company.company_id)
print(
    f"\nSynthetic DimensionScoreInput:\n{synth_score_input.model_dump_json(indent=2)}")

# Synthetic SectorCalibration
synth_sector_calibration = generate_synthetic_sector_calibration(
    sector_id="software_dev", sector_name="Software Development")
print(
    f"\nSynthetic SectorCalibration:\n{synth_sector_calibration.model_dump_json(indent=2)}")
