from utils import *
import matplotlib.pyplot as plt

shops_capacities = [15,15,20,20,15,20,30,30,35,25,30,30,30,35,30,40,25,20,15,20]

plant_positions = [(1,2),(6,5)]
warehouse_positions = [(4,3),(9,4)]
shop_positions = [(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
                  (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)]


plants = [Plant(i,plant_positions[i][0],plant_positions[i][1]) for i in range(len(plant_positions))]
warehouses = [Warehouse(i,warehouse_positions[i][0],warehouse_positions[i][1]) for i in range(len(warehouse_positions))]
shops = [Shop(i,shop_positions[i][0],shop_positions[i][1],shops_capacities[i]) for i in range(len(shop_positions))]

import numpy as np
import matplotlib.pyplot as plt

def perpendicular_offset(dx, dy, scale=0.3):
    norm = np.hypot(dx, dy)
    if norm == 0:
        return 0, 0
    return -dy / norm * scale, dx / norm * scale

def print_configuration():
    print("Plants :")
    for plant in plants:
        print(f"Plant {plant.id} at position ({plant.x},{plant.y})")
    print("Warehouses :")
    for warehouse in warehouses:
        print(f"Warehouse {warehouse.id} at position ({warehouse.x},{warehouse.y}) with stock {warehouse.current_stock}")

    print("Shops :")
    for shop in shops:
        print(f"Shop {shop.id} at position ({shop.x},{shop.y}) with capacity {shop.capacity} and current stock {shop.current_stock}")


#print_configuration()

def plot_configuration():
    plt.figure(figsize=(10,6))
    for plant in plants:
        plt.scatter(plant.x, plant.y, c='green', marker='x', s=50, label='Plant' if plant.id == 0 else "")
        plt.text(plant.x, plant.y, f"P{plant.id}", fontsize=12, ha='center', va='center', color='black')

    for warehouse in warehouses:
        plt.scatter(warehouse.x, warehouse.y, c='blue', marker='x', s=50, label='Warehouse' if warehouse.id == 0 else "")
        plt.text(warehouse.x, warehouse.y, f"W{warehouse.id}", fontsize=12, ha='center', va='center', color='black')
        plt.text(warehouse.x, warehouse.y-0.2, f"S:{warehouse.current_stock}", fontsize=10, ha='center', va='center', color='black')

    for shop in shops:
        plt.scatter(shop.x, shop.y, c='red', marker='x', s=50, label='Shop' if shop.id == 0 else "")
        plt.text(shop.x, shop.y, f"S{shop.id}", fontsize=12, ha='center', va='center', color='black')
        plt.text(shop.x, shop.y-0.2, f"C:{shop.current_stock}", fontsize=10, ha='center', va='center', color='black')
    
    plt.title("Stock Configuration")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.show()


#plot_configuration()

def plot_tournee(tournee : Tournee,name=None):
    home = tournee.home
    list_arrets = tournee.list_arrets
    list_tournee= [[home,(0,0)]] + list_arrets + [[tournee.end,(0,0)]]
    stock_truck = (0,0)

    plt.figure(figsize=(20,12))
    for plant in plants:
        plt.scatter(plant.x, plant.y, c='green', marker='x', s=50, label='Plant' if plant.id == 0 else "")
        plt.text(plant.x, plant.y, f"P{plant.id}", fontsize=12, ha='center', va='center', color='black')

    for warehouse in warehouses:
        plt.scatter(warehouse.x, warehouse.y, c='blue', marker='x', s=50, label='Warehouse' if warehouse.id == 0 else "")
        plt.text(warehouse.x, warehouse.y, f"W{warehouse.id}", fontsize=12, ha='center', va='center', color='black')
        #plt.text(warehouse.x, warehouse.y-0.2, f"S:{warehouse.current_stock}", fontsize=10, ha='center', va='center', color='black')

    for shop in shops:
        plt.scatter(shop.x, shop.y, c='red', marker='x', s=50, label='Shop' if shop.id == 0 else "")
        plt.text(shop.x, shop.y, f"S{shop.id}", fontsize=12, ha='center', va='center', color='black')
        #plt.text(shop.x, shop.y-0.2, f"C:{shop.current_stock}", fontsize=10, ha='center', va='center', color='black')
    
    for i in range(len(list_tournee) - 1):
        x0 = list_tournee[i][0].x
        y0 = list_tournee[i][0].y
        x1 = list_tournee[i+1][0].x
        y1 = list_tournee[i+1][0].y

        dx = x1 - x0
        dy = y1 - y0

        plt.arrow(
            x0, y0,
            dx, dy,
            length_includes_head=True,
            head_width=0.2,
            head_length=0.2,
            fc='black',
            ec='black',
            alpha=0.6
        )
        #print("list_tournee[i]:", list_tournee[i])
        stock_truck = sub_tuples(stock_truck,list_tournee[i][1])
        if stock_truck != (0,0):
            plt.text((x0+x1)/2,(y0+y1)/2, f"stock={stock_truck}", fontsize=10, ha='center', va='center', color='black')

    
    plt.title("Tournee Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    if name is None :
        plt.show()
    else :
        plt.savefig(name)
        plt.close()

def plot_tournees(tournees: list):
    plt.figure(figsize=(30,18))

    # --- colormap pour les tournées ---
    cmap = plt.cm.get_cmap("tab20", len(tournees))

    # --- points fixes ---
    for plant in plants:
        plt.scatter(plant.x, plant.y, c='green', marker='x', s=80)
        plt.text(plant.x, plant.y+0.2, f"P{plant.id}", fontsize=12, ha='center')

    for warehouse in warehouses:
        plt.scatter(warehouse.x, warehouse.y, c='blue', marker='x', s=80)
        plt.text(warehouse.x, warehouse.y+0.2, f"W{warehouse.id}", fontsize=12, ha='center')
        plt.text(warehouse.x, warehouse.y-0.3, f"S:{warehouse.current_stock}", fontsize=10, ha='center')

    for shop in shops:
        plt.scatter(shop.x, shop.y, c='red', marker='x', s=80)
        plt.text(shop.x, shop.y+0.2, f"S{shop.id}", fontsize=12, ha='center')
        plt.text(shop.x, shop.y-0.3, f"C:{shop.current_stock}", fontsize=10, ha='center')

    # --- tournées ---
    for t_idx, tournee in enumerate(tournees):
        color = cmap(t_idx)

        list_tournee = (
            [[tournee.home, (0,0)]] +
            tournee.list_arrets +
            [[tournee.end, (0,0)]]
        )

        stock_truck = (0,0)

        for i in range(len(list_tournee) - 1):
            n0, _ = list_tournee[i]
            n1, delta = list_tournee[i+1]

            dx = n1.x - n0.x
            dy = n1.y - n0.y

            plt.arrow(
                n0.x, n0.y,
                dx, dy,
                length_includes_head=True,
                head_width=0.30-0.01*t_idx,
                head_length=0.4-0.01*t_idx,
                fc=color,
                ec=color,
                alpha=0.7
            )

            stock_truck = sub_tuples(stock_truck, list_tournee[i][1])

            # --- position texte décalée ---
            ox, oy = perpendicular_offset(dx, dy, scale=0.4 + 0.01*t_idx)

            xm = (n0.x + n1.x) / 2 + ox
            ym = (n0.y + n1.y) / 2 + oy

            plt.text(
                xm, ym,
                f"{stock_truck}",
                fontsize=10,
                ha='center',
                va='center',
                bbox=dict(facecolor='white', alpha=0.6, edgecolor='none')
            )

    plt.title("Tournees Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


        


