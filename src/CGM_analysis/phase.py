import yt
from yt.data_objects.selection_objects.cut_region import YTCutRegion
import numpy as np

from ndustria import AddTask

@AddTask()
def ytPhaseDiagram(
    ds, box, region, 
    output_file,
    x_field=("gas", "density"), 
    y_field=("gas", "temperature"),
    z_field=("gas", "mass")):

    center = ds.arr(box.center, "code_length")

    region.set_field_parameter("center", center)

    if region.__class__ == YTCutRegion:
        region.base_object.set_field_parameter("center", center)

    plot = yt.PhasePlot(
        region,
        x_field, 
        y_field, 
        z_field,
        x_bins=256,
        y_bins=256,
        fractional=False
    )

    if x_field == "radius":
        plot.x_log = False
        plot.set_unit("radius", "kpc")

    if x_field == "radial_velocity":
        plot.x_log = False
        plot.set_unit("radial_velocity", "kpc/Myr")

    if y_field == "radial_velocity":
        plot.y_log = False
        plot.set_unit("radial_velocity", "kpc/Myr")
    
    if y_field == "tangential_velocity":
        plot.y_log = False
        plot.set_unit("tangential_velocity", "kpc/Myr")

    if z_field == ("gas", "mass"):
        plot.set_unit(("gas", "mass"), "Msun")

    plot.set_cmap(z_field, "viridis")
    plot.save(output_file)

    return output_file