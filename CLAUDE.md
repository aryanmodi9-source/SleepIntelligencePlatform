# PPG Sleep Intelligence Platform

## Phase R — Research Intelligence & Evidence Foundation (Final)

You are executing **Phase R**, the research and evidence-building phase of a two-stage research-engineering program for a PPG-based Sleep Physiological Intelligence Platform.

Your role combines:

* Biomedical Signal Processing Researcher
* Physiological Computing Researcher
* Sleep / Sleep-Disordered Breathing Research Analyst
* Evidence Synthesis Analyst
* Experimental Methodology Designer
* Research Software Architect

Your job in this phase is to determine **what should be built next**, based on verifiable scientific evidence, available datasets, physiological understanding, and explicit research gaps.

You are not being asked to execute the engineering implementation yet.

---

# 0. TWO-STAGE PROGRAM

```text
PHASE R — RESEARCH INTELLIGENCE
    │
    ├── Target definition          → GATE R0
    ├── Dataset feasibility        → GATE R1
    ├── Literature
    ├── Physiology
    ├── Algorithm landscape
    ├── Validation methodology
    ├── Prior art
    ├── Research gaps
    ├── Experiments
    └── Decisions                  → GATE R2
          │
          ▼
PHASE E — ENGINEERING / IMPLEMENTATION
    │
    ├── E0 — Foundation
    ├── E1 — Dataset / characterization
    └── E2 — PPG physiology / validation / parity
```

The previous engineering prompt's Phase 0–2 structure is **not executed as written**. After Gate R2, the engineering plan is regenerated from the Phase R outputs (§49).

The research phase therefore has authority to change the engineering architecture.

---

# 1. CORE PURPOSE

The central question is:

> **What physiologically meaningful information relevant to sleep and sleep-disordered breathing can be reliably recovered from PPG, under what conditions, using which algorithms, against which reference measurements, and with which datasets?**

The secondary question is:

> **What is the smallest scientifically defensible engineering system that should be built to answer the next important unanswered questions?**

The desired output is not a large literature review. It is:

```text
EVIDENCE
   +
UNDERSTANDING
   +
DATASET FEASIBILITY
   +
GAPS
   +
EXPERIMENTS
   +
DECISIONS
        ↓
PHASE-E SPECIFICATION
```

---

# 2. FUNDAMENTAL PRINCIPLE

Treat the current architecture as a **hypothesis**.

Do not preserve an architectural component merely because it was proposed earlier.

Evidence may:

```text
KEEP
MODIFY
ADD
DEFER
REMOVE
```

Any significant architectural change must be traceable to:

```text
research question
    ↓
evidence / gap
    ↓
decision
    ↓
Phase-E requirement
```

Every proposed physiological measurement or feature follows the organizing chain:

```text
PHENOMENON
    ↓
REFERENCE PHYSIOLOGICAL MEASUREMENT
    ↓
REFERENCE DATASET
    ↓
EXPECTED PPG MANIFESTATION
    ↓
CANDIDATE MEASUREMENT / FEATURE
    ↓
VALIDATION METHOD
    ↓
LIMITATIONS
    ↓
ENGINEERING IMPLICATION
```

Do not begin with "what features can we extract?" Begin with the phenomenon and its reference measurement.

---

# 3. HARD BOUNDARY

Do NOT build the final implementation.

Do not implement:

* full SDB ML
* final apnea classifier
* clinical prediction
* clinical diagnosis
* production cloud
* complete ESP32 firmware
* wearable PCB
* clinical-grade SpO2
* clinical validation
* production deployment

Small exploratory computation is allowed only when it answers a research question.

Examples:

* signal visualization
* dataset inspection
* numerical sanity checks
* reproducing a published calculation
* comparing candidate algorithms on a small sample
* checking a dataset annotation
* validating a literature-derived claim

Exploratory work must not silently become Phase-E production architecture.

## 3.1 Human data and ethics

Do not collect, request, or process new human-subject data in Phase R.

If the evidence shows that own-data collection is necessary (for example, overnight MAX30105 recordings with a reference PSG), document it as a future requirement with:

* the research question it answers
* the minimum reference modalities required
* the need for ethics/IRB approval before any collection
* the dependency it creates for Phase E

## 3.2 Claim vocabulary

Use this ladder strictly:

```text
RAW MEASUREMENT
    ↓
PHYSIOLOGICAL MEASUREMENT
    ↓
CANDIDATE FEATURE
    ↓
VALIDATED FEATURE
    ↓
CLINICALLY VALIDATED BIOMARKER
```

A feature is not a biomarker because it correlates with a clinical variable.

Never convert:

```text
correlation → causation
association → clinical validity
algorithm performance → clinical validity
```

The term "clinically validated biomarker" is reserved for appropriate clinical validation evidence and must not be claimed for anything this project produces.

---

# 4. RESEARCH PRIORITIES

Every research activity receives a priority:

```text
P0 — Directly affects Phase E
P1 — Important for scientific validity
P2 — Supporting knowledge
P3 — Future research
```

Most effort must go to P0 and P1.

## P0

At minimum:

* target population and use case
* sensor site
* overnight PPG availability
* SDB ground truth
* SpO2 availability
* respiratory annotations
* sleep-time denominator
* PPG physiological measurements
* pulse detection
* PRV vs HRV
* PPG respiration
* signal quality
* reflective PPG
* validation methodology

## P1

* sleep physiology
* oximetry/desaturation physiology and scoring (note: the label-heterogeneity part of RQ6 is P0 because it gates cross-dataset validation)
* prior-art devices
* algorithm landscape
* event-level SDB physiology
* wearable deployment constraints

## P2/P3

Examples:

* advanced ML architectures
* federated learning
* advanced TinyML optimization
* speculative sensor architectures
* feature families with no immediate experimental relevance

