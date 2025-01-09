import os
import h5py
import argparse
import numpy as np
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


def get_args_parser():
    parser = argparse.ArgumentParser('Consolidate data in multiple files into a single file', add_help=False)
    parser.add_argument('--data_dir',default="/home/emin/Documents/nwb/makin",type=str, help='Data directory')
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
    spike_counts_list, identifier_list = [], []

    for file_path in sorted(mat_files):
        # open the file
        with h5py.File(file_path, "r") as f:
            data = f['spikes']
            u, n = data.shape
            all_channels = []
            for i_n in range(n):
                spike_times = []
                for i_u in range(u):
                    group = f['spikes'][i_u, i_n]
                    obj = f[group][()]
                    if obj.ndim == 2:
                        spike_times.append(obj.flatten())
                if spike_times != []:
                    spike_times = np.concatenate(spike_times)
                all_channels.append(spike_times)

            max_time = max([-np.inf if isinstance(u, list) else u.max() for u in all_channels])
            min_time = min([np.inf if isinstance(u, list) else u.min() for u in all_channels])

            spike_counts = np.vstack([np.histogram(row, bins=np.arange(min_time, max_time + 0.02, 0.02))[0] for row in all_channels])  # spike count matrix (nxt: n is #channels, t is time bins)

            # file identifier
            identifier = os.path.splitext(os.path.basename(file_path))[0]

            # append sessions
            spike_counts_list.append(spike_counts)
            identifier_list.append(identifier)

            print(f"Spike count shape-max: {spike_counts.shape}, {spike_counts.max()}")

    def gen_data():
        for a, b in zip(spike_counts_list, identifier_list):
            yield {
                "spike_counts": a,
                "identifier": b,
                }

    ds = Dataset.from_generator(gen_data, writer_batch_size=1)

    # push all data to hub
    ds.push_to_hub("eminorhan/makin", token=True)