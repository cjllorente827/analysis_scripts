import yt
import numpy as np

from ndustria import AddTask

from analysis_scripts import CMAPS

@AddTask()
def ytProjectionPlot(
    ds, box, region, 
    save_to="image.png",
    title="",
    field=("gas", "density"),
    weight_field="density",
    method="integrate",
    zlims=None,    
    zlabel=None,
):

    if weight_field != None:
        plot = yt.ProjectionPlot(ds, 'z', field, 
            center=box.center, 
            width=box.length, 
            method=method,
            weight_field="density",
            data_source=region)
    else:
        plot = yt.ProjectionPlot(ds, 'z', field, 
            center=box.center, 
            width=box.length,
            method=method, 
            data_source=region)
    plot.annotate_timestamp(redshift=True)

    plot.set_cmap(field, CMAPS[field])

    if zlabel != None:
        plot.set_colorbar_label(field, zlabel)

    if zlims != None:
        plot.set_zlim(field, zlims[0], zlims[1])
        
    plot.annotate_title(title)

    plot.save(save_to)

    return save_to