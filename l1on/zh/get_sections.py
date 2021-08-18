import pandas as pd

cad_df = pd.read_csv('full_csv.csv')
print(cad_df.columns)

print(cad_df['sector'].unique())
print(cad_df['industry'].unique())