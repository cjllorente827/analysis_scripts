
import numpy as np

from sklearn.preprocessing import StandardScaler as StandardScaler

from ndustria import AddTask

@AddTask()
def umap_preprocessing(raw_data, sub_sample_size=0, random_seed=42):

    # raw_data is a list of yt arrays
    # with fields as rows and cells as columns

    # UMAP wants a matrix that is n_cells by n_fields
    # so this will need to be transposed 

    # first strip the data of its yt baggage
    original_data = []
    for i, field in enumerate(raw_data):

        original_data.append(
                np.log10(field.v, where=[field.v != 0] )
            )

    # convert to numpy array
    original_data = np.array(original_data)

    # get a random sub-sample of the data 
    # if necessary
    if sub_sample_size != 0:
        rng = np.random.default_rng(random_seed)
        original_data = rng.choice(
            original_data, 
            size=sub_sample_size, 
            replace=False,
            axis=1, #select data by column here
        )

    # transpose the data to make it n_cells by n_fields
    matrix = original_data.T

    # scale the data to the order of std dev
    # with mean at zero
    # with each value = (x - u)/s
    # x = original value
    # u = mean
    # s = std dev
    data_scaler = StandardScaler()
    scaled_data = data_scaler.fit_transform(matrix)

    return scaled_data, original_data

@AddTask()
def print_data(data):

    print(data)

    return "file.out"
