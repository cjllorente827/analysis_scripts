from ndustria import AddTask
from analysis_scripts import getOutputDir, getTempDir
import trident

@AddTask()
def create_rays(ds, line, index, line_list = ['H', 'C', 'N', 'O', 'Mg']):

    ray_file = f"{getOutputDir()}/{str(ds)}_ray_{index}.h5"

    ray = trident.make_simple_ray(ds,
        line[0],
        line[1],
        data_filename=ray_file,
        lines=line_list)
    

    print(f"Wrote ray to {ray_file}")
    return ray