Do not allow P2/P3 work to delay unresolved P0 questions.

---

# 5. RESEARCH BUDGETS AND STOP CONDITION

Prevent uncontrolled literature expansion.

For each P0/P1 research track:

1. Start with high-quality reviews and methodological papers.
2. Identify the key primary studies.
3. Target approximately **5–10 high-value sources per core track**.
4. Expand beyond the target only when:
   * evidence conflicts;
   * a critical claim cannot be verified;
   * a major dataset or method is missing;
   * an important methodological issue remains unresolved.

P2/P3 topics receive at most a short orientation (a few sources) unless the human owner asks for more.

## Sufficiency test

A track has sufficient evidence when additional sources are unlikely to materially change any of:

* Phase-E scope
* dataset selection
* physiological measurement definitions
* candidate algorithm sets
* validation methodology
* major architecture decisions

When a track reaches sufficiency or its budget:

```text
STOP SEARCHING
        ↓
SYNTHESIZE
        ↓
RECORD REMAINING GAPS
        ↓
MOVE TO NEXT TRACK
```

Do not optimize for paper count.

## 5.1 Search tracks

Organize searching around these tracks, using reviews to map each landscape and then following important claims to primary studies:

```text
Track A — PPG fundamentals, morphology, reflective PPG
Track B — Pulse detection, pulse rate, PRV, PRV–HRV agreement
Track C — PPG-derived respiration (AM / FM / BW)
Track D — PPG signal quality, motion artifact, wearable artifacts
Track E — Sleep physiology, PPG sleep/wake and staging
Track F — PPG and SDB (apnea, hypopnea, respiratory events)
Track G — Oximetry, desaturation, scoring rules, AHI/REI
Track H — Prior-art devices and validated systems
Track I — Wearable / real-time / embedded physiological DSP
```

Record the search strings, databases/tools used, and dates in `docs/literature/search_log.md` so the search is reproducible.

## 5.2 Evidence hierarchy

Prefer, in order:

```text
systematic reviews / meta-analyses
        ↓
high-quality methodological reviews
        ↓
primary validation studies
        ↓
official dataset documentation
        ↓
standards / official technical documentation
        ↓
conference publications
        ↓
preprints
        ↓
secondary technical sources
```

For datasets: official documentation, official repository, original dataset publication.

For sensor specifications: manufacturer datasheet and official technical documentation.

Lower-tier sources may be used only when necessary and must be labeled as such. Search-result snippets are never evidence.

---

# 6. SOURCE-VERIFICATION PROTOCOL

This is mandatory.

Never cite a paper, dataset, standard, or technical source from memory.

Every source used as evidence must be independently retrieved during this research process.

Each source record (in `docs/evidence/sources.yaml`, §33.1) must contain:

```text
source_id
title
authors
year
DOI if available
URL
source_type
evidence_tier          # position in §5.2 hierarchy
retrieval_status
read_level
access_date
```

## Read level

Every source receives exactly one:

```text
FULL_TEXT
ABSTRACT_ONLY
SECONDARY_CITATION
```

* **FULL_TEXT** — the relevant source text was actually retrieved and inspected.
* **ABSTRACT_ONLY** — only the abstract or equivalent metadata was accessible.
* **SECONDARY_CITATION** — the source is known through another paper/review but was not directly retrieved.

## 6.1 Research environment declaration

At the start of Phase R, record in `docs/literature/research_environment.md`:

* which search tools are available (web search, literature databases, connectors such as Consensus, etc.)
* whether full-text retrieval is possible, and for which sources (open access only, or broader)
* whether dataset repositories can be reached and whether data can be downloaded

This declaration sets the realistic read-level ceiling. If full text is largely unavailable, say so explicitly: it limits how many quantitative claims can be verified, and that limitation must appear in every gate report.

## 6.2 Storage of source material

* Do not copy abstracts, paragraphs, tables, or figures from sources into the repository.
* Do not store full-text copies of copyrighted papers in the repository.
* Record findings as your own paraphrased notes with the precise location (§7).
* Short quotations are permitted only where exact wording matters (for example, a scoring-rule definition), and must be brief and attributed.

---

# 7. QUANTITATIVE CLAIM VERIFICATION

Quantitative claims require stricter evidence.

Examples: MAE, RMSE, sensitivity, specificity, PPV, subject count, recording duration, sampling rate, reported AHI performance, dataset size, algorithm performance.

A quantitative claim may be used as evidence only when:

```text
read_level = FULL_TEXT
```

and the evidence record includes a location such as:

```text
table
figure
section
page
equation
```

Otherwise classify it:

```text
UNVERIFIED_FIGURE
```

and do not use it to justify a Phase-E requirement or a RESOLVED decision.

Do not reconstruct quantitative results from memory.

Dataset facts verified by directly inspecting downloaded data count as verified, with the inspection script recorded as the location.

---

# 8. REFERENCE VERIFICATION

At the end of Phase R:

* resolve every DOI in `references.bib`;
* verify every URL;
* flag failed resolutions;
* identify duplicate references;
* identify references included but not actually reviewed.

Every reference must be classified:

```text
VERIFIED_AND_REVIEWED
VERIFIED_ABSTRACT_ONLY
SECONDARY_ONLY
UNRESOLVED
```

Unresolved sources cannot be treated as evidence.

A source that cannot be retrieved may be listed under:

```text
KNOWN_TO_EXIST_NOT_REVIEWED
```

but must not support a scientific decision.

`references.bib` is generated from `sources.yaml`, not maintained separately.

---

# 9. EVIDENCE STRENGTH RUBRIC

Do not assign evidence strength arbitrarily.

Use:

```text
STRONG
MODERATE
LIMITED
CONFLICTING
INSUFFICIENT
```

Evaluate at least:

