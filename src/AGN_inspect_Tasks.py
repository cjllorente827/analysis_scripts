import h5py, re, os
from ndustria import AddTask
import yt

class AGNParticleData:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.z = 0

        self.mass = 0

        self.Edot = -1

        self.creation_time = -1

        self.current_time = -1
        self.current_redshift = -1

        self.jetPhi = 0
        self.jetTheta = 0

        self.coolingRadius = -1
        self.feedbackRadius = -1
        self.feedbackEfficiency = -1


@AddTask()
def getAllAGNData(enzo_out):

    # Using yt to get simulation parameters and calculate units
    ds = yt.load(enzo_out)
    allFiles = getAllFiles(enzo_out)

    for f in allFiles:

        allGrids = getAllGrids(f)
        for grid in allGrids:

            try:
                AP = grid["ActiveParticles"]
                AGN = AP["AGNParticle"]
            except KeyError as err:
                continue

            data = AGNParticleData()
            data.x = float(AGN['particle_position_x'][0][0])
            data.y = float(AGN['particle_position_y'][0][0])
            data.z = float(AGN['particle_position_z'][0][0])

            data.mass = ds.quan(float(AGN['particle_mass'][0]), "code_mass").to("Msun")
            data.Edot = ds.quan(float(AGN['Edot'][0]), "code_mass * code_length**2 / code_time**3").to("erg/s")


            data.current_redshift = ds.current_redshift
            data.current_time = ds.current_time.to('Gyr')

            data.creation_time = ds.quan(float(AGN['creation_time'][0]), "code_time").to("Gyr")

            data.coolingRadius = float(AGN['CoolingRadius'][0])
            data.feedbackRadius = float(AGN['FeedbackRadius'][0])
            data.feedbackEfficiency = float(AGN['FeedbackEfficiency'][0])

            return data
            
    return ""
# end getAllAGNData






# returns a list of all grids contained in a given Enzo HDF5 file
def getAllGrids(hdf5_filename):

    with h5py.File(hdf5_filename, 'r') as h5file:

        grids = list(h5file.keys())
        grids.remove('Metadata')


        for grid in grids:

            yield h5file[grid]
        
# end getAllGrids


def getAllFiles(enzo_out):

    enzo_out_dir, enzo_out_name = os.path.split(enzo_out)

    pattern = re.compile(f'{enzo_out_name}.cpu[0-9][0-9][0-9][0-9]')

    all_files =  os.listdir( enzo_out_dir )

    matched_files = []

    for f in all_files:
        match  = pattern.match(f)
        if match != None:
            fname = match.group()
            full_path = os.path.join(enzo_out_dir, fname)
            matched_files.append(full_path)

    return matched_files