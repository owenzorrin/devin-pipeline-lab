# Review guidelines

## Money handling (`src/ledger/`)
- Amounts are always integer cents. Flag any code that stores, returns or
  does arithmetic on money as `float`.
- Conversions between dollars and cents must go through `Decimal` with
  `ROUND_HALF_UP`. Flag `round()`, `int(x * 100)` on floats, or any other
  rounding mode.
- `parse_amount` must reject ambiguous input (e.g. double negatives like
  `-$-3`) with `ValueError` rather than guessing. Flag changes that make it
  silently accept malformed amounts.
- `format_cents` output must round-trip through `parse_amount`. Flag changes
  that break this for negatives or large values.

## Tests
- New or changed behavior in `src/ledger/` needs a test in `tests/`. Flag
  PRs that change behavior without one.
- Edge cases worth checking: zero, negatives, thousands separators, a single
  cent, and values with more than two decimal places.

## Repo process
- CI runs `ruff check .`, `ruff format --check .` and `pytest -q`; line length
  is 88. Flag lines or imports that will fail these.
- The PR description must fill every section of
  `.github/pull_request_template.md`. Flag ticked checkboxes for work the diff
  does not show.
- Do not flag `scripts/fault.sh`: it intentionally injects faults for drills.