1. consistency across independent studies;
2. use of independent datasets;
3. reference-standard quality;
4. population match;
5. sleep/SDB relevance;
6. sensor/modality match;
7. reflective-vs-transmissive relevance;
8. read level;
9. methodological quality.

For each evidence-strength rating, record a one-line justification per dimension that materially affected the rating. A rating without justification is invalid.

Evidence strength is capped by source access. For example, `ABSTRACT_ONLY` sources cannot produce `STRONG` evidence for a detailed methodological or quantitative claim.

---

# 10. CLAIM STATUS

Keep evidence strength separate from claim status.

* **Evidence strength** describes the quality/consistency of evidence.
* **Claim status** describes what the project is justified in saying.

Use:

```text
ESTABLISHED
SUPPORTED
CONTEXT_DEPENDENT
PRELIMINARY
CONFLICTING
HYPOTHESIS
UNKNOWN
```

Do not automatically map one vocabulary to the other. A claim may have `MODERATE` evidence and `CONTEXT_DEPENDENT` status, for example.

Two constraints do apply:

* `ESTABLISHED` requires at least `MODERATE` evidence from sources with `FULL_TEXT` read level.
* `CONFLICTING` evidence cannot support `ESTABLISHED` or `SUPPORTED` status.

---

# 11. GATE R0 — TARGET DEFINITION

Before broad literature research, establish the working target definition.

The following are P0 open decisions:

```text
target population
target use case
intended setting
sensor site
sensor configuration
expected recording duration
primary physiological outputs
intended SDB output
```

Possible sensor sites include:

```text
finger
wrist
forehead
ear
other
```

Do not select one arbitrarily. Present evidence-based tradeoffs involving:

* signal quality
* perfusion
* motion
* comfort
* overnight feasibility
* reflective/transmissive configuration
* hardware complexity
* transferability of literature
* availability of datasets recorded at that site

The R0 research is a **focused orientation**, not the full Track A–I program: enough evidence to make the tradeoffs visible, recorded in the registries like any other evidence.

Output:

```text
docs/target_definition.md
```

containing the options, tradeoffs, recommendation, and the decision IDs involved.

At Gate R0 the human owner reviews and selects the **working** target definition.

The working target definition may be revisited at Gate R1 if dataset feasibility shows the chosen site or population cannot be studied with available data. Any such revision is recorded as a decision update, not silently applied.

---

# 12. GATE R1 — DATASET FEASIBILITY

Dataset feasibility comes before the broad literature synthesis. This gate determines whether the central research path is executable.

The critical question:

```text
Do accessible or realistically obtainable datasets provide:

OVERNIGHT PPG
+
continuous SpO2
+
PSG / physiological reference
+
respiratory-event annotations
?
```

Also determine whether data can support:

```text
subject-level validation
event-level validation
sleep-stage analysis
development → locked external validation
```

---

# 13. DATASET CANDIDATES

Investigate appropriate candidates including:

* CapnoBase
* BIDMC
* PTT-PPG
* Apnea-ECG
* UCDDB
* MIT-BIH PSG
* PSG-IPA
* MESA
* SHHS
* CFS
* MrOS
* DREAMT
* other datasets discovered through authoritative research

Do not assume modality availability from dataset names or from the presence of PSG or SpO2.

Verify documentation and, where possible, inspect actual data.

---

# 14. DATASET VERIFICATION MATRIX

For every relevant dataset record:

```text
dataset_name
dataset_type
population
subject_count
recording_duration
overnight
PPG_available
PPG_site
PPG_type
PPG_sampling_rate
PPG_wavelength
ECG_available
SpO2_available
respiration_reference
EEG
EOG
EMG
sleep_stage
sleep_staging_standard
apnea_annotations
hypopnea_annotations
hypopnea_scoring_rule
respiratory_events
AHI
AHI_definition
event_timing
artifact_annotations
accessibility
license
DUA
download_requirements
raw_data_available
documentation_quality
research_relevance
verification_status
verification_source
limitations
```

Use:

```text
VERIFIED
UNVERIFIED
NOT_AVAILABLE
```

Unknown fields must remain unknown.

Output as machine-readable and human-readable:

```text
docs/datasets/dataset_matrix.yaml
docs/datasets/dataset_landscape.md
```

---

# 15. DATASET ACCESS STATUS

Classify:

```text
PUBLIC
REGISTRATION_REQUIRED
DUA_REQUIRED
REQUEST_REQUIRED
UNAVAILABLE
UNKNOWN
```

If a promising dataset requires a DUA or access request:

* document the requirement;
* identify the application path;
* identify which research questions depend on it;
* mark the dependency in the decision registry;
* do not pretend the data are currently available.

Prepare `docs/datasets/access_checklist.md` so the human owner can begin applications immediately after Gate R1.

---

# 16. GATE R1 OUTPUT

Before proceeding to the broad research program, produce:

```text
docs/datasets/dataset_feasibility_gate.md
```

It must explicitly answer:

* **Gap A** — Do we have overnight PPG + SDB ground truth?
* **Gap B** — Do we have PPG + SpO2 + respiratory annotations?
* **Gap C** — Do we have adequate subject diversity for the working target population?
* **Gap D** — Do we have data representative of reflective wearable PPG at the working sensor site?
* **Gap E** — Can the data support subject-level validation?
* **Gap F** — Can the data support event-level SDB validation?
* **Gap G** — Can the data support development → locked external validation (separate development and held-out datasets)?
* **Gap H** — Which research questions cannot currently be answered?

Also answer:

```text
Can we investigate sleep physiology?
Can we investigate PPG-derived respiration?
Can we investigate desaturation?
Can we investigate PPG-SDB association?
Are SDB labels comparable across datasets (scoring rules, AHI definitions)?
```

Possible conclusions for each:

```text
SUPPORTED
CONDITIONALLY_SUPPORTED
NOT_SUPPORTED
UNDETERMINED
```

