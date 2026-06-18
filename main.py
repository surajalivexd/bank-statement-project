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
df1 = pd.read_sql_query(query1,conn)


# High-Value Transactions (Greater than ₹1,500):
query2="""
select *
from users 
where abs(amount) > 1500
order by abs(amount) > 1500
"""
df2 = pd.read_sql_query(query2,conn)

# savings
query3 = """
select
strftime('%Y-%m', Date) AS Month,
SUM(CASE WHEN type = 'Income' THEN ABS(amount) ELSE 0 END) -
SUM(CASE WHEN type = 'Expense' THEN ABS(amount) ELSE 0 END) AS Net_Savings
from users
group by Month
"""
df3=pd.read_sql_query(query3,conn)

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
df4=pd.read_sql_query(query4,conn)

# Highest cash drain days
query5 =  """
select Date , Description , Amount 
from users
where Type = "Expense"
order by abs(Amount) desc
limit 5
"""
df5=pd.read_sql_query(query5,conn)
df5['Amount'] = df5['Amount'].abs()
df5['Date'] = pd.to_datetime(df5['Date']).dt.strftime('%d %b')
conn.close()

#Visualising 

sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(3, 2, figsize=(16, 16))

fig.suptitle('Bank Statement Insights Dashboard', fontsize=22, weight='bold', y=0.95)

# Graph 1 
sns.barplot(data=df1, x="Total_Spent", y="Category", palette="Blues_r", ax=axes[0, 0])
axes[0, 0].set_title("1. Budget Leakage per Category", fontsize=13, weight="bold", pad=12)
axes[0, 0].set_xlabel("Total Spent (₹)")
axes[0, 0].set_ylabel('')

# Graph 2
df2['Amount'] = df2['Amount'].abs()
sns.barplot(data=df2, x="Amount", y="Description", palette="Reds_r", ax=axes[1, 0])
axes[1, 0].set_title("3. High-Value Transactions (Greater than ₹1,500)", fontsize=13, weight="bold", pad=12)
axes[1, 0].set_xlabel("Value (₹)")
axes[1, 0].set_ylabel("")

# Graph 3
sns.lineplot(data=df3, x="Month", y="Net_Savings", marker="o", color="b", linewidth=3, ax=axes[0, 1])
sns.scatterplot(data=df3, x="Month", y="Net_Savings", color="red", s=100, zorder=5, ax=axes[0, 1])
axes[0, 1].set_title("2. Net Savings Per Month", fontsize=13, weight="bold", pad=12)
axes[0, 1].set_ylabel("Savings Value (₹)")
axes[0, 1].set_xlabel("")

# Graph 4
sns.barplot(data=df4, x="occurance", y="Description", palette="crest", ax=axes[1, 1])
axes[1, 1].set_title("4. Recurring Expense", fontsize=13, weight="bold", pad=12)
axes[1, 1].set_xlabel("Billing Incidents")
axes[1, 1].set_ylabel("")

#Graph 5 
sns.barplot(data=df5, x='Date', y='Amount', palette='flare', ax=axes[2, 0])
axes[2, 0].set_title('5. Highest drain days', fontsize=13, weight="bold", pad=12)
axes[2, 0].set_ylabel('Day Expense (₹)')
axes[2, 0].set_xlabel('')


fig.delaxes(axes[2, 1])

fig.subplots_adjust(top=0.88, bottom=0.08, left=0.12, right=0.95, hspace=0.45, wspace=0.35)
plt.show()