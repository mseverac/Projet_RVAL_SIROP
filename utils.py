
TRUCK_CAPACITY = 20 # m3
WAREHOUSE_CAPACITY = 650 # items for each product

V_heater = 0.4 # m3
V_clim = 0.8 # m3


def add_tuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


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
            remplissage_camion += V_heater * amount[0] + V_clim * amount[1]
            if remplissage_camion > TRUCK_CAPACITY:
                return False
            if not lieu.can_truck_stop(amount):
                return False
        return True

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
            