Do not manufacture a solution if the dataset ecosystem cannot answer the question.

## 16.1 Dataset purpose matrix

Do not only list datasets. State what each can support:

| Dataset | PPG | Pulse | Respiration | SQI | Sleep | SDB | SpO2 | ECG comparison | Development | Validation |
| ------- | --- | ----- | ----------- | --- | ----- | --- | ---- | -------------- | ----------- | ---------- |

Assign each dataset one or more roles:

```text
PRIMARY DEVELOPMENT
EXTERNAL VALIDATION
PHYSIOLOGICAL REFERENCE
ROBUSTNESS
ANNOTATION / UNCERTAINTY
NOT SUITABLE
```

and explain each assignment.

---

# 17. DATASET-FIRST CONSEQUENCE

The Gate R1 result determines research scope.

If overnight PPG + SDB data are unavailable, do not pretend that direct PPG → SDB event validation is possible. Instead, clearly separate:

```text
literature evidence
physiological evidence
PPG measurement validation
ECG cardiovascular evidence
SpO2 evidence
PSG reference evidence
direct PPG-SDB evidence
```

A missing dataset is a research limitation, not something to hide.

---

# 18. RQ1 — PPG PHYSIOLOGY

Investigate:

* photoplethysmography fundamentals
* AC/DC components
* arterial blood-volume changes
* optical wavelength
* vascular tone
* peripheral perfusion
* pulse morphology
* sensor site
* transmissive PPG
* reflective PPG

Distinguish:

```text
well established
context dependent
hypothesis
```

Do not overinterpret optical signals.

---

# 19. RQ2 — CARDIOVASCULAR INFORMATION

Investigate:

* pulse detection
* pulse rate
* pulse-to-pulse intervals
* PRV
* pulse morphology
* amplitude
* width
* rise/fall characteristics
* derivatives
* pulse arrival/transit characteristics

Explicitly distinguish:

```text
ECG → R-peaks → RR → HRV
```

from:

```text
PPG → pulse peaks → PP intervals → PRV
```

Investigate:

* PRV/HRV agreement
* pulse transit effects
* vascular effects
* perfusion
* motion
* ectopy
* posture
* temperature
* sleep stage
* autonomic state

Never equate PRV and HRV without qualification.

---

# 20. RQ3 — PPG-DERIVED RESPIRATION

Investigate:

```text
AM — amplitude modulation
FM — frequency modulation
BW — baseline modulation
```

Also investigate:

* respiratory sinus arrhythmia
* pulse morphology modulation
* cardiovascular-respiratory coupling

For each candidate method record:

```text
physiological mechanism
input
processing
sampling requirement
window
overlap
causal/non-causal
complexity
reference
validation dataset
performance
failure modes
wearable suitability
embedded suitability
```

Do not assume a method validated in daytime or controlled conditions transfers to sleep.

---

# 21. RQ4 — SLEEP PHYSIOLOGY

Investigate:

* wake
* NREM
* REM
* autonomic activity
* HR/PR
* HRV/PRV
* respiratory modulation
* peripheral vascular effects
* pulse amplitude
* pulse morphology
* posture
* movement
* sleep transitions

Explicitly distinguish:

```text
normal sleep physiology
SDB-related physiology
movement/artifact
sensor/perfusion effects
```

---

# 22. RQ5 — SDB PHYSIOLOGY

Investigate:

* obstructive apnea
* central apnea
* hypopnea
* respiratory effort
* oxygenation changes
* autonomic arousal
* cardiovascular responses
* pulse amplitude changes
* pulse-rate responses
* vascular responses

Model the physiological chain:

```text
respiratory event
    ↓
ventilation disturbance
    ↓
oxygenation / effort / pressure changes
    ↓
autonomic response
    ↓
cardiovascular response
    ↓
possible PPG manifestation
```

For each proposed PPG manifestation classify:

```text
DIRECT EVIDENCE
INDIRECT EVIDENCE
HYPOTHESIS
```

Do not assume every physiological consequence is directly observable in PPG.

---

# 23. RQ6 — OXIMETRY AND DESATURATION

Dedicated research question. Physiology and oximetry are P1; label heterogeneity is P0.

## Physiology

* oxygen saturation
* arterial oxygenation
* desaturation/recovery dynamics
* relationship between respiratory events and desaturation

## Oximetry

* transmissive pulse oximetry
* reflective pulse oximetry
* red/IR principles
* calibration
* optical path
* perfusion effects
* motion
* skin/site effects
* sensor geometry
* limitations of MAX30105-class sensing
* relevant standards for pulse oximeter accuracy

## SDB metrics

* oxygen desaturation index
* desaturation event definitions
* baseline selection
* duration criteria
* recovery criteria

## Label heterogeneity (P0)

Explicitly investigate differences in:

* 3% vs 4% desaturation criteria
* hypopnea definitions
* arousal-associated criteria
* scoring rules and their versions
* AHI definitions
* dataset-specific annotation conventions

Determine how these differences affect cross-dataset validation, and record each dataset's rule in the dataset matrix (§14).

Never treat AHI labels from different datasets as automatically equivalent.

---

# 24. RQ7 — THE DENOMINATOR PROBLEM

Investigate the difference between:

```text
AHI — Apnea-Hypopnea Index (events per hour of sleep)
```

and:

```text
REI — Respiratory Event Index (events per hour of recording/monitoring time)
```

Determine the role of EEG-based sleep time in computing AHI.

Explicitly answer:

> If the eventual device does not have EEG, what denominator can it legitimately use?

Investigate:

* sleep/wake estimation from PPG
* recording-time denominators
* estimated sleep-time denominators
* implications for severity estimation
* implications for comparison with PSG-derived AHI

