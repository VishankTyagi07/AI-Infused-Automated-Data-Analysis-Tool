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

