
from __future__ import annotations
from typing import Any

CLAUSE_TEXT = {
    "damage_or_defect": "Claims for damaged or defective items may be approved if submitted within policy window and supported by clear photo evidence.",
    "wrong_item": "Claims for wrong-item delivery may be approved if order mismatch is verified.",
    "delayed_delivery": "Late-delivery complaints may qualify for partial goodwill credit but not full refund unless item is unusable.",
    "discounted_item_exclusion": "Discounted items are not eligible unless damaged, defective, or wrong item was delivered.",
    "international_return_exclusion": "International orders are not eligible unless damage or wrong item is confirmed with evidence.",
    "evidence_required": "Photos or equivalent evidence are required for damage claims.",
    "manager_discretion": "Borderline cases, repeat claimant cases, and policy conflicts must be escalated.",
}

def detect_missing_evidence(case: dict[str, Any]) -> list[str]:
    missing = []
    evidence = [e.lower() for e in case.get("evidence_available", [])]
    claim_type = case.get("claim_type", "")
    if claim_type == "damage_or_defect" and not any("photo" in e for e in evidence):
        missing.append("No photo evidence for damage claim")
    if claim_type == "wrong_item" and not evidence:
        missing.append("No mismatch evidence provided for wrong-item claim")
    return missing

def should_abstain(case: dict[str, Any], citations: list[str], missing: list[str]) -> tuple[bool, list[str]]:
    reasons = []
    if case.get("policy_version") == "conflict":
        reasons.append("Conflicting policy version context")
    if not citations:
        reasons.append("No safely grounded policy clause available")
    if case.get("claim_type") == "damage_or_defect" and "No photo evidence for damage claim" in missing:
        reasons.append("Insufficient evidence for damage recommendation")
    return bool(reasons), reasons

def grounded_citations(case: dict[str, Any]) -> list[str]:
    claim_type = case.get("claim_type", "")
    citations = []
    if claim_type == "damage_or_defect":
        citations.extend(["damage_or_defect", "evidence_required"])
        if case.get("discounted_item"):
            citations.append("discounted_item_exclusion")
    elif claim_type == "wrong_item":
        citations.append("wrong_item")
        if case.get("international_order"):
            citations.append("international_return_exclusion")
    elif claim_type == "delayed_delivery":
        citations.append("delayed_delivery")

    if case.get("repeat_claimant"):
        citations.append("manager_discretion")
    return citations

def evidence_used(case: dict[str, Any]) -> list[str]:
    out = list(case.get("evidence_available", []))
    if case.get("discounted_item"):
        out.append("discounted item flag")
    if case.get("international_order"):
        out.append("international order flag")
    if case.get("repeat_claimant"):
        out.append("repeat claimant flag")
    return out

def options_for_case(case: dict[str, Any], citations: list[str], missing: list[str]) -> list[str]:
    claim_type = case.get("claim_type", "")
    opts = []
    if claim_type == "damage_or_defect" and "No photo evidence for damage claim" not in missing:
        opts.append("Approve damage claim review under damaged/defective item clause")
        opts.append("Confirm damage evidence is sufficient before any refund decision")
    elif claim_type == "delayed_delivery":
        opts.append("Offer partial goodwill credit rather than full refund")
        opts.append("Verify carrier delay details before final resolution")
    elif claim_type == "wrong_item":
        opts.append("Verify order mismatch and consider replacement or refund path")
    else:
        opts.append("Escalate for human review")

    if case.get("repeat_claimant"):
        opts.append("Escalate due to repeat claimant pattern and borderline evidence")
    return opts[:4]

def escalation_required(case: dict[str, Any], missing: list[str]) -> bool:
    return bool(
        case.get("repeat_claimant") or
        case.get("policy_version") == "conflict" or
        (case.get("international_order") and case.get("claim_type") in {"damage_or_defect", "wrong_item"} and missing)
    )

def confidence_band(case: dict[str, Any], missing: list[str], citations: list[str]) -> str:
    if case.get("policy_version") == "conflict" or missing:
        return "low"
    if len(citations) >= 2:
        return "medium"
    return "low"
