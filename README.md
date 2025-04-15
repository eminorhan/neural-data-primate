## primate ephys data

~34B uncompressed tokens of ephys data recorded from primates (tokens=units x time bins). Unless otherwise noted, the data consist of spike counts within 20 ms time bins recorded from each unit. 

Token counts per dataset:

1. **Xiao:** 17,695,820,059 tokens ([dandi:000628](https://dandiarchive.org/dandiset/000628)); sessions = 679
2. **Neupane (PPC):** 7,899,849,087 tokens ([dandi:001275](https://dandiarchive.org/dandiset/001275)); sessions = 10
3. **Willett:** 1,796,119,552 ([dryad:x69p8czpq](https://datadryad.org/stash/dataset/doi:10.5061/dryad.x69p8czpq)); sessions = 44
4. **Churchland:** 1,278,669,504 tokens ([dandi:000070](https://dandiarchive.org/dandiset/000070)); sessions = 10
5. **Neupane (Entorhinal):** 911,393,376 tokens ([dandi:000897](https://dandiarchive.org/dandiset/000897)); sessions = 15
6. **Kim:** 804,510,741 tokens ([dandi:001357](https://dandiarchive.org/dandiset/001357)); sessions = 159
7. **Even-Chen:** 783,441,792 tokens ([dandi:000121](https://dandiarchive.org/dandiset/000121)); sessions = 12
8. **Papale:** 775,618,560 tokens ([g-node:TVSD](https://gin.g-node.org/paolo_papale/TVSD)); sessions = 2
9. **Perich:** 688,889,368 tokens ([dandi:000688](https://dandiarchive.org/dandiset/000688)); sessions = 111
10. **Wojcik:** 422,724,515 tokens ([dryad:c2fqz61kb]( https://doi.org/10.5061/dryad.c2fqz61kb)); sessions = 50
11. **Makin:** 375,447,744 tokens ([zenodo:3854034](https://zenodo.org/records/3854034)); sessions = 47
12. **H2:** 297,332,736 tokens ([dandi:000950](https://dandiarchive.org/dandiset/000950)); sessions = 47
13. **Lanzarini:** 259,179,392 tokens ([osf:82jfr](https://osf.io/82jfr/)); sessions = 10
14. **Athalye:** 101,984,317 tokens ([dandi:000404](https://dandiarchive.org/dandiset/000404)); sessions = 13
15. **M1-A:** 45,410,816 tokens ([dandi:000941](https://dandiarchive.org/dandiset/000941)); sessions = 11
16. **M1-B:** 43,809,344 tokens ([dandi:001209](https://dandiarchive.org/dandiset/001209)); sessions = 12
17. **H1:** 33,686,576 tokens ([dandi:000954](https://dandiarchive.org/dandiset/000954)); sessions = 40
18. **Moore:** 30,643,839 tokens ([dandi:001062](https://dandiarchive.org/dandiset/001062)); sessions = 1
19. **Temmar:** 27,388,320 tokens ([dandi:001201](https://dandiarchive.org/dandiset/001201)); sessions = 12
20. **Rajalingham:** 14,923,100 tokens ([zenodo:13952210](https://zenodo.org/records/13952210)); sessions = 2
21. **DMFC-rsg:** 14,003,818 tokens ([dandi:000130](https://dandiarchive.org/dandiset/000130)); sessions = 2
22. **M2:** 12,708,384 tokens ([dandi:000953](https://dandiarchive.org/dandiset/000953)); sessions = 20
23. **Area2-bump:** 7,394,070 tokens ([dandi:000127](https://dandiarchive.org/dandiset/000127)); sessions = 2

**Total number of tokens:** 34,320,949,010. 

The combined dataset can be accessed from [this](https://huggingface.co/datasets/eminorhan/neural-bench-primate) public HF repository.

### TODO:

- [ ] change script name to generic: `create_X.py` -> `create_dataset.py`
- [ ] update `create_dataset.py` scripts with added arguments
