import pandas as pd
from profiling.profiler import profile_dataset
import json

df = pd.read_csv("data/uploads/real_state_data.csv")
metadata = profile_dataset(df)

print(json.dumps(metadata, indent=2))
