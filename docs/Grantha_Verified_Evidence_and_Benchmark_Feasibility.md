# Grantha review: verified evidence update and benchmark feasibility

Date: 30 September 2026. Status: continuing review and source verification. No experimental results have been produced. Bibliographic intake now contains 66 candidate references, not 66 eligible studies.

## What changed

Two Tigalari-specific publications were identified through supplementary web searches and added to the previous 64-reference candidate bibliography. Neither DOI occurred in that bibliography. The original WoS and LeapSpace intake counts remain unchanged; these two records have separate web-search provenance. Claims that no Tigalari-specific computational research exists are unsupported and must be removed from the planned manuscript.

## Source-backed extraction

### C065 — Tigalari manuscript binarization

Sandhya, S.; Geetha, V. (2026). Multi-stage Binarization Approach for Ancient Tigalari Palm Leaf Manuscripts. CCIS 2737, pp. 364–376. DOI: 10.1007/978-3-032-14534-5_30.

Publisher record confirms first online publication on 1 February 2026. The abstract describes comparative binarization of historic Tigalari palm leaves and reports Sauvola as the best technique in that comparison. This is preprocessing evidence, not an established end-to-end OCR result. The acknowledgement identifies SDM Oriental Library assistance with data and mapping characters to Kannada. Sample counts, objective metrics, annotation method, parameter selection, split design, dataset license and downloadable data are unresolved because the full chapter was not obtained.

Source: https://link.springer.com/chapter/10.1007/978-3-032-14534-5_30 (abstract, acknowledgement and citation metadata).

### C066 — Tigalari character classification

Bhat, Sachin S.; Ananth, Alaka; Nambiar, Rajashree; Bhat, Nagaraj (2022). Building Dataset and Deep Learning-Based Inception Model for the Character Classification of Tigalari Script. AISC 1386, pp. 239–252. DOI: 10.1007/978-981-16-3342-3_20.

Springer’s contents confirm the title, authors and pages; the author’s institutional bibliography supplies the chapter DOI and 2022 citation year. The chapter page could not be retrieved. Historical-manuscript versus newly written samples, character inventory, writer/source grouping, accuracy, model details, data access and license remain unverified. Do not import performance claims from later citing papers.

Sources: https://link.springer.com/book/10.1007/978-981-16-3342-3?page=2 and https://sode-edu.in/smvitm/faculties/nagaraj-bhat/.

### Existing candidate — Vedic palm-leaf review

The Springer chapter is now independently verified: Samantaray, S.; Mohapatra, S. K.; Mohapatra, S., DOI 10.1007/978-3-031-99882-9_14, pp. 146–160. The official citation uses 2026, while first online publication is 2 October 2025. Preserve both fields. Its abstract addresses machine learning, preprocessing, feature extraction, datasets and palm-leaf recognition. The public page includes references, but the actual search methods, study-selection counts and appraisal framework remain inaccessible. Its title does not prove methodological completeness.

Source: https://link.springer.com/chapter/10.1007/978-3-031-99882-9_14.

### Existing candidate — HMPLMD

Nair and Rani’s 2023 data article reports 250 raw Malayalam palm-leaf images and 69 ground-truth samples: Kambaramayanam 151/24 and Jathakas 99/45. Acquisition used DSLR and iPhone imaging. Ground truth was produced through enhancement, adaptive thresholding and manual Photoshop editing; missing letter regions could be manually restored. The article also describes subsampling into five images. These are binarization references rather than verified Unicode transcriptions. Therefore, ancestry, alignment and label construction require inspection before pixel-level evaluation. Article counts are not a downloaded-file inventory.

The Mendeley repository, DOI 10.17632/ssycxg2snx.1, identifies version 1, published 28 November 2022, and CC BY 4.0. Its license was checked separately from the article license. Direct file access was blocked: the dataset page could not be fetched and a public metadata endpoint returned HTTP 403. File pairing, dimensions, parent identifiers and actual downloadable sample counts remain pending.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC9938152/ (indexed article text, Table 1 and sections 2–3) and https://data.mendeley.com/datasets/ssycxg2snx/1 (indexed repository record).

## Benchmark decision

**Provisional route:** evaluate a small set of binarization methods on an existing licensed palm-leaf dataset, then document errors and methodological limits. HMPLMD is a comparative Malayalam candidate. Results on it would not measure Grantha recognition or establish Tigalari transfer. The final scope must accurately state that limitation.

