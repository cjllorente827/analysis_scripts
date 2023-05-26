
import yt
from analysis_scripts import getOutputDir
from ndustria import AddView

@AddView()
def create_ray_overlay(ds, box, region, sightlines, dwarvs):
    print("Stage 2: Creating overlay...")

    field = "radial_velocity"

    # make a plot to show where the sightlines will appear
    proj = yt.ProjectionPlot(ds, 'z', field, 
        center=region.field_parameters["center"], 
        width=box.length, 
        weight_field="density",
        data_source=region)
    proj.annotate_timestamp(redshift=True)

    for dwarv, line in zip(dwarvs, sightlines):

        if dwarv.value > 10:
            proj.annotate_marker(line[0], coord_system="data", color="red")
        elif dwarv.value < -10:
            proj.annotate_marker(line[0], coord_system="data", color="blue")
        else:
            proj.annotate_marker(line[0], coord_system="data", color="black")



    #print("Calculating limits...")
    # set limits on colorbar with min and max values
    #zmin, zmax = region.quantities.extrema(field)
    #print("Done.")

    #proj.set_zlim(field, zmin=zmin, zmax=zmax)
    proj.set_unit(field, 'km/s')
    proj.set_cmap(field, 'coolwarm')
    proj.set_log(field, False)
    proj.set_axes_unit('kpc')

    image_file = f"{getOutputDir()}/{str(ds)}_sightlines.png"
    proj.save(image_file)

    print("Finished overlay.")
