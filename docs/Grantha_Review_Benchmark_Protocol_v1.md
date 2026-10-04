# Grantha manuscript recognition: review and controlled benchmark

**Working protocol v1 — 29 September 2026.** This is a prospective study plan, not a completed review or a report of experimental results.

## Working title

From Character Accuracy to Manuscript Readability: A Systematic Review and Controlled Evaluation of Historical Indic Script Recognition, with Grantha as a Case Study

## Research questions

1. What tasks are evaluated in historical Indic manuscript recognition (character, word, line, page, script identification, transliteration), and which results concern genuine handwritten manuscripts rather than modern handwriting, print, or synthetic images?
2. How well are dataset provenance, annotation, licensing, writer/manuscript splits, and code documented?
3. Which reported accuracy measures can be compared, and which cannot because of differing units, scripts, collections, or protocols?
4. On a small verified Grantha set, how do accessible baselines perform on manuscript-held-out transcription, and what errors arise from degradation, ligatures, Vedic signs, and mixed script?
5. Does optional linguistic correction reduce error without replacing an attested manuscript reading with a plausible but incorrect one?

## Review protocol

- **Databases:** Scopus, Web of Science, ACL Anthology, IEEE Xplore, ACM Digital Library, SpringerLink, and relevant open repositories. Record search dates, exact queries, database fields, exports, and deduplication decisions. Search citations in both directions for eligible studies.
- **Draft search concept:** `(Grantha OR Grantham OR Thigalari OR Tigalari OR "historical Indic" OR "palm leaf manuscript") AND (OCR OR "handwritten text recognition" OR transcription OR transliteration OR "document analysis")`. Adapt syntax to each source and run separate Grantha-specific and comparative-script blocks so broad results do not hide rare-script work.
- **Include:** primary computational studies or datasets with historical Indic manuscript material, recognition/transcription or closely related layout tasks, identifiable data and an assessable method. Include closely related Malayalam, Tamil, Kannada, and other historical Indic scripts for methodological comparison; mark whether Grantha is actually evaluated.
- **Separate evidence strata:** real manuscript vs. print vs. modern handwritten vs. synthetic; character vs. line vs. page; single vs. mixed script; training/validation/test separation by crop, page, manuscript, and collection.
- **Exclude from performance synthesis:** articles without an identifiable evaluation set or metric definition. Retain relevant descriptive or philological works for context, labelled separately. Do not pool reported accuracies across incompatible tasks.
- **Screening:** record title/abstract and full-text decisions with reasons, duplicate handling, and a PRISMA flow only after counts are verified. A second reviewer should independently screen a subset, with disagreements adjudicated and logged.
- **Extraction:** citation/DOI; script/language; substrate; image provenance; rights; page/line/character counts; ground truth and verification; train/test unit; baseline/model; metric and normalization; error analysis; code/data availability; risk of leakage; limitations. Never infer missing values as zero.

## Controlled benchmark: preregistered design before scoring

1. **Data gate:** obtain collection-level identifiers and image permissions; verify Grantha script and language with an expert. Prefer multiple manuscripts and scribes. A single image can demonstrate a pipeline but cannot substantiate cross-manuscript generalization.
2. **Annotation:** retain diplomatic Unicode Grantha transcription as the primary reference. Record uncertain, illegible, supplied, and damaged spans explicitly. Keep transliteration and normalized Sanskrit in separate fields. Tag Tamil or other scripts and language mixing instead of silently converting it.
3. **Split:** group every line by manuscript and keep all lines of a manuscript in one split. Document duplicate pages, editions, recrops, and near-identical images. If too few manuscripts exist, report a descriptive pilot without a held-out-manuscript generalization claim.
4. **Baselines:** evaluate an available OCR/HTR model as released, and an additional accessible baseline where compatible. Document model provenance and possible training overlap. Separate line segmentation performance from recognition using both supplied and automatically detected line crops where feasible.
5. **Measures:** normalized character error rate and word error rate on the diplomatic transcription; line detection recall/precision if annotated; script-specific error counts; damage and conjunct strata. State Unicode normalization and treatment of spaces, Vedic marks, punctuation, and uncertain spans before running scores. Report per-manuscript results and bootstrap intervals at manuscript level when there are enough independent manuscripts.
6. **Correction experiment:** compare uncorrected OCR and Sanskrit-aware correction on the same held-out lines. Count improvements and introduced substitutions, especially on names, nonstandard readings, Vedic material, and Tamil–Grantha mixtures. Never use the published edition as a substitute for diplomatic ground truth without collation.
7. **Reporting:** publish actual sample sizes, exclusions, model versions, parameters, code, annotation rules, and data-access restrictions. No claimed accuracy or significance until runs and expert adjudication are frozen.

