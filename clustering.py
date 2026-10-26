import pandas as pd
import datetime as dt 
import matplotlib.pylab as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns

df = pd.read_csv("Cleaned_Dataset.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

rfm = df.groupby("CustomerID").agg({'InvoiceDate' : lambda x: (snapshot_date-x.max()).days,
            'InvoiceNo' : 'nunique',
            'TotalPrice' : 'sum'
})

rfm.columns = ['Recency','Frequency','Monetary']

print(rfm.head())

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

inertia = []
K_range = range(1,11)

for k in K_range:
    kmeans = KMeans(n_clusters = k, random_state=42)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(K_range, inertia, marker='s', color='b')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.grid(True)
plt.tight_layout()
plt.show()

kmean = KMeans(n_clusters=4,random_state=42)
rfm['Cluster'] = kmean.fit_predict(rfm_scaled)

cluster_summary = rfm.groupby('Cluster').agg({
    'Recency' : 'mean',
    'Frequency' : 'mean',
    'Monetary' : ['mean','count']
}).round(2)

print(cluster_summary)
print("where:12346",rfm.loc[12346])

cluster_names = {
    0:"Regualr shoppers",
    1:'At-Risk/Inactive',
    2:'wholesale/vip whales',
    3:'High-values loyal'
}

rfm['Segment'] = rfm['Cluster'].map(cluster_names)

plt.figure(figsize=(10,6))
sns.scatterplot(
    data=rfm,
    x='Recency',
    y='Frequency',
    hue='Segment',
    palette = 'Set1',
    alpha = 0.6,
    s=40
)

plt.xlim(-5,300)
plt.ylim(0,45)
plt.grid(True,linestyle='--',alpha=0.4)
plt.legend(title='Customer segment',bbox_to_anchor=(1.02,1),loc='upper left')
plt.tight_layout()
plt.show()
