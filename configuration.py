from utils import *

shops_capacities = [15,15,20,20,15,20,30,30,35,25,30,30,30,35,30,40,25,20,15,20]

plant_positions = [(1,2),(6,5)]
warehouse_positions = [(4,3),(9,4)]
shop_positions = [(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
                  (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)]


plants = [Plant(i,plant_positions[i][0],plant_positions[i][1]) for i in range(len(plant_positions))]
warehouses = [Warehouse(i,warehouse_positions[i][0],warehouse_positions[i][1]) for i in range(len(warehouse_positions))]
shops = [Shop(i,shop_positions[i][0],shop_positions[i][1],shops_capacities[i]) for i in range(len(shop_positions))]


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
