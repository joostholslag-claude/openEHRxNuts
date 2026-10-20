#!/usr/bin/env python3
"""Validate the OPA datasource JSON against the JSON Schema.

Usage (from the repository root):

    python3 Authorisation/scripts/validate_datasource.py

Exits 0 when the instance is valid, 1 otherwise. Requires the
`jsonschema` package (pip install jsonschema).
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "access_policy.rego.schema.json"
INSTANCES = [ROOT / "policies" / "datasources" / "acp_access_policy_for_rego.json"]


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(schema)
    exit_code = 0
    for instance_path in INSTANCES:
        instance = json.loads(instance_path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            exit_code = 1
            print(f"INVALID {instance_path.relative_to(ROOT.parent)}")
            for error in errors:
                location = "/".join(str(p) for p in error.path) or "(root)"
                print(f"  {location}: {error.message}")
        else:
            print(f"valid   {instance_path.relative_to(ROOT.parent)}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
