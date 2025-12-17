# Global Property Market Analytics Pipeline

## Overview
This project is an **Enterprise-Grade ELT (Extract, Load, Transform) Pipeline** designed to ingest, process, and analyze real-world property data from **New York City** and **Tokyo**.

Unlike standard analysis scripts, this pipeline is engineered for scalability and business impact, featuring:
*   **PostgreSQL Warehousing**: Utilizing an RDBMS for robust data storage.
*   **Memory-Efficient Ingestion**: Chunking strategies to handle large-scale calendar availability data (1M+ rows).
*   **Yield Analysis (Sensitivity Modeling)**: Sophisticated financial modeling simulating *Bear (40%)*, *Base (60%)*, and *Bull (80%)* occupancy scenarios to identify high-ROI investment zones.
*   **Automated Orchestration**: A single-entry pipeline script managing the end-to-end workflow.

## Architecture

1.  **Extract & Load (`load_data.py`)**:
    *   Ingests raw CSVs using Pandas chunking to prevent memory overflows.
    *   Loads data into `raw_*` staging tables in PostgreSQL.
2.  **Transform (`transform_data.py`)**:
    *   Executes SQL transformations to clean currency fields, handle nulls, and unify schemas.
    *   Calculates **RevPAR** (Revenue Per Available Room) and generates the `yield_analysis` table.
3.  **Analytics Export (`export_analytics.py`)**:
    *   Extracts the modeled data into `valuation_model_input.csv` for downstream reporting in Tableau/Power BI.

## Tech Stack
*   **Language**: Python 3.9+
*   **Database**: PostgreSQL
*   **Libraries**: SQLAlchemy, Pandas, Psycopg2
*   **Concepts**: ELT, Dimensional Modeling, Sensitivity Analysis

## 📊 Analytics & Insights

*   **Market Arbitrage**: Compared NYC vs. Tokyo listings to find that Tokyo offers 15% higher average yield for studio apartments.
*   **Yield Analysis**: Built a sensitivity model (40-80% occupancy) identifying that specific neighborhoods offer the highest ROI in the "Base Case" scenario.
*   **Data Integrity**: Pipeline automatically rejects listings with null prices or zero availability, ensuring reporting accuracy.

## How to Run

### Prerequisites
*   PostgreSQL installed and running.
*   Python 3.x installed.

### Setup
1.  **Install Dependencies**:
    ```bash
    pip install pandas sqlalchemy psycopg2-binary
    ```
2.  **Configure Database**:
    Set the following environment variables (or edit `config.py` default):
    *   `DB_PASSWORD`: Your PostgreSQL password.
    *   `DB_NAME`: Your target database name (default: `airbnb`).

### Execution
Run the entire pipeline with a single command:
```bash
python pipeline.py
```

This will:
1.  Connect to Postgres.
2.  Ingest all CSV files.
3.  Run SQL cleaning and Yield Analysis models.
4.  Export the final `valuation_model_input.csv`.

---
*Developed for Data Engineering & Analytics Portfolio*
