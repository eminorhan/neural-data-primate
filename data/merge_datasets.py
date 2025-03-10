from datasets import load_dataset, concatenate_datasets, Sequence, Value

## FIXME: this whole thing is a bit hacky and clunky at the moment, will be revisited later on
## NOTE: we need to recast spike_counts to the same data type (uint8) before we can concatenate the datasets

# willett
willett_column_name = "tx1"  # FIXME: is tx1 the correct colun to use here?
willett_train = load_dataset("eminorhan/willett", split='train').select_columns([willett_column_name])
willett_test = load_dataset("eminorhan/willett", split='test').select_columns([willett_column_name])
willett_validation = load_dataset("eminorhan/willett", split='validation').select_columns([willett_column_name])
willett = concatenate_datasets([willett_train, willett_test, willett_validation])
willett = willett.rename_column("tx1", "spike_counts")
willett = willett.add_column("source_dataset", ["willett"] * len(willett))
print(willett.features["spike_counts"])

# h1
h1_column_name = "spike_counts"
h1_incalib = load_dataset("eminorhan/h1", "in-calib", split='train').select_columns([h1_column_name])
h1_inminival = load_dataset("eminorhan/h1", "in-minival", split='train').select_columns([h1_column_name])
h1_outcalib = load_dataset("eminorhan/h1", "out-calib", split='train').select_columns([h1_column_name])
h1 = concatenate_datasets([h1_incalib, h1_inminival, h1_outcalib])
h1 = h1.add_column("source_dataset", ["h1"] * len(h1))
h1 = h1.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(h1.features["spike_counts"])

# # h2
h2_column_name = "spike_counts"
h2_incalib = load_dataset("eminorhan/h2", "in-calib", split='train').select_columns([h2_column_name])
h2_inminival = load_dataset("eminorhan/h2", "in-minival", split='train').select_columns([h2_column_name])
h2_outcalib = load_dataset("eminorhan/h2", "out-calib", split='train').select_columns([h2_column_name])
h2 = concatenate_datasets([h2_incalib, h2_inminival, h2_outcalib])
h2 = h2.add_column("source_dataset", ["h2"] * len(h2))
h2 = h2.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(h2.features["spike_counts"])

# m1-a
m1a_column_name = "spike_counts"
m1a_incalib = load_dataset("eminorhan/m1-a", "in-calib", split='train').select_columns([m1a_column_name])
m1a_inminival = load_dataset("eminorhan/m1-a", "in-minival", split='train').select_columns([m1a_column_name])
m1a_outcalib = load_dataset("eminorhan/m1-a", "out-calib", split='train').select_columns([m1a_column_name])
m1a = concatenate_datasets([m1a_incalib, m1a_inminival, m1a_outcalib])
m1a = m1a.add_column("source_dataset", ["m1a"] * len(m1a))
m1a = m1a.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(m1a.features["spike_counts"])

# m1-b
m1b_column_name = "spike_counts"
m1b_incalib = load_dataset("eminorhan/m1-b", "in-calib", split='train').select_columns([m1b_column_name])
m1b_inminival = load_dataset("eminorhan/m1-b", "in-minival", split='train').select_columns([m1b_column_name])
m1b_outcalib = load_dataset("eminorhan/m1-b", "out-calib", split='train').select_columns([m1b_column_name])
m1b = concatenate_datasets([m1b_incalib, m1b_inminival, m1b_outcalib])
m1b = m1b.add_column("source_dataset", ["m1b"] * len(m1b))
m1b = m1b.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(m1b.features["spike_counts"])

# m2
m2_column_name = "spike_counts"
m2_incalib = load_dataset("eminorhan/m2", "in-calib", split='train').select_columns([m2_column_name])
m2_inminival = load_dataset("eminorhan/m2", "in-minival", split='train').select_columns([m2_column_name])
m2_outcalib = load_dataset("eminorhan/m2", "out-calib", split='train').select_columns([m2_column_name])
m2 = concatenate_datasets([m2_incalib, m2_inminival, m2_outcalib])
m2 = m2.add_column("source_dataset", ["m2"] * len(m2))
m2 = m2.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(m2.features["spike_counts"])

# area2-bump
area2_bump_column_name = "spike_counts"
area2_bump = load_dataset("eminorhan/area2-bump", split='train').select_columns([area2_bump_column_name])
area2_bump = area2_bump.add_column("source_dataset", ["area2_bump"] * len(area2_bump))
area2_bump = area2_bump.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(area2_bump.features["spike_counts"])

# dmfc-rsg
dmfc_rsg_column_name = "spike_counts"
dmfc_rsg = load_dataset("eminorhan/dmfc-rsg", split='train').select_columns([dmfc_rsg_column_name])
dmfc_rsg = dmfc_rsg.add_column("source_dataset", ["dmfc_rsg"] * len(dmfc_rsg))
dmfc_rsg = dmfc_rsg.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(dmfc_rsg.features["spike_counts"])

# xiao
xiao_column_name = "spike_counts"
xiao = load_dataset("eminorhan/xiao", split='train').select_columns([xiao_column_name])
xiao = xiao.add_column("source_dataset", ["xiao"] * len(xiao))
print(xiao.features["spike_counts"])

# churchland
churchland_column_name = "spike_counts"
churchland = load_dataset("eminorhan/churchland", split='train').select_columns([churchland_column_name])
churchland = churchland.add_column("source_dataset", ["churchland"] * len(churchland))
churchland = churchland.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(churchland.features["spike_counts"])

# perich
perich_column_name = "spike_counts"
perich = load_dataset("eminorhan/perich", split='train').select_columns([perich_column_name])
perich = perich.add_column("source_dataset", ["perich"] * len(perich))
perich = perich.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(perich.features["spike_counts"])

# makin
makin_column_name = "spike_counts"
makin = load_dataset("eminorhan/makin", split='train').select_columns([makin_column_name])
makin = makin.add_column("source_dataset", ["makin"] * len(makin))
makin = makin.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(makin.features["spike_counts"])

# lanzarini
lanzarini_column_name = "spike_counts"
lanzarini = load_dataset("eminorhan/lanzarini", split='train').select_columns([lanzarini_column_name])
lanzarini = lanzarini.add_column("source_dataset", ["lanzarini"] * len(lanzarini))
lanzarini = lanzarini.cast_column("spike_counts", Sequence(feature=Sequence(feature=Value(dtype='uint8', id=None), length=-1, id=None), length=-1, id=None))
print(lanzarini.features["spike_counts"])

# neupane-ppc
neupane_ppc_column_name = "spike_counts"
neupane_ppc = load_dataset("eminorhan/neupane-ppc", split='train').select_columns([neupane_ppc_column_name])
neupane_ppc = neupane_ppc.add_column("source_dataset", ["neupane_ppc"] * len(neupane_ppc))
print(neupane_ppc.features["spike_counts"])

# neupane-entorhinal
neupane_entorhinal_column_name = "spike_counts"
neupane_entorhinal = load_dataset("eminorhan/neupane-entorhinal", split='train').select_columns([neupane_entorhinal_column_name])
neupane_entorhinal = neupane_entorhinal.add_column("source_dataset", ["neupane_entorhinal"] * len(neupane_entorhinal))
print(neupane_entorhinal.features["spike_counts"])

# concatenate all and push to hub
neural_bench = concatenate_datasets([willett, h1, h2, m1a, m1b, m2, area2_bump, dmfc_rsg, xiao, churchland, perich, makin, lanzarini, neupane_ppc, neupane_entorhinal])
neural_bench.push_to_hub("eminorhan/neural-bench", token=True)