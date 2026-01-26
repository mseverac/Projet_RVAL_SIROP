from configuration import * 

print("DEBUT")
W1 = warehouses[0]
W2 = warehouses[1]  

P1 = plants[0]
P2 = plants[1]


exemple_tournee = Tournee(W1, [(P1,(-10,-5)), (shops[0],(5,3)), (shops[1],(5,2))])

exemple_tournee.effectuer_tournee()
print_configuration()
plot_configuration()