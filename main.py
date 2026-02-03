from datetime import date, timedelta
from routing_script import *
from ventes import *
import os



C0 = configuration_initiale()

debut = date(2024, 1, 1)

for i in range(365):
    jour = debut + timedelta(days=i)
    month = months[jour.month]
    
    C_after, dist, tournees_opt = find_livraisons(C0,month)
    name_dir = f"plots_and_data_for_day_{jour}"
    os.makedirs(name_dir,exist_ok=True)

    for i,t in enumerate(tournees_opt) :
        plot_tournee(t,name=f"{name_dir}/tournee_{i}")

    C_after.plot(title=f"Configuration After Livraisons - Iteration {i}", path=f"{name_dir}/configuration_after_livraisons_iter_{i}.png")
    C0, liste_ventes = ventes(C_after, month, df)
    C0.plot(title=f"Configuration After Ventes - Iteration {i}", path=f"{name_dir}/configuration_after_ventes_iter_{i}.png")

