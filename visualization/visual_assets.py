import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def generate_visualizations(df: pd.DataFrame) -> dict:
    figures = {}

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns
    datetime_cols = df.select_dtypes(include="datetime").columns

    # Numeric distributions
    for col in numeric_cols:
        figures[f"dist_{col}"] = px.histogram(
            df, x=col, title=f"Distribution of {col}"
        )

    # Categorical frequencies
    for col in categorical_cols:
        figures[f"count_{col}"] = px.bar(
            df[col].value_counts().head(20),
            title=f"Top Categories in {col}",
        )

    # Correlation heatmap
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        figures["correlation"] = px.imshow(
            corr, text_auto=True, title="Correlation Heatmap"
        )

    # Time series
    for col in datetime_cols:
        figures[f"time_{col}"] = px.line(
            df.sort_values(col),
            x=col,
            y=numeric_cols[0] if len(numeric_cols) else None,
            title=f"Trend over {col}",
        )

    return figures
