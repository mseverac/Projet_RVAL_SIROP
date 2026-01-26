
TRUCK_CAPACITY = 20 # m3
WAREHOUSE_CAPACITY = 650 # items for each product

V_heater = 0.4 # m3
V_clim = 0.8 # m3



class Shop : 
    def __init__(self,id,x,y,capacity):
        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity
        self.current_stock = 0,0

    def truck_stop(self, amount_delivered):
        if amount_delivered + self.current_stock  >= 0 and amount_delivered + self.current_stock  <= self.capacity:
            self.current_stock += amount_delivered
            return amount_delivered
        else:
            raise ValueError(f"Wrong stock after delivery : {self.current_stock + amount_delivered}")
            return 0
        

class Warehouse :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.current_stock = (0,0)



    def get_stock(self):
        return self.current_stock
    
    def truck_stop(self, amount_delivered):
        if amount_delivered + self.current_stock  >= 0 and amount_delivered + self.current_stock  <= WAREHOUSE_CAPACITY:
            self.current_stock += amount_delivered
            return amount_delivered
        else:
            raise ValueError(f"Wrong stock after delivery : {self.current_stock + amount_delivered}")
            return 0
        

class Plant :
    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def truck_stop(self, amount_delivered):
        if amount_delivered <= 0:
            raise ValueError("Plants cannot receive deliveries")
        

def distance(a, b):
    return ((a.x - b.x)+ (a.y - b.y))



class Tournee:
    def __init__(self, home, list_arrets):
        self.home = home
        self.list_arrets = list_arrets

    def effectuer_tournee(self):

        remplissage_camion = 0
        for lieu, amount in self.list_arrets:
            lieu.truck_stop(amount)

            remplissage_camion += V_heater * amount[0] + V_clim * amount[1]
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
            
