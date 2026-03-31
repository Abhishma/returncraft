
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import review_case
from .utils import load_jsonl

def main() -> None:
    parser = argparse.ArgumentParser(description="Run eval over seeded review cases.")
    parser.add_argument("gold_path")
    args = parser.parse_args()

    golds = load_jsonl(Path(args.gold_path))
    total = len(golds)
    status_ok = 0
    escalation_ok = 0
    citation_hit_score = 0
    rows = []

    for g in golds:
        pred = review_case(g["case"])
        st_ok = pred["status"] == g["expected_status"]
        esc_ok = pred["escalation_required"] == g["should_escalate"]
        expected_citations = set(g["expected_citations"])
        predicted_citations = set(pred["policy_citations"])
        if expected_citations:
            citation_hit_score += len(expected_citations & predicted_citations) / len(expected_citations)
        else:
            citation_hit_score += 1.0 if not predicted_citations else 0.0

        status_ok += int(st_ok)
        escalation_ok += int(esc_ok)

        rows.append({
            "case_id": g["case_id"],
            "predicted_status": pred["status"],
            "expected_status": g["expected_status"],
            "predicted_citations": sorted(predicted_citations),
            "expected_citations": sorted(expected_citations),
            "status_ok": st_ok,
            "escalation_ok": esc_ok
        })

    summary = {
        "total_cases": total,
        "status_accuracy": round(status_ok / total, 3) if total else 0.0,
        "escalation_accuracy": round(escalation_ok / total, 3) if total else 0.0,
        "citation_recall_score": round(citation_hit_score / total, 3) if total else 0.0,
        "rows": rows
    }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