**Readiness:** not ready to run. The repository license and article ground-truth description are verified, but actual files and pair alignment are not. The experimental plan below is proposed, not executed.

### Controlled pilot specification

1. **Question:** How sensitive are simple preprocessing baselines to acquisition/source variation and to manually edited binarization references?
2. **Inventory:** download versioned original/reference files; preserve names and hashes; map each crop to its parent photograph and, where supplied, leaf/manuscript/bundle. Identify repeated captures and descendants before splitting.
3. **Label audit:** inspect paired alignment, reference format and ambiguous/restored strokes. Any independently chosen uncertain-pixel mask must be documented; do not redefine references to favor a method.
4. **Baselines:** global Otsu, local Niblack and local Sauvola on identical grayscale inputs. These are proposed comparator families; parameter grids and implementation versions must be recorded before test evaluation.
5. **Tuning:** separate calibration and test groups by parent image, with manuscript/bundle grouping where known. All five subsamples and augmentations of a parent stay together. Select local-window sizes and coefficients only on calibration data. If original alignment or parent grouping is unrecoverable, do not claim a manuscript-independent evaluation.
6. **Outcomes:** foreground precision, recall, F1 and IoU per original parent, with the foreground convention stated explicitly. Aggregate crops within parent before dataset summaries. Background-dominated pixel accuracy is insufficient as the sole score. No CER/WER without verified text labels.
7. **Uncertainty:** compare methods on the same test parents. Bootstrap at the highest reliable independent source unit; report that unit. If only two source collections are identifiable, do not present image-resampled intervals as collection-generalization evidence.
8. **Error analysis:** distinguish stroke loss, fused strokes, background texture, cracks, holes, uneven illumination and reference mismatch/restoration. Report objective pixel metrics separately from visual judgements about linguistic readability.
9. **Reporting:** release code, parameters, manifest, predictions and permissible examples; cite the dataset and respect its license. Report every preregistered comparator, including weak outcomes.

HMPLMD references are partly derived from adaptive thresholding, including Sauvola. Consequently, high agreement with these masks may partly reflect reference construction. Any claim that one method is inherently superior needs independent evidence. This is a methodological risk to investigate, not proof of actual bias in the dataset.

## Contribution to pursue

Working title: **Computational Recognition of Grantha and Related Palm-Leaf Manuscripts: A Systematic Review of Data, Evaluation and Reproducibility.**

Build the review around evidence quality: actual script/material, character versus line task, historical versus newly written samples, annotation expertise, character coverage, independent splits, metrics, error analysis, reproducibility and licensing. Keep direct Grantha/Tigalari studies distinct from comparative-script evidence. A small baseline benchmark can illustrate evaluation problems once data is accessible, but does not by itself establish novelty or guarantee Q1 acceptance.

## Retrieval log for this update

Supplementary open-web searches included: “HMPLMD 108960”; “HMPLMD data.mendeley.com”; “Southeast Asian palm leaf manuscript images review pdf”; the exact Vedic-review DOI; the exact Tigalari-binarization title; “Tigalari character recognition Bhat 2020”; and the exact Bhat chapter DOI. Search date: 30 September 2026. The last query is a discovery string, not a verified publication year.

- Springer Vedic-review preview: accessible; metadata, abstract and references checked; full text pending.
- Springer Tigalari-binarization preview: accessible; metadata, abstract and acknowledgement checked; full text pending.
- Springer Bhat chapter: blocked; publisher contents and institutional bibliography checked instead.
- HMPLMD PMC direct page: browser challenge; indexed primary article text supplied relevant sections. Do not label this a complete downloaded-paper audit.
- SPIE 2017 review and institutional PDF: inaccessible in this pass; retain previous abstract-level extraction.
- HMPLMD files: not obtained; benchmark execution pending.

## Next actions

Retrieve the Tigalari chapters, Grantha CNN paper and Vedic review through institutional access if available. Obtain a versioned copy of HMPLMD originals and references, or inspect another accessible labelled dataset, before selecting the benchmark. Continue screening the 66 candidate references while collecting exact Scopus/WoS queries, dates, coverage and export counts. Full-text eligibility, PRISMA totals and experimental results remain unfinished.
