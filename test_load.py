from routing_script import *
from ventes import *

C = Configuration.load_txt("plots/plots_and_data_for_day_2024-12-17/configuration_after_ventes Configuration After Ventes - Iteration 4")

#C.plot()

for i in range(10):

    C_after, dist,tournees = find_livraisons(C,months[12])

    plt.close("all")

    C_after.plot()

    C, liste_ventes = ventes(C_after, months[12], df)


"""C_after, dist, tournees_opt,tournees = find_livraisons(C_after,months[1])
C_after.plot()
"""