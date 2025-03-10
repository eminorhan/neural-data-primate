
import argparse
import h5py
import numpy as np


def read_mat_file(filepath):
    """
    Reads a .mat file (v7.3 or newer) and returns a dictionary of variables.

    Args:
        filepath (str): The path to the .mat file.

    Returns:
        dict: A dictionary where keys are variable names and values are NumPy arrays.
        Returns None and prints an error if the file cannot be read.
    """
    try:
        with h5py.File(filepath, 'r') as f:
            data = {}
            for k, v in f.items():
                data[k] = read_h5py_item(v) #Use helper function to handle different data types.
            return data
    except Exception as e:
        print(f"Error reading .mat file: {e}")
        return None


def read_h5py_item(item):
    """
    Helper function to recursively read h5py items and convert them to NumPy arrays.
    Handles datasets, groups, and references.
    """
    if isinstance(item, h5py.Dataset):
        return np.array(item)
    elif isinstance(item, h5py.Group):
        group_data = {}
        for k, v in item.items():
            group_data[k] = read_h5py_item(v)
        return group_data
    elif isinstance(item, h5py.Reference):
        return read_h5py_item(item.file[item]) #Dereference the reference
    else:
        return item #Return the item if it's not a dataset, group, or reference.


def detect_bin_and_concatenate_spikes(mua_matrix, bin_size_ms=20):
    """
    Convert MUA into spike counts (caution: not rigorous, ideally I should use raw voltage traces)

    Args:
        mua_matrix (numpy.ndarray): MUA matrix of shape (time_bins, trials, electrodes).
        bin_size_ms (int): Size of the time bins in milliseconds.

    Returns:
        numpy.ndarray: Concatenated binned spike count matrix of shape (binned_time_bins * trials, electrodes), dtype=uint8.
    """

    time_bins, trials, electrodes = mua_matrix.shape
    spike_matrix = np.zeros_like(mua_matrix, dtype=int)

    # Calculate thresholds per electrode
    electrode_mins = np.zeros(electrodes)
    electrode_maxs = np.zeros(electrodes)
    for electrode_idx in range(electrodes):
        electrode_data = mua_matrix[:, :, electrode_idx].flatten()  # Flatten across trials

        electrode_mins[electrode_idx] = np.min(electrode_data)
        electrode_maxs[electrode_idx] = np.max(electrode_data)

    # Detect spikes using per-electrode thresholds
    for electrode_idx in range(electrodes):
        for trial_idx in range(trials):
            trial_data = mua_matrix[:, trial_idx, electrode_idx]
            spike_matrix[:, trial_idx, electrode_idx] = np.round((trial_data - electrode_mins[electrode_idx]) / (electrode_maxs[electrode_idx] - electrode_mins[electrode_idx]))

    # Bin the spikes
    bin_size_samples = bin_size_ms
    binned_time_bins = time_bins // bin_size_samples

    binned_spike_counts = np.zeros((binned_time_bins, trials, electrodes), dtype=np.uint8)

    for bin_idx in range(binned_time_bins):
        start_sample = bin_idx * bin_size_samples
        end_sample = (bin_idx + 1) * bin_size_samples
        binned_spike_counts[bin_idx, :, :] = np.sum(spike_matrix[start_sample:end_sample, :, :], axis=0).astype(np.uint8)

    # Concatenate trials
    concatenated_spikes = binned_spike_counts.reshape((binned_time_bins * trials, electrodes))

    return concatenated_spikes


def get_args_parser():
    parser = argparse.ArgumentParser('Consolidate data in multiple files into a single file', add_help=False)
    parser.add_argument('--data_dir',default="",type=str, help='Data directory')
    return parser


if __name__ == '__main__':

    args = get_args_parser()
    args = args.parse_args()
    print(args)

    data_F = read_mat_file('THINGS_MUA_trials_F.mat')
    data_N = read_mat_file('THINGS_MUA_trials_N.mat')

    spike_count_mat_F = detect_bin_and_concatenate_spikes(data_F["ALLMUA"])
    spike_count_mat_N = detect_bin_and_concatenate_spikes(data_N["ALLMUA"])

    print(f"F spike count matrix shape: {spike_count_mat_F}")
    print(f"N spike count matrix shape: {spike_count_mat_N}")
