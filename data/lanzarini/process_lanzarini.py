import os
import math
import argparse
import numpy as np
import scipy.io
from datasets import Dataset


def find_mat_files(root_dir):
    """
    Crawls through a directory (including subdirectories), finds all files
    that end with ".mat" and returns the full paths of all the found files in a list.

    Args:
        root_dir: The root directory to start the search from.

    Returns:
        A list of full paths to the found .mat files, or an empty list if
        no files are found or if the root directory is invalid.
        Returns None if root_dir is not a valid directory.
    """

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return None

    mat_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".mat"):
                full_path = os.path.join(dirpath, filename)
                mat_files.append(full_path)
    return mat_files


def extract_subject_session_id(file_path):
    """
    Extracts subject and session identifier strings from a full file path.

    Args:
        file_path (str): The full file path.

    Returns:
        str: Subject identifier string.
        str: Session identifier string.
    """
    directory, filename = os.path.split(file_path)
    subdirectory = os.path.basename(directory)
    filename_without_extension, _ = os.path.splitext(filename)
    return f"{subdirectory}", f"{filename_without_extension}"


def process_mat_files(directory, num_channels=128, bin_size=0.02):
    """
    Processes .mat files in a directory, combines spike time data, and bins it.

    Args:
        directory (str): Path to the directory containing .mat files.
        bin_size (float): Size of the time bins in seconds.

    Returns:
        dict: A dictionary where keys are filenames (without .mat) and values are
              N-by-T numpy arrays representing spike counts in time bins.
    """

    spike_counts_list, identifier_list = [], []

    for filename in os.listdir(directory):
        if filename.endswith(".mat"):
            filepath = os.path.join(directory, filename)
            mat_data = scipy.io.loadmat(filepath)

            spike_data = []
            for i in range(num_channels):
                key = f'Spk_{i:03d}a_sh'
                if key in mat_data:
                    spike_data.append(mat_data[key][0])
                else:
                    print(f"Warning: Key {key} not found in {filename}")
                    spike_data.append(np.array([])) #append empty array if channel data is missing.

            # Find the maximum spike time to determine the number of bins
            max_time = 0
            for channel_spikes in spike_data:
                if channel_spikes.size > 0:
                    max_time = max(max_time, channel_spikes.max())

            num_bins = int(np.ceil(max_time / bin_size))
            binned_spikes = np.zeros((num_channels, num_bins), dtype=np.uint8)

            for channel_idx, channel_spikes in enumerate(spike_data):
                if channel_spikes.size > 0:
                    bin_indices = (channel_spikes / bin_size).astype(int)
                    bin_indices = bin_indices[bin_indices < num_bins] # Ensure indices are within bounds.
                    np.add.at(binned_spikes[channel_idx], bin_indices, 1)

            spike_counts_list.append(binned_spikes)
            identifier_list.append(os.path.splitext(filename)[0])

            print(f"Subject: {os.path.splitext(filename)[0]}; Spike count shape-max: {binned_spikes.shape}, {binned_spikes.max()}")

    def gen_data():
        for a, b in zip(spike_counts_list, identifier_list):
            yield {
                "spike_counts": a,
                "identifier": b,
                }

    ds = Dataset.from_generator(gen_data, writer_batch_size=1)

    # push all data to hub
    ds.push_to_hub("eminorhan/lanzarini", token=True)


def get_args_parser():
    parser = argparse.ArgumentParser('Consolidate data in multiple .mat files into a single dataset', add_help=False)
    parser.add_argument('--data_dir', default="data", type=str, help='Data directory')
    parser.add_argument('--num_channels', default=128, type=int, help='Number of channels in data')
    parser.add_argument('--bin_size', default=0.02, type=int, help='Bin size (ms)')

    return parser


if __name__ == '__main__':

    args = get_args_parser()
    args = args.parse_args()
    print(args)

    # get all .mat files in the sorted folder
    mat_files = find_mat_files(args.data_dir)
    print(f"Files: {mat_files}")
    print(f"Total number of files: {len(mat_files)}")

    # lists to store results for each session
    spike_counts_list, subject_list, session_list, segment_list = [], [], [], []

    # token counter
    n_tokens = 0

    for file_path in sorted(mat_files):
        print(f"Processing file: {file_path}")
        mat_data = scipy.io.loadmat(file_path)

        spike_data = []
        for i in range(args.num_channels):
            key = f'Spk_{i:03d}a_sh'
            if key in mat_data:
                spike_data.append(mat_data[key][0])
            else:
                print(f"Warning: Key {key} not found in {file_path}")
                spike_data.append(np.array([])) #append empty array if channel data is missing.

        # Find the maximum spike time to determine the number of bins
        max_time = 0
        for channel_spikes in spike_data:
            if channel_spikes.size > 0:
                max_time = max(max_time, channel_spikes.max())

        num_bins = int(np.ceil(max_time / args.bin_size))
        spike_counts = np.zeros((args.num_channels, num_bins), dtype=np.uint8)

        for channel_idx, channel_spikes in enumerate(spike_data):
            if channel_spikes.size > 0:
                bin_indices = (channel_spikes / args.bin_size).astype(int)
                bin_indices = bin_indices[bin_indices < num_bins] # Ensure indices are within bounds.
                np.add.at(spike_counts[channel_idx], bin_indices, 1)

        # subject, session identifiers
        subject_id, session_id = extract_subject_session_id(file_path)

        # token count of current session
        total_elements = np.prod(spike_counts.shape)

        # append sessions; if session data is large, divide spike_counts array into smaller chunks
        if total_elements > 10_000_000:
            n_channels, n_time_bins = spike_counts.shape
            num_segments = math.ceil(total_elements / 10_000_000)
            segment_size = math.ceil(n_time_bins / num_segments)
            print(f"Spike count dtype / shape / max: {spike_counts.dtype} / {spike_counts.shape} / {spike_counts.max()}. Dividing into {num_segments} smaller chunks ...")
            for i in range(num_segments):
                start_index = i * segment_size
                end_index = min((i + 1) * segment_size, n_time_bins)
                sub_array = spike_counts[:, start_index:end_index]
                spike_counts_list.append(sub_array)
                subject_list.append(subject_id)
                session_list.append(session_id)
                segment_list.append(f"segment_{i}")
                print(f"Divided into segment_{i} with shape / max: {sub_array.shape} / {sub_array.max()}")
                n_tokens += np.prod(sub_array.shape)
        else:
            spike_counts_list.append(spike_counts)
            subject_list.append(subject_id)
            session_list.append(session_id)
            segment_list.append("segment_0")  # default segment id
            print(f"Spike count dtype / shape / max: {spike_counts.dtype} / {spike_counts.shape} / {spike_counts.max()} (segment_0)")
            n_tokens += np.prod(spike_counts.shape)

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
    ds.push_to_hub("eminorhan/lanzarini", max_shard_size="1GB", token=True)