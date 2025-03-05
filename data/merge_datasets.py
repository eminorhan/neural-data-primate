import datasets
from datasets import load_dataset, concatenate_datasets

def combine_and_push_datasets(dataset_names, new_dataset_name, new_dataset_repo, column_name="source_dataset"):
    """
    Combines multiple Hugging Face datasets into a single dataset, adds an identifier column,
    and pushes it to the Hugging Face Hub.

    Args:
        dataset_names (list): List of Hugging Face dataset repository names.
        new_dataset_name (str): Name of the new combined dataset.
        new_dataset_repo (str): The name of the repo to push the new dataset to, for example "myusername/combined-dataset".
        column_name (str, optional): Name of the column to add identifying the source dataset. Defaults to "source_dataset".
    """

    combined_dataset = None

    for dataset_name in dataset_names:
        try:
            # Load the dataset in streaming mode
            ds = load_dataset(dataset_name, streaming=True)
            # Take the first split for simplicity. You might need to handle multiple splits.
            split_name = list(ds.keys())[0]
            ds = ds[split_name]

            # Add an identifier column
            def add_source_column(example, dataset_name=dataset_name):
                example[column_name] = dataset_name
                return example

            ds = ds.map(add_source_column)

            # Convert streaming dataset to a normal dataset
            ds = datasets.Dataset.from_list(list(ds))

            if combined_dataset is None:
                combined_dataset = ds
            else:
                combined_dataset = concatenate_datasets([combined_dataset, ds])

            print(f"Successfully processed {dataset_name}")

        except Exception as e:
            print(f"Error processing {dataset_name}: {e}")

    if combined_dataset is not None:
        try:
            # Push the combined dataset to the Hugging Face Hub
            combined_dataset.push_to_hub(new_dataset_repo)
            print(f"Successfully pushed the combined dataset '{new_dataset_name}' to {new_dataset_repo}")
        except Exception as e:
            print(f"Error pushing the combined dataset: {e}")
    else:
        print("No datasets were successfully combined.")

# Example usage:
dataset_names = [
    "imdb",
    "rotten_tomatoes",
    "yelp_review_full",
]

new_dataset_name = "combined_sentiment_datasets"
new_dataset_repo = "your_username/combined_sentiment_datasets" # Replace with your username and repo name.

combine_and_push_datasets(dataset_names, new_dataset_name, new_dataset_repo)