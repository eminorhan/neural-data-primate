Area2-bump dataset. Dataset URL: https://dandiarchive.org/dandiset/000127

To download the data and create the corresponding HF dataset, *e.g.*:
```python
mkdir data && cd data
dandi download DANDI:000127
python create_dataset.py --hf_repo_name "eminorhan/area2-bump" --token_count_limit 10_000_000 --bin_size 0.02
```
where `hf_repo_name` is the HF datasets repository name where the processed data will be pushed to, `token_count_limit` is the maximum token count per dataset row (sessions with larger token counts than this will be split into smaller chunks), and `bin_size` is the bin size in seconds for aggregating spike counts (default: 20 ms).

Token count: 7,394,070

HF repo: https://huggingface.co/datasets/eminorhan/area2-bump