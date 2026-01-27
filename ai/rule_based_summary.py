def generate_dataset_summary(metadata: dict) -> str:
    dataset = metadata["dataset"]
    columns = metadata["columns"]
    flags = metadata["flags"]

    row_count = dataset["row_count"]
    column_count = dataset["column_count"]

    # Count column types
    numeric_cols = [c for c in columns if c["is_numeric"]]
    categorical_cols = [c for c in columns if c["is_categorical"]]
    datetime_cols = [c for c in columns if c["is_datetime"]]

    summary_parts = []

    # 1. Dataset overview
    summary_parts.append(
        f"Dataset Overview\n"
        f"This dataset contains {row_count} rows and {column_count} columns."
    )

    # 2. Data composition
    composition = []
    if numeric_cols:
        composition.append("numeric variables suitable for statistical analysis")
    if categorical_cols:
        composition.append("categorical variables that enable segmentation")
    if datetime_cols:
        composition.append("datetime fields that allow time-based trend analysis")

    if composition:
        summary_parts.append(
            "Data Composition\n"
            "The dataset includes " + ", ".join(composition) + "."
        )

    # 3. Analytical opportunities
    opportunities = []

    if numeric_cols:
        opportunities.append("descriptive statistics and distribution analysis")
    if numeric_cols and categorical_cols:
        opportunities.append("group-wise comparisons across categories")
    if numeric_cols and datetime_cols:
        opportunities.append("trend and time-series analysis")

    if opportunities:
        summary_parts.append(
            "Analytical Opportunities\n"
            "Recommended analyses include " + ", ".join(opportunities) + "."
        )

    # 4. Data quality considerations
    quality_notes = []

    if flags["high_missing_columns"]:
        quality_notes.append(
            "some columns exhibit high missing values, which may impact reliability"
        )
    if flags["constant_columns"]:
        quality_notes.append(
            "certain columns contain constant values and may not be useful for analysis"
        )
    if flags["possible_id_columns"]:
        quality_notes.append(
            "some columns appear to be identifiers and should be excluded from aggregations"
        )

    if quality_notes:
        summary_parts.append(
            "Data Quality Considerations\n"
            "Please note that " + "; ".join(quality_notes) + "."
        )

    # 5. Next steps
    summary_parts.append(
        "Next Steps\n"
        "Use the options below to generate profiling reports, clean the dataset, "
        "create SQL queries, or visualize the data."
    )

    return "\n\n".join(summary_parts)

# Generate cleaning process summary
def cleaning_process_summary(metadata: dict) -> str:
    flags = metadata["flags"]

    summary = [
        "### Cleaning Process Overview",
        "When you proceed, the dataset will undergo the following steps:",
        "- Column names will be standardized",
        "- Common missing value patterns will be normalized",
        "- Data types will be inferred automatically (numeric, datetime, categorical)",
        "- Duplicate records will be removed",
    ]

    if flags["high_missing_columns"]:
        summary.append(
            f"- Columns with high missing values detected: {', '.join(flags['high_missing_columns'])}"
        )

    if flags["possible_id_columns"]:
        summary.append(
            f"- Identifier-like columns detected: {', '.join(flags['possible_id_columns'])}"
        )

    summary.append(
        "This process improves data consistency and prepares the dataset for analysis."
    )

    return "\n".join(summary)


def generate_cleaning_result_summary(original_df, cleaned_df) -> str:
    summary = []

    summary.append("### Cleaning Results Summary")

    # Rows
    if len(original_df) != len(cleaned_df):
        summary.append(
            f"- Removed {len(original_df) - len(cleaned_df)} duplicate rows."
        )

    # Columns
    removed_cols = set(original_df.columns) - set(cleaned_df.columns)
    if removed_cols:
        summary.append(
            f"-Cleaned columns: {', '.join(removed_cols)}."
        )

    # Type changes
    type_changes = []
    for col in cleaned_df.columns:
        if col in original_df.columns:
            if original_df[col].dtype != cleaned_df[col].dtype:
                type_changes.append(
                    f"{col} → {cleaned_df[col].dtype}"
                )

    if type_changes:
        summary.append(
            "- Inferred and standardized data types:\n  - "
            + "\n  - ".join(type_changes)
        )

    if len(summary) == 1:
        summary.append("- No structural changes detected.")

    summary.append("The dataset is now standardized and ready for analysis.")

    return "\n".join(summary)

def generate_profile_summary(metadata: dict) -> str:
    cols = metadata["columns"]
    flags = metadata["flags"]

    lines = [
        "### Profiling Report Overview",
        "This process will generate an exploratory profiling report containing:",
        "- Dataset shape and structure",
        "- Column-wise statistics and data types",
        "- Missing value analysis",
        "- Distribution summaries for numeric variables",
        "- Frequency analysis for categorical variables",
    ]

    if flags["high_missing_columns"]:
        lines.append(
            f"- High missing values detected in: {', '.join(flags['high_missing_columns'])}"
        )

    if flags["possible_id_columns"]:
        lines.append(
            f"- Identifier-like columns detected: {', '.join(flags['possible_id_columns'])}"
        )

    lines.append(
        "The report is intended for human exploration and data quality inspection."
    )

    return "\n".join(lines)

def generate_sql_summary(metadata: dict) -> str:
    flags = metadata["flags"]

    lines = [
        "### SQL Generation Overview",
        "This process will generate exploratory SQL queries for:",
        "- Basic dataset inspection",
        "- Descriptive statistics on numeric columns",
        "- Frequency analysis of categorical columns",
        "- Missing value checks",
    ]

    if flags["possible_id_columns"]:
        lines.append(
            f"- Identifier-like columns detected: {', '.join(flags['possible_id_columns'])} "
            "(these will be excluded from aggregations)"
        )

    if flags["high_missing_columns"]:
        lines.append(
            f"- Columns with high missing values: {', '.join(flags['high_missing_columns'])}"
        )

    lines.append(
        "The queries are database-agnostic and can be adapted to most SQL engines."
    )

    return "\n".join(lines)

def generate_viz_summary(df) -> str:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    datetime_cols = df.select_dtypes(include="datetime").columns.tolist()

    lines = [
        "### Visualization Plan",
        "The system will automatically generate visual insights including:",
    ]

    if numeric_cols:
        lines.append(f"- Distributions for numeric columns: {', '.join(numeric_cols)}")

    if categorical_cols:
        lines.append(
            f"- Frequency charts for categorical columns: {', '.join(categorical_cols)}"
        )

    if len(numeric_cols) > 1:
        lines.append("- Correlation heatmap for numeric features")

    if datetime_cols:
        lines.append(f"- Time-series trends for: {', '.join(datetime_cols)}")

    lines.append(
        "These visualizations help identify patterns, outliers, and relationships."
    )

    return "\n".join(lines)
