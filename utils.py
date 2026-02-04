import matplotlib.pyplot as plt
import math as ma
import pandas as pd
from scipy.stats import norm
import copy as cp   


TRUCK_CAPACITY = 20 # m3
WAREHOUSE_CAPACITY = 650 # items for each product

V_heater = 0.4 # m3
V_clim = 0.8 # m3

months = {1:'Janvier', 2:'Février', 3:'Mars', 4:'Avril', 5:'Mai', 6:'Juin', 7:'Juillet', 8:'Août', 9:'Septembre', 10:'Octobre', 11:'Novembre', 12:'Décembre'}
ratio_clim_heater = {'Janvier': 0.26 , 'Février' : 0.51 , 'Mars' : 0.7 , 'Avril' : 0.86 , 'Mai' : 0.97 , 'Juin' : 1 , 'Juillet' : 0.97 , 'Août' : 0.86 , 'Septembre': 0.72 , 'Octobre' : 0.52 , 'Novembre' : 0.26 , 'Décembre' : 0}
#ratio_clim_heater = {'Janvier': 0.36 , 'Février' : 0.61 , 'Mars' : 0.8 , 'Avril' : 0.96 , 'Mai' : 1 , 'Juin' : 1 , 'Juillet' : 1 , 'Août' : 0.96 , 'Septembre': 0.82 , 'Octobre' : 0.62 , 'Novembre' : 0.36 , 'Décembre' : 0.1}

def ratio_plus_epsilon(ratio : dict,epsilon = 0.05):
    for k in ratio.keys():
        ratio[k] = min(1,ratio[k]+epsilon)

    return ratio

ratio_clim_heater = ratio_plus_epsilon(ratio_clim_heater,0.05)



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


    def get_free_space(self):
        return sub_tuples(self.capacity,self.current_stock)

    def __str__(self):
        return f"Shop {self.id} at position ({self.x},{self.y}) with capacity {self.capacity} and current stock {self.current_stock}"

    def can_truck_stop(self, amount_delivered): 
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= self.capacity:
            return True
        else:
            return False

    def truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock)[0] >= 0 and add_tuples(amount_delivered, self.current_stock)[1] >= 0 and add_tuples(amount_delivered, self.current_stock)[0] <= self.capacity[0] and add_tuples(amount_delivered, self.current_stock)[1] <= self.capacity[1]:
            self.current_stock = add_tuples(amount_delivered, self.current_stock)
            return amount_delivered
        else:
            print("Current stock :", self.current_stock)
            print("Amount delivered :", amount_delivered)
            print("Capacity :", self.capacity)
            raise ValueError(f"Wrong stock after delivery in shop: {add_tuples(self.current_stock, amount_delivered)}")
            return 0
        

class Warehouse :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.current_stock = (0,0)


    def is_stock_eleve(self):
        if self.current_stock[0] > 300 or self.current_stock[1] > 300:
            return True 
        else :
            return False

    def __str__(self):
        return f"Warehouse {self.id} at position ({self.x},{self.y}) with stock {self.current_stock}"



    def get_stock(self):
        return self.current_stock
    
    def can_truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock) >= (0,0) and add_tuples(amount_delivered, self.current_stock) <= (WAREHOUSE_CAPACITY, WAREHOUSE_CAPACITY):
            return True
        else:
            return False
    
    def truck_stop(self, amount_delivered):
        if add_tuples(amount_delivered, self.current_stock)[0] >= 0 and add_tuples(amount_delivered, self.current_stock)[1] >= 0 and add_tuples(amount_delivered, self.current_stock)[0] <= WAREHOUSE_CAPACITY and add_tuples(amount_delivered, self.current_stock)[1] <= WAREHOUSE_CAPACITY:
            self.current_stock = add_tuples(amount_delivered, self.current_stock)
            return amount_delivered
        else:
            print(f"self : {self}")
            print(f"delivery : {amount_delivered}")
            raise ValueError(f"Wrong stock after delivery in warehouse: {add_tuples(self.current_stock, amount_delivered)}, Warehouse : {self}")
            return 0
        

