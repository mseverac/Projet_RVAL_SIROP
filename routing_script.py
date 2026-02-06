from utils import *
from esperance_perte import *
from configuration import *

import copy as cp
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import traceback

import matplotlib.pyplot as plt

"""V_clim10 = int(V_clim * 10)
V_heater10 = int(V_heater * 10)
"""
V_clim10 = 8
V_heater10 = 4

N_MAX_VEHICLES = 80

plant_positions = [(1,2),(6,5)]
warehouse_positions = [(4,3),(9,4)]
shop_positions = [(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
                (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)]

locations = [(4,3),(9,4),(1,2),(6,5),(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
            (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)] #positions of warehouses ,plants and shops



distance_matrix = []

for a in locations:
    row = []
    for b in locations:
        row.append(int((abs(a[0]-b[0]) + abs((a[1]-b[1])))))
    distance_matrix.append(row)

def compute_volume(demand1, demand2):
    return V_clim10 * demand1 + V_heater10 * demand2

#def plot_solution(data, manager, routing, solution):
    locations = [(1,2),(6,5),(4,3),(9,4),(2,0),(10,0),(3,1),(5,1),(8,1),(0,2),(2,3),(6,3),(10,3),(12,3),
            (1,4),(4,4),(11,4),(3,5),(8,5),(10,5),(2,6),(4,6),(7,6),(12,6)]


    routes = []
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue

        route = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append((vehicle_id, route))

    plt.figure(figsize=(12, 10))
    colors = ['r', 'b', 'g', 'm', 'c', 'y', 'orange', 'purple']

    # Clients
    for i, (x, y) in enumerate(locations):
        plt.plot(x, y, 'ko', markersize=7)
        plt.text(
            x + 15, y + 15,
            f"{i}",
            fontsize=9
        )

    # Dépôts
    for depot in data["depots"]:
        x, y = locations[depot]
        plt.plot(x, y, 'r*', markersize=20)
        plt.text(x + 20, y + 20, f"Dépôt {depot}", fontsize=12, color='red')

    # Routes
    for vehicle_id, route in routes:
        x_coords = [locations[n][0] for n in route]
        y_coords = [locations[n][1] for n in route]
        plt.plot(
            x_coords, y_coords,
            color=colors[vehicle_id % len(colors)],
            marker='o',
            label=f'Vehicle {vehicle_id}'
        )

    plt.title("CVRP multi-dépôts (2 dépôts, capacité volume)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.show()

def compute_demands(C0 : Configuration, C1 : Configuration):
    demande1 = []
    demande2 = []
    for shop0, shop1 in zip(C0.shops, C1.shops):
        demand_p1 = max(0, shop1.current_stock[0] - shop0.current_stock[0])
        demand_p2 = max(0, shop1.current_stock[1] - shop0.current_stock[1])
        demande1.append(demand_p1)
        demande2.append(demand_p2)
    return demande1, demande2


def supr_shops_with_no_demand(data):
    new_demands = []
    new_demands2 = []
    new_start = []
    new_end = []
    ids_removed = []
    for i, (d1, d2) in enumerate(zip(data["demands"], data["demands2"])):
        if d1 == 0 and d2 == 0:
            continue
        else:
            new_demands.append(d1)
            new_demands2.append(d2)
            new_start.append(data["start"][i])
            new_end.append(data["end"][i])
    data["demands"] = new_demands
    data["demands2"] = new_demands2
    data["start"] = new_start
    data["end"] = new_end


def create_data_models(C0, C1, starts,ends):

    def build_configs(starts, ends ):
        """Retourne la liste des couples (start, end) selon le type de stock."""
        
        return [(i, j) for i in starts for j in ends]

    def expand_configs(configs, N=10):
        """Génère les listes start et end répétées N fois."""
        start, end = [], []
        for s, e in configs:
            start += [s] * N
            end += [e] * N
        return start, end

    def build_data(demande1, demande2):
        """Construit un dictionnaire data à partir des demandes."""
        data = {}

        data["distance_matrix"] = distance_matrix
        data["demands"]  = [0, 0, 0, 0] + demande1
        data["demands2"] = [0, 0, 0, 0] + demande2
        data["depots"] = [0, 1, 2, 3]

        configs = build_configs(starts,ends)
        start, end = expand_configs(configs)

        data["start"] = start
        data["end"] = end

        data["num_vehicles"] = len(start)
        data["vehicle_volume_capacity"] = [200] * len(start)

        return data

    # ---- Corps principal ----

    demande1, demande2 = compute_demands(C0, C1)

    demande1_prime = [0] * len(demande1)
    demande2_prime = [0] * len(demande2)

    double_demand = False

    for i, (d1, d2) in enumerate(zip(demande1, demande2)):
        if compute_volume(d1, d2) > 200:
            double_demand = True
            print(f"Warning: demand at shop {i} exceeds vehicle capacity.")

            demande1_prime[i] = d1 // 2
            demande2_prime[i] = d2 // 2

            demande1[i] = d1 - demande1_prime[i]
            demande2[i] = d2 - demande2_prime[i]

    datas = [build_data(demande1, demande2)]

    if double_demand:
        datas.append(build_data(demande1_prime, demande2_prime))

    return datas



def print_solution(data, manager, routing, solution):
    print(f"Objective: {solution.ObjectiveValue()}")

    volume_dim = routing.GetDimensionOrDie("Volume")


    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue

        index = routing.Start(vehicle_id)
        route_distance = 0
        print(f"\nRoute for vehicle {vehicle_id}:")

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            load = solution.Value(volume_dim.CumulVar(index))
            print(f" {node} (Volume={load/10:.1f} m3) -> ", end="")
            next_index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                index, next_index, vehicle_id
            )
            index = next_index

        node = manager.IndexToNode(index)
        load = solution.Value(volume_dim.CumulVar(index))
        print(f"{node} (Volume={load/10:.1f} m3)")
        print(f" Distance: {route_distance}")

def create_tournees(data, manager, routing, solution, nodes):
    """
    Crée une liste d'objets Tournee à partir de la solution OR-Tools
    """

    tournees = []

    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue

        index = routing.Start(vehicle_id)
        route = []

        while not routing.IsEnd(index):
            node_id = manager.IndexToNode(index)
            route.append(node_id)
            index = solution.Value(routing.NextVar(index))

        # dernier noeud (end)
        route.append(manager.IndexToNode(index))

        # --- Construction de la tournée ---
        home_node_id = route[0]
        end_node_id = route[-1]

        home = nodes[home_node_id]
        end = nodes[end_node_id]

        list_arrets = []

        d1_total = 0
        d2_total = 0



        # on enlève le home et le end
        for node_id in route[1:-1]:
            node = nodes[node_id]

            # Variation de stock (à adapter selon ton modèle)
            d1 = data["demands"][node_id]
            d2 = data["demands2"][node_id]
            delta_stock = (d1, d2)

            list_arrets.append([node, delta_stock])
            d1_total += d1
            d2_total += d2

        

        list_arrets.insert(0, [home, (-d1_total, -d2_total)])

        

        tournee = Tournee(
            home=home,
            list_arrets=list_arrets,
            end=end
        )

        tournees.append(tournee)

    return tournees



def solve_and_create_tournees(C0 : Configuration, C1 ,month,starts,ends,plot = False):



    datas = create_data_models(C0,C1, starts,ends)

    tournees = []

    for data in datas:

        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]),
            data["num_vehicles"],
            data["start"],
            data["end"]
        )

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            return data["distance_matrix"][
                manager.IndexToNode(from_index)
            ][
                manager.IndexToNode(to_index)
            ]

        routing.SetArcCostEvaluatorOfAllVehicles(
            routing.RegisterTransitCallback(distance_callback)
        )

        def volume_callback(from_index):
            node = manager.IndexToNode(from_index)
            return V_clim10 * data["demands"][node] + V_heater10 * data["demands2"][node]

        routing.AddDimensionWithVehicleCapacity(
            routing.RegisterUnaryTransitCallback(volume_callback),
            0,
            data["vehicle_volume_capacity"],
            True,
            "Volume"
        )

        for node in range(len(data["distance_matrix"])):
            if node not in data["start"] and node not in data["end"]:
                if data["demands"][node] == 0 and data["demands2"][node] == 0:
                    routing.AddDisjunction([manager.NodeToIndex(node)], 0)




        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.FromSeconds(2)

        solution = routing.SolveWithParameters(search_parameters)

        #print(solution)

        if solution:
            warehouses = C0.warehouses 
            plants = C0.plants
            shops = C0.shops
            #print_solution(data, manager, routing, solution)
            tournees1 = create_tournees(data, manager, routing, solution,warehouses + plants + shops)
            #plot_tournees(tournees1)
            tournees = tournees + tournees1


    if plot :

        for t in tournees:
            plot_tournee(t)
        plot_tournees(tournees)
        

    #print(f"Total number of tournees: {len(tournees)}")

    for t in tournees:
        #print(f"tourne home before : {t.home}")
        if isinstance(t.home, Plant):
            t.start_at_warehouse(C0)
            #print(f"tourne home after : {t.home}")
        if isinstance(t.end, Plant):
            #plot_tournee(t)
            t.end_at_warehouse(C0, month) 
            #print(f"tourne end after : {t.end}")
            #plot_tournee(t)

    



    return tournees


