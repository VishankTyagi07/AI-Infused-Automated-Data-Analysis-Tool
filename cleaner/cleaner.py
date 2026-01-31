import pandas as pd
import numpy as np


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a dataset using rule-based transformations.
    Returns a cleaned DataFrame.
    """

    df = df.copy()

    
    # Normalize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )


    # Normalize missing values
    missing_values = [
        "", "na", "n/a", "null", "--", "none", "nan",
        "undefined", " ", "?", "-"
    ]
    df.replace(missing_values, np.nan, inplace=True)

    # Drop fully empty columns
    df.dropna(axis=1, how="all", inplace=True)

    # type inference 
    for col in df.columns:
        series = df[col]

        if len(series) == 0:
            continue

        # Numeric conversion
        numeric = pd.to_numeric(series, errors="coerce")
        if numeric.notna().mean() > 0.8:
            df[col] = numeric
            continue

        # Datetime conversion
        datetime = pd.to_datetime(series, errors="coerce")
        if datetime.notna().mean() > 0.8:
            df[col] = datetime
            continue

        # Categorical cleanup (ONLY for non-numeric, non-datetime)
        df[col] = (
            series.astype(str)
            .str.strip()
            .str.lower()
            .replace("nan", np.nan)
        )

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
