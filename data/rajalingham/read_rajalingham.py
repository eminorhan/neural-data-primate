
import numpy as np
from scipy.io import loadmat
from datasets import Dataset


def read_mat_file(filepath):
    """
    Reads a .mat file and returns the reliable neural responses.

    Args:
        filepath (str): The path to the .mat file.

    Returns:
        dict: A dictionary where keys are variable names and values are NumPy arrays.
        Returns None and prints an error if the file cannot be read.
    """
    try:
        data = loadmat(filepath)
        return np.nan_to_num(data['neural_responses_reliable'][0,0][0])
    except Exception as e:
        print(f"Error reading .mat file: {e}")
        return None


def convert_mua_to_spikes(mua_matrix):
    """
    Convert MUA into spike counts (caution: not rigorous, ideally I should use raw voltage traces)

    Args:
        mua_matrix (numpy.ndarray): MUA matrix of shape (electrodes, trials, time_bins).

    Returns:
        numpy.ndarray: Concatenated binned spike count matrix of shape (electrodes, binned_time_bins * trials), dtype=uint8.
    """

    electrodes, trials, time_bins = mua_matrix.shape
    spike_matrix = np.zeros_like(mua_matrix, dtype=int)

    # calculate min/max response per electrode
    electrode_mins = np.zeros(electrodes)
    electrode_maxs = np.zeros(electrodes)
    for electrode_idx in range(electrodes):
        electrode_data = mua_matrix[electrode_idx, :, :].flatten()  # flatten across trials and time bins
        electrode_mins[electrode_idx] = np.min(electrode_data)
        electrode_maxs[electrode_idx] = np.max(electrode_data)

    # normalize responses using per-electrode min/max calculated above
    for electrode_idx in range(electrodes):
        trial_data = mua_matrix[electrode_idx, :, :]
        spike_matrix[electrode_idx, :, :] = np.round(10.0 * (trial_data - electrode_mins[electrode_idx]) / (electrode_maxs[electrode_idx] - electrode_mins[electrode_idx]))

    # concatenate trials
    concatenated_spikes = spike_matrix.reshape((electrodes, time_bins * trials))

    return concatenated_spikes.astype(np.uint8)


if __name__ == '__main__':

    data_mahler = read_mat_file('data/mahler/mahler_hand_dmfc_dataset_50ms.mat')
    data_perle = read_mat_file('data/perle/perle_hand_dmfc_dataset_50ms.mat')
    print(f"Loaded data files.")

    spike_count_mat_mahler = convert_mua_to_spikes(data_mahler)
    spike_count_mat_perle = convert_mua_to_spikes(data_perle)

    print(f"mahler spike count matrix shape/dtype: {spike_count_mat_mahler.shape}/{spike_count_mat_mahler.dtype}; max/min/median: {spike_count_mat_mahler.max()}/{spike_count_mat_mahler.min()}/{np.median(spike_count_mat_mahler)}")
    print(f"perle spike count matrix shape/dtype: {spike_count_mat_perle.shape}/{spike_count_mat_perle.dtype}; max/min/median: {spike_count_mat_perle.max()}/{spike_count_mat_perle.min()}/{np.median(spike_count_mat_perle)}")

    n_tokens = np.prod(spike_count_mat_mahler.shape) + np.prod(spike_count_mat_perle.shape)

    # # lists to store results for each session
    spike_counts_list = [spike_count_mat_mahler, spike_count_mat_perle]
    subject_list = ["Mahler", "Perle"]
    session_list = ["M_0", "P_0"]
    segment_list = ["segment_0", "segment_0"]

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
    ds.push_to_hub("eminorhan/rajalingham", max_shard_size="1GB", token=True)