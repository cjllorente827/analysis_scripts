from analysis_scripts import *

import yt, trident, os
yt.set_log_level(50)
import numpy as np
from ndustria import Pipeline

from .phase import ytPhaseDiagram
from .project import ytProjectionPlot
from .hist2d import plotHist2d, FourPanelHist2d
from .basicStats import  getGasMass, printReport, getInOutRate
from ..utils import getFieldData

def run_pipeline(enzo_dataset, box_spec_file):

    ds, box, region = getDataBoxAndRegion(enzo_dataset, box_spec_file)

    # set the center
    # Its important to set the center field parameter to a ytarray
    # in code_length units. 
    # If you don't yt will be sad :(
    center = ds.arr(box.center, "code_length") 
    region.set_field_parameter("center", box.center)

    # cut the disk out
    inner_sphere = ds.sphere(box.center, (10, "kpc"))
    outer_sphere = ds.sphere(box.center, (200, "kpc")) 

    cgm = outer_sphere - inner_sphere

    cgm_cut = cgm.cut_region("(obj['temperature'] > 1.5e4) | (obj['density'] < 2e-26)")
    # Cut regions don't use their own field_parameters for calculations
    # they use their underlying base_object parameters
    cgm_cut.base_object.set_field_parameter("center", center)

    # make temperature to separate the different phases of the gas
    cold_cgm = cgm_cut.cut_region("(obj['temperature'] <= 1e5)")
    cold_cgm.base_object.set_field_parameter("center", center)

    warm_cgm = cgm_cut.cut_region("(1e5 < obj['temperature']) & (obj['temperature'] <= 2e6)")
    warm_cgm.base_object.set_field_parameter("center", center)

    hot_cgm = cgm_cut.cut_region("2e6 < (obj['temperature'])")
    hot_cgm.base_object.set_field_parameter("center", center)

    # on my ion bullshit
    all_ion_list=[
        'H I',
        'C II','C III','C IV',
        'Si II','Si III','Si IV',
        'O I','O II','O III','O IV','O V','O VI','O VII','O VIII'
    ]

    important_ion_list = [
        'H I',
        'C IV',
        'O VI',
        'Mg II'
    ]

    trident.add_ion_fields(ds, ions=important_ion_list)


    fields = ["density", "temperature"]
    # project the cut to see what got cut
    for field in fields:
        ytProjectionPlot(ds, box, region, f"{getOutputDir()}/{str(ds)}_{field}.png", field=field)
        ytProjectionPlot(ds, box, cgm_cut, f"{getOutputDir()}/{str(ds)}_cgm_{field}.png", field=field)

    # project the cold, warm, and hot cuts
    ytProjectionPlot(ds, box, cold_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_cold_cgm_density.png", 
                     field="density",
                     title="Cold CGM cut ($T < 10^5$ K)"
    )
    ytProjectionPlot(ds, box, warm_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_warm_cgm_density.png", 
                     field="density",
                     title=r"Warm CGM cut ($10^5$ K $< T < 2 \times 10^6$ K)"
    )
    ytProjectionPlot(ds, box, hot_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_hot_cgm_density.png", 
                     field="density",
                     title=r"Hot CGM cut ($2 \times 10^6$ K $ < T$)"
    )


    ######################################################
    # Projections of each cut with O VI
    ######################################################
    full_O6 = ytProjectionPlot(ds, box, cgm_cut, 
                     save_to=f"{getOutputDir()}/{str(ds)}_cgm_OVI.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title="O[VI] Column Density (Entire CGM)",
                     zlims=[1e11, 1e15]
    )

    cold_O6 = ytProjectionPlot(ds, box, cold_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_cold_OVI.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title="O[VI] Column Density (Cold)",
                     zlims=[1e11, 1e15]
    )


    warm_O6 = ytProjectionPlot(ds, box, warm_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_warm_OVI.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title="O[VI] Column Density (Warm)",
                     zlims=[1e11, 1e15]
    )


    hot_O6 = ytProjectionPlot(ds, box, hot_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_hot_OVI.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title="O[VI] Column Density (Hot)",
                     zlims=[1e11, 1e15]
    )

    ######################################################
    # Projections of O[VI] fraction > threshold
    # i.e. the OVI DICHOTOMY
    ######################################################

    threshold = 0.1
    cold_cgm_O6_frac = cold_cgm.cut_region(f"(obj['O_p5_ion_fraction'] >= {threshold})")
    warm_cgm_O6_frac = warm_cgm.cut_region(f"(obj['O_p5_ion_fraction'] >= {threshold})")

    cold_cgm_O6_plot = ytProjectionPlot(ds, box, cold_cgm_O6_frac, 
                     save_to=f"{getOutputDir()}/{str(ds)}_cold_OVI_frac_gt_{threshold}.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title=r"Cool CGM $f_{OVI} >"+ f"{threshold}$",
                     zlims=[1e11, 1e15],
                     zlabel=r"O[VI] Column Density (1/cm$^2$)",
    )

    cold_cgm_O6_frac_plot = ytProjectionPlot(ds, box, cold_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_cold_OVI_frac.png", 
                     field="O_p5_ion_fraction", # read as Oxygen +5, i.e. O[VI]
                     method="max",
                     zlims=[1e-2,1],
                     weight_field=None,
                     title=r"Cool CGM $f_{OVI}$",
    )

    warm_cgm_O6_plot = ytProjectionPlot(ds, box, warm_cgm_O6_frac, 
                     save_to=f"{getOutputDir()}/{str(ds)}_warm_OVI_frac_gt_{threshold}.png", 
                     field="O_p5_number_density", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     title=r"Warm CGM $f_{OVI} >"+ f"{threshold}$",
                     zlims=[1e11, 1e15],
                     zlabel=r"O[VI] Column Density (1/cm$^2$)",
    )

    warm_cgm_O6_frac_plot = ytProjectionPlot(ds, box, warm_cgm, 
                     save_to=f"{getOutputDir()}/{str(ds)}_warm_OVI_frac.png", 
                     field="O_p5_ion_fraction", # read as Oxygen +5, i.e. O[VI]
                     weight_field=None,
                     method="max",
                     zlims=[1e-2,1],
                     title=r"Warm CGM $f_{OVI}$",
    )

    # make phase plots
    # standard phase plot with Temperature v density v cell_mass
    ytPhaseDiagram(ds, box, cgm_cut, f"{getOutputDir()}/{str(ds)}_phase.png")
    

    ######################################################
    # Plots for the entire CGM Cut
    ######################################################

    radius = getFieldData(cgm_cut, "radius")
    Rvel = getFieldData(cgm_cut, "radial_velocity")
    Tvel = getFieldData(cgm_cut, "tangential_velocity")
    cell_mass = getFieldData(cgm_cut, "cell_mass")
    temperature = getFieldData(cgm_cut, "temperature")
    density = getFieldData(cgm_cut, "density")
    metallicity = getFieldData(cgm_cut, "metallicity")
    OVI_density = getFieldData(cgm_cut, "O_p5_number_density")
    OVI_frac = getFieldData(cgm_cut, "O_p5_ion_fraction")

    ######################################################
    # phase diagram with OVI density color axis
    # saved to RDXXXX_phase_OVI_density.png
    ######################################################
    plotHist2d(
        density, "g/cm**3", "Density (g/cc)",
        temperature, "K", "Temperature (K)",
        OVI_density, "1/cm**3", "O[VI] number density",
        save_to=f"{getOutputDir()}/{str(ds)}_phase_OVI_density.png",
        cmap="viridis"
    )

    ######################################################
    # phase diagram with OVI density color axis
    # saved to RDXXXX_phase_OVI_density.png
    ######################################################
    plotHist2d(
        density, "g/cm**3", "Density (g/cc)",
        temperature, "K", "Temperature (K)",
        OVI_frac, "dimensionless", "O[VI] fraction",
        save_to=f"{getOutputDir()}/{str(ds)}_phase_OVI_frac.png",
        cmap="bwr",
        z_lim=[1e-2, 1]
    )

    ######################################################
    # 2d histogram of radial velocity v radius v cell mass
    # saved to RDXXXX_Rvel_radius_mass.png
    ######################################################
    plotHist2d(
        radius, "kpc", "Radius (kpc)",
        Rvel, "kpc/Myr", "Radial Velocity (kpc/Myr)",
        temperature, "K", "Temperature (K)",
        save_to=f"{getOutputDir()}/{str(ds)}_Rvel_radius.png",
        cmap="plasma"
    )

    ######################################################
    # 2d histogram of temperature v radius v cell mass
    # saved to RDXXXX_T_radius.png
    ######################################################
    plotHist2d(
        radius, "kpc", "Radius (kpc)",
        temperature, "K", "Temperature (K)",
        cell_mass, "Msun", "Cell Mass (Msun)",
        save_to=f"{getOutputDir()}/{str(ds)}_T_radius.png"
    )

    ######################################################
    # Data for the cold CGM Cut T < 1e5 K
    ######################################################

    cold_radius = getFieldData(cold_cgm, "radius")
    cold_Rvel = getFieldData(cold_cgm, "radial_velocity")
    cold_Tvel = getFieldData(cold_cgm, "tangential_velocity")
    cold_cell_mass = getFieldData(cold_cgm, "cell_mass")
    cold_temperature = getFieldData(cold_cgm, "temperature")
    cold_density = getFieldData(cold_cgm, "density")
    cold_metallicity = getFieldData(cold_cgm, "metallicity")

    ######################################################
    # Data for the warm CGM Cut 1e5 K < T < 2e6 K
    ######################################################

    warm_radius = getFieldData(warm_cgm, "radius")
    warm_Rvel = getFieldData(warm_cgm, "radial_velocity")
    warm_Tvel = getFieldData(warm_cgm, "tangential_velocity")
    warm_cell_mass = getFieldData(warm_cgm, "cell_mass")
    warm_temperature = getFieldData(warm_cgm, "temperature")
    warm_density = getFieldData(warm_cgm, "density")
    warm_metallicity = getFieldData(warm_cgm, "metallicity")


    ######################################################
    # Data for the hot CGM Cut 2e6 K < T
    ######################################################

    hot_radius = getFieldData(hot_cgm, "radius")
    hot_Rvel = getFieldData(hot_cgm, "radial_velocity")
    hot_Tvel = getFieldData(hot_cgm, "tangential_velocity")
    hot_cell_mass = getFieldData(hot_cgm, "cell_mass")
    hot_temperature = getFieldData(hot_cgm, "temperature")
    hot_density = getFieldData(hot_cgm, "density")
    hot_metallicity = getFieldData(hot_cgm, "metallicity")

    ######################################################
    # 4 Panel comparison plot of all cuts
    ######################################################

    ######################################################
    # 2d histogram of radial velocity v radius v temperature
    # saved to RDXXXX_Rvel_radius_4phase.png
    ######################################################


    FourPanelHist2d(
        x_data=[radius, cold_radius, warm_radius, hot_radius],
        x_units="kpc", x_label="Radius (kpc)",
        y_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        y_units="kpc/Myr", y_label="Radial Velocity (kpc/Myr)",
        z_data=[temperature, cold_temperature, warm_temperature, hot_temperature],
        z_units="K", z_label="Temperature (K)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Rvel_radius_4phase.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        cmap="plasma"
    )

    ######################################################
    # 2d histogram of radial velocity v radius v cell mass
    # saved to RDXXXX_Rvel_radius_4phase_mass.png
    ######################################################


    FourPanelHist2d(
        x_data=[radius, cold_radius, warm_radius, hot_radius],
        x_units="kpc", x_label="Radius (kpc)",
        y_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        y_units="kpc/Myr", y_label="Radial Velocity (kpc/Myr)",
        z_data=[cell_mass, cold_cell_mass, warm_cell_mass, hot_cell_mass],
        z_units="Msun", z_label=r"Cell Mass ($M_{\odot}$)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Rvel_radius_4phase_mass.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        cmap="viridis"
    )

    ######################################################
    # 2d histogram of tangential velocity v radial velocity v temperature
    # saved to RDXXXX_Tvel_Rvel_4phase_temp.png
    ######################################################


    FourPanelHist2d(
        x_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        x_units="kpc/Myr", x_label="Radial Velocity (kpc/Myr)",
        y_data=[Tvel, cold_Tvel, warm_Tvel, hot_Tvel],
        y_units="kpc/Myr", y_label="Tangential Velocity (kpc/Myr)",
        z_data=[temperature, cold_temperature, warm_temperature, hot_temperature],
        z_units="K", z_label="Temperature (K)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Tvel_Rvel_4phase_temp.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        plot_one_to_one=True,
        cmap="plasma"
    ) 

    ######################################################
    # 2d histogram of tangential velocity v radial velocity v cell_mass
    # saved to RDXXXX_Tvel_Rvel_4phase_mass.png
    ######################################################


    FourPanelHist2d(
        x_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        x_units="kpc/Myr", x_label="Radial Velocity (kpc/Myr)",
        y_data=[Tvel, cold_Tvel, warm_Tvel, hot_Tvel],
        y_units="kpc/Myr", y_label="Tangential Velocity (kpc/Myr)",
        z_data=[cell_mass, cold_cell_mass, warm_cell_mass, hot_cell_mass],
        z_units="Msun", z_label=r"Cell Mass ($M_{\odot}$)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Tvel_Rvel_4phase_mass.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        plot_one_to_one=True,
        cmap="viridis"
    )

    ######################################################
    # 2d histogram of radial velocity v radius v metallicity
    # saved to RDXXXX_Rvel_radius_4phase_metals.png
    ######################################################


    FourPanelHist2d(
        x_data=[radius, cold_radius, warm_radius, hot_radius],
        x_units="kpc", x_label="Radius (kpc)",
        y_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        y_units="kpc/Myr", y_label="Radial Velocity (kpc/Myr)",
        z_data=[metallicity, cold_metallicity, warm_metallicity, hot_metallicity],
        z_units="Zsun", z_label=r"Metallicity ($Z/Z_{\odot}$)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Rvel_radius_4phase_metals.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        cmap="dusk"
    )

    ######################################################
    # 2d histogram of tangential velocity v radial velocity v metallicity
    # saved to RDXXXX_Tvel_Rvel_4phase_metals.png
    ######################################################


    FourPanelHist2d(
        x_data=[Rvel, cold_Rvel, warm_Rvel, hot_Rvel],
        x_units="kpc/Myr", x_label="Radial Velocity (kpc/Myr)",
        y_data=[Tvel, cold_Tvel, warm_Tvel, hot_Tvel],
        y_units="kpc/Myr", y_label="Tangential Velocity (kpc/Myr)",
        z_data=[metallicity, cold_metallicity, warm_metallicity, hot_metallicity],
        z_units="Zsun", z_label=r"Metallicity ($Z/Z_{\odot}$)",
        log_z=True, 
        save_to=f"{getOutputDir()}/{str(ds)}_Tvel_Rvel_4phase_metals.png",
        title="Tempest ($z=0$)",
        annotations=["All", "Cold", "Warm", "Hot"],
        plot_one_to_one=True,
        cmap="dusk"
    )

    # gas mass calculations
    cgm_mass = getGasMass(cell_mass)
    cold_gas_mass = getGasMass(cold_cell_mass)
    warm_gas_mass = getGasMass(warm_cell_mass)
    hot_gas_mass = getGasMass(hot_cell_mass)

    # accretion rate calculations
    in_rate, out_rate = getInOutRate(Rvel, cell_mass, radius)
    cold_in_rate, cold_out_rate = getInOutRate(cold_Rvel, cold_cell_mass, cold_radius)
    warm_in_rate, warm_out_rate = getInOutRate(warm_Rvel, warm_cell_mass, warm_radius)
    hot_in_rate, hot_out_rate = getInOutRate(hot_Rvel, hot_cell_mass, hot_radius)

    printReport(
        cgm_mass,
        cold_gas_mass,
        warm_gas_mass,
        hot_gas_mass,
        in_rate, out_rate,
        cold_in_rate, cold_out_rate,
        warm_in_rate, warm_out_rate,
        hot_in_rate, hot_out_rate,
        save_to="stats.out"
    )

    Pipeline.run(parallel=True)

