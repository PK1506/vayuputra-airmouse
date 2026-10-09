# Frozen Unseen Test Set

## Dataset

UAV-SAR Human Detection Dataset — V1

## Source

Roboflow Universe

## URL

https://universe.roboflow.com/hamzaghitri/uav-sar-human-detection-dataset

## Authors

Hamza Ghitri, Jakub Gutt, Wojciech Seman, Krzysztof Połeć

## License

CC BY 4.0

## Dataset characteristics

- 300 manually annotated frames
- DJI Air 3S
- 4K / 60 FPS source
- 15 m and 30 m altitude
- 45° and 90° camera angles
- 75 frames per flight condition
- Single class: Person
- Unique unmodified frames
- Sampled at 1 FPS
- No augmentation

## Role in NIDAR

This dataset is used exclusively as the frozen unseen evaluation set.

It must not be used for:
- model training
- training augmentation
- hyperparameter tuning
- confidence-threshold selection
- model selection

## Selection date

2026-10-05

## Expected image count

300

## Expected label count

300