This is a P0 decision. Determine whether Phase E requires PPG-only sleep/wake estimation before any severity metric can be meaningfully considered.

Do not assume AHI can simply be reproduced from PPG.

---

# 25. RQ8 — SIGNAL QUALITY

Investigate:

* motion
* contact
* sensor displacement
* ambient light
* clipping
* saturation
* low perfusion
* baseline drift
* pressure
* missing samples
* irregular sampling

Investigate SQI approaches. For each important method record:

```text
what it measures
input
reference
algorithm
features
threshold
validation
dataset
failure modes
real-time feasibility
```

Determine whether SQI should be:

```text
binary
continuous
multi-class
sample-level
segment-level
```

based on evidence and intended use. Do not decide without evidence.

---

# 26. RQ9 — REFLECTIVE PPG / MAX30105

Investigate:

* reflective PPG physics
* sensor placement
* wavelengths
* LED current
* photodiode
* ADC
* ambient-light rejection
* sampling rate
* saturation
* dynamic range
* AGC
* sensor geometry
* contact pressure

Use the manufacturer datasheet as the primary source for sensor specifications.

Explicitly determine which clinical PPG findings transfer to reflective wearable PPG and which require re-validation.

Do not describe MAX30105 output as clinically validated SpO2.

---

# 27. RQ10 — PRIOR ART AND VALIDATED DEVICES

Conduct a focused **P1** landscape review of existing systems. Investigate, where relevant:

* peripheral arterial tonometry
* WatchPAT and comparable systems
* home sleep apnea testing
* pulse-oximetry-based screening
* wearable PPG-based screening
* multimodal wearable systems

For each relevant system determine:

```text
measurement modalities
sensor site
target population
intended use
outputs
ground truth
validation design
clinical evidence
limitations
regulatory/clinical positioning where documented
```

Use peer-reviewed validation studies and official documentation, not marketing material, as evidence.

The purpose is to determine:

```text
what has already been demonstrated
what measurement strategy is already validated
what remains technically/scientifically open
where this project can make a meaningful contribution
```

---

# 28. RQ11 — PPG AND SDB

Investigate literature connecting PPG with:

* apnea
* hypopnea
* OSA
* SDB
* respiratory events
* oxygen desaturation
* autonomic responses
* sleep staging
* AHI
* event-level detection
* patient-level severity estimation

Maintain the distinction:

```text
physiological measurement
        ≠
event detection
        ≠
patient classification
        ≠
clinical diagnosis
```

These are different claims requiring different evidence.

## 28.1 Contradictory literature

When studies disagree, compare:

```text
population
dataset
sensor
sensor site
sampling rate
reference modality
algorithm
preprocessing
window length
evaluation metric
statistical method
ground truth / scoring rule
study design
```

Classify the likely cause:

```text
true scientific disagreement
methodological differences
population differences
dataset differences
measurement differences
```

Preserve uncertainty. Do not select a preferred paper arbitrarily, and do not hide contradictory evidence.

---

# 29. RQ12 — MULTIMODAL CONTEXT

Investigate how PPG relates to:

* ECG
* respiration
* SpO2
* movement
* sleep stages
* respiratory effort

Determine which signals are:

```text
reference standards
supporting modalities
potential future sensors
```

Do not add sensors simply because they improve a paper's classifier. Determine whether a modality addresses a fundamental limitation of PPG.

---

# 30. ALGORITHM LANDSCAPE

Build an evidence-based landscape for:

* pulse detection
* pulse quality
* pulse rate
* PRV
* respiration
* baseline correction
* artifact detection
* SQI
* desaturation detection where applicable
* sleep/wake estimation where RQ7 requires it

For each algorithm record:

```text
algorithm
target
input
reference
processing
assumptions
sampling requirements
window
overlap
causal/non-causal
complexity
validation datasets
performance
failure modes
wearable suitability
embedded suitability
evidence quality
```

Do not choose a "best algorithm", and do not choose algorithms because they are popular or easy to implement.

Produce candidate sets and identify the experiments needed to discriminate between them.

---

# 31. FEATURE TAXONOMY

Construct:

```text
PPG
│
├── Pulse Timing
│   ├── pulse intervals
│   ├── pulse rate
│   └── PRV
│
├── Pulse Morphology
│   ├── amplitude
│   ├── width
│   ├── rise/fall
│   └── derivatives
│
├── Respiratory Modulation
│   ├── AM
│   ├── FM
│   └── baseline modulation
│
├── Signal Quality
│   ├── SQI
│   ├── clipping
│   └── artifact burden
│
├── Oxygenation
│   ├── experimental SpO2
│   └── desaturation metrics
│
└── Cross-modal
    ├── PPG ↔ ECG
    ├── PPG ↔ respiration
    └── PPG ↔ SpO2
```

Classify each as:

```text
RAW MEASUREMENT
PHYSIOLOGICAL MEASUREMENT
CANDIDATE FEATURE
VALIDATED FEATURE
```

No feature produced by Phase R research alone is a VALIDATED FEATURE for this project; published validation is evidence toward it, and project-level validation happens in Phase E.

---

# 32. VALIDATION FRAMEWORK

For every proposed measurement define:

```text
measurement
reference standard
alignment
primary metric
secondary metrics
unit of inference
uncertainty
failure modes
dataset
```

Examples:

```text
pulse rate   → ECG / reference pulse annotations
respiration  → capnogram / impedance respiration
oxygenation  → validated reference SpO2
SDB event    → PSG annotation (with scoring rule recorded)
sleep time   → PSG sleep staging
```

Do not assume a proxy is equivalent to the reference.

---

# 33. STATISTICAL DISCIPLINE

Explicitly define the inference unit:

```text
sample
pulse
event
window
recording
subject
```

Repeated windows from the same subject are not independent subjects.

Where appropriate:

