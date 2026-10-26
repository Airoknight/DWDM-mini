import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_csv("Cleaned_Dataset.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Date'] = df['InvoiceDate'].dt.date
df['Date'] = pd.to_datetime(df['Date'])

dailySales = df.groupby('Date')['TotalPrice'].sum()
dailySales = dailySales.asfreq('D',fill_value=0)
print(dailySales.head())

model = ExponentialSmoothing(
    dailySales,
    trend = 'add',
    seasonal='add',
    seasonal_periods=7
).fit()

forecast_days = 30
forecast = model.forecast(forecast_days)
print("\n ---Next 7 days forecast ---")
print(forecast.head(7))
plt.figure(figsize=(12,6))
plt.plot(dailySales.index[-90:],dailySales.values[-90:],label='Actual sales',color='blue')
plt.plot(forecast.index,forecast.values,label='30days forecast',color='orange',linestyle='--',linewidth=2)
plt.title('supermarket daily sales forecast',fontsize=14)
plt.xlabel('date',fontsize=12)
plt.ylabel('sales',fontsize=12)
plt.legend()
plt.grid(True,linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()