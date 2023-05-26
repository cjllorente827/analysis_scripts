#!/usr/bin/env python3

from analysis_scripts import *

import yt, trident, os
yt.set_log_level(50)
import numpy as np
from ndustria import Pipeline

##################################################################
# Special Task functions that save their results to the hard drive
# after they're done
##################################################################
from make_spectra import make_spectra
from create_sightlines import create_sightlines
from create_rays import create_rays
from create_ray_overlay import create_ray_overlay
from calculate_dwarv import calculate_dwarv



def run_pipeline(enzo_dataset, box_spec_file, n_sightlines):

    ds, box, region = getDataBoxAndRegion(enzo_dataset, box_spec_file)
    
    # set field parameters for accurate radial velocity calculation
    bulk_velocity = region.quantities.bulk_velocity()
    region.set_field_parameter("bulk_velocity", bulk_velocity)

    # This is necessary to keep yt from shitting its pants
    center_field_parameter = yt.YTArray(
        [
            ds.quan(box.center[0], "code_length"),
            ds.quan(box.center[1], "code_length"),
            ds.quan(box.center[2], "code_length")
        ]
    )
    region.set_field_parameter("center", center_field_parameter)

    sightlines = create_sightlines(box, n_sightlines)

    rays = []
    dwarvs = []
    for i,line in enumerate(sightlines):

        dwarvs.append( calculate_dwarv(ds, region, line))
        #rays.append( create_rays(ds, line, i) )

    create_ray_overlay(ds, box, region, sightlines, dwarvs)
    

    for i,line in enumerate(sightlines):
        make_spectra(ds, i, line)

    Pipeline.run(parallel=True)



if __name__ == "__main__":
    
    enzoOuts = findEnzoOuts()
    boxSpec = "Tempest_box_at_z_0.csv"
    n_sightlines = 100
    run_pipeline(enzoOuts, boxSpec, n_sightlines)