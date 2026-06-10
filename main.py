import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\suraj\Documents\suraj doc\bank_statement.csv")
df["Amount"]=df["Amount"].astype(str).replace('"',"").replace (",",'').str.strip()
print(df)