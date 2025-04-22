H1 dataset. Dataset URL: https://dandiarchive.org/dandiset/000954

To download the data and create the corresponding HF dataset, *e.g.*:
```python
mkdir data && cd data
dandi download DANDI:000954
python create_dataset.py --hf_repo_name "eminorhan/h1" --token_count_limit 10_000_000 --bin_size 0.02
```
where `hf_repo_name` is the HF datasets repository name where the processed data will be pushed to, `token_count_limit` is the maximum token count per dataset row (sessions with larger token counts than this will be split into smaller chunks), and `bin_size` is the bin size in seconds for aggregating spike counts (default: 20 ms).

Token count: 33,686,576

HF repo: https://huggingface.co/datasets/eminorhan/h1