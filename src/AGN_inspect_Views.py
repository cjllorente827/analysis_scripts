from ndustria import AddView
# from AGN_inspect_Tasks import *

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm as colormap
matplotlib.rcParams.update({'font.size': 16})
import numpy as np

from .utils import getOutputDir

USE_DARK = False

if USE_DARK:
    plt.style.use('dark_background')


@AddView(root_only=True)
def AGNFullView(allData):
    
    fig = plt.figure(figsize=(19.3,10.6))
    plt.suptitle("AGN Particle Data")
    grid = plt.GridSpec(4, 2, 
                        left=0.05, right=0.95, top=0.95, bottom=0.05,
                        wspace=0.25, hspace=0.5)

    position_xy = fig.add_subplot(grid[0:2,0])
    position_yz = fig.add_subplot(grid[2:4,0])

    info_table = fig.add_subplot(grid[0,1])
    info_table.axis('off')
    mass_over_time = fig.add_subplot(grid[1,1])
    Edot_over_time = fig.add_subplot(grid[2,1])
    acc_over_time = fig.add_subplot(grid[3,1])


    redshift = np.ones(len(allData))*-1
    masses = redshift.copy()
    edots = redshift.copy()

    x = redshift.copy()
    y = redshift.copy()
    z = redshift.copy()

    for i, data in enumerate(allData):

        if data == "": continue

        x[i] = data.x
        y[i] = data.y
        z[i] = data.z

        redshift[i] = data.current_redshift

        masses[i] = data.mass

        edots[i] = data.Edot
    # end for     

    # throw away null values
    x = x[redshift != -1]
    y = y[redshift != -1]
    z = z[redshift != -1]

    masses = masses[redshift != -1]

    edots = edots[redshift != -1]

    redshift = redshift[redshift != -1]

    jet = colormap.get_cmap('jet', len(redshift))

    redshift_normed = redshift / np.max(redshift)
    colors = [jet(n) for n in redshift_normed]


    position_xy.scatter(x, y, marker='o', c=colors)
    position_xy.set_xlabel("x")
    position_xy.set_ylabel("y")
    position_xy.set_xlim(0, 1)
    position_xy.set_ylim(0, 1)


    position_yz.scatter(z, y, marker='o', c=colors)
    position_yz.set_xlabel("z")
    position_yz.set_ylabel("y")
    position_yz.set_xlim(0, 1)
    position_yz.set_ylim(0, 1)

    # populate the table data
    lastData = allData[-1]
    table_data = [
        ["Creation Time", lastData.creation_time],
        ["Feedback Efficiency", lastData.feedbackEfficiency],
        ["Feedback Radius", lastData.feedbackRadius],
        ["Cooling Radius", lastData.coolingRadius],
    ]

    cell_colors = [
        ["black", "black"],
        ["black", "black"],
        ["black", "black"],
        ["black", "black"],
    ] if USE_DARK else None

    table = info_table.table(
        cellText=table_data,
        cellColours=cell_colors,
        cellLoc="center",
        loc='center'
    )

    table.scale(1, 2)

    # print(redshift)
    # print(masses)
    mass_over_time.scatter(redshift, masses)
    mass_over_time.invert_xaxis()
    mass_over_time.set_ylabel("$M_{BH}$ (M$_{\odot}$)")
    mass_over_time.set_xlabel("Redshift")

    Edot_over_time.scatter(redshift, edots, c=colors)
    Edot_over_time.invert_xaxis()
    Edot_over_time.set_ylabel("$\dot E$ (erg/s)")
    Edot_over_time.set_xlabel("Redshift")


    #plt.tight_layout()
    plt.savefig(f"{getOutputDir()}/AGN_inspect.png")

