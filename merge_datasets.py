from datasets import concatenate_datasets, load_dataset, DatasetDict


def concatenate_hf_datasets_and_push(repo_list, new_repo_name):
    """
    Concatenates Hugging Face datasets from a list of repositories and pushes to the Hugging Face Hub.
    Adds a 'source_dataset' column to each component dataset, using only the name after the backslash.

    Args:
        repo_list (list): A list of Hugging Face dataset repository names.
        new_repo_name (str): The name for the new concatenated dataset repository.
    """

    ds_list = []

    for repo_name in repo_list:
        ds = load_dataset(repo_name, split="train", download_mode="force_redownload")
        source_name = repo_name.split("/")[-1] # Extract the name after the last backslash

        ds = ds.add_column("source_dataset", [source_name] * len(ds))

        ds_list.append(ds)
        print(f"Dataset {repo_name} has been added.")

    # concatenate component datasets
    ds = concatenate_datasets(ds_list)
    ds = ds.train_test_split(test_size=0.01, shuffle=True)

    # push to hub
    ds.push_to_hub(new_repo_name, max_shard_size="1GB", token=True)
    print(f"Concatenated dataset pushed to {new_repo_name} on the Hugging Face Hub. Train / test len: {len(ds["train"])} / {len(ds["test"])}")


if __name__ == '__main__':

    # list of component dataset repositories to be concatenated
    repo_list = [
        "eminorhan/xiao", "eminorhan/neupane-ppc", "eminorhan/willett", "eminorhan/churchland", "eminorhan/neupane-entorhinal", 
        "eminorhan/kim", "eminorhan/even-chen", "eminorhan/papale", "eminorhan/perich", "eminorhan/wojcik", "eminorhan/makin", 
        "eminorhan/h2", "eminorhan/lanzarini", "eminorhan/athalye", "eminorhan/m1-a", "eminorhan/m1-b", "eminorhan/h1", "eminorhan/moore",
        "eminorhan/temmar", "eminorhan/rajalingham", "eminorhan/dmfc-rsg", "eminorhan/m2", "eminorhan/area2-bump" 
    ]
    new_repo_name = "neural-bench-primate"

    concatenate_hf_datasets_and_push(repo_list, new_repo_name)