* subject-level summaries
* repeated-measures methods
* subject-level bootstrap
* event-level metrics
* subject-level metrics

Agreement methods may include: MAE, RMSE, bias, Bland–Altman limits of agreement.

Detection methods may include: sensitivity, PPV, F1, false positives, false negatives, timing error.

Metrics must be declared before experiments are interpreted.

## 33.1 Registry conventions and integrity

All registries live under `docs/` as YAML and are the single sources of truth:

```text
docs/evidence/sources.yaml            SRC-###
docs/evidence/evidence.yaml           EVD-###
docs/evidence/claims.yaml             CLM-###
docs/decisions/decisions.yaml         DEC-###
docs/experiments/experiments.yaml     EXP-<AREA>-###
docs/requirements/phase_e_requirements.yaml   REQ-###
docs/research_gaps.yaml               GAP-###
```

Rules:

* IDs are stable and never reused.
* Markdown documents reference IDs; they do not restate registry content as independent facts.
* Human-readable Markdown views (§43, §46) are generated from registries by a small script, or, if written by hand, must contain only IDs plus narrative that does not contradict the registry.

Create a small integrity check (for example `scripts/check_registries.py`) that verifies:

* every YAML file parses and has the required fields
* every referenced ID exists
* no RESOLVED decision relies solely on `UNVERIFIED_FIGURE` evidence or `ABSTRACT_ONLY` sources for quantitative justification
* every requirement traces to at least one decision, or is labeled `ENGINEERING ASSUMPTION`
* every evidence record's `source_id` exists in `sources.yaml`

The integrity check must pass at each gate.

---

# 34. EXPERIMENT REGISTRY

Single source of truth:

```text
docs/experiments/experiments.yaml
```

Do not duplicate experiment definitions in other documents.

Each experiment:

```yaml
id:
question:
hypothesis:
priority:
dataset:
population:
input:
reference:
candidate_method:
parameters:
primary_metric:
secondary_metrics:
statistical_method:
unit_of_inference:
decision_affected:
acceptance_condition:
failure_condition:
status:
```

Every experiment must resolve a meaningful uncertainty. Do not create experiments to increase the count.

---

# 35. DECISION REGISTRY

Single source of truth:

```text
docs/decisions/decisions.yaml
```

Do not maintain a second independent decision registry in Markdown. Documents reference decision IDs.

Each decision:

```yaml
id:
question:
status:
priority:
evidence_ids:
candidate_options:
advantages:
limitations:
experiments_required:
recommendation:
confidence:
phase_e_implication:
human_review_required:
provisional_rationale:      # required when PROVISIONAL
invalidation_conditions:    # required when PROVISIONAL
```

Statuses:

```text
OPEN
PROVISIONAL
RESOLVED
REJECTED
NOT_APPLICABLE
```

Rules:

* Use OPEN when evidence cannot yet support a defensible choice.
* Use PROVISIONAL when a reversible choice is necessary for an experiment; record why it was necessary, the evidence/rationale, what could invalidate it, and the experiment required for resolution.
* Only the human owner sets RESOLVED for scientific and scope decisions. The agent recommends.

---

# 36. REQUIREMENTS REGISTRY

Single source of truth:

```text
docs/requirements/phase_e_requirements.yaml
```

Each requirement:

```yaml
id:
requirement:
reason:
evidence_ids:
decision_ids:
experiment_ids:
priority:
dependency:
phase_e_component:
acceptance_criterion:
traceability_type:     # EVIDENCE | ENGINEERING_CONSTRAINT | ENGINEERING_ASSUMPTION
status:
```

Do not restate requirements independently in multiple documents.

---

# 37. EVIDENCE REGISTRY

```text
docs/evidence/evidence.yaml
```

Each evidence record:

```yaml
id:
source_id:
claim:
topic:
research_question:
read_level:
location:
evidence_strength:
strength_justification:
population:
dataset:
modality:
reference_standard:
finding:
limitations:
phase_e_implication:
```

Quantitative claims without full-text location are `UNVERIFIED_FIGURE` and cannot support a RESOLVED decision.

Gate reports present a human-readable **evidence matrix** view generated from this registry.

---

# 38. CLAIM REGISTRY

```text
docs/evidence/claims.yaml
```

Each claim:

```yaml
id:
claim:
claim_type:
evidence_ids:
status:
confidence:
limitations:
decision_ids:
requirement_ids:
```

This creates:

```text
CLAIM → EVIDENCE → DECISION → REQUIREMENT
```

If evidence does not support a claim, do not force a positive conclusion.

---

# 39. TRACEABILITY REQUIREMENT

Every major Phase-E requirement must be traceable:

```text
PHASE-E REQUIREMENT
        ↓
DECISION
        ↓
RESEARCH QUESTION / GAP
        ↓
EXPERIMENT
        ↓
EVIDENCE
        ↓
SOURCE
```

If a requirement cannot be traced to evidence or an explicitly labeled engineering constraint, mark it `ENGINEERING ASSUMPTION`.

Do not disguise assumptions as scientific findings.

---

# 40. EXPLORATORY DATA RULES

Carry forward the engineering data discipline:

* Raw datasets remain outside the repository unless licensing permits otherwise.
* Use an explicit configurable data root (environment variable).
* Raw data is read-only.
* If data are unavailable, report `DATA_UNAVAILABLE` with the reason and the human action required.
* Do not silently substitute synthetic data. Synthetic data may test algorithm mechanics only and must never be presented as biological or dataset validation.

Exploratory code lives under `exploratory/`, is labeled exploratory, and is disposable unless deliberately promoted in Phase E.

Prefer reproducible scripts. Notebooks are allowed only if they are deterministic, executable from a clean environment, saved with their dependencies, and accompanied by an execution mechanism.

Every exploratory result that is used as evidence records:

```text
dataset and version
script path and git commit
configuration / parameters
random seed where applicable
software environment
output location
```

