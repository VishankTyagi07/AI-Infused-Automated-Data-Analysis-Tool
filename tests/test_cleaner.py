from cleaner.cleaner import clean_dataset
import pandas as pd

df=pd.read_csv("data/uploads/real_state_data.csv")
cleaned_df=clean_dataset(df)
print(cleaned_df.head())