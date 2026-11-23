"""Money helpers. Amounts are always stored as integer cents."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


def parse_amount(text: str) -> int:
    """Parse a human-entered amount such as "12.50" or "$3" into cents."""
    cleaned = text.strip().lstrip("$")
    try:
        value = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"not a valid amount: {text!r}") from exc
    return int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def format_cents(cents: int) -> str:
    """Format cents as a dollar string, e.g. 1234 -> "$12.34"."""
    dollars, rem = divmod(cents, 100)
    return f"${dollars}.{rem:02d}"


def apply_discount(subtotal_cents: int, percent: float) -> int:
    """Return the subtotal after a percentage discount, rounded half-up."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    factor = Decimal(1) - Decimal(str(percent)) / Decimal(100)
    discounted = Decimal(subtotal_cents) * factor
    return int(discounted.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
