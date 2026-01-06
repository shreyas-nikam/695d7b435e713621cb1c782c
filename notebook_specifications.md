
# Jupyter Notebook Specification: Building Robust Data Models for AI-Readiness Assessment

## 1. Introduction: Laying the Foundation for PE Org-AI-R Platform

**Persona:** Sarah, a Data Engineer at "PE Org-AI-R Platform".

**Organization:** PE Org-AI-R Platform, a new venture focused on providing private equity firms with advanced AI-readiness assessments for their portfolio and target companies. The platform aims to offer comprehensive scoring, sector-specific benchmarks, and actionable insights into a company's AI capabilities.

**Story + Context + Real-World Relevance:**
Sarah's primary responsibility is to design and implement the robust data models that underpin the entire AI-readiness assessment system. Ensuring data integrity, consistency, and strict adherence to business rules is paramount for the platform's credibility and the accuracy of its insights. This notebook walks through Sarah's process of defining core entities, scoring inputs, and calibration parameters using Pydantic, a powerful data validation library. This work directly supports the platform's goal of delivering reliable AI-readiness scores to private equity clients.

---

## 2. Installing Required Libraries

```python
!pip install pydantic pandas matplotlib seaborn Faker
```

---

## 3. Importing Required Dependencies

```python
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from faker import Faker

fake = Faker()
```

---

## 4. Defining Core Business Entities: The Company Model

### Story + Context + Real-World Relevance

Sarah starts by defining the fundamental entity in the PE Org-AI-R Platform: the `Company`. This involves structuring essential company information and using Python `Enum` types to enforce categorical data, such as `CompanyStatus` and `OwnershipType`. By using Pydantic, she ensures that all company data ingested into the system will conform to predefined rules, preventing common data quality issues and facilitating consistent reporting.

```latex
The use of Pydantic's `BaseModel` for `Company` and `Field` for individual attributes ensures schema validation and data type enforcement. `Enum` types provide a finite set of allowed values, reducing ambiguity and errors in categorical fields.
```

### Code cell (function definition + function execution)

