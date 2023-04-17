#!/usr/bin/env python3

#from ndustria import AddTask
from ..Box import Box
import yt, trident, os
import numpy as np
from ..utils import findEnzoOuts, getDataBoxAndRegion, getOutputDir, getTempDir
from ndustria import AddTask

line_list = ['H', 'C', 'N', 'O', 'Mg']
field = "density"


#@AddTask
def create_dataset(enzo_dataset, box_spec_file, n_sightlines):

    ds, box, region = getDataBoxAndRegion(enzo_dataset, box_spec_file)

    sightlines = create_sightlines(box, n_sightlines)

    # set limits on colorbar with min and max values
    zmin, zmax = region.quantities.extrema(field)

    # make a plot to show where the sightlines will appear
    proj = yt.ProjectionPlot(ds, 'z', field, 
        center=box.center, 
        width=box.length, 
        weight_field=field,
        data_source=region)
    proj.annotate_timestamp(redshift=True)

    for line in sightlines:
        proj.annotate_marker(line[0], coord_system="data")

    proj.set_zlim(field, zmin=zmin, zmax=zmax)
    proj.set_cmap(field, 'viridis')
    proj.set_axes_unit('kpc')

    proj.save(f"{getOutputDir()}/{str(ds)}_sightlines.png")


    for i,line in enumerate(sightlines):
        make_spectra(ds, i, line, line_list)

# Note to self: This assumes we're projecting our sightlines along z
# Eventually might have to transform the result onto arbitrary axis
def create_sightlines(box, N):

    L = box.length
    root = int(np.sqrt(N))
    d = L / (root+1)

    sightlines = np.zeros((N, 2, 3))

    for i in range(root):
        for j in range(root):

            sightlines[i*root+j][0] = box.lowerLeft()
            sightlines[i*root+j][1] = box.lowerLeft()

            sightlines[i*root+j][0] += [d*(j+1), d*(i+1), 0.]
            sightlines[i*root+j][1] += [d*(j+1), d*(i+1), 1.]

    return sightlines

#@AddTask()
def make_spectra(ds, index, line, line_list):

    ray = trident.make_simple_ray(ds,
        line[0],
        line[1],
        data_filename="ray.h5",
        lines=line_list)

    sg = trident.SpectrumGenerator('COS-G130M')
    sg.make_spectrum(ray, lines=line_list)

    sg.add_qso_spectrum()
    #sg.add_gaussian_noise(30)

    output_file = f'{getOutputDir()}/spec_raw_{index}.txt'
    sg.save_spectrum(output_file)
    sg.plot_spectrum(f"{getOutputDir()}/{str(ds)}_spectra_{index}.png")

    return output_file


if __name__ == "__main__":
    
    enzoOuts = findEnzoOuts()
    boxSpec = "Tempest_box_at_z_0.csv"
    n_sightlines = 4
    create_dataset(enzoOuts, boxSpec, n_sightlines)