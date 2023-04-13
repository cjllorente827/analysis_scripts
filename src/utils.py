import os, re

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