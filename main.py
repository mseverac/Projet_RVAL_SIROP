
from routing_script import *
from ventes import *


C0 = configuration_initiale()


for i in range(10):

    C_after, dist, tournees_opt = find_livraisons(C0,"Mai")


    C_after.plot(title=f"Configuration After Livraisons - Iteration {i}", path=f"plots/configuration_after_livraisons_iter_{i}.png")
    C0, liste_ventes = ventes(C_after, "Mai", df)
    C0.plot(title=f"Configuration After Ventes - Iteration {i}", path=f"plots/configuration_after_ventes_iter_{i}.png")

