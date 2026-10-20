# Authorisation

An experiment to express access control policy (authorisations) for openEHR data,
based on Nuts verifiable credentials. It addresses
[upstream issue #11](https://github.com/jorritspee/openEHRxNuts/issues/11); the first
OPA/Rego draft was contributed in
[upstream PR #14](https://github.com/jorritspee/openEHRxNuts/pull/14).

[DESIGN.md](DESIGN.md) reviews that draft and proposes how to standardise the
evaluation input, the resource scope and the policy format (in Dutch).

## Contents

| Path | What |
|---|---|
| `policies/rules/openEHR_template_id.rego` | Generic Rego rule: `allow` is true when the template id and the user role are both allowed for the operation |
| `policies/datasources/acp_access_policy_for_rego.json` | The ACP-specific data the rule reads: allowed template ids and roles per operation |
| `policies/openehr_tests/openehr_template_test.rego` | Unit tests for the rule |
| `access_policy.rego.schema.json` | JSON Schema (draft-07) that the datasource file must conform to |
| `scripts/validate_datasource.py` | Validates the datasource file against the schema |
| `docs/` | Architecture diagram (draw.io, PNG, PDF) and a screenshot of the policy in an editor |
| `DESIGN.md` | Design proposal for issue #11 |

## Running the tests locally

You need the [OPA](https://www.openpolicyagent.org/docs/#running-opa) binary
(version 1.x) and Python 3 with the `jsonschema` package. Run everything from the
repository root:

```sh
opa fmt --fail --list Authorisation/policies
opa check --strict Authorisation/policies
opa test Authorisation/policies -v
python3 -m pip install jsonschema
python3 Authorisation/scripts/validate_datasource.py
```

The same commands run in CI on every push and pull request that touches this
directory, see [`.github/workflows/authz.yml`](../.github/workflows/authz.yml).

Note that plain OPA loads a JSON file under its directory path, so the datasource
is available to the rule as `data.datasources`, not under its file name. This is
why the rule imports `data.datasources` and not
`data.datasources["acp_access_policy_for_rego.json"]` (which only works in Styra
DAS).
