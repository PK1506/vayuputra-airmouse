# Dataset Split

## Training / Validation / Test

The merged dataset contains:

- Train: 600 images
- Validation: 171 images
- Test: 87 images
- Total: 858 images

All three splits contain only class `0` (`person`).

## Frozen Unseen Test

The frozen unseen test set contains:

- 300 images
- 300 label files

It is stored separately under:

`dataset/unseen_test/`

The unseen set must not be used for:

- training
- augmentation
- hyperparameter tuning
- confidence-threshold selection
- model selection

Frozen checksums are stored in:

- `dataset/unseen_test/FILES.sha256`
- `dataset/unseen_test/LABELS.sha256`