def optimise_tournees(C, month, list_tournees):
    for t in list_tournees:
        t.optimiser_tournee(C, month)


def find_livraisons(C0, month):

    def try_solve(starts,ends, message=None):
        """Tente de résoudre avec un stock donné. Retourne True si succès."""
        try:
            if message:
                print("\033[92m" + message + "\033[0m")

            tournees = solve_and_create_tournees(C0, C1, month, starts,ends, plot=False)


            C0p : Configuration = cp.deepcopy(C0)
            C0p.plot(title="Config avant effectuer tournee ",show=False)


            for t in tournees :
                t : Tournee
                t.with_config(C0p)
                #print(" t :",t)
                t.effectuer_tournee()
                #print(" t apres : ",t)

            C0p.plot(title="Config apres effectuer tournee ",show=False)


            tournees_opt = []

            for t in tournees : 
                t.with_config(C0p)
                
                t_opt = cp.deepcopy(t)
                t : Tournee

                C0p.plot(title="Config avant opt",show=False)
                t_opt.plot(C0p,title = "tournee non optimisée" , show = False)

                t_opt.with_config(C0p)
                t_opt.optimiser(C0p, month)
                t_opt.unload_final_warehouse()


                t_opt.plot(C0p,title = "tournee optimisée" , show = False)
                #plt.show()

                tp = sub_tournees(t_opt,t)
                tp.plot(C0p,title="tp",show=False)

                tp.plot(C0p,title = "diff tournee " , show = False)

                #plt.show()

                tp.with_config(C0p)

            
                tp.effectuer_tournee()


                C0p.plot(title="Config tournee apres tournee opt ",show=False)
                #plt.show()


                tournees_opt.append(t_opt)
                plt.close("all")
            return tournees

        except Exception as e:
            if message:
                print("Fail de :", message)

            """print("Erreur :", e)
            traceback.print_exc()"""
            plt.close("all")


            return False
        

    C1 = configuration_minimale(month, df)
    C0p = cp.deepcopy(C0)

    W0 : Warehouse= C0p.warehouses[0] 
    W1 : Warehouse= C0p.warehouses[1] 


    if W0.is_stock_eleve() and W1.is_stock_eleve() :
        strategies = [
        (range(2),range(2), "W->W"),
        (range(3),range(2), "W,P0->W"),
        ((0,1,3),range(2), "W,P1->W"),

        (range(4),range(2), "W,P->W"),
        ((0,2,3),range(2), "W0,P->W"),
        ((1,2,3),range(2), "W1,P->W"),

        (range(2,4),range(2), "P->W"),
        ]

    elif W0.is_stock_eleve():
        strategies = [
        ((0,1,3),(0,1,3), "W,P1->W,P1"),
        (range(4),(0,1,3), "W,P->W,P1"),
        ((0,2,3),(0,1,2), "W0,P->W,P1"),
        (range(2,4),(0,1,3), "P->W,P1"),

        ]

    elif W1.is_stock_eleve():
        strategies = [
        ((0,1,2),(0,1,2), "W,P0->W,P0"),
        (range(4),(0,1,2), "W,P->W,P0"),
        (range(1,4),(0,1,2), "W1,P->W,P0"),
        (range(2,4),(0,1,2), "P->W,P0"),        
        ]


    else :
        strategies = [
            (range(4),range(4), "W,P->W,P"),
            (range(2,4),range(4), "P->W,P"),
            
        ]


    


    for starts,ends, message in strategies:
        tournees = try_solve(starts,ends, message)
        if tournees is not False :
            break



    #C0p.plot()


    C0p : Configuration

    for t in tournees:

        t.with_config(C0p)
        
        t : Tournee

        t.effectuer_tournee()



    return C0p,total_dist(tournees), tournees


