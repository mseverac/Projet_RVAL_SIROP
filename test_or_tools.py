from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np

# ---------------------------
# DATA
# ---------------------------

def create_data_model():
    data = {}

    data["num_depots"] = 4
    data["num_shops"] = 20
    data["num_nodes"] = data["num_depots"] + data["num_shops"]

    data["num_vehicles"] = 6  # par exemple

    # Dépôts possibles pour chaque camion
    data["starts"] = [0, 1, 2, 3, 0, 1]
    data["ends"]   = [0, 1, 2, 3, 0, 1]

    # Matrice de coûts (EXEMPLE)
    np.random.seed(0)
    cost_matrix = np.random.randint(10, 100, size=(data["num_nodes"], data["num_nodes"]))
    np.fill_diagonal(cost_matrix, 0)

    data["cost_matrix"] = cost_matrix.tolist()

    return data

# ---------------------------
# MODEL
# ---------------------------

def main():
    data = create_data_model()

    manager = pywrapcp.RoutingIndexManager(
        data["num_nodes"],
        data["num_vehicles"],
        data["starts"],
        data["ends"]
    )

    routing = pywrapcp.RoutingModel(manager)

    # ---------------------------
    # COST CALLBACK
    # ---------------------------
    def cost_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["cost_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(cost_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # ---------------------------
    # CONSTRAINTS
    # ---------------------------

    # Chaque shop est visité exactement une fois
    for shop in range(data["num_depots"], data["num_nodes"]):
        routing.AddDisjunction([manager.NodeToIndex(shop)], 10_000)

    # ---------------------------
    # SOLVER PARAMS
    # ---------------------------
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 10

    # ---------------------------
    # SOLVE
    # ---------------------------
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("Pas de solution trouvée")

# ---------------------------
# DISPLAY
# ---------------------------

def print_solution(data, manager, routing, solution):
    total_cost = 0

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_cost = 0
        route = []

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_cost += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        route.append(manager.IndexToNode(index))
        total_cost += route_cost

        print(f"Camion {vehicle_id} : {route} | coût = {route_cost}")

    print(f"\nCoût total = {total_cost}")

# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    main()
