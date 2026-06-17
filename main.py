import pandas as pd
import numpy as np
import sqlite3 as sq
import matplotlib as plt
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf 
from plotly.offline import iplot
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
# High-Value Transactions (Greater than ₹1,500):
query2="""
select *
from users 
where abs(amount) > 1500
order by abs(amount) > 1500
"""
# savings
query3 = """
select
SUM(CASE WHEN type = 'Income' THEN ABS(amount) ELSE 0 END) -
SUM(CASE WHEN type = 'Expense' THEN ABS(amount) ELSE 0 END) AS Net_Savings
from users
"""
# recurring expense
query4="""
select Description,Category , count(*) as occurance,
sum(abs(amount)) as total_spent
from users
where Type = "Expense"
group by Category
having count(*) > 1
order by occurance desc

"""
# Highest cash drain days
query5 =  """
select Date , Description , Amount 
from users
where Type = "Expense"
order by abs(Amount) desc
limit 5
"""

ans = pd.read_sql_query(query4,conn)
print(ans)

conn.close()

#Visualising 
