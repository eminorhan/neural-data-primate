import h5py
import numpy as np

with h5py.File('indy_20160407_02.mat', 'r') as file:
    dataset = file['spikes']  # Access the dataset named "spikes"
    
    # Convert the dataset to a numpy array
    data_array = np.array(dataset)
      
# data = read_hdf5_with_references('indy_20160407_02.mat','spikes')
# # data = np.array(data) # For converting to a NumPy array
