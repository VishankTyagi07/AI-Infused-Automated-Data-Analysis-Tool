DATASET_SUMMARY_PROMPT = """
You are a senior data analyst.

You will receive structured dataset metadata extracted programmatically.
Do not invent columns or metrics.
Base all conclusions strictly on the metadata.

Metadata:
{metadata}

Tasks:
1. Describe what the dataset likely represents.
2. Identify key business KPIs.
3. Suggest meaningful analyses.
4. Highlight data quality risks.
5. State assumptions clearly.
"""