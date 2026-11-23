import pytest

from ledger import apply_discount, format_cents, parse_amount


@pytest.mark.parametrize(
    ("text", "cents"),
    [
        ("12.50", 1250),
        ("$3", 300),
        (" 0.01 ", 1),
        ("0.005", 1),
        ("1,234.50", 123450),
        ("$1,234,567", 123456700),
        ("(12.00)", -1200),
        ("($1,234.50)", -123450),
        ("-$3.25", -325),
        ("$-3.25", -325),
        ("-0.005", -1),
    ],
)
def test_parse_amount(text, cents):
    assert parse_amount(text) == cents


@pytest.mark.parametrize(
    "text",
    ["twelve", "", "1,23.45", "12,34", ",123", "--3", "-$-3", "(-12.00)", "(12.00"],
)
def test_parse_amount_rejects_garbage(text):
    with pytest.raises(ValueError):
        parse_amount(text)


@pytest.mark.parametrize(
    ("cents", "text"),
    [
        (1234, "$12.34"),
        (5, "$0.05"),
        (0, "$0.00"),
        (-5, "-$0.05"),
        (-1234, "-$12.34"),
        (-100, "-$1.00"),
    ],
)
def test_format_cents(cents, text):
    assert format_cents(cents) == text


def test_apply_discount():
    assert apply_discount(1000, 15) == 850
    assert apply_discount(999, 50) == 500


def test_apply_discount_bounds():
    with pytest.raises(ValueError):
        apply_discount(1000, 101)