class Plant :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return f"Plant {self.id} at position ({self.x},{self.y})"

    def truck_stop(self, amount_delivered):
        if amount_delivered > (0,0):
            raise ValueError("Plants cannot receive deliveries")
        
    def can_truck_stop(self, amount_delivered):
        if amount_delivered > (0,0):
            return False
        else:
            return True
        

def distance(a, b):
    return (abs(a.x - b.x)+ abs(a.y - b.y))






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

    def plot(self,title="Stock Configuration",path=None):
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
        
        plt.title(title)
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        #plt.legend()
        plt.grid()
        if path is not None:
            plt.savefig(path)
            plt.close()
        else :
            plt.show()


def get_nearest_warehouse(x,y,config: Configuration):
    min_dist = ma.inf
    nearest_warehouse = None
    for warehouse in config.warehouses:
        dist = abs(warehouse.x - x) + abs(warehouse.y - y)
        if dist < min_dist:
            min_dist = dist
            nearest_warehouse = warehouse
    if x == config.plants[0].x and y == config.plants[0].y:
        nearest_warehouse = config.warehouses[1]
    
    return nearest_warehouse


def best_truck_load(month, max_V=TRUCK_CAPACITY):
    """Truck capacity en m3"""


    max_V = int(round(max_V * 10))
    V_clim = 8
    V_heater = 4
    
    ratio = ratio_clim_heater[month]

    best_load = (0, 0)
    best_error = float("inf")
    best_volume = 0

    # On parcourt toutes les quantités possibles de clim
    max_clim = max_V // V_clim

    for n_clim in range(int(max_clim + 1)):

        # Volume restant pour les heaters
        remaining = max_V - n_clim * V_clim


        n_heater = remaining // V_heater


        total = n_clim + n_heater
        if total == 0:
            continue

        current_ratio = n_clim / total
        error = abs(current_ratio - ratio)

        volume = n_clim * V_clim + n_heater * V_heater

        # On choisit la solution :
        # - d'abord par erreur de ratio minimale
        # - en cas d'égalité, par volume maximal
        if error < best_error or (error == best_error and volume > best_volume):
            best_error = error
            best_volume = volume
            best_load = (int(n_clim), int(n_heater))

    return best_load


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


def ajoute_produit_au_meilleur(shops, product,month):

    for s in shops:
        current_stock = s.current_stock[0] if product == "P1" else s.current_stock[1]
        if current_stock >= s.capacity[0] if product == "P1" else s.capacity[1]:
            shops.remove(s)

    max_perte_reduction = 0
    best_shop = None
    i_best_shop = None
    for i, shop in enumerate(shops):
        current_stock = shop.current_stock[0] if product == "P1" else shop.current_stock[1]
        if current_stock >= shop.capacity[0] if product == "P1" else shop.capacity[1]:
            continue
        current_pertes = esperance_pertes(shop.id+1, product, current_stock, month, df)
        new_pertes = esperance_pertes(shop.id+1, product, current_stock + 1, month, df)
        perte_reduction = current_pertes - new_pertes
        if perte_reduction > max_perte_reduction:
            max_perte_reduction = perte_reduction
            best_shop = shop
            i_best_shop = i
    return best_shop, i_best_shop

def repartir_among_free_spaces(load, fs: list):
    n = len(fs)
    repartition = [0] * n

    if n == 0:
        return repartition, load

    total_capacity = sum(fs)

    # Si le load dépasse la capacité totale
    if load >= total_capacity:
        return fs.copy(), load - total_capacity

    remaining = load

    # Tant qu'il reste quelque chose à distribuer
    while remaining > 0:
        distributed = False

        for i in range(n):
            if remaining == 0:
                break

            if repartition[i] < fs[i]:
                repartition[i] += 1
                remaining -= 1
                distributed = True

        # Si on n'a rien pu distribuer → tout est saturé
        if not distributed:
            break

    return repartition, remaining


