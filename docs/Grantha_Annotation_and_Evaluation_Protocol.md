# Grantha preprocessing study: annotation and evaluation protocol

Draft protocol, 30 September 2026. No new reference labels or quantitative scores have been produced. This document turns the unresolved annotation requirement into an executable research procedure.

## Additional evidence and novelty implication

Kesiman et al., **An Analysis of Ground Truth Binarized Image Variability of Palm Leaf Manuscripts**, IPTA 2015, pp. 229–233, DOI **10.1109/IPTA.2015.7367134**, already investigated differences between ground truths produced by different annotators. Indexed author-uploaded primary text describes comparisons between two annotators and a semi-automatic ground-truth framework. This check did not retrieve a complete local PDF or verify experimental tables. No numerical findings are extracted.

Primary author manuscript locator: https://www.researchgate.net/publication/283711193_An_Analysis_of_Ground_Truth_Binarized_Image_Variability_of_Palm_Leaf_Manuscripts

A related 2015 study, **An Initial Study on the Construction of Ground Truth Binarized Images of Ancient Palm Leaf Manuscripts**, DOI **10.1109/ICDAR.2015.7333843**, is a further retrieval lead. Its complete methods have not been appraised in this step.

Consequently, annotation variability itself cannot be claimed as a new palm-leaf research problem. Our proposed contribution is its application to a documented Grantha dataset audit and a transparent evaluation of accessible Grantha material. Whether prior Grantha work already addresses this combination remains an open full-text review question. These leads have not been assigned new candidate IDs or counted as new inclusions; they require reconciliation with the working register first.

## Current data boundary

The previously audited upload contains ten nominal image/reference pairs but five unique pairs. The existing references are continuous grayscale JPEGs with an unresolved binary-label specification. Preserve them as supplied references. Do not threshold them and relabel the result as independently verified ground truth.

The existing Otsu, Niblack and Sauvola outputs remain qualitative examples. None of the steps below has yet been executed on newly annotated references.

## Annotation procedure

1. **Register sources.** For every unique image, record image ID, original filename, SHA256, repository version, license, dimensions, manuscript/leaf identity where known and parent-crop relationship. Unknown source identity must be recorded as unknown.
2. **Define the target.** Label visible writing strokes at the original pixel grid. Exclude leaf fibres, scratches, holes, borders and stains unless evidence supports their membership in a writing stroke. Pixel annotation does not itself establish character identity or transcription.
3. **Preserve uncertainty.** Use a foreground mask and a separate uncertainty mask. Keep uncertain pixels out of the primary scoring region under a policy fixed before method evaluation. Record the excluded fraction for every image. Do not remove difficult pixels after seeing method errors.
4. **Make independent annotations.** Two annotators inspect the original images without viewing the tested baseline predictions. Each saves their own foreground and uncertainty masks. Use lossless PNGs, original dimensions, and values 0 for background and 255 for foreground; the uncertainty mask uses 255 for uncertain pixels.
5. **Check agreement.** Compare annotators over the common non-uncertain region using foreground F1 and IoU. Retain both masks. Inspect disagreements, especially faint strokes and scratches. Record annotator experience and any use of script expertise.
6. **Adjudicate.** Resolve disagreements by reviewing the original image, recording the decision and reason. An unresolved ambiguity remains uncertain. Save an adjudicated mask without overwriting the independent masks. Document whether a Grantha reader assisted; do not infer linguistic verification from pixel agreement.
7. **Validate files.** Require matching shapes, exact binary mask values, valid image IDs and no accidental resizing. Check overlays against the originals. Freeze the approved annotation version and hashes before calculating baseline scores.

If independent checking is unavailable, label the reference set as single-annotator and preliminary. Do not report agreement or expert validation that did not occur.

## Evaluation plan

Use the already documented fixed baseline settings initially: Otsu; Niblack with window 25 and k = -0.2; Sauvola with window 25, k = 0.2 and R = 128. Keep preprocessing and foreground conventions consistent with the preserved baseline implementation. This is a proposed scored comparison; it has not been run against approved masks.

Report each method's foreground precision, recall, F1 and IoU per unique image, using the frozen evaluable pixels. Explicitly report cases with an empty denominator; do not silently replace undefined values with zero or one. Supply raw confusion counts and excluded pixel counts alongside derived metrics.

Do not use pixel accuracy as the headline result because large background areas can dominate it. Keep the five unique images visible in the result table rather than reporting only a mean. Do not treat duplicate files, pixels or related crops as independent manuscripts. Source-level uncertainty analysis requires known source groups; broad generalization is unsupported with the present small set.

As a planned sensitivity analysis, score against each independent annotator's reference as well as the adjudicated reference, under a documented common evaluation-region policy. Report whether method ordering changes. This analysis measures dependence on the reference definition; it does not make any annotation automatically correct.

## Error analysis form

| Field | Required entry |
|---|---|
| Image and region | Unique ID and pixel bounding box |
| Method | Baseline name and frozen settings |
| Error category | Faint-stroke loss; background retention; broken stroke; merged strokes; border artefact; other |
| Supporting evidence | Original crop, prediction crop and reference overlay |
| Interpretation confidence | Confirmed against adjudicated visible-ink label, or unresolved |
| Annotation issue | Agreement/disagreement history and uncertain-pixel involvement |
| Consequence | Pixel-level error; downstream effect untested unless separately evaluated |

Select examples using a declared rule, such as inspecting all five images for every method and recording every observed category. Do not use only favourable examples or infer OCR improvement from a cleaner-looking binary image.

## Completion gates

- Annotation definition and source manifest complete.
- Independent references and disagreements preserved, or single-annotator limitation explicitly retained.
- Masks validated and frozen before scoring.
- Per-image results and error examples produced from actual runs.
- Claims restricted to the annotated images and tested task.

The immediate dependency is checked visible-ink annotation, not a private manuscript collection. The review can continue while this dependency remains unresolved. The five-image experiment, even after annotation, should be described as a limited case study; a stronger journal submission requires an adequate completed review and experimental scope supported by the available data.

## Retrieval status for earlier reviews

C007 full-text routes returned access errors/timeouts; C040 and C042 remain publisher-abstract evidence; C063 remains publisher-abstract evidence. A 2018 comparative benchmark, DOI 10.3390/jimaging4020043, has a publisher-indexed abstract but its full page was inaccessible in this step. None has been promoted to full-text appraisal on the basis of a search excerpt. No candidate count, eligibility decision or PRISMA total changed.
