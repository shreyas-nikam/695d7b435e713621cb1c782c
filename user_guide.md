id: 695d7b435e713621cb1c782c_user_guide
summary: Week 1: Platform Foundation & Framework Architecture User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Week 1: Platform Foundation & Framework Architecture

## Introduction: Architecting the PE Org-AI-R Platform
Duration: 00:05:00

Welcome to **QuLab: Week 1: Platform Foundation & Framework Architecture**! This codelab guides you through the initial architectural sprint for the PE Org-AI-R Platform's AI Readiness Assessment system. You'll take on the persona of Alex, a Senior Software Engineer, tasked with laying a robust foundation for an enterprise AI system.

<aside class="positive">
<b>Why is this important?</b>
In the rapidly evolving landscape of enterprise AI, it's a common adage that "AI that lives in notebooks dies in production." The journey from a promising model in a research environment to a reliable, scalable, and maintainable production system is fraught with challenges. This codelab focuses on tackling these challenges head-on by emphasizing robust system architecture, clear data contracts, and disciplined engineering practices right from the start.
</aside>

This application demonstrates how to establish foundational elements that prevent common pitfalls like "prototype purgatory" – where promising prototypes fail to translate into production systems – and "ML technical debt" – the hidden costs of maintaining machine learning systems. We'll explore how APIs and data schemas serve as critical contracts between teams and system modules, crucial for preventing data chaos and integration headaches.

Our core objectives for this week include:
- Establishing a standardized, monorepo-friendly project structure.
- Defining precise data structures using Pydantic, acting as unambiguous data contracts.
- Ensuring data quality and integrity through built-in validation.
- Generating formal, machine-readable JSON Schemas for external integration.
- Creating synthetic data for accelerated development and testing.

<aside class="info">
Use the sidebar navigation on the left to navigate through Alex's architectural journey. Each section represents a crucial step in building a resilient enterprise AI platform.
</aside>

## 1. Project Environment Setup
Duration: 00:03:00

Alex's first step is to prepare the development environment and establish a standardized directory structure. A well-organized project structure is not merely a formality; it's a critical component for managing the complexity of a growing enterprise AI system. It enforces the **separation of concerns**, ensuring that different parts of the system handle distinct responsibilities, which is vital for preventing failures and simplifying maintenance in large-scale projects.

In this step, you'll simulate the creation of a foundational directory structure for the PE Org-AI-R Platform's monorepo. This structure aligns with industry best practices, setting the stage for efficient future development and collaboration.

<aside class="positive">
<b>Action: Initialize Project Structure</b>
Click the "Create/Verify Project Structure" button below. This action simulates the creation of the necessary folders and subdirectories. If a `src` directory already exists, the system will first clean it up to ensure a fresh, idempotent setup.
</aside>

Once the button is clicked, the application will display a verification of key directories.

If all critical directories are in place, you'll see a success message. This confirms that the foundational skeleton for your platform is successfully established. This systematic initialization helps reduce technical debt from the outset, enabling future development to proceed smoothly and efficiently.

## 2. Defining Core Data Schemas with Pydantic
Duration: 00:07:00

With the project structure in place, Alex moves on to defining the core data structures that will represent entities within the AI Readiness Assessment system. This is where Pydantic models come into play. Pydantic is a powerful data validation and parsing library that allows you to define clear **data contracts (schemas)** with built-in validation. This capability is paramount for ensuring data quality across different system components and is a key defense against **prototype purgatory**, where data inconsistencies can halt a project's progress.

### Pydantic Enums: Standardizing Categorical Data
Enums (enumerations) are used to define a set of named constant values. This ensures consistency across the codebase, preventing common issues like typos or variations in categorical data. The application uses Enums for:
- **`CompanyStatus`**: Defines the possible states of a company (e.g., Active, Inactive).
- **`OwnershipType`**: Specifies different types of company ownership (e.g., Target, Portfolio).
- **`DimensionName`**: Lists the seven core AI Readiness dimensions (e.g., Data Infrastructure, MLOps, AI Strategy).

