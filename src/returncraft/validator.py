
from __future__ import annotations
from pathlib import Path
from jsonschema import validate

from .utils import load_json

ROOT = Path(__file__).resolve().parents[2]

def validate_case(case: dict) -> None:
    schema = load_json(ROOT / "schemas" / "case_input.schema.json")
    validate(instance=case, schema=schema)

def validate_review(review: dict) -> None:
    schema = load_json(ROOT / "schemas" / "review_output.schema.json")
    validate(instance=review, schema=schema)
