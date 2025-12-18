import pandas as pd
try:
    df = pd.read_csv("comprehensive_data.csv")
    print(df.dtypes)
    print(df.head())
except Exception as e:
    print(e)
