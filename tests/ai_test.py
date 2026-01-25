import pandas as pd
from profiling.profiler import profile_dataset
from ai.rule_based_summary import generate_dataset_summary

# 1. Load a sample dataset
df = pd.read_csv("data/uploads/real_state_data.csv")

# 2. Generate metadata
metadata = profile_dataset(df)

# 3. Generate rule-based summary
summary = generate_dataset_summary(metadata)

# 4. Print output
print("\n=== DATASET SUMMARY ===\n")
print(summary)
