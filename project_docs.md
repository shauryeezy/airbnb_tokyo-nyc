# Global Property Market Analytics Pipeline

## 1. Executive Summary
This project implements an **Enterprise-Grade ELT (Extract, Load, Transform)** pipeline designed to analyze real-world property data from **New York City** and **Tokyo**. 

**Business Goal**: To identify high-ROI real estate investment opportunities by modeling revenue potential across varying occupancy scenarios.

**Key Features**:
*   **Scalable Architecture**: Utilizes PostgreSQL as a central data warehouse, capable of handling millions of records.
*   **Robust Ingestion**: Implements memory-safe chunking to process large datasets (400MB+) without crashing standard environments.
*   **Advanced Analytics**: Features a **Sensitivity Analysis Model** (Bear/Base/Bull case) to forecast annual yields.
*   **Automated Workflow**: A single orchestration script (`pipeline.py`) manages the end-to-end lifecycle.

---

## 2. Technical Architecture

### High-Level Design
The system follows a modern ELT pattern where raw data is loaded into the warehouse *first*, and transformations happen *in-database* for maximum performance.

```mermaid
graph LR
    A[Raw CSVs] -->|Load (Chunked)| B(PostgreSQL Staging Tables)
    B -->|SQL Transformation| C(Cleaned Core Layer)
    C -->|Yield Modeling| D(Analytics Layer)
    D -->|Export| E[Valuation Model CSV]
    E -->|Ingest| F[Power BI / Tableau]
```

### Components
1.  **Extract & Load (`load_data.py`)**: 
    *   Iterates through raw files (`listings_*.csv`).
    *   Uses `pandas.read_csv(chunksize=100000)` to stream data.
    *   Loads data into `raw_listings_tokyo`, `raw_listings_nyc`, etc.
2.  **Transform (`transform_data.py`)**:
    *   **Cleaning**: unifies currency symbols, removes non-numeric characters, and handles NULLs.
    *   **Logic**: Calculates RevPAR (Revenue Per Available Room).
    *   **Modeling**: Generates the `yield_analysis` table with sensitivity scenarios.
3.  **Analytics Export (`export_analytics.py`)**:
    *   Extracts final modeled data into `valuation_model_input.csv` for BI tools.

---

## 3. Data Dictionary & Schema Design

### Raw Layer (Staging)
*   `raw_listings_nyc` / `raw_listings_tokyo`: Direct copies of source CSVs.
    *   *Key Columns*: `id`, `name`, `host_id`, `neighbourhood`, `price` (text), `availability_365`.

### Transformation Layer (Core)
**Table: `clean_listings`**
A unified view of all cities with determining data types fixed.
| Column | Type | Description |
| :--- | :--- | :--- |
| `city` | TEXT | 'NYC' or 'Tokyo' |
| `id` | BIGINT | Unique Listing ID |
| `name` | TEXT | Listing Title |
| `neighbourhood` | TEXT | Cleansed Neighbourhood Name |
| `price_clean` | FLOAT | Price converted from Text (e.g., "$1,200.00" -> 1200.0) |
| `reviews` | INT | Number of reviews (Nulls handled as 0) |

### Analytics Layer (Mart)
**Table: `yield_analysis`**
The primary output for financial modeling.
| Column | Type | Calculation / Logic |
| :--- | :--- | :--- |
| `revenue_bear` | FLOAT | `price_clean * 365 * 40%` (Conservative Estimate) |
| `revenue_base` | FLOAT | `price_clean * 365 * 60%` (Realistic Estimate) |
| `revenue_bull` | FLOAT | `price_clean * 365 * 80%` (Optimistic Estimate) |

**Table: `neighbourhood_stats`**
Aggregated metrics for high-level reporting.
*   `avg_annual_revenue`: Average of Base Case revenue per neighbourhood.
*   `total_listings`: Supply volume per neighbourhood.

---

## 4. Business Logic: Yield Analysis
Real estate revenue is highly sensitive to occupancy rates. Instead of a single "average," we model three distinct scenarios to stress-test investment viability.

*   **🐻 Bear Case (40% Occupancy)**: Represents economic downturns or off-peak performance.
*   **⚖️ Base Case (60% Occupancy)**: The calibrated standard for performing assets.
*   **🐂 Bull Case (80% Occupancy)**: Peak season or high-demand performance.

This approach allows investors to filter out properties that only perform well in "Bull" scenarios, focusing instead on resilient assets that are profitable even in "Bear" markets.

---

## 5. Security & Configuration
*   **Configuration**: managed via `config.py` and environment variables.
*   **Secrets Management**: Database passwords are **not** hardcoded. They are retrieved via `os.getenv('DB_PASSWORD')`.
*   `.gitignore` is configured to exclude:
    *   Large Data Files (`*.csv`)
    *   Python Cache (`__pycache__`)
    *   Virtual Environment artifacts

---

## 6. How to Run

### Prerequisites
*   Python 3.8+
*   PostgreSQL 12+ (Locally or Cloud)

### One-Click Execution
The entire pipeline is orchestrated via `pipeline.py`.

```bash
# 1. Install Dependencies
pip install pandas sqlalchemy psycopg2-binary

# 2. Run Pipeline
python pipeline.py
```

### Expected Output
1.  **Console Logs**: Detailed progress bars for valid chunks.
2.  **Database**: creation of `clean_listings`, `yield_analysis`, and `neighbourhood_stats` tables.
3.  **File System**: Generation of `valuation_model_input.csv` (ready for Power BI).

---
*Documentation generated for Project Review*
