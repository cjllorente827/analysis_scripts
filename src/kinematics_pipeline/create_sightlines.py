# Note to self: This assumes we're projecting our sightlines along z
# Eventually might have to transform the result onto arbitrary axis

import numpy as np
from ndustria import AddTask

@AddTask()
def create_sightlines(box, N):
    print("Stage 1: Creating sightlines...")

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
    
    
    print("Finished creating sightlines")

    return sightlines