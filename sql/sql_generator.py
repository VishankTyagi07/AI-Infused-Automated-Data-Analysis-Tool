def sql_type(dtype, dialect="ANSI"):
    if "int" in dtype:
        return "INTEGER"
    if "float" in dtype:
        return "FLOAT"
    if "datetime" in dtype:
        return "TIMESTAMP"
    return "VARCHAR(255)"


def generate_create_table(metadata, table_name, dialect="ANSI"):
    cols = metadata["columns"]

    lines = [f"CREATE TABLE {table_name} ("]
    col_defs = []

    for col in cols:
        col_defs.append(
            f"  {col['name']} {sql_type(col['dtype'], dialect)}"
        )

    lines.append(",\n".join(col_defs))
    lines.append(");")

    return "\n".join(lines)


def generate_sql_queries(metadata, table_name="dataset", dialect="ANSI"):
    columns = metadata["columns"]
    flags = metadata["flags"]

    numeric_cols = [
        c["name"] for c in columns
        if c["is_numeric"] and c["name"] not in flags["possible_id_columns"]
    ]

    categorical_cols = [
        c["name"] for c in columns
        if c["is_categorical"]
    ]

    queries = []

    # CREATE TABLE
    queries.append("-- Schema definition")
    queries.append(generate_create_table(metadata, table_name, dialect))

    # Basic inspection
    queries.append("\n-- Preview data")
    queries.append(f"SELECT * FROM {table_name} LIMIT 10;")

    queries.append("\n-- Row count")
    queries.append(f"SELECT COUNT(*) AS row_count FROM {table_name};")

    # Missing values
    for col in columns:
        queries.append(
            f"\n-- Missing values in {col['name']}\n"
            f"SELECT COUNT(*) AS missing_{col['name']} "
            f"FROM {table_name} WHERE {col['name']} IS NULL;"
        )

    # Numeric stats
    for col in numeric_cols:
        if dialect == "PostgreSQL":
            queries.append(
                f"\n-- Stats for {col}\n"
                f"SELECT "
                f"MIN({col}), MAX({col}), AVG({col}), "
                f"PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {col}) AS median "
                f"FROM {table_name};"
            )
        else:
            queries.append(
                f"\n-- Stats for {col}\n"
                f"SELECT MIN({col}), MAX({col}), AVG({col}) "
                f"FROM {table_name};"
            )

    # Categorical frequencies
    for col in categorical_cols:
        queries.append(
            f"\n-- Frequency distribution for {col}\n"
            f"SELECT {col}, COUNT(*) AS frequency "
            f"FROM {table_name} "
            f"GROUP BY {col} "
            f"ORDER BY frequency DESC;"
        )

    return "\n".join(queries)

