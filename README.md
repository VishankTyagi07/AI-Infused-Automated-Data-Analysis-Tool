# AI-Infused Automated Data Analysis Tool

An end-to-end data analysis system that automates **exploratory data analysis (EDA)**, **data cleaning**, **SQL generation**, and **visual analytics**, enhanced with **rule-based AI explanations** to ensure transparency and interpretability at every step.

The tool transforms a raw CSV dataset into **analysis-ready data and reusable analytical artifacts** within seconds, without relying on external AI APIs.

---

## Overview

Early-stage data analysis often involves repetitive yet critical steps:
- Understanding dataset structure
- Cleaning inconsistencies
- Writing exploratory SQL queries
- Creating initial visual summaries

This project consolidates those steps into a **single, explainable workflow** that mirrors how a data analyst or data scientist approaches a new dataset.

The system is designed to be deterministic, transparent, and artifact-driven.

---

## Key Features

### Dataset Ingestion
- Upload any CSV dataset
- Automatic extraction of schema, data types, and structural metadata

### Rule-Based AI Explanations
- Pre-action explanations describing what will be performed
- Post-action summaries explaining what changed and why
- Deterministic logic (no hallucinations, no black-box decisions)

### Automated Data Cleaning
- Column name standardization
- Missing value normalization
- Data type inference (numeric, datetime, categorical)
- Duplicate detection and removal
- Cleaned dataset preview before download
- Export of analysis-ready CSV

### Data Profiling
- Structural and statistical overview of the dataset
- Column-level data quality indicators
- Exportable HTML profiling report for exploratory inspection

### SQL Query Generation (EDA-Focused)
- Automatic generation of:
  - `CREATE TABLE` schema
  - Row counts
  - Missing value checks
  - Numeric summaries
  - Categorical frequency distributions
- Supports multiple SQL dialects:
  - ANSI SQL
  - PostgreSQL
  - MySQL
- User-defined table names
- Downloadable `.sql` file for direct database usage

### Automated Visualization
- Numeric distributions
- Categorical frequency charts
- Correlation heatmaps
- Time-series trends (when applicable)
- Interactive visualizations rendered in-app
- Exportable **standalone HTML dashboard** with professional styling

---

## Analytical Workflow

1. Upload dataset  
2. Review dataset summary  
3. Select an analysis action  
4. Review AI explanation (what will be done)  
5. Execute analysis  
6. Review AI log (what changed)  
7. Inspect results visually  
8. Download analytical artifacts  

UI state management ensures outputs are context-aware and do not persist incorrectly across actions.

---

## Project Structure

```
AI-Infused Automated Data Analysis Tool
├── app.py                      # Streamlit application
├── ai/
│   └── rule_based_summary.py   # Explainability layer
├── profiling/
│   └── profiler.py             # Dataset metadata & profiling
├── cleaner/
│   └── cleaner.py              # Data cleaning engine
├── sql/
│   └── sql_generator.py        # SQL generation logic
├── viz/
│   ├── visualizer.py           # Visualization engine
│   └── exporter.py             # HTML dashboard export
└── requirements.txt
```

## Design Principles

- **Explainability over automation**
- **Reproducibility over convenience**
- **Artifacts over screenshots**
- **User trust over black-box intelligence**

The system is intentionally rule-based to demonstrate strong fundamentals in:

- Exploratory data analysis
- Data preprocessing
- Analytical SQL
- Visual reasoning
- End-to-end analytical workflows

---

## Potential Extensions

- Optional LLM-based natural language querying
- Executable SQL via DuckDB
- Column-level visualization controls
- Session persistence and experiment tracking
- Cloud deployment

---

## Author

**Vishank Tyagi**  
GitHub: https://github.com/VishankTyagi07  
LinkedIn: https://www.linkedin.com/in/vishank-t/
