
from returncraft.pipeline import review_case

def test_abstain_on_policy_conflict():
    case = {
        "case_id": "T-1",
        "order_id": "ORD-X",
        "case_summary": "Damage claim with conflicting policy notes",
        "days_since_delivery": 8,
        "evidence_available": ["chat transcript"],
        "discounted_item": False,
        "international_order": False,
        "claim_type": "damage_or_defect",
        "repeat_claimant": False,
        "policy_version": "conflict"
    }
    review = review_case(case)
    assert review["status"] == "abstained"

def test_delayed_delivery_gets_policy_citation():
    case = {
        "case_id": "T-2",
        "order_id": "ORD-Y",
        "case_summary": "Late delivery complaint",
        "days_since_delivery": 1,
        "evidence_available": ["carrier delay note"],
        "discounted_item": False,
        "international_order": False,
        "claim_type": "delayed_delivery",
        "repeat_claimant": False,
        "policy_version": "v2"
    }
    review = review_case(case)
    assert "delayed_delivery" in review["policy_citations"]
