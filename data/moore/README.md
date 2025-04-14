Moore dataset. Dataset URL: https://dandiarchive.org/dandiset/001062

To download the data and create the corresponding HF dataset, *e.g.*:
```python
mkdir data && cd data
dandi download DANDI:001062
python create_kim.py --hf_repo_name "eminorhan/moore" --token_count_limit 10_000_000 --bin_size 0.02
```
where `hf_repo_name` is the HF repo name where the processed data will be pushed to, `token_count_limit` is the maximum token count per dataset row (sessions with larger token counts than this will be split into smaller chunks), and `bin_size` is bin size in seconds for calculating spike counts (default: 20 ms).

Token count: 30,643,839

HF repo: https://huggingface.co/datasets/eminorhan/moore