You can see the defined Enum values in the application. These structured definitions are essential for maintaining data integrity.

### Default Dimension Weights
The platform also defines default weights for each AI readiness dimension. These weights represent the initial importance assigned to each dimension and can be customized later for specific sector calibrations. A critical business rule, also enforced by the schema, is that the sum of these weights must always be 1.0. This is expressed mathematically as:

$$ \sum_{d \in \text{DimensionName}} W_d = 1.0 $$

where $W_d$ is the weight assigned to dimension $d$. You can view the default weights displayed in the application.

### Core Pydantic Models Overview
The core Pydantic models serve as the blueprints for our data. Each `BaseModel` specifies the expected data types, required fields, and validation rules.
- **`Company` Model:** This model defines the comprehensive structure for companies within the system, including both user-provided fields and system-generated attributes like `company_id` and creation timestamps.
- **`DimensionScoreInput` Model:** This model structures how individual dimension scores are submitted. It includes validation rules for the score range (e.g., 0-100) and acceptable confidence levels.
- **`SectorCalibration` Model:** This model captures sector-specific baselines and dimension weights. Crucially, it enforces the business rule that the sum of dimension weights must always be 1.0. This prevents scoring inconsistencies between data science models and operational processes.

The application displays the JSON Schema representation of these models. These schemas define the unambiguous contracts that ensure data quality and seamless integration across all PE Org-AI-R platform components.

## 3. Enforcing Data Integrity through Schema Validation
Duration: 00:10:00

One of Pydantic's most significant advantages is its robust, automatic data validation. This mechanism is crucial for ensuring that all data flowing through the PE Org-AI-R platform adheres to the defined contracts. By catching errors early, validation prevents invalid or malformed data from entering the system, thereby averting **brittle orchestration** – where interconnected system components break due to unexpected data formats – and reducing **ML technical debt** caused by inconsistent data quality.

### Interactive Data Validation Examples
This section provides interactive forms where you can experiment with Pydantic's validation in real-time.

<aside class="positive">
<b>Experiment: Try entering both valid and invalid data into the forms below.</b> Observe how the application responds to ensure data integrity.
</aside>

#### Validate `CompanyCreate` Model
This form allows you to input details for a new company.
- Fill in the fields such as "Company Name", "Sector ID", and "Ownership Type".
- **Valid Data Example:** Provide a company name, a valid sector ID (like "tech_ai"), and select an ownership type. Enter a reasonable "Enterprise Value" and "EV Currency".
- **Invalid Data Example:** Try leaving a required field blank, or entering a non-numeric value where a number is expected. For example, enter `abc` for "Enterprise Value".

Click "Validate CompanyCreate" to see the validation result. If the data is valid, you'll see a JSON representation of the `CompanyCreate` object. If it's invalid, you'll see a `ValidationError` detailing the issues.

#### Validate `DimensionScoreInput` Model
This form validates the input for an individual AI readiness dimension score.
- **Valid Data Example:** Select a dimension, enter a score between 0 and 100 (e.g., 85.50), and select a confidence level. Add some rationale.
- **Invalid Data Example:** Try entering a "Score" outside the 0-100 range (e.g., 101 or -5).

Click "Validate DimensionScoreInput" to check the input.

#### Validate `SectorCalibration` Model
This form tests the validation for sector-specific calibration data, including a critical business rule.
- **Valid Data Example:** Provide a "Sector ID", "Sector Name", "H^R Baseline", and a "Effective Date".
    - For "Dimension Weights (JSON)", use the default weights provided (or any set of weights that **sum up to 1.0**).
    - For "Dimension Targets (JSON)", use any valid JSON dictionary with dimension names as keys and numeric targets as values.
- **Invalid Data Example:**
    - Try entering "Dimension Weights (JSON)" where the values **do not sum up to 1.0**. You will see a `ValidationError` due to the custom validation logic in the `SectorCalibration` model.
    - Try providing invalid JSON syntax in the weights or targets fields.

Click "Validate SectorCalibration" to observe the validation feedback.

