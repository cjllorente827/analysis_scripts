import os, re
from .Box import Box
import yt
import numpy as np

from ndustria import AddTask

CMAPS = {
    "density" : "viridis",
    "temperature" : "plasma",
    "entropy" : "cividis",
    'radial_velocity' : "coolwarm",
    "O_p5_number_density" : "magma",
    "O_p5_ion_fraction" : "bwr",
}

def ensureDirExists(path):

    if(not os.path.exists(path)):
        os.mkdir(path)


def findEnzoOuts():

    cwd = os.getcwd()
    print(f"Looking for Enzo outputs in {cwd}")
    pattern = re.compile(f'[DR]D[0-9][0-9][0-9][0-9]')

    all_folders =  os.listdir( cwd )
    matched_files = []

    for f in all_folders:
        match  = pattern.match(f)
        if match != None:
            fname = match.group()
            full_path = os.path.join(cwd, fname, fname)
            matched_files.append(full_path)

    if len(matched_files) == 1:
        return matched_files[0]
    
    return matched_files

def getDataBoxAndRegion(enzo_dataset, box_spec_file):

    """Convenience function that takes the filepaths of an enzo dataset and
    and Box specifier and returns a YTDataset and YTRegion for each on
    respectively. Also sets field parameters to keep YT happy
    
    Arguments:
    enzo_dataset -- Filepath to a single enzo dataset
    box_spec_file -- Filepath to a Box specifier
    """

    ds = yt.load(enzo_dataset)

    box = Box(box_spec_file)

    LL = box.lowerLeft()
    UR = box.upperRight()

    region = ds.r[
        LL[0]:UR[0],
        LL[1]:UR[1],
        LL[2]:UR[2],
    ]

    # This is necessary to keep yt from shitting its pants
    center_field_parameter = yt.YTArray(
        [
            ds.quan(box.center[0], "code_length"),
            ds.quan(box.center[1], "code_length"),
            ds.quan(box.center[2], "code_length")
        ]
    )
    region.set_field_parameter("center", center_field_parameter)


    return ds, box, region


def getOutputDir():

    if "ANALYSIS_OUT" not in os.environ:
        return f"{os.path.expanduser('~/analysis_scripts/output')}"
    else:
        return os.path.expanduser(os.environ["ANALYSIS_OUT"])
    
def getTempDir():

    if "ANALYSIS_TEMP" not in os.environ:
        return f"{os.path.expanduser('~/analysis_scripts/temp')}"
    else:
        return os.path.expanduser(os.environ["ANALYSIS_TEMP"])


# Simply returns the data of the given field within the given region
# and stores it away for future use
@AddTask()
def getFieldData(region, field):

    data = region[field]

    return data