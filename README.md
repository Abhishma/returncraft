# Returncraft

AI-assisted returns and refund exception handling with policy grounding, evidence traceability, and human review.

## Why this exists

Refund decisions look simple until they are not.

The hardest cases are exactly where inconsistency appears:
- damaged item with weak proof
- delayed shipment with mixed blame
- discounted item exception requests
- goodwill vs abuse tension
- conflicting policy versions
- repeat claimant patterns

This problem originates in real ecommerce CX operations where reviewer inconsistency on ambiguous cases creates customer experience variance and policy application risk. The recurring failure is not a lack of policy but the absence of a system that grounds case reviews in the policy version active at case time.

**Returncraft** helps reviewers handle these cases by producing:
- policy-linked resolution options
- evidence summary
- missing information checklist
- escalation guidance
- confidence band
- abstention when the case is under-grounded

This is **not** an auto-refund bot.
It is a review support system for high-variance operational decisions.

## Policy versioning architecture

This repo implements a versioned policy index (`policies/policy_index.json`) referencing `policy_v1.md` and `policy_v2.md`. Every case review is resolved against the policy version active at case time, not the current policy. This is a deliberate design choice reflecting real operational pain: policy updates create a window of ambiguous edge cases that must be resolved against the policy the customer reasonably expected to apply.

This architecture is one of the key PM design decisions in the repo — most AI demos skip policy versioning entirely and treat policy as a static input.

## What it does

Input:
- order facts
- case transcript
- evidence metadata
- policy text
- policy version

Output:
- decision options
- cited policy clauses
- evidence used
- missing evidence
- escalation triggers
- abstention when confidence is weak

## What it does not do

- It does not auto-approve refunds
- It does not auto-deny refunds
- It does not invent policy clauses
- It does not replace final human review

## Run

```bash
pip install -r requirements.txt
export PYTHONPATH=src
python -m returncraft.cli data/example_case_001.json
python -m returncraft.eval_runner eval/goldens/review_cases.jsonl
streamlit run streamlit_app.py
```

## Design choices

- **Policy citation is mandatory for recommendations** — no resolution option is surfaced without a traced clause reference
- **Policy versioning by design** — case reviews reference the policy version active at case creation, not the current policy
- **Escalation is a feature, not a failure** — cases with policy conflict or weak evidence surface an escalation path rather than forcing a resolution
- **Abstention is preferred over unsupported certainty** — the system refuses to recommend when case grounding is insufficient
- **v1 uses constrained rule-based policy matching** — this is intentional. Auditable, clause-traceable matching is more appropriate in a review workflow than a model inferring policy intent from prose.

## Repo structure

- `src/returncraft/` — core implementation
- `data/` — example and synthetic cases
- `policies/` — versioned policy files and index
- `schemas/` — case input and review output JSON schemas
- `eval/` — rubrics and evaluation harness
- `demo/` — sample reviews

## Portfolio point

This repo is about trustworthy exception handling under policy and uncertainty. The PM design decisions are the artifact: policy versioning, citation requirements, escalation logic, and abstention conditions — not the classifier.

## Known limitations

- policy matching is narrow and rule-like in v1
- synthetic cases simplify how messy real CX evidence can be
- citations are clause-level, not legal interpretation
- next upgrade: richer synthetic case set, semantic policy matching layer, HTML review export

## Where automation stops

- no refund or denial is executed automatically
- no case is auto-closed
- escalation remains a human workflow
- policy ambiguity forces abstention rather than overclaiming

## Trust boundary

This project is decision support, not automation. It produces structured outputs for human review and abstains when case evidence or policy grounding is insufficient.
