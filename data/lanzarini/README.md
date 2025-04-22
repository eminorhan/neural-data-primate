Lanzarini dataset. Dataset URL: https://osf.io/82jfr

Dataset downloaded manually from above URL.

To create the corresponding HF dataset, *e.g.*:
```python
python create_dataset.py --hf_repo_name "eminorhan/lanzarini" --token_count_limit 10_000_000 --bin_size 0.02
```
where `hf_repo_name` is the HF repo name where the processed data will be pushed to, `token_count_limit` is the maximum token count per dataset row (sessions with larger token counts than this will be split into smaller chunks), and `bin_size` is the bin size in seconds for aggregating spike counts (default: 20 ms).

Token count: 259,179,392 tokens

HF repo: https://huggingface.co/datasets/eminorhan/lanzarini
