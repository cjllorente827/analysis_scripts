import yt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from ..utils import CMAPS

from ndustria import AddTask, AddView

plt.style.use("publication")

@AddView()
def plotHist2d(
    x, x_units, x_label,
    y, y_units, y_label,
    z, z_units, z_label,
    z_lim=[],
    save_to="image.png", 
    bins=128, 
    cmap="viridis",
    title="" 
):

    X = x.to(x_units) 
    Y = y.to(y_units) 
    Z = z.to(z_units) 

    # if the ratio of max to min is larger than 3 orders of magnitude
    # plot/bin this in logspace
    log_x = np.log10( np.abs(np.max(X)/np.min(X)) ) >= 3
    log_y = np.log10( np.abs(np.max(Y)/np.min(Y)) ) >= 3
    log_z = np.log10( np.abs(np.max(Z)/np.min(Z)) ) >= 3

    z_norm = None
    if log_z :
        if len(z_lim) > 0:
            z_norm = LogNorm(vmin=z_lim[0], vmax=z_lim[1])
        else:
            z_norm = LogNorm() 
    # end if log_z

    plt.hexbin(
        X,
        Y,
        C=Z,
        xscale='log' if log_x else 'linear',
        yscale='log' if log_y else 'linear',
        norm=z_norm,
        cmap=cmap,
        gridsize=bins,
        reduce_C_function=np.median,
    )

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.colorbar(label=z_label)
    plt.tight_layout()
    plt.savefig(save_to)
    plt.title(title)
    plt.clf()
    

@AddView()
def FourPanelHist2d(
    x_data=[], x_units="", x_label="x",
    y_data=[], y_units="", y_label="y",
    z_data=[], z_units="", z_label="z",
    log_x=False, log_y=False, log_z=False,
    save_to="image.png",
    cmap="viridis",
    bins=128,
    annotations=None,
    plot_one_to_one=False,
    title=""
):
    """ Creates a four panel plot with 2d histograms in each panel
    
    Arguments should be lists in the order:
    upper_left, upper_right, lower_left, lower_right

    or 

    1, 2,
    3, 4

    """

    fig = plt.figure(figsize=(12, 12))
    plt.suptitle(title)
    grid = plt.GridSpec(2, 2, 
                        left=0.075, right=0.99, top=0.95, bottom=0.05,
                        wspace=0.25, hspace=0.15)
    

    upper_left_plot = fig.add_subplot(grid[0,0])
    upper_right_plot = fig.add_subplot(grid[0,1])
    lower_left_plot = fig.add_subplot(grid[1,0])
    lower_right_plot = fig.add_subplot(grid[1,1])

    all_panels = [
        upper_left_plot,
        upper_right_plot,
        lower_left_plot,
        lower_right_plot
    ]

    all_plots = []

    # This kind of figure is explicitly for making comparisons of different
    # cuts of the same data, so all plot axes should have the same:
    # - labels
    # - units
    # - min and max
    # - scale

    xmin = 1e50
    xmax = -1e50

    ymin = 1e50
    ymax = -1e50

    zmin = 1e50
    zmax = -1e50

    for i, plot in enumerate(all_panels):
            
        X = x_data[i].to(x_units)
        Y = y_data[i].to(y_units)
        Z = z_data[i].to(z_units)

        xmin = min(xmin, X.min())
        xmax = max(xmax, X.max())

        ymin = min(ymin, Y.min())
        ymax = max(ymax, Y.max())

        zmin = min(zmin, Z.min())
        zmax = max(zmax, Z.max())

        new_plot = plot.hexbin(
            X,
            Y,
            C=Z,
            xscale="log" if log_x else "linear",
            yscale="log" if log_y else "linear",
            cmap=cmap,
            gridsize=bins,
            reduce_C_function=np.median,
        )

        if plot_one_to_one:
            plot.plot(X,X)

        all_plots.append(new_plot)

        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        
        if not annotations == None:
            plot.text( 
                0.85, 0.9, 
                annotations[i],
                transform=plot.transAxes
            )
    # end for i, plot
    
    for p in all_panels:
        p.set_xlim(xmin, xmax)
        p.set_ylim(ymin, ymax)

    norm = (
        LogNorm(vmin=zmin, vmax=zmax) 
        if log_z 
        else Normalize(vmin=zmin, vmax=zmax)
    )

    for p in all_plots:
        p.set_norm(norm)
        
    fig.colorbar(
        all_plots[0], 
        ax=all_panels, 
        label=z_label, 
        location="bottom",
        fraction=.025
    )

    plt.savefig(save_to)
    plt.clf()