```python
class CompanyStatus(str, Enum):
    """Enumeration for company status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ACQUIRED = "acquired"
    EXITED = "exited"

class OwnershipType(str, Enum):
    """Enumeration for company ownership type."""
    PORTFOLIO = "portfolio"
    TARGET = "target"
    EXITED = "exited"
    BENCHMARK = "benchmark"

class CompanyBase(BaseModel):
    """Base company model with common fields."""
    name: str = Field(..., min_length=1, max_length=200, description="Company's official name.")
    ticker: Optional[str] = Field(None, max_length=20, description="Stock ticker symbol, if applicable.")
    domain: Optional[str] = Field(None, max_length=200, description="Company's primary domain/website.")
    cik: Optional[str] = Field(None, max_length=20, description="Central Index Key (CIK) for SEC filers.")
    sector_id: str = Field(..., description="Reference to sector calibration identifier.")
    sub_sector_id: Optional[str] = None

class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    enterprise_value: Optional[Decimal] = Field(None, ge=0, description="Monetary value of the company.")
    ev_currency: str = Field(default="USD", max_length=3, description="Currency of the enterprise value (e.g., 'USD').")
    ev_as_of_date: Optional[date] = None
    ownership_type: OwnershipType = OwnershipType.TARGET
    fund_id: Optional[str] = None

class Company(CompanyBase):
    """Full company model with all fields, including system-generated ones."""
    company_id: str = Field(..., description="Unique identifier for the company.")
    enterprise_value: Optional[Decimal] = Field(None, ge=0)
    ev_currency: str = Field(default="USD")
    ev_as_of_date: Optional[date] = None
    status: CompanyStatus = CompanyStatus.ACTIVE
    ownership_type: Optional[OwnershipType] = None
    fund_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Example usage: Instantiate a valid Company object
print("--- Valid Company Instance ---")
try:
    example_company = Company(
        company_id="comp_001",
        name="Tech Innovators Inc.",
        ticker="TINV",
        sector_id="tech_saas",
        enterprise_value=Decimal("150000000.00"),
        ownership_type=OwnershipType.PORTFOLIO,
        created_at=datetime(2023, 1, 1, 10, 0, 0)
    )
    print(example_company.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Error creating company: {e}")

# Example usage: Demonstrate validation error for Company
print("\n--- Invalid Company Instance (name too long) ---")
try:
    invalid_company = Company(
        company_id="comp_002",
        name="A very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very extremely detailed, yet clear and concise, as if a domain expert is explaining to another. The technical aspects must be precise and actionable. This is not for beginners.

**Goal:** Sarah needs to construct, validate, and generate synthetic data for these critical data models that will be consumed by other services within the PE Org-AI-R Platform.

---

## 5. Capturing Dimension Scores: Input & Result Models

### Story + Context + Real-World Relevance

The core of the AI-readiness assessment involves scoring companies across several predefined dimensions (e.g., Data Infrastructure, AI Governance). Sarah must define models to handle these dimension scores effectively. This includes `DimensionName` (an Enum for the specific dimensions), `DimensionScoreInput` (for raw input scores), and `DimensionScoreResult` (for validated and processed scores).

A key requirement for `DimensionScoreInput` is to ensure scores are within a valid range (0-100) and are rounded to two decimal places. This is crucial for maintaining numerical precision in downstream calculations. The `confidence_level` also needs validation to ensure it's one of 'high', 'medium', or 'low'.

```latex
The `DimensionScoreInput` model utilizes a custom `field_validator` to enforce a specific rounding rule for scores. The score value $s$ is rounded to two decimal places:
$$ s_{rounded} = \text{round}(s, 2) $$
Additionally, the score must satisfy $0 \le s \le 100$. The `confidence_level` field employs a regular expression pattern to restrict its values to 'high', 'medium', or 'low', denoted by $C \in \{\text{'high', 'medium', 'low'}\}$.
```

### Code cell (function definition + function execution)

```python
class DimensionName(str, Enum):
    """Seven validated dimensions of AI readiness."""
    DATA_INFRASTRUCTURE = "data_infrastructure"
    AI_GOVERNANCE = "ai_governance"
    TECHNOLOGY_STACK = "technology_stack"
    TALENT = "talent"
    LEADERSHIP = "leadership"
    USE_CASE_PORTFOLIO = "use_case_portfolio"
    CULTURE = "culture"

