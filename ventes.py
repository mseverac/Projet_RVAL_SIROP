import pandas as pd
from utils import *
#from routing_script import *
from configuration import *
import numpy as np
import random

df = pd.read_excel("sales_month.xlsx")

def ventes(config : Configuration, current_month, df):
    month_data = df[df['Month'] == current_month]
    liste_ventes = []
    for shop in config.shops:
        shop_id = shop.id + 1
        for product_index, product in enumerate(["P1", "P2"]):
            col = f"S{shop_id}_{product}"
            monthly_sales = month_data[col].values[0]
            # On prend +/-10% de variation alÃ©atoire des monthly_sales
            var = random.uniform(-0.1, 0.1)
            sales = int(monthly_sales * (1 + var))
            available_stock = shop.current_stock[product_index]
            actual_sales = min(sales, available_stock)
            liste_ventes.append((shop.id, product, actual_sales))
            new_stock = available_stock - actual_sales
            if product_index == 0:
                shop.current_stock = (new_stock, shop.current_stock[1])
            else:
                shop.current_stock = (shop.current_stock[0], new_stock)
    return config, liste_ventes


    