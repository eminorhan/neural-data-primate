import math
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

    return concatenated_spikes.T  # transposed so the shape is (n, t) where n is the unit count, t is time bins


if __name__ == '__main__':

    # lists to store results for each session
    spike_counts_list, subject_list, session_list, segment_list = [], [], [], []

    # token counter
    n_tokens = 0

    data_F = read_mat_file('THINGS_MUA_trials_F.mat')
    data_N = read_mat_file('THINGS_MUA_trials_N.mat')
    print(f"Loaded data files.")


    # ====== monkey F ======
    spike_counts_F = convert_mua_to_spikes(data_F["ALLMUA"])
    n_tokens_F = np.prod(spike_counts_F.shape)

    # append sessions; if session data is large, divide spike_counts array into smaller chunks
    if n_tokens_F > 10_000_000:
        n_channels, n_time_bins = spike_counts_F.shape
        num_segments = math.ceil(n_tokens_F / 10_000_000)
        segment_size = math.ceil(n_time_bins / num_segments)
        print(f"Spike count shape / max: {spike_counts_F.shape} / {spike_counts_F.max()}. Dividing into {num_segments} smaller chunks ...")
        for i in range(num_segments):
            start_index = i * segment_size
            end_index = min((i + 1) * segment_size, n_time_bins)
            sub_array = spike_counts_F[:, start_index:end_index]
            spike_counts_list.append(sub_array)
            subject_list.append("monkey_F")
            session_list.append("F_0")
            segment_list.append(f"segment_{i}")
            print(f"Divided into segment_{i} with shape / max: {sub_array.shape} / {sub_array.max()}")
            n_tokens += np.prod(sub_array.shape)
    else:
        spike_counts_list.append(spike_counts_F)
        subject_list.append("monkey_F")
        session_list.append("F_0")
        segment_list.append("segment_0")  # default segment id
        print(f"Spike count shape / max: {spike_counts_F.shape} / {spike_counts_F.max()} (segment_0)")
        n_tokens += np.prod(spike_counts_F.shape)


    # ====== monkey N ======
    spike_counts_N = convert_mua_to_spikes(data_N["ALLMUA"])
    n_tokens_N = np.prod(spike_counts_N.shape)

    # append sessions; if session data is large, divide spike_counts array into smaller chunks
    if n_tokens_N > 10_000_000:
        n_channels, n_time_bins = spike_counts_N.shape
        num_segments = math.ceil(n_tokens_N / 10_000_000)
        segment_size = math.ceil(n_time_bins / num_segments)
        print(f"Spike count shape / max: {spike_counts_N.shape} / {spike_counts_N.max()}. Dividing into {num_segments} smaller chunks ...")
        for i in range(num_segments):
            start_index = i * segment_size
            end_index = min((i + 1) * segment_size, n_time_bins)
            sub_array = spike_counts_N[:, start_index:end_index]
            spike_counts_list.append(sub_array)
            subject_list.append("monkey_N")
            session_list.append("N_0")
            segment_list.append(f"segment_{i}")
            print(f"Divided into segment_{i} with shape / max: {sub_array.shape} / {sub_array.max()}")
            n_tokens += np.prod(sub_array.shape)
    else:
        spike_counts_list.append(spike_counts_N)
        subject_list.append("monkey_N")
        session_list.append("N_0")
        segment_list.append("segment_0")  # default segment id
        print(f"Spike count shape / max: {spike_counts_N.shape} / {spike_counts_N.max()} (segment_0)")
        n_tokens += np.prod(spike_counts_N.shape)

    def gen_data():
        for a, b, c, d in zip(spike_counts_list, subject_list, session_list, segment_list):
            yield {
                "spike_counts": a,
                "subject_id": b,
                "session_id": c,
                "segment_id": d
                }
            
    ds = Dataset.from_generator(gen_data, writer_batch_size=1)
    print(f"Number of tokens in dataset: {n_tokens} tokens")
    print(f"Number of rows in dataset: {len(ds)}")

    # push all data to hub 
    ds.push_to_hub("eminorhan/papale", max_shard_size="1GB", token=True)