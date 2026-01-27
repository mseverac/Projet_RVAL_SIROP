from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from configuration import *
from espérence_perte import *


TRUCK_CAPACITY = 20 # m3


def compute_shop_demands(config_init, config_goal):
    demands = {}
    for shop_init, shop_goal in zip(config_init.shops, config_goal.shops):
        dh = shop_goal.current_stock[0] - shop_init.current_stock[0]
        dc = shop_goal.current_stock[1] - shop_init.current_stock[1]
        if dh < 0 or dc < 0:
            raise ValueError("Negative demand at shop")
        demands[shop_init.id] = (dh, dc)
    return demands



def shop_volume(demand):
    return V_heater * demand[0] + V_clim * demand[1]


def solve_warehouse_vrp(warehouse, shops, demands):
    # Nodes: depot + shops with demand > 0
    nodes = [warehouse] + [s for s in shops if demands[s.id] != (0,0)]
    node_ids = {node.id: i for i, node in enumerate(nodes)}

    def distance_cb(from_i, to_i):
        a = nodes[from_i]
        b = nodes[to_i]
        return int((a.x-b.x)+ (a.y-b.y))

    manager = pywrapcp.RoutingIndexManager(
        len(nodes),
        len(nodes),      # unlimited vehicles
        0                # depot index
    )

    routing = pywrapcp.RoutingModel(manager)

    transit_cb = routing.RegisterTransitCallback(
        lambda i, j: distance_cb(manager.IndexToNode(i),
                                 manager.IndexToNode(j))
    )

    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb)

    # Capacity constraint (volume)
    def demand_cb(index):
        node = nodes[manager.IndexToNode(index)]
        if isinstance(node, Warehouse):
            return 0
        return int(100 * shop_volume(demands[node.id]))

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_cb)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        [int(100 * TRUCK_CAPACITY)] * len(nodes),
        True,
        "Capacity"
    )

    print("begin solving VRP...")

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search_params.time_limit.seconds = 300

    print("searching for solution...")




    solution = routing.SolveWithParameters(search_params)
    if not solution:
        return []
    
    print("solution found!")

    tours = []

    for v in range(len(nodes)):
        index = routing.Start(v)
        if routing.IsEnd(solution.Value(routing.NextVar(index))):
            continue

        tour = []
        while not routing.IsEnd(index):
            node = nodes[manager.IndexToNode(index)]
            if not isinstance(node, Warehouse):
                tour.append(node)
            index = solution.Value(routing.NextVar(index))

        if tour:
            tours.append(tour)

    return tours


def build_tournees(config_init, config_goal):
    demands = compute_shop_demands(config_init, config_goal)
    print("Demands:", demands)
    tournees = []

    for warehouse in config_init.warehouses:
        
        tours = solve_warehouse_vrp(warehouse, config_init.shops, demands)

        print(f"Tours for warehouse {warehouse.id}: {tours}")

        for tour in tours:
            arrets = []
            remaining_volume = TRUCK_CAPACITY

            for shop in tour:
                dh, dc = demands[shop.id]
                max_h = min(dh, remaining_volume // V_heater)
                remaining_volume -= max_h * V_heater
                max_c = min(dc, remaining_volume // V_clim)

                delivered = (int(max_h), int(max_c))
                demands[shop.id] = (
                    dh - delivered[0],
                    dc - delivered[1]
                )

                arrets.append((shop, delivered))

            tournees.append(Tournee(warehouse, arrets))

    return tournees


if __name__ == "__main__":
    C0 = configuration_initiale()
    C1 = configuration_minimale("Mai", df)

    C1.plot()

    tournees = build_tournees(C0, C1)

    print("Tournees planned:")
    print(tournees)

    for i, tournee in enumerate(tournees):
        print(f"Tournee {i+1}:")
        for lieu, amount in tournee.list_arrets:
            print(f"  Stop at {lieu.id} to deliver {amount}")
        print(f"  Total distance: {tournee.calculer_distance_totale():.2f}\n")