class DimensionScoreInput(BaseModel):
    """Input for a single dimension score."""
    dimension: DimensionName = Field(..., description="Name of the AI-readiness dimension.")
    score: Decimal = Field(..., ge=0, le=100, description="Score for the dimension (0-100).")
    confidence_level: Optional[str] = Field(
        default="medium",
        pattern="^(high|medium|low)$",
        description="Confidence level of the score assessment."
    )
    rationale: Optional[str] = Field(None, max_length=1000, description="Brief explanation for the score.")
    evidence_chunk_ids: List[str] = Field(default_factory=list, description="IDs of evidence chunks supporting the score.")

    @field_validator('score', mode='before')
    @classmethod
    def round_score(cls, v: Any) -> Decimal:
        """Scores should be rounded to 2 decimal places."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        if not isinstance(v, Decimal):
            raise ValueError("Score must be a number.")
        return v.quantize(Decimal("0.01"))

class DimensionScoreResult(BaseModel):
    """Stored dimension score with metadata."""
    score_id: str = Field(..., description="Unique identifier for the stored score.")
    company_id: str = Field(..., description="ID of the company being scored.")
    assessment_id: str = Field(..., description="ID of the overall assessment this score belongs to.")
    dimension: DimensionName = Field(..., description="Name of the AI-readiness dimension.")
    score: Decimal = Field(..., ge=0, le=100, description="Validated and rounded score for the dimension (0-100).")
    weight: Decimal = Field(..., ge=0, le=1, description="Weight applied to this dimension in overall score calculation.")
    confidence_level: str = Field(
        pattern="^(high|medium|low)$",
        description="Confidence level of the score assessment."
    )
    assessor_id: Optional[str] = None
    assessment_method: str = Field(..., description="Method used for assessment (e.g., 'manual', 'automated').")
    assessment_date: date = Field(..., description="Date of the assessment.")
    evidence_count: int = Field(0, ge=0, description="Number of evidence pieces linked to this score.")
    created_at: datetime = Field(default_factory=datetime.now)

# Example usage: Valid DimensionScoreInput
print("--- Valid DimensionScoreInput Instance ---")
try:
    valid_score_input = DimensionScoreInput(
        dimension=DimensionName.DATA_INFRASTRUCTURE,
        score=75.567, # Will be rounded to 75.57
        confidence_level="high",
        rationale="Strong data governance practices."
    )
    print(valid_score_input.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Error creating score input: {e}")

# Example usage: Invalid DimensionScoreInput (score out of bounds)
print("\n--- Invalid DimensionScoreInput (score < 0) ---")
try:
    invalid_score_input_low = DimensionScoreInput(
        dimension=DimensionName.TALENT,
        score=-5,
        confidence_level="medium"
    )
    print(invalid_score_input_low.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Validation Error: {e}")

print("\n--- Invalid DimensionScoreInput (confidence_level pattern mismatch) ---")
try:
    invalid_score_input_confidence = DimensionScoreInput(
        dimension=DimensionName.CULTURE,
        score=60,
        confidence_level="very_high" # Invalid value
    )
    print(invalid_score_input_confidence.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Validation Error: {e}")

# Example usage: Valid DimensionScoreResult
print("\n--- Valid DimensionScoreResult Instance ---")
try:
    valid_score_result = DimensionScoreResult(
        score_id="score_123",
        company_id="comp_001",
        assessment_id="assess_abc",
        dimension=DimensionName.AI_GOVERNANCE,
        score=82.75,
        weight=Decimal("0.20"),
        confidence_level="high",
        assessment_method="manual",
        assessment_date=date(2023, 10, 26)
    )
    print(valid_score_result.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Error creating score result: {e}")
```

### Markdown cell (explanation of execution)

The output demonstrates successful instantiation of `DimensionScoreInput` and `DimensionScoreResult` objects when valid data is provided. Notably, the `round_score` validator automatically rounds `75.567` to `75.57`. The subsequent error messages illustrate how Pydantic's `ValidationError` catches invalid inputs, such as scores outside the `[0, 100]` range or `confidence_level` values that do not match the specified regex pattern. For Sarah, this robust validation ensures that only clean, well-formatted scores enter the system, which is critical for accurate AI-readiness calculations and preventing upstream data processing errors.

---

## 6. Tailoring to Sectors: The Sector Calibration Model

### Story + Context + Real-World Relevance

AI-readiness is not a one-size-fits-all metric. Different sectors might have varying baselines, risk profiles, and most importantly, different weightings for each AI dimension. For instance, "Data Infrastructure" might be more critical for a FinTech company than for a Media company. Sarah needs to define the `SectorCalibration` model to capture these sector-specific adjustments. This model must include a robust validator to ensure that the sum of dimension weights for any given sector always totals 1.0, reflecting a complete and accurate distribution of importance across dimensions. This is a fundamental constraint for any weighted scoring model.

```latex
The `SectorCalibration` model includes a critical `model_validator` that checks the sum of dimension weights. Let $w_d$ be the weight for a dimension $d \in DimensionName$. The validator ensures that the sum of all weights equals 1.0, with a tolerance for floating-point inaccuracies:
$$ \left| \sum_{d \in DimensionName} w_d - 1.0 \right| \le 0.001 $$
If this condition is not met, a `ValueError` is raised. The `h_r_baseline`, `h_r_ci_lower`, and `h_r_ci_upper` fields represent the baseline Systematic Opportunity (H^R) and its confidence interval for a given sector, and must satisfy $0 \le \text{value} \le 100$.
```

### Code cell (function definition + function execution)

```python
DEFAULT_WEIGHTS: Dict[DimensionName, Decimal] = {
    DimensionName.DATA_INFRASTRUCTURE: Decimal("0.25"),
    DimensionName.AI_GOVERNANCE: Decimal("0.20"),
    DimensionName.TECHNOLOGY_STACK: Decimal("0.15"),
    DimensionName.TALENT: Decimal("0.15"),
    DimensionName.LEADERSHIP: Decimal("0.10"),
    DimensionName.USE_CASE_PORTFOLIO: Decimal("0.10"),
    DimensionName.CULTURE: Decimal("0.05"),
}

class SectorCalibration(BaseModel):
    """Sector calibration data including H^R and dimension weights."""
    sector_id: str = Field(..., description="Unique identifier for the sector.")
    sector_name: str = Field(..., description="Human-readable name of the sector.")
    
    # Systematic Opportunity (H^R)
    h_r_baseline: Decimal = Field(..., ge=0, le=100, description="Baseline Systematic Opportunity (H^R) score for the sector.")
    h_r_ci_lower: Optional[Decimal] = Field(None, ge=0, le=100, description="Lower bound of the H^R confidence interval.")
    h_r_ci_upper: Optional[Decimal] = Field(None, ge=0, le=100, description="Upper bound of the H^R confidence interval.")
    
    # Dimension weights
    weights: Dict[DimensionName, Decimal] = Field(
        default_factory=lambda: DEFAULT_WEIGHTS,
        description="Weights for each dimension, summing to 1.0."
    )
    
    # Sector targets (75th percentile benchmarks)
    targets: Dict[DimensionName, Decimal] = Field(
        default_factory=lambda: {d: Decimal("75.00") for d in DimensionName},
        description="75th percentile benchmark scores for each dimension in this sector."
    )
    effective_date: date = Field(..., description="Date from which this calibration is effective.")

    @model_validator(mode='after')
    def validate_weights_sum(self) -> 'SectorCalibration':
        """Dimension weights must sum to 1.0."""
        total = sum(self.weights.values())
        if abs(total - Decimal("1.0")) > Decimal("0.001"):
            raise ValueError(f"Dimension weights must sum to 1.0, got {total}")
        return self

# Example usage: Valid SectorCalibration
print("--- Valid SectorCalibration Instance (with default weights) ---")
try:
    valid_calibration = SectorCalibration(
        sector_id="tech_saas",
        sector_name="Technology - SaaS",
        h_r_baseline=Decimal("70.5"),
        h_r_ci_lower=Decimal("65.0"),
        h_r_ci_upper=Decimal("76.0"),
        effective_date=date(2023, 1, 1)
    )
    print(f"Weights sum for valid_calibration: {sum(valid_calibration.weights.values()):.2f}")
    print(valid_calibration.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Error creating valid calibration: {e}")

# Example usage: Invalid SectorCalibration (weights do not sum to 1.0)
print("\n--- Invalid SectorCalibration (weights sum != 1.0) ---")
try:
    bad_weights = {d: Decimal("0.10") for d in DimensionName} # Sums to 0.70
    invalid_calibration_weights = SectorCalibration(
        sector_id="retail_ecommerce",
        sector_name="Retail - E-commerce",
        h_r_baseline=Decimal("60.0"),
        weights=bad_weights,
        effective_date=date(2023, 3, 1)
    )
    print(invalid_calibration_weights.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Validation Error: {e}")

# Example usage: Invalid SectorCalibration (H^R baseline out of bounds)
print("\n--- Invalid SectorCalibration (H^R baseline > 100) ---")
try:
    invalid_calibration_hr = SectorCalibration(
        sector_id="healthcare_biotech",
        sector_name="Healthcare - Biotech",
        h_r_baseline=Decimal("110.0"), # Invalid baseline
        effective_date=date(2023, 6, 1)
    )
    print(invalid_calibration_hr.model_dump_json(indent=2))
except ValidationError as e:
    print(f"Validation Error: {e}")
```

### Markdown cell (explanation of execution)

The execution clearly demonstrates the `validate_weights_sum` validator in action. The first example shows a `SectorCalibration` instance successfully created using the `DEFAULT_WEIGHTS` which correctly sum to 1.0. The output confirms the sum of weights is `1.00`. The second example, where custom `bad_weights` sum to `0.70`, results in a `ValidationError` with a clear message, confirming the model's enforcement of the crucial sum-to-one constraint. The third example validates the bounds of `h_r_baseline`. This strict validation prevents erroneous weighting schemas from affecting the overall AI-readiness calculations, ensuring that the platform's sector-specific insights are always based on sound mathematical principles.

---

## 7. Data Generation and Validation in Practice

### Story + Context + Real-World Relevance

With the core Pydantic models defined and validated, Sarah's next step is to demonstrate their real-world application by generating synthetic data. This isn't just for testing; in a development cycle, synthetic data is vital for populating development environments, stress-testing new features, and creating realistic scenarios for analytics and reporting without relying on sensitive production data. She will generate data for `Company` entities, `DimensionScoreInput` records, and `SectorCalibration` profiles, showcasing both successful data instantiation and explicit handling of validation errors when malformed data is intentionally introduced.

```latex
Synthetic data generation allows for systematic testing of Pydantic models. For a given Pydantic model $M$, a set of synthetic instances $I = \{m_1, m_2, \ldots, m_k\}$ is generated. Each $m_i$ is then validated against $M$. The process includes:
1. Generating valid data to confirm successful parsing: $m_i = M(\text{valid\_data})$.
2. Generating invalid data to confirm error handling: $M(\text{invalid\_data}) \implies \text{ValidationError}$.
```

### Code cell (function definition + function execution)

```python
# Helper function to generate a random Decimal score
def generate_random_decimal_score(min_val: int = 0, max_val: int = 100) -> Decimal:
    return Decimal(str(round(random.uniform(min_val, max_val), 2)))

# Generate synthetic Company data
def generate_companies(num_companies: int) -> List[Company]:
    companies = []
    for i in range(num_companies):
        company_id = f"comp_{i:03d}"
        name = fake.company()
        ticker = fake.bothify(text='???###', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        domain = fake.domain_name()
        sector_id = random.choice(["tech_saas", "fintech", "healthcare_biotech", "manufacturing", "retail_ecommerce"])
        ownership_type = random.choice(list(OwnershipType))
        status = random.choice(list(CompanyStatus))
        created_at = fake.date_time_between(start_date="-2y", end_date="now")
        updated_at = fake.date_time_between(start_date=created_at, end_date="now")
        
        try:
            company = Company(
                company_id=company_id,
                name=name,
                ticker=ticker,
                domain=domain,
                sector_id=sector_id,
                enterprise_value=Decimal(str(round(random.uniform(1_000_000, 1_000_000_000), 2))),
                ownership_type=ownership_type,
                status=status,
                created_at=created_at,
                updated_at=updated_at
            )
            companies.append(company)
        except ValidationError as e:
            print(f"Failed to generate company {company_id}: {e}")
    return companies

# Generate synthetic DimensionScoreInput data
def generate_dimension_score_inputs(companies: List[Company], num_scores_per_company: int) -> List[DimensionScoreInput]:
    score_inputs = []
    for company in companies:
        for _ in range(num_scores_per_company):
            dimension = random.choice(list(DimensionName))
            score = generate_random_decimal_score()
            confidence_level = random.choice(["high", "medium", "low"])
            
            try:
                score_input = DimensionScoreInput(
                    dimension=dimension,
                    score=score,
                    confidence_level=confidence_level,
                    rationale=fake.sentence(),
                    evidence_chunk_ids=[fake.uuid4() for _ in range(random.randint(0, 3))]
                )
                score_inputs.append(score_input)
            except ValidationError as e:
                print(f"Failed to generate score for {company.company_id}, dimension {dimension}: {e}")
    return score_inputs

# Generate synthetic SectorCalibration data
def generate_sector_calibrations(sector_ids: List[str]) -> List[SectorCalibration]:
    calibrations = []
    for sector_id in sector_ids:
        sector_name = sector_id.replace("_", " ").title() # Simple conversion
        h_r_baseline = generate_random_decimal_score(min_val=50, max_val=85)
        h_r_ci_lower = h_r_baseline - generate_random_decimal_score(min_val=5, max_val=10)
        h_r_ci_upper = h_r_baseline + generate_random_decimal_score(min_val=5, max_val=10)
        effective_date = fake.date_this_year()

        # Randomly vary weights for some sectors to ensure validation
        weights_sum = Decimal("0.0")
        sector_weights = {}
        # Ensure weights sum to 1.0 (with slight variation for testing validation)
        for dim in DimensionName:
            sector_weights[dim] = generate_random_decimal_score(min_val=0, max_val=30)
            weights_sum += sector_weights[dim]
        
        # Normalize weights to sum to 1.0, or create invalid ones for testing
        if random.random() < 0.2: # 20% chance to create invalid weights
            # Intentionally make weights not sum to 1.0
            pass 
        else:
            if weights_sum != Decimal("0.0"):
                factor = Decimal("1.0") / weights_sum
                sector_weights = {dim: w * factor for dim, w in sector_weights.items()}
            else: # All weights were zero, assign default
                sector_weights = DEFAULT_WEIGHTS

        try:
            calibration = SectorCalibration(
                sector_id=sector_id,
                sector_name=sector_name,
                h_r_baseline=h_r_baseline,
                h_r_ci_lower=h_r_ci_lower.quantize(Decimal("0.01")),
                h_r_ci_upper=h_r_ci_upper.quantize(Decimal("0.01")),
                weights=sector_weights,
                effective_date=effective_date
            )
            calibrations.append(calibration)
        except ValidationError as e:
            print(f"Failed to generate calibration for sector {sector_id}: {e}")
    return calibrations

# Execute data generation
num_companies_to_generate = 10
num_scores_per_company = 5
unique_sector_ids = ["tech_saas", "fintech", "healthcare_biotech", "manufacturing", "retail_ecommerce"]

generated_companies = generate_companies(num_companies_to_generate)
generated_score_inputs = generate_dimension_score_inputs(generated_companies, num_scores_per_company)
generated_sector_calibrations = generate_sector_calibrations(unique_sector_ids)

print(f"\nGenerated {len(generated_companies)} companies.")
print(f"Generated {len(generated_score_inputs)} dimension score inputs.")
print(f"Generated {len(generated_sector_calibrations)} sector calibrations.")

# Demonstrate an explicit ValidationError with invalid data for Company
print("\n--- Explicit Validation Error Demonstration (Company) ---")
try:
    Company(
        company_id="invalid_comp",
        name="", # Invalid: min_length=1
        sector_id="valid_sector",
        enterprise_value=Decimal("-100") # Invalid: ge=0
    )
except ValidationError as e:
    print("Caught expected ValidationError for invalid Company data:")
    for error in e.errors():
        print(f"  Field: {error.get('loc')}, Message: {error.get('msg')}")

# Demonstrate an explicit ValidationError with invalid data for DimensionScoreInput
print("\n--- Explicit Validation Error Demonstration (DimensionScoreInput) ---")
try:
    DimensionScoreInput(
        dimension=DimensionName.CULTURE,
        score=150, # Invalid: le=100
        confidence_level="unknown" # Invalid pattern
    )
except ValidationError as e:
    print("Caught expected ValidationError for invalid DimensionScoreInput data:")
    for error in e.errors():
        print(f"  Field: {error.get('loc')}, Message: {error.get('msg')}")

# Demonstrate an explicit ValidationError with invalid data for SectorCalibration
print("\n--- Explicit Validation Error Demonstration (SectorCalibration) ---")
try:
    SectorCalibration(
        sector_id="test_sector_invalid_weights",
        sector_name="Test Invalid",
        h_r_baseline=Decimal("70.0"),
        weights={dim: Decimal("0.10") for dim in DimensionName}, # Sums to 0.70
        effective_date=date(2024, 1, 1)
    )
except ValidationError as e:
    print("Caught expected ValidationError for invalid SectorCalibration data (weights):")
    for error in e.errors():
        print(f"  Field: {error.get('loc')}, Message: {error.get('msg')}")
```

### Markdown cell (explanation of execution)

The synthetic data generation functions successfully create lists of valid `Company`, `DimensionScoreInput`, and `SectorCalibration` objects. The output confirms the number of generated instances for each model. More importantly, the explicit error demonstrations showcase how Sarah's Pydantic models effectively catch invalid data. For example, trying to create a `Company` with an empty name or negative enterprise value, a `DimensionScoreInput` with a score above 100 or an invalid confidence level, or a `SectorCalibration` with weights that don't sum to 1.0 (within tolerance), all correctly raise `ValidationError` with specific error messages. This granular error reporting is invaluable for debugging data pipelines and ensuring that data quality gates are enforced rigorously.

---

## 8. Exploring the AI-Readiness Data Landscape

### Story + Context + Real-World Relevance

After generating and validating the foundational data, Sarah needs to provide initial insights into this data. Visualizations are key for understanding distributions, identifying potential biases, and quickly verifying that the generated synthetic data (and by extension, future real data) behaves as expected. For instance, visualizing the distribution of dimension scores helps confirm if the assessment system is producing a reasonable range of values. Plotting dimension weights across sectors offers a direct way to compare calibration strategies and ensure they align with business expectations. This step is crucial for Sarah to communicate her data model's implications to analysts and business stakeholders.

```latex
Visualizations aid in understanding the statistical properties of the generated data.
1. Histograms illustrate the distribution of scores: $P(S=s)$.
2. Bar charts compare dimension weights across sectors: $w_d(\text{sector})$.
3. Line plots show sector baselines and confidence intervals: $(H_{R_{baseline}}, H_{R_{CI_{lower}}}, H_{R_{CI_{upper}}})(\text{sector})$.
```

### Code cell (function definition + function execution)

```python
# Convert generated Company data to a Pandas DataFrame for summary and visualization
def companies_to_dataframe(companies: List[Company]) -> pd.DataFrame:
    data = [c.model_dump() for c in companies]
    df = pd.DataFrame(data)
    # Ensure Decimal columns are converted to float for plotting if necessary, handle NaNs
    for col in ['enterprise_value']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: float(x) if x is not None else x)
    return df

# Convert generated DimensionScoreInput data to a Pandas DataFrame
def score_inputs_to_dataframe(score_inputs: List[DimensionScoreInput]) -> pd.DataFrame:
    data = [s.model_dump() for s in score_inputs]
    df = pd.DataFrame(data)
    df['score'] = df['score'].astype(float) # Convert Decimal to float for plotting
    return df

# Convert generated SectorCalibration data to a Pandas DataFrame
def sector_calibrations_to_dataframe(calibrations: List[SectorCalibration]) -> pd.DataFrame:
    data = []
    for c in calibrations:
        entry = c.model_dump()
        entry['weights_sum'] = sum(c.weights.values()) # Add weights sum for verification
        # Flatten weights and targets for easier plotting
        for dim_name, weight_val in c.weights.items():
            entry[f'weight_{dim_name.value}'] = float(weight_val)
        for dim_name, target_val in c.targets.items():
            entry[f'target_{dim_name.value}'] = float(target_val)
        
        # Convert Decimal fields to float for plotting
        for field in ['h_r_baseline', 'h_r_ci_lower', 'h_r_ci_upper']:
            if field in entry and entry[field] is not None:
                entry[field] = float(entry[field])

        data.append(entry)
    df = pd.DataFrame(data)
    return df


# Execute conversion to DataFrames
companies_df = companies_to_dataframe(generated_companies)
score_inputs_df = score_inputs_to_dataframe(generated_score_inputs)
sector_calibrations_df = sector_calibrations_to_dataframe(generated_sector_calibrations)

print("--- Summary of Generated Company Data ---")
print(companies_df.head())
print("\n--- Summary of Generated Dimension Scores ---")
print(score_inputs_df.head())
print("\n--- Summary of Generated Sector Calibrations ---")
print(sector_calibrations_df.head())

# Visualization 1: Distribution of Enterprise Values
plt.figure(figsize=(10, 6))
sns.histplot(companies_df['enterprise_value'], kde=True, bins=10)
plt.title('Distribution of Company Enterprise Values')
plt.xlabel('Enterprise Value (Log Scale)')
plt.ylabel('Number of Companies')
plt.xscale('log') # Use log scale due to potential wide range
plt.grid(True, which="both", ls="--", c='0.7')
plt.show()

# Visualization 2: Distribution of Dimension Scores
plt.figure(figsize=(12, 7))
sns.histplot(score_inputs_df, x='score', hue='dimension', multiple='stack', bins=20, palette='viridis')
plt.title('Distribution of Dimension Scores by Dimension Name')
plt.xlabel('Score (0-100)')
plt.ylabel('Count')
plt.grid(True, which="both", ls="--", c='0.7')
plt.legend(title='Dimension', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Visualization 3: Dimension Weights Across Sectors
weights_data = []
for index, row in sector_calibrations_df.iterrows():
    for dim in DimensionName:
        weight_col = f'weight_{dim.value}'
        if weight_col in row:
            weights_data.append({
                'sector_name': row['sector_name'],
                'dimension': dim.value,
                'weight': row[weight_col]
            })
weights_df = pd.DataFrame(weights_data)

plt.figure(figsize=(14, 8))
sns.barplot(data=weights_df, x='dimension', y='weight', hue='sector_name', palette='tab10')
plt.title('Dimension Weights Across Different Sectors')
plt.xlabel('AI-Readiness Dimension')
plt.ylabel('Weight')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Visualization 4: H^R Baseline and Confidence Interval for Sectors
hr_cols = ['sector_name', 'h_r_baseline', 'h_r_ci_lower', 'h_r_ci_upper']
hr_df = sector_calibrations_df[hr_cols].set_index('sector_name').dropna()

plt.figure(figsize=(12, 7))
hr_df[['h_r_baseline', 'h_r_ci_lower', 'h_r_ci_upper']].plot(kind='bar', figsize=(12,7), ax=plt.gca(), width=0.8)
plt.errorbar(
    x=range(len(hr_df)),
    y=hr_df['h_r_baseline'],
    yerr=[hr_df['h_r_baseline'] - hr_df['h_r_ci_lower'], hr_df['h_r_ci_upper'] - hr_df['h_r_baseline']],
    fmt='none', capsize=5, color='black', label='CI Range'
)
plt.title('H^R Baseline and Confidence Interval by Sector')
plt.xlabel('Sector Name')
plt.ylabel('Score (0-100)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
```

### Markdown cell (explanation of execution)

The visualizations provide immediate, actionable insights into the structured data. The histograms of `Enterprise Value` and `Dimension Scores` confirm the ranges and distributions are reasonable for synthetic data. The `Dimension Weights Across Different Sectors` bar chart allows Sarah to visually inspect if sector-specific weighting strategies are distinct and sum up correctly (though individual bars only show weights, the underlying data was validated to sum to 1.0). Finally, the `H^R Baseline and Confidence Interval by Sector` plot clearly displays the sector-specific systematic opportunity benchmarks, highlighting both the central tendency and the uncertainty range for each sector. For Sarah and her team, these plots are vital for sanity-checking the data generation process, validating the impact of calibration parameters, and quickly communicating key data characteristics to non-technical stakeholders in PE firms. This proactive data exploration helps in refining models and ensuring the platform's outputs are both accurate and interpretable.

