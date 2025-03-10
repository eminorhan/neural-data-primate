import os
import argparse
import numpy as np
from pynwb import NWBHDF5IO
from datasets import Dataset


def find_nwb_files(root_dir):
    """
    Crawls through a directory (including subdirectories), finds all files
    that end with ".nwb", and returns the full paths of all the found files in a list.

    Args:
        root_dir: The root directory to start the search from.

    Returns:
        A list of full paths to the found .nwb files, or an empty list if
        no files are found or if the root directory is invalid.
        Returns None if root_dir is not a valid directory.
    """

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return None

    nwb_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith("_behavior+ecephys.nwb"):
                full_path = os.path.join(dirpath, filename)
                nwb_files.append(full_path)
    return nwb_files


def get_args_parser():
    parser = argparse.ArgumentParser('Consolidate data in multiple files into a single file', add_help=False)
    parser.add_argument('--data_dir',default="",type=str, help='Data directory')
    return parser


if __name__ == '__main__':

    args = get_args_parser()
    args = args.parse_args()
    print(args)

    # get all .nwb files in the sorted folder
    nwb_files = find_nwb_files(args.data_dir)
    print(f"Files: {nwb_files}")
    print(f"Total number of files: {len(nwb_files)}")

    # lists to store results for each session
    spike_counts_list, identifier_list = [], []

    for file_path in sorted(nwb_files):
        print(f"Processing file: {file_path}")
        with NWBHDF5IO(file_path, "r") as io:
            nwbfile = io.read()

            # we will save just spike activity for now
            units = nwbfile.processing['ecephys']['units'].to_dataframe()
            max_time = max([u.max() for u in units['spike_times']])
            spike_counts = np.vstack([np.histogram(row, bins=np.arange(0, max_time + 0.02, 0.02))[0] for row in units['spike_times']]).astype(np.uint8)  # spike count matrix (nxt: n is #channels, t is time bins)

            # file identifier
            identifier = nwbfile.identifier

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
    print(ds._estimate_nbytes())

    # push all data to hub
    ds.push_to_hub("eminorhan/neupane-entorhinal", num_shards=15, token=True)