By actively using these forms, you can see how Pydantic's schema validation acts as strong guardrails, preventing common data quality issues that can lead to significant problems down the line.

## 4. Generating Formal Data Contracts (JSON Schemas)
Duration: 00:05:00

After defining and validating our Pydantic models, the next crucial step is to generate **formal data contracts** in a universal format. This is where JSON Schema comes in. JSON Schema is a powerful tool for describing the structure, data types, and validation rules of JSON data. By generating JSON Schemas directly from our Pydantic models, we enable **contract-first development**. This approach ensures that all components interacting with our data – whether they are frontend applications, backend services, or external partner systems – operate with an agreed-upon, precise definition of the data structure. This is language-agnostic, making it ideal for heterogeneous environments.

### Generate JSON Schemas from Pydantic Models
Click the buttons below to generate and display the formal JSON Schemas for our core data models.

<aside class="positive">
Click each of the "Generate JSON Schema" buttons to dynamically create and display the corresponding JSON Schema.
</aside>

- **Generate `Company` JSON Schema:** This will output the comprehensive JSON Schema for the `Company` model, detailing all fields, their types, required status, and any specific validations (e.g., string length, date format).
- **Generate `DimensionScoreInput` JSON Schema:** This will show the schema for submitting individual dimension scores, including constraints like the score being between 0 and 100.
- **Generate `SectorCalibration` JSON Schema:** This schema will include all the details for sector-specific calibrations, notably how the `weights` field is structured and the implicit validation ensuring they sum to 1.0.

These machine-readable schemas provide an unambiguous definition of our data. Alex can now confidently share these contracts, knowing they enforce strict data integrity and facilitate seamless integration across different systems and teams. In a real-world project, these schemas would typically be version-controlled and exported to a designated directory, becoming a cornerstone of a continuous integration and deployment pipeline.

## 5. Generating Synthetic Data for Development and Testing
Duration: 00:05:00

Before live data pipelines are fully operational, Alex needs a way to accelerate API development, UI prototyping, and early-stage feature work. This is where **synthetic data generation** becomes invaluable. By generating synthetic data that rigorously adheres to the defined Pydantic schemas, developers can work independently, iterate faster, and avoid the common pitfall of **prototype purgatory** – where development stalls waiting for real data or complex integrations.

Synthetic data allows teams to build and test functionality in isolation, ensuring that components work correctly against expected data structures before integrating with upstream or downstream systems.

### Interactive Synthetic Data Generation
Use the controls below to generate synthetic data instances for companies, dimension scores, and sector calibrations. Observe how the generated data consistently conforms to the Pydantic schemas, making it immediately usable in development and testing environments.

First, you can specify a "Sector ID" and "Sector Name" that will be used for generating the synthetic data.

<aside class="positive">
<b>Action: Generate Synthetic Data</b>
Click each of the "Generate" buttons to create synthetic data for `Company`, `DimensionScoreInput`, and `SectorCalibration`.
</aside>

#### Generate Synthetic `Company`
Click "Generate Company". A new, unique synthetic `Company` object will be created, complete with a `company_id`, `created_at`, and other details, all conforming to the `Company` schema.

#### Generate Synthetic `DimensionScoreInput`
Click "Generate Dimension Score Input". A synthetic `DimensionScoreInput` will be generated. Notice that if you've already generated a synthetic company, the `company_id` from that company will be dynamically used, showcasing how synthetic data can be interconnected. Otherwise, a placeholder ID will be used.

#### Generate Synthetic `SectorCalibration`
Click "Generate Sector Calibration". This will produce a synthetic `SectorCalibration` object using the specified sector ID and name, along with randomly generated yet valid baselines, confidence intervals, weights (summing to 1.0), and targets.

This concludes Alex's foundational architectural sprint. By establishing a robust directory structure, defining clear data contracts enforced by Pydantic, generating formal JSON schemas, and creating synthetic data for accelerated development, the PE Org-AI-R platform is now well-positioned for future sprints and the seamless integration of advanced AI capabilities. This structured approach significantly reduces technical debt and prepares the platform for scalable and maintainable growth.
