<p align="left">
    <a href="https://huggingface.co/datasets/eminorhan/neural-bench-primate"><img alt="neural-bench-primate" src="https://img.shields.io/badge/HF_datasets-neural_bench_primate-blue"></a>
</p>

# primate ephys data

~34B uncompressed tokens of ephys data recorded from primates (tokens=units x time bins). Unless otherwise noted, the data consist of spike counts within 20 ms time bins recorded from each unit. 

The current component datasets and token counts per dataset are as follows:

| Dataset Name       | Tokens          | Sessions | Source                                                                            |
|--------------------|----------------:|---------:|-----------------------------------------------------------------------------------|
| Xiao               | 17,695,820,059  | 679      | [dandi:000628](https://dandiarchive.org/dandiset/000628)                           |
| Neupane (PPC)      | 7,899,849,087   | 10       | [dandi:001275](https://dandiarchive.org/dandiset/001275)                           |
| Willett            | 1,796,119,552   | 44       | [dryad:x69p8czpq](https://datadryad.org/stash/dataset/doi:10.5061/dryad.x69p8czpq) |
| Churchland         | 1,278,669,504   | 10       | [dandi:000070](https://dandiarchive.org/dandiset/000070)                           |
| Neupane (Entorhinal)| 911,393,376     | 15       | [dandi:000897](https://dandiarchive.org/dandiset/000897)                           |
| Kim                | 804,510,741     | 159      | [dandi:001357](https://dandiarchive.org/dandiset/001357)                           |
| Even-Chen          | 783,441,792     | 12       | [dandi:000121](https://dandiarchive.org/dandiset/000121)                           |
| Papale             | 775,618,560     | 2        | [g-node:TVSD](https://gin.g-node.org/paolo_papale/TVSD)                           |
| Perich             | 688,889,368     | 111      | [dandi:000688](https://dandiarchive.org/dandiset/000688)                           |
| Wojcik             | 422,724,515     | 50       | [dryad:c2fqz61kb](https://doi.org/10.5061/dryad.c2fqz61kb)                        |
| Makin              | 375,447,744     | 47       | [zenodo:3854034](https://zenodo.org/records/3854034)                              |
| H2                 | 297,332,736     | 47       | [dandi:000950](https://dandiarchive.org/dandiset/000950)                           |
| Lanzarini          | 259,179,392     | 10       | [osf:82jfr](https://osf.io/82jfr/)                                                |
| Athalye            | 101,984,317     | 13       | [dandi:000404](https://dandiarchive.org/dandiset/000404)                           |
| M1-A               | 45,410,816      | 11       | [dandi:000941](https://dandiarchive.org/dandiset/000941)                           |
| M1-B               | 43,809,344      | 12       | [dandi:001209](https://dandiarchive.org/dandiset/001209)                           |
| H1                 | 33,686,576      | 40       | [dandi:000954](https://dandiarchive.org/dandiset/000954)                           |
| Moore              | 30,643,839      | 1        | [dandi:001062](https://dandiarchive.org/dandiset/001062)                           |
| Temmar             | 27,388,320      | 12       | [dandi:001201](https://dandiarchive.org/dandiset/001201)                           |
| Rajalingham        | 14,923,100      | 2        | [zenodo:13952210](https://zenodo.org/records/13952210)                            |
| DMFC-rsg           | 14,003,818      | 2        | [dandi:000130](https://dandiarchive.org/dandiset/000130)                           |
| M2                 | 12,708,384      | 20       | [dandi:000953](https://dandiarchive.org/dandiset/000953)                           |
| Area2-bump         | 7,394,070       | 2        | [dandi:000127](https://dandiarchive.org/dandiset/000127)                           |

**Total number of tokens:** 34,320,949,010. 

The combined dataset can be accessed from [this](https://huggingface.co/datasets/eminorhan/neural-bench-primate) public HF repository. The combined dataset takes up about 6 GB when stored as `.parquet` files and roughly 34 GB when stored as memory-mapped `.arrow` files (see [this](https://stackoverflow.com/a/56481636) for an explanation of the differences between these file formats). The HF `datasets` library uses `.arrow` files for local caching, so you will need at least this much free disk space in order to be able to utilize it. 

## Creating the component datasets
`data` directory contains all the information needed to download and preprocess the individual component datasets and push them to the HF datasets hub (quick links to the subdirectories for component datasets are provided in the Details column in the table above). You can use these as a starting point if you would like to add more datasets to the mix. Adding further `dandisets` should be particularly easy based off of the current examples. When creating the component datasets, we split long sessions (>10M tokens) into smaller equal-sized chunks of no more than 10M tokens. This makes data loading more efficient and prevents errors while creating and uploading HF datasets.

## Merging the component datasets into a single dataset
Once we have created the individual component datasets, we merge them into a single dataset with the `merge_datasets.py` script. This also shuffles the combined dataset, creates a separate test split, and pushes the dataset to the HF datasets hub. 

## Visualizing the datasets
`visualize_datasets.py` provides some basic functionality to visualize random samples from the datasets:
```python
python visualize_datasets.py --repo_name 'eminorhan/xiao' --n_examples 6
```
This will randomly sample `n_examples` examples from the corresponding dataset and visualize them as below, where *x* is the time axis (binned into 20 ms windows) and the *y* axis represents the recorded units:

![](assets/xiao.jpg)

### TODO:

- [ ] update `create_dataset.py` scripts with added arguments
