import pandas as pd
import numpy as np
import sqlite3 as sq
df = pd.read_csv(r"C:\Users\suraj\Documents\suraj doc\bank_statement.csv")
df["Amount"]=df["Amount"].astype(str).replace('"',"").replace (",",'').str.strip()
df["Amount"]=pd.to_numeric(df["Amount"],errors='coerce')
df['Amount'] = np.where(df['Description'].str.contains('SALARY', case=False), 50000.00, df['Amount'])
df["Date"] =  pd.to_datetime(df["Date"])
df['Category'] = np.where(df['Description'].str.contains('SALARY', case=False), 'Salary', df['Category'])
values={
    "FITNESS GARAGE GYM" : 1200,
    "MUSCLEBLAZE NUTRITION" : 2000
}
fallback_amounts= df["Description"].map(values)
df["Amount"]=df["Amount"].fillna(fallback_amounts)
df["Amount"]=df["Amount"].fillna(100)
df["Type"] =  np.where(df["Amount"]>0, "Income" , "Expense")




#cleaned dataframe

#filtring 




conn = sq.connect("project1.db")
df.to_sql("users",conn,if_exists="replace",index=False)
# total spent per category
query1= """
select Category ,sum(abs(Amount)) as Total_Spent 
from users
where Type = "Expense"
group by Category
order by Total_Spent desc

"""
#High-Value Transactions (Greater than ₹1,500):
query2="""
select *
from users 
where abs(amount) > 1500
order by abs(amount) > 1500
"""
ans = pd.read_sql_query(query2,conn)
print(ans)

conn.close()


