# Computational Analysis of Grantha Manuscripts

## Reproducibility Materials

**Author:** Vinod Chandra S S  
**Version:** 1.0.0  
**Release date:** 2026-10-04

This repository contains reproducibility materials associated with a
study of computational analysis of Grantha manuscripts. The work combines
systematic evidence synthesis, dataset/provenance assessment, and a
controlled line-segmentation benchmark.

The repository is intended to support transparent inspection and
reproduction of the computational workflow while maintaining conservative
claims regarding benchmark generalisability and third-party manuscript
image rights.

## Repository contents

### `scripts/`

Contains the frozen computational scripts required for the controlled
line-segmentation workflow and evaluation.

Key scripts include:

- `grantha_line_batch_v3_frozen.py`
- `g3c4_finalize_26lines.py`
- `g3c5_complete_evaluation.py`

### `results/`

Contains frozen human-reference grouping and quantitative evaluation
outputs for the independently annotated evaluation sample.

### `metadata/`

Contains evidence-review and benchmark metadata used in the study.

### `docs/`

Contains methodological protocols and supporting reproducibility
documentation.

## Controlled line-segmentation benchmark

The independently annotated evaluation sample `ISADI_004` contained
42 human-annotated polygon components.

A geometry-audited grouping procedure consolidated these components into
26 logical text lines:

- 17 full-width lines
- 7 three-fragment lines
- 2 two-fragment lines

All 42 human annotation components were uniquely accounted for.

The automatic segmentation also produced 26 candidate text lines.

Evaluation used polygon-union rasterisation of the human logical-line
annotations followed by one-to-one Hungarian assignment maximizing
intersection-over-union (IoU).

### Frozen evaluation results

| Measure | Result |
|---|---:|
| Human logical lines | 26 |
| Automatic lines | 26 |
| Mean matched IoU | 0.6278 |
| Median matched IoU | 0.6323 |
| Minimum matched IoU | 0.4666 |
| F1 at IoU >= 0.25 | 1.0000 |
| F1 at IoU >= 0.50 | 0.9231 |
| F1 at IoU >= 0.75 | 0.0385 |

At the primary IoU threshold of 0.50:

- TP = 24
- FP = 2
- FN = 2
- Precision = 0.9231
- Recall = 0.9231
- F1 = 0.9231

All Hungarian assignments preserved the corresponding logical-line order.
The two matches below the primary threshold were GT line 01 and GT line 08.

These results represent a controlled evaluation sample and must not be
interpreted as a population-level estimate of performance across all
Grantha manuscripts, collections, writing styles, preservation states,
or imaging conditions.

## Reproducibility

Python dependencies are listed in:

`requirements.txt`

Install them using:

    pip install -r requirements.txt

The principal evaluation script is:

    python scripts/g3c5_complete_evaluation.py

Some scripts retain paths associated with the frozen local experimental
environment. Users reproducing the experiment with independently obtained
source images may need to adapt local path configuration without changing
the underlying evaluation procedure.

## Manuscript image availability

The source palm-leaf manuscript images are not redistributed in this
release by default.

This exclusion is intentional. Historical age of the manuscript does not
by itself establish unrestricted redistribution rights for a particular
digital image or scan.

See:

`MANUSCRIPT_IMAGE_AVAILABILITY.md`

Users seeking full image-level reproduction should obtain the corresponding
source images from the identified source repository or rights holder under
the applicable access and reuse conditions.

## Licensing boundary

Any software licence supplied with this repository applies only to material
for which the repository author has the authority to grant such rights.

It does not grant rights over third-party manuscript photographs, scans,
database records, bibliographic content, or other externally sourced
material.

Third-party materials remain subject to their respective rights,
licences, terms of use, and attribution requirements.

## Integrity

`SHA256SUMS.txt` provides SHA-256 checksums for the files included in the
release package.

The controlled evaluation preserves cryptographic provenance for the
independent human annotation and frozen automatic segmentation input.

## Citation

Citation metadata are provided in:

`CITATION.cff`

When using these reproducibility materials, please cite the associated
article and the relevant repository release.

## Version

**v1.0.0**