## Expert annotation template

Create one record per visible text line (and a separate page record). Recommended fields:

`collection_id, manuscript_id, folio_side, image_id, source_url, rights, line_id, reading_order, bbox_xyxy, script_tags, language_tags, grantha_diplomatic_unicode, transliteration_IAST, normalized_text_optional, uncertainty_spans, damage_tags, annotator_id, reviewer_id, adjudication_status, notes`

**Instructions:** Transcribe what is visible, not what a familiar verse is expected to say. Keep original punctuation and accent marks. Use a consistent convention for illegible spans, documented in an annotation guide. A second reader resolves uncertain lines; retain both initial and adjudicated versions for audit.

## Seed-source audit (not a completed systematic search)

| Source | Evidence and immediate use | Current status |
|---|---|---|
| Mendeley DOI 10.17632/y2s635w8wd.1 | Grantha character crops from palm leaves; CC BY 4.0 listing | Character-level resource; line transcript not described |
| Mendeley DOI 10.17632/zjtd63zhz6.1 | 3,900 character images, 39 classes, from Kerala-linked palm leaves | Character-level resource; not a manuscript transcription benchmark |
| GHCR, Data in Brief 2024, DOI 10.1016/j.dib.2024.110783 | 5,852 modern handwritten numeral/vowel images | Separate from historical manuscript testing |
| Shreeshrii/kraken_grantha repository | Line-image/ground-truth repository and model | Determine image provenance, manuscript status, licensing, and overlap before use |
| UniLipi project, 2026 | Multi-script HTR including Grantha; project page describes a model | Dataset page displayed “coming soon” at audit; code and checkpoint access need checking |
| Wikimedia Commons, Vedas palm leaf manuscript, Tamil Grantha script | First supplied palm-leaf image traced to source; original 2568×1253, CC BY-SA 4.0 | Suitable for illustrative/pipeline pilot; no verified line transcript identified; use original without caption overlay |
| Second supplied palm-leaf image | Plausible Grantha manuscript leaf | Collection identity, rights, and transcription unresolved |
| Dasam Granth images supplied earlier | Gurmukhi-script material | Exclude from Grantha benchmark |
| Veeraraghavan Grantha training handbook | Expert-reading reference | Not an image–line ground-truth benchmark |
| Hamburg CSMC project on Grantha in Tamil manuscripts | Demonstrates mixed-script manuscript context | Contextual source; corpus access and reuse not established |
| IISc Thigalari/Grantha multimodal digitization project | Relevant prior expert-in-the-loop approach | Project description, not a verified downloadable benchmark |

## Next gates

1. Export and deduplicate complete searches; screen and extract source-backed evidence. Do not present this seed list as exhaustive.
2. Trace the second leaf's provenance and locate a coherent multi-page Grantha collection with clear rights.
3. Pilot the annotation guide on a few lines with an expert; revise conventions before scaling annotation.
4. Freeze manuscript splits and evaluation scripts before baseline scoring.
5. Draft results, discussion, and journal-specific manuscript only after review and benchmark audits are complete.

## Source URLs recorded at protocol creation

- https://data.mendeley.com/datasets/y2s635w8wd/1
- https://data.mendeley.com/datasets/zjtd63zhz6/1
- https://www.sciencedirect.com/science/article/pii/S2352340924007480
- https://github.com/Shreeshrii/kraken_grantha
- https://ihdia.iiit.ac.in/unilipi/
- https://commons.wikimedia.org/wiki/File:Vedas_palm_leaf_manuscript,_Tamil_Grantha_Script,_Sanskrit,_Tamil_Nadu.jpg
- https://www.csmc.uni-hamburg.de/uwa-i/cluster-projects/field-h/rfh03.html
- https://www.indiascienceandtechnology.gov.in/research/digitization-ancient-manuscripts-thigalari-and-grantha-scripts-using-multimodal-recognition-speech
- https://www.prisma-statement.org/prisma-2020
