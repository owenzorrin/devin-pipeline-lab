import pytest

from ledger import apply_discount, format_cents, parse_amount


@pytest.mark.parametrize(
    ("text", "cents"),
    [("12.50", 1250), ("$3", 300), (" 0.01 ", 1), ("0.005", 1)],
)
def test_parse_amount(text, cents):
    assert parse_amount(text) == cents


def test_parse_amount_rejects_garbage():
    with pytest.raises(ValueError):
        parse_amount("twelve")


@pytest.mark.parametrize(
    ("cents", "text"),
    [(1234, "$12.34"), (5, "$0.05"), (0, "$0.00")],
)
def test_format_cents(cents, text):
    assert format_cents(cents) == text


def test_apply_discount():
    assert apply_discount(1000, 15) == 850
    assert apply_discount(999, 50) == 500


def test_apply_discount_bounds():
    with pytest.raises(ValueError):
        apply_discount(1000, 101)
