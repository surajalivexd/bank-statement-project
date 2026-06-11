import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\suraj\Documents\suraj doc\bank_statement.csv")
df["Amount"]=df["Amount"].astype(str).replace('"',"").replace (",",'').str.strip()
df["Amount"]=pd.to_numeric(df["Amount"],errors='coerce')
df['Amount'] = np.where(df['Description'].str.contains('SALARY', case=False), 50000.00, df['Amount'])
df["Date"] =  pd.to_datetime(df["Date"])
df["Type"] =  np.where(df["Amount"]>0, "Income" , "Expense")
df['Category'] = np.where(df['Description'].str.contains('SALARY', case=False), 'Salary', df['Category'])
values={
    "FITNESS GARAGE GYM" : 1200,
    "MUSCLEBLAZE NUTRITION" : 2000
}
fallback_amounts= df["Description"].map(values)
df["Amount"]=df["Amount"].fillna(fallback_amounts)
df["Amount"]=df["Amount"].fillna(0)
print(df)