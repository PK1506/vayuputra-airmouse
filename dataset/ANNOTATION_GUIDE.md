# Survivor Detection Annotation Guide

## 1. Purpose

This guide defines the annotation rules for supplementary images used
for the Vayuputra NIDAR M6 Survivor Detection dataset.

The detection task uses a single object class:

- Class 0: person

The objective is to detect people/survivors from RGB or elevated/drone-view
imagery.

---

## 2. Class Definition

| Class ID | Class Name |
|----------|------------|
| 0        | person     |

Only the `person` class should be annotated.

Do not create additional classes such as:
- survivor
- victim
- rescuer
- adult
- child
- soldier

---

## 3. Bounding Box Rule

Draw a tight bounding box around the visible part of the person.

The bounding box should contain the person while avoiding unnecessary
background area.

Do not deliberately expand the bounding box to include large areas of
ground, buildings, vehicles, vegetation, or other surroundings.

---

## 4. Partially Occluded People

Annotate a partially occluded person when a clear portion of the person
is visible and the object can reasonably be identified as a person.

Examples of possible occlusion:
- vegetation
- rubble
- objects
- structures
- other people

The bounding box should cover the visible/annotatable extent of the person
according to the annotation tool's bounding-box convention.

---

## 5. Lying People

People lying on the ground must be annotated.

A person does not need to be standing or upright to belong to class 0.

Examples include:
- lying horizontally
- sitting or crouching
- partially visible people lying among debris

---

## 6. Crowds

When individual people can be visually separated, create one bounding box
for each person.

If people are merged together so that individual bounding boxes cannot be
reasonably separated, record the case and follow the project-approved
crowd handling decision rather than inventing inaccurate boxes.

---

## 7. Objects That Must NOT Be Annotated

Do not annotate objects that are not real people, including:

- posters
- statues
- mannequins

Do not create a person bounding box simply because an object has a
human-like appearance.

---

## 8. Annotation Format

Annotations must be exported in YOLO format.

Each annotated person is represented as:

class_id center_x center_y width height

All coordinates are normalized to the range 0 to 1.

Example:

0 0.52 0.48 0.12 0.35

where:

- `0` = person
- `0.52` = normalized bounding-box center X
- `0.48` = normalized bounding-box center Y
- `0.12` = normalized bounding-box width
- `0.35` = normalized bounding-box height

---

## 9. Quality Check

Approximately 10% of supplementary annotations must receive a second
review.

The second review should check for:

- missed people
- incorrect bounding boxes
- boxes that are unnecessarily large
- boxes that are too small
- incorrect class IDs
- incorrectly annotated non-person objects
- inconsistent treatment of occluded people
- inconsistent treatment of lying people
- inconsistent treatment of crowds

Any disagreements should be recorded and resolved consistently.

---

## 10. Supplementary Dataset Target

Target: 100-300 supplementary images.

If fewer images can be collected, record the actual number collected
rather than claiming the target was achieved.

---

## 11. Frozen Unseen Test Set

The `dataset/unseen_test/` set must contain images/videos from scenes that
are not present in the training or validation data.

The frozen unseen set must never be used for:

- training
- model tuning
- confidence-threshold selection

Checksums must be generated after the unseen set is finalized so that
the frozen files can be verified later.

---

## 12. Annotation Workflow

1. Collect mission-relevant supplementary imagery.
2. Annotate people using the rules in this document.
3. Export annotations in YOLO format.
4. Validate the annotations.
5. Perform the approximately 10% second-pass quality check.
6. Resolve annotation disagreements.
7. Freeze the unseen test set separately.
8. Generate checksums for the frozen unseen set.

---

## 13. Scope

This guide applies to the M6 Survivor Detection supplementary
annotation work.

The detection task is limited to person detection. Downstream depth
localization, map coordinates, and GCS integration are outside the scope
of this annotation guide.
