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

## Verification Record

The frozen unseen set was checked on 2026-10-09.

- Image checksum manifest: verified successfully.
- Label checksum manifest: verified successfully.
- Frozen unseen images: 300.
- Frozen unseen labels: 300.
- Exact-filename overlap between train and unseen: 0.
- Exact-filename overlap between validation and unseen: 0.
- Exact-filename overlap between train and validation: 0.

These checks establish manifest integrity and no exact-filename overlap.
They do not rule out duplicate image content under different filenames.

## Outstanding Day 5 Work

- Supplementary annotated images and labels have not been located under
  `dataset/supplementary/images/` and `dataset/supplementary/labels/`.
- The planned second-pass annotation review is not yet evidenced here.

Day 5 must remain incomplete until the remaining annotation requirements
are completed or explicitly accepted as deferred by the team lead.