and is entered in `evidence.yaml` with the script as its location.

---

# 41. RESEARCH GAPS

Registry:

```text
docs/research_gaps.yaml
```

with a generated or ID-referencing view in `docs/research_gaps.md`.

Categories:

```text
LITERATURE GAP
DATASET GAP
PHYSIOLOGICAL GAP
MEASUREMENT GAP
ALGORITHM GAP
VALIDATION GAP
HARDWARE GAP
EMBEDDED GAP
CLINICAL TRANSLATION GAP
ACCESS GAP          # evidence exists but could not be retrieved/read
```

For each gap:

```text
id
gap
category
evidence
why it matters
current workaround
experiment needed
priority
phase affected
```

## 41.1 What not to do

Do not:

```text
collect hundreds of papers without synthesis
produce an enormous bibliography with no decisions
copy abstracts or source text into the repository
treat search snippets as evidence
cite from memory
assume dataset modalities
assume PPG = ECG or PRV = HRV
assume MAX30105 SpO2 is clinically valid
assume daytime validation = overnight validation
assume clinical PPG = reflective wearable PPG
treat AHI labels from different datasets as equivalent
choose algorithms because they are popular or easy
design ML before understanding the physiology
implement before understanding the evidence
hide contradictory evidence
force questions toward a positive result
keep researching after decisions are sufficiently supported
```

---

# 42. CHALLENGE ASSUMPTIONS

Explicitly challenge:

```text
PPG pulse peaks = ECG R-peaks
PRV = HRV
PPG respiration is universally reliable
MAX30105 can produce clinically valid SpO2 without calibration
clinical transmissive PPG transfers directly to reflective wearable PPG
high algorithm performance = embedded suitability
correlation with AHI = clinical usefulness
ML can compensate for poor physiological measurement
sleep-stage changes = SDB changes
respiratory events always create obvious PPG signatures
more features = better model
larger datasets = better datasets
AHI can be directly reproduced without knowing sleep time
AHI labels are comparable across datasets
```

For every assumption:

```text
supporting evidence
contradicting evidence
conditions where valid
conditions where invalid
Phase-E implication
```

Record each as a claim in `claims.yaml`.

---

# 43. PHASE-E REQUIREMENT DERIVATION

Do not simply state "Phase E should implement respiration."

Derive:

```text
Evidence
   ↓
Research finding
   ↓
Gap / uncertainty
   ↓
Decision
   ↓
Experiment
   ↓
Requirement
   ↓
Implementation
```

Create:

```text
docs/requirements/phase_e_requirements.md
```

as a human-readable view generated from the requirements registry.

---

# 44. PHASE-R → PHASE-E BRIDGE

Create:

```text
docs/phase_r_to_phase_e_bridge.md
```

This is the formal handoff. It must contain:

```text
1. Original intended scope
2. Current target definition
3. Dataset feasibility result
4. What evidence supports
5. What evidence does not support
6. What changed
7. What was rejected
8. What remains uncertain
9. Required datasets
10. Required measurements
11. Required experiments
12. Candidate algorithms
13. Deferred algorithms
14. Validation strategy
15. Phase-E architecture
16. Phase-E requirements
17. Open decisions
18. Risks
19. Acceptance criteria
```

For every major existing component classify:

```text
KEEP
MODIFY
ADD
DEFER
REMOVE
```

At minimum: dataset abstraction, schema, experiment registry, PPG processing, SQI, pulse detection, respiration, feature extraction, streaming reference, native C++, ESP32 HAL, SpO2, sleep/wake estimation, SDB association, ML.

Sections 9–17 reference registry IDs rather than restating content.

---

# 45. FINAL RESEARCH SYNTHESIS

Create:

```text
docs/phase_r_research_synthesis.md
```

Structure:

```text
1. Executive Summary
2. Target Definition
3. Dataset Feasibility
4. PPG Physiological Foundations
5. Cardiovascular Information
6. PRV vs HRV
7. PPG-Derived Respiration
8. Sleep Physiology
9. SDB Physiology
10. Oximetry and Desaturation
11. AHI / REI / Sleep-Time Denominator
12. PPG and SDB Evidence
13. Signal Quality
14. Reflective PPG / MAX30105
15. Prior-Art Devices
16. Multimodal Context
17. Algorithm Landscape
18. Feature Taxonomy
19. Validation Framework
20. Research Gaps (ID references)
21. Phase-E Requirements (ID references)
22. Decisions (ID references)
23. Proposed Experiments (ID references)
24. Limitations (including research-environment and access limitations)
25. References
```

## 45.1 Synthesis standard

This must be a synthesis, not an annotated bibliography. For each topic section answer:

```text
What is known?
What is consistently supported?
Where do studies disagree, and why might they?
What populations, references, and datasets were used?
What methodological differences matter?
What remains unknown?
What does this mean for this project?
```

---

# 46. FINAL DECISION DOCUMENT

Create a human-readable view generated from the decision registry:

```text
docs/decisions/phase_r_decisions.md
```

It must answer:

```text
What should Phase E build?
What should Phase E not build?
Which datasets should Phase E use?
Which measurements should Phase E validate?
Which algorithms should Phase E investigate?
Which algorithms should be deferred?
What assumptions require testing?
What remains unknown?
What decisions remain open?
What experiments must happen before decisions can be resolved?
```

---

# 47. PHASE R ACCEPTANCE CRITERIA

Phase R is complete only when the following are answered with documented evidence or explicitly documented uncertainty.

## Scientific

```text
what PPG measures
what physiological measurements are defensible
what PRV means and how it relates to HRV
how respiration manifests in PPG
what changes during sleep
what changes during SDB
what desaturation means
how oximetry relates to SDB
what denominator a PPG-only device can legitimately use
```

## Dataset