def find_lieu(x,y,config: Configuration):
    for plant in config.plants:
        if plant.x == x and plant.y == y:
            return plant
    for warehouse in config.warehouses:
        if warehouse.x == x and warehouse.y == y:
            return warehouse
    for shop in config.shops:
        if shop.x == x and shop.y == y:
            return shop
    return None


class Tournee:
    def __init__(self, home, list_arrets,end=None):
        self.home = home
        self.list_arrets = list_arrets

        if end is None:
            self.end = home
        else:
            self.end = end

    def unload_final_warehouse(self):
        total_load = (0,0)
        for lieu, amount in self.list_arrets:
            total_load = sub_tuples(total_load, amount)

        if isinstance(self.end, Warehouse):
            self.list_arrets.append((self.end, total_load))
            #print(f"Unloading final warehouse {self.end.id} with load {total_load}")


    def with_config(self, config: Configuration):
        new_home = find_lieu(self.home.x, self.home.y, config)
        new_end = find_lieu(self.end.x, self.end.y, config)
        new_list_arrets = []
        for lieu, amount in self.list_arrets:
            new_lieu = find_lieu(lieu.x, lieu.y, config)
            new_list_arrets.append((new_lieu, amount))

        self.home = new_home
        self.end = new_end
        self.list_arrets = new_list_arrets
        



    def take_max_load_at(self, lieu,id, month):
        #print(" ")
        #print(f"Taking max load at {lieu} for stop id {id}")
        #print(f"tournee before taking load: {self}")
        #print(" ")
        current_amount = (0,0)
        current_volume = 0
        for i, (l, amount) in enumerate(self.list_arrets):
            current_amount = sub_tuples(current_amount, amount)
            current_volume = V_clim * current_amount[0] + V_heater * current_amount[1]
            #print("-------")
            #print(f"At stop {i} : {l} with amount {amount}, current volume {current_volume}")
            if l == lieu and i == id :
                if isinstance(lieu, Plant) :
                    load = best_truck_load(month, TRUCK_CAPACITY - current_volume)
                    #print(f"Taking load {load} at Plant")
                    load_clim, load_heater = load
                    self.list_arrets[i] = (l, add_tuples(amount, (-load_clim, -load_heater)))
                elif isinstance(lieu, Warehouse) :
                    print(f"taking max load in warehouse : {lieu}")
                    available_clim, available_heater = lieu.get_stock()
                    print(f"available load : {available_clim,available_heater}")

                    load_clim1, load_heater1 = best_truck_load(month, TRUCK_CAPACITY - current_volume)
                    load_clim = min(load_clim1, available_clim)
                    load_heater = min(load_heater1, available_heater)

                    print(f"load taken : {load_clim,load_heater} ")

                    if load_clim1 < load_clim :
                        V = load_clim * V_clim + load_heater * V_heater
                        while V <= TRUCK_CAPACITY - current_volume :
                            load_heater += 1
                            V = load_clim * V_clim + load_heater * V_heater
                        load_heater -= 1
                    if load_heater1 < load_heater :
                        V = load_clim * V_clim + load_heater * V_heater
                        while V <= TRUCK_CAPACITY - current_volume :
                            load_clim += 1
                            V = load_clim * V_clim + load_heater * V_heater
                        load_clim -= 1

                    print(f"arret avant : {self.list_arrets[i]}")
                    self.list_arrets[i] = (l, add_tuples(amount, (-load_clim, -load_heater)))

                    print(f"arret après : {self.list_arrets[i]}")

        return i, load_clim, load_heater
        

    def repartir_load_among_shops(self,load_clim,load_heater, shops, month):

        

        free_spaces = [s.get_free_space() for s,_ in shops]
        



        free_space_clim = [fs[0] for fs in free_spaces]

        free_space_heater = [fs[1] for fs in free_spaces]

        repart_clim,remaing_clim = repartir_among_free_spaces(load_clim,free_space_clim)
        repart_heater,remaining_heater = repartir_among_free_spaces(load_heater,free_space_heater)
        

        return (remaing_clim,remaining_heater)
        




    def optimiser(self, config: Configuration, month):
        current_amount = (0,0)
        current_volume = 0
        load_clim = 0
        load_heater = 0
        shops = []
        for id_stop, (lieu, amount) in enumerate(self.list_arrets):
            
            current_amount = sub_tuples(current_amount, amount)
            current_volume = V_clim * current_amount[0] + V_heater * current_amount[1]
            if isinstance(lieu, Plant) or isinstance(lieu, Warehouse):
                load_clim, load_heater = self.repartir_load_among_shops(load_clim, load_heater, shops, month)
                shops = []
                _,i_load_clim, i_load_heater = self.take_max_load_at(lieu,id_stop, month)
                load_clim += i_load_clim
                load_heater += i_load_heater
            elif isinstance(lieu, Shop) and (load_clim > 0 or load_heater > 0):
                shops.append((lieu, id_stop))
        load_clim, load_heater = self.repartir_load_among_shops(load_clim, load_heater, shops, month)

        """if load_clim > 0 or load_heater > 0:

            print(f"After optimisation, remaining load : clim {load_clim}, heater {load_heater}")
                
"""





    def __str__(self):
        tournee_str = f"Tournee starting at {self.home}:\n"
        load = 0,0
        for lieu, amount in self.list_arrets:
            tournee_str += f"  Stop at {lieu} with delivery {amount}\n"
            load = sub_tuples(load, amount)
            tournee_str += f"load camion : {load}\n"
        tournee_str += f"Ending at {self.end}"
        return tournee_str
    

    def add_take_load(self, lieu):
        load = (0,0)
        for l, amount in self.list_arrets:
            load = sub_tuples(load, amount)

        #print(f"Current load before taking from {lieu}: {load}")
        if load != (0,0):
            self.ajoute_arret((lieu, load),0)

    def start_at_warehouse(self,config: Configuration):
        W = get_nearest_warehouse(self.home.x, self.home.y, config)
        if not isinstance(self.home, Plant):
            print("Warning: start_at_warehouse called but home is not a Plant")

        self.home = W

    def end_at_warehouse(self,config: Configuration, month = None): 
        if isinstance(self.end, Plant):
            load_clim,load_heater = best_truck_load(month)
            self.ajoute_arret((self.end, (-load_clim, -load_heater)),-1)


        W = get_nearest_warehouse(self.end.x, self.end.y, config)
        self.end = W
        total_load = self.get_total_load()

        self.ajoute_arret((W, total_load),-1)
        #print(f"End at warehouse {W.id} with load {total_load}")



    def get_total_load(self):
        total_load = (0,0)
        for lieu, amount in self.list_arrets:
            total_load = sub_tuples(total_load, amount)
        return total_load

    def ajoute_arret(self,arret,i=0):
        if i == -1:
            self.list_arrets.append(arret)
        else:
            self.list_arrets.insert(i,arret)


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
            

    def undo_tournee(self):
        for lieu, amount in self.list_arrets:
            if isinstance(lieu, Plant) is False:
                
                lieu.truck_stop((-amount[0], -amount[1]))
    

            
            

    def calculer_distance_totale(self):
        total_distance = 0
        current_location = self.home

        for lieu, _ in self.list_arrets:
            total_distance += distance(current_location, lieu)
            current_location = lieu

        total_distance += distance(current_location, self.home)

        return total_distance
            


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


def total_dist(list_tournee : list):
    total_distance = 0
    for t in list_tournee:
        total_distance += t.calculer_distance_totale()
    return total_distance












