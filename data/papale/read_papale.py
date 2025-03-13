
import h5py
import numpy as np
from datasets import Dataset


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
                data[k] = read_h5py_item(v)  # use helper function to handle different data types.
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
        return read_h5py_item(item.file[item])  # dereference the reference
    else:
        return item  # return the item if it's not a dataset, group, or reference.


def convert_mua_to_spikes(mua_matrix, bin_size_ms=10):
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

    # calculate min/max response per electrode
    electrode_mins = np.zeros(electrodes)
    electrode_maxs = np.zeros(electrodes)
    for electrode_idx in range(electrodes):
        electrode_data = mua_matrix[:, :, electrode_idx].flatten()  # flatten across trials
        electrode_mins[electrode_idx] = np.min(electrode_data)
        electrode_maxs[electrode_idx] = np.max(electrode_data)

    # normalize responses using per-electrode min/max calculated above
    for electrode_idx in range(electrodes):
        trial_data = mua_matrix[:, :, electrode_idx]
        spike_matrix[:, :, electrode_idx] = np.round((trial_data - electrode_mins[electrode_idx]) / (electrode_maxs[electrode_idx] - electrode_mins[electrode_idx]))

    # sum up spikes in each bin
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


if __name__ == '__main__':

    data_F = read_mat_file('THINGS_MUA_trials_F.mat')
    data_N = read_mat_file('THINGS_MUA_trials_N.mat')
    print(f"Loaded data files.")

    spike_count_mat_F = convert_mua_to_spikes(data_F["ALLMUA"])
    spike_count_mat_N = convert_mua_to_spikes(data_N["ALLMUA"])

    print(f"F spike count matrix shape/dtype: {spike_count_mat_F.shape}/{spike_count_mat_F.dtype}; max/min/median: {spike_count_mat_F.max()}/{spike_count_mat_F.min()}/{np.median(spike_count_mat_F)}")
    print(f"N spike count matrix shape/dtype: {spike_count_mat_N.shape}/{spike_count_mat_N.dtype}; max/min/median: {spike_count_mat_N.max()}/{spike_count_mat_N.min()}/{np.median(spike_count_mat_N)}")

    # lists to store results for each session
    spike_counts_list = [spike_count_mat_F, spike_count_mat_N]
    identifier_list = ["Monkey_F", "Monkey_N"]

    def gen_data():
        for a, b in zip(spike_counts_list, identifier_list):
            yield {
                "spike_counts": a,
                "identifier": b,
                }

    ds = Dataset.from_generator(gen_data, writer_batch_size=1)

    # push all data to hub
    ds.push_to_hub("eminorhan/papale", num_shards=2, token=True)