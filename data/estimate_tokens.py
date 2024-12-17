import numpy as np
from datasets import load_dataset, concatenate_datasets

def count_tokens_in_dataset(dataset, column_name):
    n_tok = 0
    for sample in dataset:
        sh = np.array(sample[column_name]).shape
        n_tok += np.prod(sh)
    return n_tok

n_tokens = 0

# willett
willett_column_name = "tx1"
willett_train = load_dataset("eminorhan/willett", split='train').select_columns([willett_column_name])
willett_test = load_dataset("eminorhan/willett", split='test').select_columns([willett_column_name])
willett_validation = load_dataset("eminorhan/willett", split='validation').select_columns([willett_column_name])
willett = concatenate_datasets([willett_train, willett_test, willett_validation])
n_tokens += count_tokens_in_dataset(willett, willett_column_name)
print("1")

# h1
h1_column_name = "spike_counts"
h1_incalib = load_dataset("eminorhan/h1", "in-calib", split='train').select_columns([h1_column_name])
h1_inminival = load_dataset("eminorhan/h1", "in-minival", split='train').select_columns([h1_column_name])
h1_outcalib = load_dataset("eminorhan/h1", "out-calib", split='train').select_columns([h1_column_name])
h1 = concatenate_datasets([h1_incalib, h1_inminival, h1_outcalib])
n_tokens += count_tokens_in_dataset(h1, h1_column_name)
print("2")

# # h2
h2_column_name = "spike_counts"
h2_incalib = load_dataset("eminorhan/h2", "in-calib", split='train').select_columns([h2_column_name])
h2_inminival = load_dataset("eminorhan/h2", "in-minival", split='train').select_columns([h2_column_name])
h2_outcalib = load_dataset("eminorhan/h2", "out-calib", split='train').select_columns([h2_column_name])
h2 = concatenate_datasets([h2_incalib, h2_inminival, h2_outcalib])
n_tokens += count_tokens_in_dataset(h2, h2_column_name)
print("3")

# m1-a
m1a_column_name = "spike_counts"
m1a_incalib = load_dataset("eminorhan/m1-a", "in-calib", split='train').select_columns([m1a_column_name])
m1a_inminival = load_dataset("eminorhan/m1-a", "in-minival", split='train').select_columns([m1a_column_name])
m1a_outcalib = load_dataset("eminorhan/m1-a", "out-calib", split='train').select_columns([m1a_column_name])
m1a = concatenate_datasets([m1a_incalib, m1a_inminival, m1a_outcalib])
n_tokens += count_tokens_in_dataset(m1a, m1a_column_name)
print("4")

# m1-b
m1b_column_name = "spike_counts"
m1b_incalib = load_dataset("eminorhan/m1-b", "in-calib", split='train').select_columns([m1b_column_name])
m1b_inminival = load_dataset("eminorhan/m1-b", "in-minival", split='train').select_columns([m1b_column_name])
m1b_outcalib = load_dataset("eminorhan/m1-b", "out-calib", split='train').select_columns([m1b_column_name])
m1b = concatenate_datasets([m1b_incalib, m1b_inminival, m1b_outcalib])
n_tokens += count_tokens_in_dataset(m1b, m1b_column_name)
print("5")

# m2
m2_column_name = "spike_counts"
m2_incalib = load_dataset("eminorhan/m2", "in-calib", split='train').select_columns([m2_column_name])
m2_inminival = load_dataset("eminorhan/m2", "in-minival", split='train').select_columns([m2_column_name])
m2_outcalib = load_dataset("eminorhan/m2", "out-calib", split='train').select_columns([m2_column_name])
m2 = concatenate_datasets([m2_incalib, m2_inminival, m2_outcalib])
n_tokens += count_tokens_in_dataset(m2, m2_column_name)
print("6")

# mc-maze
mc_maze_column_name = "spike_counts"
mc_maze = load_dataset("eminorhan/mc-maze", split='train').select_columns([mc_maze_column_name])
n_tokens += count_tokens_in_dataset(mc_maze, mc_maze_column_name)
print("7")

# mc-rtt
mc_rtt_column_name = "spike_counts"
mc_rtt = load_dataset("eminorhan/mc-rtt", split='train').select_columns([mc_rtt_column_name])
n_tokens += count_tokens_in_dataset(mc_rtt, mc_rtt_column_name)
print("8")

print(f"total number of tokens {n_tokens}")