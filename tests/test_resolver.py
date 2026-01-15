"""Tests for the layered resolver."""
import pytest

from cfgstack import KIND_SCALAR, KIND_SEQUENCE, resolve


# ---- scalar kind ---------------------------------------------------------

def test_scalar_first_non_none_wins():
    assert resolve([None, "a", "b"], KIND_SCALAR) == "a"


def test_scalar_all_none_returns_none():
    assert resolve([None, None], KIND_SCALAR) is None


def test_scalar_false_overrides_lower_true():
    """A False override at a higher layer must not fall through."""
    assert resolve([False, True], KIND_SCALAR) is False


def test_scalar_zero_overrides_lower_positive():
    """Zero is a value, not the absence of one."""
    assert resolve([0, 42], KIND_SCALAR) == 0


def test_scalar_empty_string_overrides_lower_value():
    """An explicit empty string must override a lower non-empty value."""
    assert resolve(["", "hello"], KIND_SCALAR) == ""


# ---- sequence kind -------------------------------------------------------

def test_sequence_first_nonempty_wins():
    assert resolve([None, ("a", "b"), ("c",)], KIND_SEQUENCE) == ("a", "b")


def test_sequence_all_none_returns_none():
    assert resolve([None, None], KIND_SEQUENCE) is None


# ---- public contract -----------------------------------------------------

def test_resolve_rejects_unknown_kind():
    with pytest.raises(ValueError):
        resolve([1], "unknown")
