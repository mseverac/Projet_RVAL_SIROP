import pandas as pd   
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

df = pd.read_excel("sales_month.xlsx")

def esperance_pertes(shop_id, product, stock, current_month,df):
    col = f"S{shop_id}_{product}"
    mu = df.loc[df["Month"] == current_month, col].values[0]

    sigma = 0.1*mu

    Z = (stock - mu) / sigma
    pertes = sigma * norm.pdf(Z) + (mu - stock) * (1 - norm.cdf(Z))
    return pertes

for stock in [0, 3, 6, 9, 12, 15]:
    print(f"Stock: {stock}")
    print(esperance_pertes(1, "P1", stock=stock, current_month="Mai", df=df))

plt.figure(figsize=(10, 6))
stocks = np.arange(0, 21, 1)
pertes_values = [esperance_pertes(1, "P1", stock=s, current_month="Mai", df=df) for s in stocks]
plt.plot(stocks, pertes_values, marker='o') 
plt.title("Espérance des pertes en fonction du stock pour le Shop 1, Produit P1 en Mai")
plt.xlabel("Stock disponible")
plt.ylabel("Espérance des pertes")
plt.grid()
plt.show()

"""for shop in range(1, 21):
    for product in ["P1", "P2"]:
        pertes = esperance_pertes(shop, product, stock=6, current_month="Mai", df=df)
        print(f"Shop {shop}, Product {product}, Expected Losses: {pertes:.2f}")"""