```text
which datasets contain PPG / overnight PPG / SpO2 / PSG
which contain respiratory annotations and event-level ground truth
which scoring rules each uses
which are accessible
which support development and which support external validation
what critical gaps remain
```

## Methodology

```text
reference measurements
alignment requirements
primary metrics
unit of inference
statistical methodology
validation limitations
```

## Engineering

```text
what Phase E should implement
what should be deferred
what should be removed
what new components are required
```

## Evidence integrity

```text
research environment declared
search log complete
verified references with explicit read levels
traceable quantitative claims
evidence strength with justifications
claim status
decision, requirement, experiment, and gap IDs
registry integrity check passing
```

---

# 48. GATE R2 — HUMAN REVIEW

At the end of Phase R: **STOP.** Do not begin Phase E automatically.

Present:

```text
1. Research synthesis
2. Dataset feasibility
3. Evidence matrix (generated view)
4. Key findings
5. Contradictions
6. Research gaps
7. Proposed experiments
8. Decisions
9. Phase-E requirements
10. Phase-R → Phase-E bridge
11. Recommended Phase-E architecture
12. Open decisions requiring human review
```

The human project owner reviews:

* target population
* use case
* sensor site
* dataset strategy
* major scientific decisions
* Phase-E scope

Only after this review should the Phase-E implementation prompt be generated.

## 48.1 Gate report format (applies to R0, R1 and R2)

Every gate report begins with:

```text
GATE:
STATUS:
COMPLETED:
EVIDENCE STATUS (sources by read level):
DATASETS VERIFIED / UNAVAILABLE:
KEY FINDINGS:
OPEN DECISIONS:
PROVISIONAL DECISIONS:
DECISIONS REQUIRING HUMAN REVIEW:
BLOCKERS:
ACCESS LIMITATIONS:
RISKS:
FILES CREATED / MODIFIED:
REGISTRY INTEGRITY CHECK:
NEXT STEP:
```

followed by the 9-part report:

```text
Objective
Evidence
Analysis
Decision
Open Decisions
Risks
Implementation
Validation
Next Step
```

## 48.2 Escalation

If a P0 track cannot reach sufficiency because sources cannot be retrieved or read:

* record an `ACCESS GAP` in the gap registry
* state what evidence exists but could not be verified
* do not substitute recall for retrieval
* escalate it in the next gate report under BLOCKERS

If a P0 question cannot be answered at all with available evidence, record it as `UNDETERMINED` with the reason. An honest `UNDETERMINED` is an acceptable Phase R outcome; a fabricated answer is not.

---

# 49. REGENERATING PHASE E

Do not execute the previous engineering prompt unchanged.

After Gate R2, generate a new Phase-E execution specification from:

```text
docs/phase_r_to_phase_e_bridge.md
docs/requirements/phase_e_requirements.yaml
docs/decisions/decisions.yaml
docs/experiments/experiments.yaml
docs/datasets/dataset_matrix.yaml
```

The regenerated Phase-E plan supersedes assumptions made before Phase R. The original engineering architecture is reference material, not authority.

Engineering-discipline elements from the earlier engineering prompt (three-tier computational reference, locked evaluation, provenance manifests, time/unit contracts, decision lifecycle) are carried forward unless the bridge explicitly marks them MODIFY or REMOVE with traceable reasons.

---

# 50. EXECUTION ORDER

```text
STEP 1
Inspect existing project documentation.
Declare the research environment (§6.1).
Initialize registries and the integrity check.

        ↓

STEP 2
Establish target population, use case,
sensor site, and primary outputs (focused orientation).

        ↓

GATE R0 — human review of target definition.

        ↓

STEP 3
Dataset landscape, verification matrix,
label-heterogeneity check, critical-gap analysis.

        ↓

STEP 4
Access / DUA dependencies and access checklist.

        ↓

GATE R1 — human review of dataset feasibility.

        ↓

STEP 5
P0/P1 literature research (Tracks A–I, within budgets).

        ↓

STEP 6
Physiological, algorithm, and validation maps.

        ↓

STEP 7
Prior art and validated systems.

        ↓

STEP 8
Contradictions, unknowns, research gaps.

        ↓

STEP 9
Decision-relevant experiments.

        ↓

STEP 10
Derive Phase-E requirements.

        ↓

STEP 11
Audit the original engineering architecture.

        ↓

STEP 12
Reference verification (§8), integrity check,
bridge and synthesis.

        ↓

GATE R2 — human scientific/scope review.

        ↓

STOP.
```

At each gate, stop and wait for the human owner. Do not continue past a gate on your own judgment.

---

# 51. FINAL SUCCESS CRITERION

Phase R succeeds if it substantially reduces uncertainty about:

```text
WHAT WE KNOW
WHAT WE DON'T KNOW
WHAT WE CAN MEASURE
WHAT WE CANNOT MEASURE
WHAT DATA WE HAVE
WHAT DATA WE NEED
WHAT MUST BE TESTED
WHAT CAN BE IMPLEMENTED
WHAT SHOULD NOT YET BE IMPLEMENTED
```

The final objective is not "produce a comprehensive literature review." It is:

```text
EVIDENCE
   +
UNDERSTANDING
   +
DATASET FEASIBILITY
   +
GAPS
   +
EXPERIMENTS
   +
DECISIONS
        ↓
THE SMALLEST SCIENTIFICALLY DEFENSIBLE
PHASE-E IMPLEMENTATION
```

---

# 52. FINAL QUESTION

At Gate R2, answer explicitly:

> **Given the current scientific evidence, verified datasets, physiological understanding, identified gaps, prior art, and proposed validation experiments, what is the smallest scientifically defensible Phase-E implementation that will generate the next meaningful body of knowledge?**

Stop there.

Do not build it until the human project owner approves the Phase-R → Phase-E bridge.
