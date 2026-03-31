
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import review_case
from .utils import load_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Review a returns/refund case.")
    parser.add_argument("case_path", help="Path to case JSON file")
    args = parser.parse_args()

    case = load_json(Path(args.case_path))
    review = review_case(case)
    print(json.dumps(review, indent=2))

if __name__ == "__main__":
    main()
