import pandas as pd

df= pd.read_excel("online+retail/Online Retail.xlsx")

df = df.dropna(subset=['CustomerID'])
df = df[(df['Quantity']>0) & (df['UnitPrice']>0)]
df['CustomerID'] = df['CustomerID'].astype(int)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df.to_csv("Cleaned_Dataset.csv", index = False)

print(df.head())
print(df.info())
print(df.describe())