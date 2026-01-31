'''
IN this module there will be functions to profile a user given dataset into useful insights.
by providing dictionary with json data.
'''
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport

def profile_dataset(df: pd.DataFrame) -> dict:
 

    row_count = df.shape[0]

    profile_data = {
        "dataset": {
            "row_count": row_count,
            "column_count": df.shape[1],
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2),
        },
        "columns": [],
        "flags": {
            "high_missing_columns": [],
            "constant_columns": [],
            "possible_id_columns": [],
        },
    }

    for col in df.columns:
        series = df[col]

        missing_pct = round(series.isnull().mean() * 100, 2)
        unique_values = int(series.nunique(dropna=True))

        # Semantic type detection
        is_numeric = pd.api.types.is_numeric_dtype(series)
        is_datetime = pd.api.types.is_datetime64_any_dtype(series)
        is_categorical = not is_numeric and not is_datetime

        column_metadata = {
            "name": col,
            "dtype": str(series.dtype),
            "missing_pct": missing_pct,
            "unique_values": unique_values,
            "sample_values": series.dropna().unique()[:3].tolist(),
            "is_numeric": is_numeric,
            "is_categorical": is_categorical,
            "is_datetime": is_datetime,
        }

        profile_data["columns"].append(column_metadata)

        # Flags
        if missing_pct > 30:
            profile_data["flags"]["high_missing_columns"].append(col)

        if unique_values <= 1:
            profile_data["flags"]["constant_columns"].append(col)

        if unique_values >= 0.95 * row_count:
            profile_data["flags"]["possible_id_columns"].append(col)

    return profile_data



def generate_profile_report(df):
    profile = ProfileReport(df, explorative=True)
    return profile.to_html()
