Wojcik dataset. Dataset URL: https://doi.org/10.5061/dryad.c2fqz61kb

Dataset downloaded manually from above URL.

To create the corresponding HF dataset, *e.g.*:
```python
python create_dataset.py --hf_repo_name "eminorhan/wojcik" --token_count_limit 10_000_000 --bin_size 20
```
where `hf_repo_name` is the HF repo name where the processed data will be pushed to, `token_count_limit` is the maximum token count per dataset row (sessions with larger token counts than this will be split into smaller chunks).

Token count: 422,724,515 tokens

HF repo: https://huggingface.co/datasets/eminorhan/wojcik
