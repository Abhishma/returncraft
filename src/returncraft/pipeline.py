
from __future__ import annotations
from typing import Any

from .logic import (
    grounded_citations,
    detect_missing_evidence,
    should_abstain,
    options_for_case,
    evidence_used,
    escalation_required,
    confidence_band,
)
from .validator import validate_case, validate_review

def review_case(case: dict[str, Any]) -> dict[str, Any]:
    validate_case(case)

    citations = grounded_citations(case)
    missing = detect_missing_evidence(case)
    abstain, reasons = should_abstain(case, citations, missing)

    if abstain:
        review = {
            "case_id": case["case_id"],
            "status": "abstained",
            "confidence_band": "low",
            "options": [
                "Do not make a recommendation until policy grounding or evidence is complete",
                "Escalate for human review"
            ],
            "policy_citations": [],
            "evidence_used": evidence_used(case),
            "missing_evidence": list(dict.fromkeys(missing + reasons)),
            "escalation_required": True
        }
        validate_review(review)
        return review

    review = {
        "case_id": case["case_id"],
        "status": "review_ready",
        "confidence_band": confidence_band(case, missing, citations),
        "options": options_for_case(case, citations, missing),
        "policy_citations": citations,
        "evidence_used": evidence_used(case),
        "missing_evidence": missing,
        "escalation_required": escalation_required(case, missing)
    }
    validate_review(review)
    return review
