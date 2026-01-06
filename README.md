# PE Org-AI-R Platform: Week 1 - Platform Foundation & Framework Architecture

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-deployment-link-here.streamlit.app/)

## Project Title and Description

This repository contains the foundational code for **"QuLab: Week 1: Platform Foundation & Framework Architecture"** for the **PE Org-AI-R Platform**. This Streamlit application serves as an interactive guide for **Alex, a Senior Software Engineer**, on a critical mission: to architect the initial framework for an AI Readiness Assessment system.

In the fast-evolving landscape of enterprise AI, the maxim **"AI that lives in notebooks dies in production"** underscores the necessity of robust engineering practices. This lab project addresses this challenge by focusing on:

*   Establishing a disciplined project environment and monorepo structure.
*   Defining clear, validated data contracts using Pydantic models.
*   Generating formal JSON Schemas to prevent "prototype purgatory" and ensure seamless integration across services.
*   Creating synthetic data for accelerated API development and UI prototyping, mitigating "brittle orchestration" and "ML technical debt."

By emphasizing strong architectural principles from day one, this project aims to build a scalable, maintainable, and reliable platform for evaluating potential portfolio companies based on their AI readiness.

## Features

This Streamlit application provides a guided, interactive experience through the core architectural steps:

1.  **Project Environment Setup**: Simulate and verify the creation of a standardized monorepo directory structure, ensuring separation of concerns and best practices.
2.  **Defining Core Data Schemas**: Explore and understand the Pydantic models (`Company`, `DimensionScoreInput`, `SectorCalibration`) that define the foundational data structures and enums for the platform.
3.  **Enforcing Data Integrity**: Interact with forms to validate data against Pydantic schemas, demonstrating how automatic validation prevents malformed data and ensures consistency. This includes complex validations like ensuring weights sum to 1.0.
4.  **Generating Formal Data Contracts**: Generate and display machine-readable JSON Schemas directly from Pydantic models, facilitating contract-first development and cross-team communication.
5.  **Generating Synthetic Data**: Interactively create synthetic data instances that strictly conform to the defined schemas, accelerating development, testing, and UI prototyping without requiring live data pipelines.
6.  **Interactive Navigation**: A sidebar allows users to navigate seamlessly through different architectural stages of the lab.
7.  **Session State Management**: Ensures that form inputs and outputs persist across interactions, providing a smooth user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    *(Replace `your-username/your-repo-name.git` and `your-repo-name` with the actual repository details.)*

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    Create a `requirements.txt` file in the project root with the following content:
    ```
    streamlit
    pandas
    pydantic~=2.0 # or latest stable pydantic v2
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Streamlit application:

1.  Ensure you have followed the installation steps.
2.  Navigate to the root directory of the cloned repository.
3.  Execute the Streamlit command:
    ```bash
    streamlit run src/ui/app.py
    ```
    This will open the application in your default web browser.

Once the application is running, use the sidebar navigation to explore the different sections of the architectural lab. Experiment with the forms, observe validation messages, and generate schemas and synthetic data to understand the foundational principles of the PE Org-AI-R Platform.

## Project Structure

The application simulates and verifies a monorepo structure designed for an enterprise AI platform. Key directories within the project are:

```
.
├── src/
│   ├── pe_orgair/              # The root of the PE Org-AI-R platform application logic
│   │   ├── api/                # FastAPI application routes (stubs for future development)
│   │   │   └── routes/
│   │   ├── schemas/            # Pydantic models defining data contracts
│   │   │   └── v1/             # Versioned schemas
│   │   │       └── exports/    # Location for exported JSON Schemas
│   │   ├── services/           # Business logic and service implementations
│   │   │   └── scoring/        # AI readiness scoring logic
│   │   └── ...                 # Other platform modules
│   ├── ui/                     # Streamlit User Interface
│   │   └── app.py              # The main Streamlit application script
│   └── source.py               # (Assumed location) Contains Pydantic models, enums,
│                               # helper functions for project structure, and synthetic data generation.
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
The `source.py` file contains the core Pydantic models (`Company`, `DimensionScoreInput`, `SectorCalibration`), `Enum` definitions (`CompanyStatus`, `OwnershipType`, `DimensionName`), default dimension weights, and utility functions (`create_project_structure`, `generate_synthetic_company`, etc.) that power the Streamlit application's logic and data definitions.

## Technology Stack

*   **Python 3.x**: The core programming language.
*   **Streamlit**: For building the interactive web application interface.
*   **Pydantic**: For defining data schemas, models, and ensuring data validation and integrity.
*   **Pandas**: For potential data manipulation (imported, though not explicitly used for DataFrame display in the provided app code).
*   **FastAPI** (conceptual): The intended framework for the backend API, whose structure is being scaffolded.

## Contributing

This project is primarily a lab exercise to demonstrate architectural concepts. Contributions in the form of bug reports or suggestions for improving the clarity and educational value of the lab are welcome. Please open an issue in the repository.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
*(A `LICENSE` file would typically be present in the root directory for a full project.)*

## Contact

For questions or further information, please contact:

*   **QuantUniversity** - [https://www.quantuniversity.com](https://www.quantuniversity.com)
*   **Project Maintainer**: [Your Name/Team Name Here] - [your.email@example.com]
    *(Replace with actual contact information if applicable.)*