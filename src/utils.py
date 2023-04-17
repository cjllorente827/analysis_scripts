import os, re
from .Box import Box
import yt

CMAPS = {
    "density" : "viridis",
    "temperature" : "plasma",
    "entropy" : "cividis",
    'radial_velocity' : "coolwarm"
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
    respectively.
    
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

    return ds, box, region


def getOutputDir():

    if "ANALYSIS_OUT" not in os.environ:
        return f"{os.path.expanduser('~/analysis_scripts/output')}"
    else:
        return os.environ["ANALYSIS_OUT"]
    
def getTempDir():

    if "ANALYSIS_TEMP" not in os.environ:
        return f"{os.path.expanduser('~/analysis_scripts/temp')}"
    else:
        return os.environ["ANALYSIS_TEMP"]