import pandas as pd
from mlxtend.frequent_patterns import apriori,association_rules

df = pd.read_csv("Cleaned_Dataset.csv")
pd.set_option('display.max_columns',None)
pd.set_option('display.width',1000)
df['Description'] = df['Description'].str.strip()

basket_frace = df[df['Country']=='France']

basket = (basket_frace.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))

if 'POSTAGE' in basket.columns:
    basket = basket.drop(columns=['POSTAGE'])

basket_set = (basket>0).astype(bool)

frequent_itemset = apriori(basket_set,min_support=0.05,use_colnames=True)

rules = association_rules(frequent_itemset,metric="lift",min_threshold=1.2)
rules = rules.sort_values(by = 'lift',ascending = False)

print(rules[['antecedents','consequents','support','confidence','lift']].head())