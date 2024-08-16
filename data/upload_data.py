from huggingface_hub import HfApi

api = HfApi()

# upload data files

api.upload_file(
    path_or_fileobj="/scratch/eo41/speech-bci/data/train.npz",
    path_in_repo="train.npz",
    repo_id="eminorhan/speech-bci-willett",
    repo_type="dataset",
    token='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'
)

api.upload_file(
    path_or_fileobj="/scratch/eo41/speech-bci/data/test.npz",
    path_in_repo="test.npz",
    repo_id="eminorhan/speech-bci-willett",
    repo_type="dataset",
    token='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'
)

api.upload_file(
    path_or_fileobj="/scratch/eo41/speech-bci/data/val.npz",
    path_in_repo="val.npz",
    repo_id="eminorhan/speech-bci-willett",
    repo_type="dataset",
    token='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'
)
