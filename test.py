from configuration import * 

print("DEBUT")
"""W1 = warehouses[0]
W2 = warehouses[1]  

P1 = plants[0]
P2 = plants[1]



exemple_tournee.effectuer_tournee()
print_configuration()
#plot_configuration()
plot_tournee(exemple_tournee)"""


C0 = configuration_initiale()
C0.print()
#C0.plot()


exemple_tournee = Tournee(C0.warehouses[0], [(C0.plants[0],(-10,-5)), (C0.shops[0],(5,3)), (C0.shops[1],(5,2))])
exemple_tournee.effectuer_tournee()


plot_tournee(exemple_tournee)

C0.print()
#C0.plot()
