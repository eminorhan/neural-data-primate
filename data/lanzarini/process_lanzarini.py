import os
import argparse
import numpy as np
import scipy.io
from datasets import Dataset


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
            binned_spikes = np.zeros((num_channels, num_bins), dtype=int)

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
    parser = argparse.ArgumentParser('Consolidate data in multiple .mat files into a single file', add_help=False)
    parser.add_argument('--data_dir', default="/home/emin/Documents/nwb/lanzarini", type=str, help='Data directory')
    parser.add_argument('--num_channels', default=128, type=int, help='Number of channels in data')
    parser.add_argument('--bin_size', default=0.02, type=int, help='Bin size (ms)')

    return parser


if __name__ == '__main__':

    args = get_args_parser()
    args = args.parse_args()
    print(args)
    process_mat_files(args.data_dir, num_channels=args.num_channels, bin_size=args.bin_size)