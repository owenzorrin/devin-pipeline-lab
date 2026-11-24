"""Money helpers. Amounts are always stored as integer cents."""

import os
import re
from decimal import ROUND_HALF_UP, Decimal

_AMOUNT = re.compile(
    r"(?P<neg1>-)?\$?(?P<neg2>-)?"
    r"(?P<num>(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d*)?|\.\d+)"
)


def parse_amount(text: str) -> int:
    """Parse a human-entered amount into cents.

    Accepts "12.50", "$3", "1,234.50", "-$3.25", "$-3.25" and accounting-style
    negatives such as "(12.00)".
    """
    cleaned = text.strip()
    parenthesized = cleaned.startswith("(") and cleaned.endswith(")")
    if parenthesized:
        cleaned = cleaned[1:-1].strip()
    match = _AMOUNT.fullmatch(cleaned)
    if not match:
        raise ValueError(f"not a valid amount: {text!r}")
    signs = [match["neg1"], match["neg2"], parenthesized]
    if sum(map(bool, signs)) > 1:
        raise ValueError(f"not a valid amount: {text!r}")
    value = Decimal(match["num"].replace(",", ""))
    cents = int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return -cents if any(signs) else cents


def format_cents(cents: int) -> str:
    """Format cents as a dollar string, e.g. 1234 -> "$12.34", -5 -> "-$0.05"."""
    sign = "-" if cents < 0 else ""
    dollars, rem = divmod(abs(cents), 100)
    return f"{sign}${dollars}.{rem:02d}"


def apply_discount(subtotal_cents: int, percent: float) -> int:
    """Return the subtotal after a percentage discount, rounded half-up."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    factor = Decimal(1) - Decimal(str(percent)) / Decimal(100)
    discounted = Decimal(subtotal_cents) * factor
    return int(discounted.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
