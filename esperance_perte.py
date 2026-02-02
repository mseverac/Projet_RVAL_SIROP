import pandas as pd   
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from utils import *

df = pd.read_excel("sales_month.xlsx")

def esperance_pertes(shop_id, product, stock, current_month,df):
    """shop id : int de 1 à 20
       product : "P1" ou "P2"
       """
    col = f"S{shop_id}_{product}"
    mu = df.loc[df["Month"] == current_month, col].values[0]

    if mu == 0:
        return 0
    else : 
        sigma = 0.1*mu

    Z = (stock - mu) / sigma
    pertes = sigma * norm.pdf(Z) + (mu - stock) * (1 - norm.cdf(Z))
    return pertes


def esperance_pertes_global(config : Configuration, current_month, df):
    total_pertes_heater = 0
    total_pertes_clim = 0
    for shop in config.shops:
        for product in ["P1", "P2"]:
            stock = shop.current_stock[0] if product == "P1" else shop.current_stock[1]
            pertes = esperance_pertes(shop.id+1, product, stock, current_month, df)
            if product == "P1":
                total_pertes_clim += pertes
            else:
                total_pertes_heater += pertes
    return  300*total_pertes_clim, 100*total_pertes_heater

# Recherche de la configuration minimale pour avoir une espérance de pertes nulle

def configuration_minimale(current_month, df):
    C0 = configuration_initiale()
    for shop in C0.shops:
        while esperance_pertes(shop.id+1, "P1", shop.current_stock[0], current_month, df) > 0.01 or esperance_pertes(shop.id+1, "P2", shop.current_stock[1], current_month, df) > 0.01:
            for product in ["P1", "P2"]:
                stock = 0
                pertes = esperance_pertes(shop.id+1, product, stock, current_month, df)
                while pertes > 0.01:
                    stock += 1
                    pertes = esperance_pertes(shop.id+1, product, stock, current_month, df)
                if product == "P1":
                    shop.current_stock = (stock, shop.current_stock[1])
                else:
                    shop.current_stock = (shop.current_stock[0], stock)
    return C0

"""C1 = configuration_minimale("Mai", df)
for shop in C1.shops:
    print(shop.current_stock)

"""



"""config_test=configuration_initiale()
print(esperance_pertes_global(config_test, "Juillet", df))"""


"""for stock in [0, 3, 6, 9, 12, 15]:
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
plt.show()"""

"""for shop in range(1, 21):
    for product in ["P1", "P2"]:
        pertes = esperance_pertes(shop, product, stock=6, current_month="Mai", df=df)
        print(f"Shop {shop}, Product {product}, Expected Losses: {pertes:.2f}")"""