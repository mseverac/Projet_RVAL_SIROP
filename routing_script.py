from utils import *
from espérence_perte import *
from configuration import *

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import matplotlib.pyplot as plt

"""V_clim10 = int(V_clim * 10)
V_heater10 = int(V_heater * 10)
"""
V_clim10 = 8
V_heater10 = 4

N_MAX_VEHICLES = 40

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

def create_data_models():

    data = {}

    C0 = configuration_initiale()

    for w in C0.warehouses: 
        w.current_stock = (100,100)

    C1 = configuration_minimale("Mai", df)

    demande1 , demande2 = compute_demands(C0, C1)
    demande1_prime = [0 for _ in range(len(demande1))] 
    demande2_prime = [0 for _ in range(len(demande2))]

    double_demand = False   

    for i,(d1, d2) in enumerate(zip(demande1, demande2)):
        if compute_volume(d1,d2) > 200 :
            double_demand = True
            print(f"Warning: demand at shop {i} exceeds vehicle capacity.")

            demande1_prime[i] = d1 // 2
            demande2_prime[i] = d2 // 2

            demande1[i] = d1 - demande1_prime[i]
            demande2[i] = d2 - demande2_prime[i]



    data["distance_matrix"] = distance_matrix

    data["demands"]  = [0,0,0,0] + demande1
    data["demands2"] = [0,0,0,0] + demande2

    data["depots"] = [0,1]

    data["num_vehicles"] = N_MAX_VEHICLES
    data["vehicle_volume_capacity"] = [200] * data["num_vehicles"]

    print(data)

    if double_demand:
        datas = []

        data_prime = {}

        data_prime["distance_matrix"] = distance_matrix

        data_prime["demands"]  = [0,0,0,0] + demande1_prime
        data_prime["demands2"] = [0,0,0,0] + demande2_prime

        data_prime["depots"] = [2, 3]

        data_prime["num_vehicles"] = N_MAX_VEHICLES
        data_prime["vehicle_volume_capacity"] = [200] * data_prime["num_vehicles"]

        datas.append(data)
        datas.append(data_prime)

        return datas
    else:
        return [data]



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



def main():
    data = create_data_models()[0]

    N = N_MAX_VEHICLES // 4

    starts = [0]*N + [1]*N + [0]*N + [1]*N
    ends   = [0]*N + [1]*N + [1]*N + [0]*N

    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        starts,
        ends
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



    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(2)

    solution = routing.SolveWithParameters(search_parameters)

    print(solution)

    if solution:
        print_solution(data, manager, routing, solution)
        tournees = create_tournees(data, manager, routing, solution,warehouses + plants + shops)
        for t in tournees:
            plot_tournee(t)
        plot_tournees(tournees)

if __name__ == "__main__":
    main()
