import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Cleaned_Dataset.csv")

topProduct = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
topRevenue = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
topCountries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print(topRevenue)
print(topProduct)
print(topCountries)

plt.figure(figsize=(10,5))
sns.barplot(x=topRevenue.values,
            y=topRevenue.index,
            hue=topRevenue.index,
            palette='magma',legend = False)

plt.title("Top Revenue Generating Products")
plt.xlabel("total sales")
plt.tight_layout()
plt.show()

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
monthly_sales = df.groupby(df['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
plt.figure(figsize=(12,5))
monthly_sales.index = monthly_sales.index.astype(str)
plt.plot(monthly_sales.index,monthly_sales.values,marker='o',color='red',linewidth=2)
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("total sales")
plt.xticks(rotation = 45)
plt.grid(True,linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()