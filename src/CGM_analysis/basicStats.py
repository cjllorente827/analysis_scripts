import yt
import numpy as np

from ndustria import AddTask

@AddTask()
def getGasMass(cell_mass):
    
    return cell_mass.sum()

@AddTask()
def getInOutRate(Rvel, cell_mass, radius):
    
    in_rate = np.abs(cell_mass[Rvel < 0] * Rvel[Rvel < 0] / radius[Rvel < 0]).sum()
    out_rate = np.abs(cell_mass[Rvel > 0] * Rvel[Rvel > 0] / radius[Rvel > 0]).sum()

    return in_rate, out_rate


@AddTask()
def printReport(
    cgm_mass,
    cold_gas_mass,
    warm_gas_mass,
    hot_gas_mass,
    in_rate, out_rate,
    cold_in_rate, cold_out_rate,
    warm_in_rate, warm_out_rate,
    hot_in_rate, hot_out_rate,
    save_to
):

    with open(save_to, "w") as stats_file:

        print(f"""
|---------------------------------------------------------
| Basic statistics report
|---------------------------------------------------------
CGM gas mass            : {cgm_mass.to('Msun'):.5e} 
Cold gas mass           : {cold_gas_mass.to('Msun'):.5e} 
Cold gas fraction       : {cold_gas_mass/cgm_mass:.5e} 
Warm gas mass           : {warm_gas_mass.to('Msun'):.5e} 
Warm gas fraction       : {warm_gas_mass/cgm_mass:.5e}  
Hot gas mass            : {hot_gas_mass.to('Msun'):.5e} 
Hot gas fraction        : {hot_gas_mass/cgm_mass:.5e}  
Infall rate             : {in_rate.to('Msun/yr'):.5e}
Outflow rate            : {out_rate.to('Msun/yr'):.5e}
Cold gas Infall rate    : {cold_in_rate.to('Msun/yr'):.5e}
Cold gas Outflow rate   : {cold_out_rate.to('Msun/yr'):.5e}
Warm gas Infall rate    : {warm_in_rate.to('Msun/yr'):.5e}
Warm gas Outflow rate   : {warm_out_rate.to('Msun/yr'):.5e}
Hot gas Infall rate     : {hot_in_rate.to('Msun/yr'):.5e}
Hot gas Outflow rate    : {hot_out_rate.to('Msun/yr'):.5e}
""", file=stats_file)

    return save_to