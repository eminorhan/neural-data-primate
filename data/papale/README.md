Papale dataset. Dataset URL: https://gin.g-node.org/paolo_papale/TVSD

However, download speeds from the above URL are excrutiatingly slow in my experience (server side issue). So, to download the MUA data much faster through OneDrive links kindly provided by the author instead, please use:
```python
wget "https://herseninstituut-my.sharepoint.com/:u:/g/personal/papale_herseninstituut_knaw_nl/EZ5Z6MdGxbhLvk59Vn70pn8B-fk-4r5Tr5klhsfqEIm-Zw?e=kk7TUf&download=1"
wget "https://herseninstituut-my.sharepoint.com/:u:/g/personal/papale_herseninstituut_knaw_nl/EWuwwM-hXHlMi58rbgpTxwIBWxurgaf4EYfKk1Krf4k-Mw?e=ssyZSQ&download=1"
```
for data from monkey F and monkey N, respectively.

We do per-trial spike detection on the MUAs.

Token count: 775,618,560

HF repo: https://huggingface.co/datasets/eminorhan/papale
