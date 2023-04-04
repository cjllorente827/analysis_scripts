import os

CMAPS = {
    "density" : "viridis",
    "temperature" : "plasma",
    "entropy" : "cividis"
}

def ensureDirExists(path):

    if(not os.path.exists(path)):
        os.mkdir(path)