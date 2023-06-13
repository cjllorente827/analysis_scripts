
import umap
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm, Normalize

from ndustria import AddTask

@AddTask()
def do_umap(data,
        n_neighbors=15,
        min_dist=0.1,
    ):

    scaled_data, original_data = data

    fit = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        )

    u = fit.fit_transform(scaled_data)

    return u, original_data

    


@AddTask(rerun=True)
def plot_umap_result(
    umap_result,
    title="Title",
    save_to="image.png",
    ):
    
    u, original_data = umap_result

    fig = plt.figure(figsize=(24,10))
    plt.suptitle(title, fontsize=18)
    grid = plt.GridSpec(2, 4, 
                        left=0.05, right=0.95, top=0.95, bottom=0.05,
                        wspace=0.15, hspace=0.2)

    T_axis = fig.add_subplot(grid[0,0])
    rho_axis = fig.add_subplot(grid[0,1])
    Z_axis = fig.add_subplot(grid[1,0])
    fO6_axis = fig.add_subplot(grid[1,1])
    fSi3_axis = fig.add_subplot(grid[0,2])
    fC4_axis = fig.add_subplot(grid[0,3])
    fH1_axis = fig.add_subplot(grid[1,2])
    fMg2_axis = fig.add_subplot(grid[1,3])
    
    T_plot = T_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[1],
               cmap="plasma",
               norm=LogNorm())
    
    rho_plot = rho_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[0],
               cmap="viridis",
               norm=LogNorm())
    
    Z_plot = Z_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[2],
               cmap="dusk",
               norm=LogNorm())
    
    fO6_plot = fO6_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[3],
               cmap="bwr",
               norm=Normalize())
    
    fSi3_plot = fSi3_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[4],
               cmap="bwr",
               norm=Normalize())
    
    fC4_plot = fC4_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[5],
               cmap="bwr",
               norm=Normalize())

    fH1_plot = fH1_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[6],
               cmap="bwr",
               norm=Normalize())
    
    fMg2_plot = fMg2_axis.scatter(u[:,0], u[:,1], 
               s=1,
               c=original_data[7],
               cmap="bwr",
               norm=Normalize())
    
    
    plt.colorbar(T_plot, ax=T_axis)
    #plt.colorbar(rho_plot, ax=rho_axis)
    plt.colorbar(Z_plot, ax=Z_axis)
    plt.colorbar(fO6_plot, ax=fO6_axis)
    plt.colorbar(fSi3_plot, ax=fSi3_axis)
    plt.colorbar(fC4_plot, ax=fC4_axis)
    plt.colorbar(fH1_plot, ax=fH1_axis)
    plt.colorbar(fMg2_plot, ax=fMg2_axis)
    plt.savefig(save_to)

    return save_to