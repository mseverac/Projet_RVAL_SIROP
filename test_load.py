from routing_script import *

C = Configuration.load_txt("plots/plots_and_data_for_day_2024-01-10/configuration_after_ventes Configuration After Ventes - Iteration 6")

#C.plot()


C_after, dist,tournees = find_livraisons(C,months[1])

C_after.plot()


"""C_after, dist, tournees_opt,tournees = find_livraisons(C_after,months[1])
C_after.plot()
"""