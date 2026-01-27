import matplotlib.pyplot as plt
import math as ma
TRUCK_CAPACITY = 20 # m3
WAREHOUSE_CAPACITY = 650 # items for each product

V_heater = 0.4 # m3
V_clim = 0.8 # m3


def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def sub_tuples(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])

class Shop : 
    def __init__(self,id,x,y,capacity):
        self.id = id
        self.x = x
        self.y = y
        self.capacity = (capacity, capacity)
        self.current_stock = (0,0)

    def can_truck_stop(self, amount_delivered): 
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= self.capacity:
            return True
        else:
            return False

    def truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= self.capacity:
            self.current_stock = add_tuples(amount_delivered, self.current_stock)
            return amount_delivered
        else:
            raise ValueError(f"Wrong stock after delivery : {add_tuples(self.current_stock, amount_delivered)}")
            return 0
        

class Warehouse :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.current_stock = (0,0)



    def get_stock(self):
        return self.current_stock
    
    def can_truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= (WAREHOUSE_CAPACITY, WAREHOUSE_CAPACITY):
            return True
        else:
            return False
    
    def truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= (WAREHOUSE_CAPACITY, WAREHOUSE_CAPACITY):
            self.current_stock = add_tuples(amount_delivered, self.current_stock)
            return amount_delivered
        else:
            raise ValueError(f"Wrong stock after delivery : {add_tuples(self.current_stock, amount_delivered)}")
            return 0
        

class Plant :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def truck_stop(self, amount_delivered):
        if amount_delivered > (0,0):
            raise ValueError("Plants cannot receive deliveries")
        
    def can_truck_stop(self, amount_delivered):
        if amount_delivered > (0,0):
            return False
        else:
            return True
        

def distance(a, b):
    return ((a.x - b.x)+ (a.y - b.y))


class Tournee:
    def __init__(self, home, list_arrets):
        self.home = home
        self.list_arrets = list_arrets

    def is_valid(self):
        remplissage_camion = 0
        for lieu, amount in self.list_arrets:
            remplissage_camion += V_clim * amount[0] + V_heater * amount[1]
            if remplissage_camion > TRUCK_CAPACITY:
                return False
            if not lieu.can_truck_stop(amount):
                return False
        return True

    def effectuer_tournee(self):

        remplissage_camion = 0
        for lieu, amount in self.list_arrets:
            lieu.truck_stop(amount)

            remplissage_camion += V_clim * amount[0] + V_heater * amount[1]
            if remplissage_camion > TRUCK_CAPACITY:
                raise ValueError("Truck over capacity")
            

    def calculer_distance_totale(self):
        total_distance = 0
        current_location = self.home

        for lieu, _ in self.list_arrets:
            total_distance += distance(current_location, lieu)
            current_location = lieu

        total_distance += distance(current_location, self.home)

        return total_distance
            



class Configuration():
    def __init__(self, plants, warehouses, shops):
        self.plants = plants
        self.warehouses = warehouses
        self.shops = shops

    def print(self):
        print("Plants :")
        for plant in self.plants:
            print(f"Plant {plant.id} at position ({plant.x},{plant.y})")
        print("Warehouses :")
        for warehouse in self.warehouses:
            print(f"Warehouse {warehouse.id} at position ({warehouse.x},{warehouse.y}) with stock {warehouse.current_stock}")

        print("Shops :")
        for shop in self.shops:
            print(f"Shop {shop.id} at position ({shop.x},{shop.y}) with capacity {shop.capacity} and current stock {shop.current_stock}")

    def plot(self):
        plt.figure(figsize=(10,6))
        for plant in self.plants:
            plt.scatter(plant.x, plant.y, c='green', marker='x', s=50, label='Plant' if plant.id == 0 else "")
            plt.text(plant.x, plant.y, f"P{plant.id}", fontsize=12, ha='center', va='center', color='black')

        for warehouse in self.warehouses:
            plt.scatter(warehouse.x, warehouse.y, c='blue', marker='x', s=50, label='Warehouse' if warehouse.id == 0 else "")
            plt.text(warehouse.x, warehouse.y, f"W{warehouse.id}", fontsize=12, ha='center', va='center', color='black')
            plt.text(warehouse.x, warehouse.y-0.2, f"S:{warehouse.current_stock}", fontsize=10, ha='center', va='center', color='black')

        for shop in self.shops:
            plt.scatter(shop.x, shop.y, c='red', marker='x', s=50, label='Shop' if shop.id == 0 else "")
            plt.text(shop.x, shop.y, f"S{shop.id}", fontsize=12, ha='center', va='center', color='black')
            plt.text(shop.x, shop.y-0.2, f"C:{shop.current_stock}", fontsize=10, ha='center', va='center', color='black')
        
        plt.title("Stock Configuration")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        #plt.legend()
        plt.grid()
        plt.show()


def configuration_initiale():
    shops_capacities = [15,15,20,20,15,20,30,30,35,25,30,30,30,35,30,40,25,20,15,20]

    plant_positions = [(1,2),(6,5)]
    warehouse_positions = [(4,3),(9,4)]
    shop_positions = [(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
                    (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)]


    plants = [Plant(i,plant_positions[i][0],plant_positions[i][1]) for i in range(len(plant_positions))]
    warehouses = [Warehouse(i,warehouse_positions[i][0],warehouse_positions[i][1]) for i in range(len(warehouse_positions))]
    shops = [Shop(i,shop_positions[i][0],shop_positions[i][1],shops_capacities[i]) for i in range(len(shop_positions))]


    return Configuration(plants, warehouses, shops)


def configuration_parfaite():

    C0 = configuration_initiale()
    # Remplir les entrepots
    for warehouse in C0.warehouses:
        warehouse.current_stock = (WAREHOUSE_CAPACITY, WAREHOUSE_CAPACITY)
    # Remplir les magasins
    for shop in C0.shops:
        shop.current_stock = shop.capacity
    return C0


CONFIG_PARFAITE = configuration_parfaite()



def config_dist_to_parfaite(config: Configuration):
    total_distance = 0

    for warehouse in config.warehouses:
        stock_ideal = CONFIG_PARFAITE.warehouses[warehouse.id].current_stock
        stock_actuel = warehouse.current_stock
        diff_stock = sub_tuples(stock_ideal, stock_actuel)
        total_distance += (diff_stock[0])**2 + (diff_stock[1])**2

    for shop in config.shops:
        stock_ideal = CONFIG_PARFAITE.shops[shop.id].current_stock
        stock_actuel = shop.current_stock
        diff_stock = sub_tuples(stock_ideal, stock_actuel)
        total_distance += (diff_stock[0])**2 + (diff_stock[1])**2

    return ma.sqrt(total_distance)












