## Problem

Finance pasted amounts from a spreadsheet into the invoicing tool and two things broke.

1. `parse_amount` rejects amounts that use thousands separators or accounting-style
   negatives. Both of these raise `ValueError` today:
   - `"1,234.50"` should be `123450`
   - `"(12.00)"` should be `-1200`
   - `"-$3.25"` and `"$-3.25"` should both be `-325`
2. `format_cents` prints negative amounts wrong. `format_cents(-5)` returns `"$-1.95"`.
   It should return `"-$0.05"`. `format_cents(-1234)` should return `"-$12.34"`.

## Acceptance criteria

- [ ] All examples above work and have tests in `tests/test_money.py`.
- [ ] Existing tests still pass.
- [ ] `ruff check .`, `ruff format --check .` and `pytest -q` pass, same as CI.
- [ ] PR uses the repo PR template and says `Closes #1`.

## Out of scope

Currency symbols other than `$`, and locale-specific separators such as `1.234,50`.
