# Copyright (c) 2026 The cfgstack authors
# SPDX-License-Identifier: MIT
"""Layered value resolution for cfgstack.

A layered configuration is an ordered stack of values, highest priority
first. Each value in the stack may set the key to a concrete value, or leave
it unset. The effective value is the highest-priority value that counts as
"set" for the key's kind.

Two kinds are supported:

* ``KIND_SCALAR`` -- booleans, numbers, strings, arbitrary objects.
  A layer sets a scalar when the value is not ``None``. ``False``, ``0`` and
  ``""`` are ordinary scalar values and count as set.
* ``KIND_SEQUENCE`` -- tuples, lists, and other sized collections.
  A layer sets a sequence when it provides a non-empty collection. An empty
  collection reads as "no entries to contribute at this layer", so
  resolution falls through to the next layer.

The distinction exists because a scalar carries no separate notion of
"empty": ``False`` is a value, not the absence of one. A sequence does:
``()`` reads naturally as "no entries to contribute".
"""
from __future__ import annotations

from typing import Any, Iterable

KIND_SCALAR = "scalar"
KIND_SEQUENCE = "sequence"
KINDS = (KIND_SCALAR, KIND_SEQUENCE)


def _check_kind(kind: str) -> None:
    if kind not in KINDS:
        raise ValueError(
            "unknown kind: %r; expected one of %r" % (kind, KINDS)
        )


def _is_set(value: Any, kind: str) -> bool:
    """Return whether ``value`` sets the key for the given ``kind``."""
    _check_kind(kind)
    # A layer sets the key when it contributes a truthy value.
    return bool(value)


def resolve(layers: Iterable[Any], kind: str) -> Any:
    """Return the effective value from ``layers`` for ``kind``.

    ``layers`` is ordered highest priority first. The first layer that sets
    the key wins. If no layer sets it, ``None`` is returned.
    """
    _check_kind(kind)
    for value in layers:
        if _is_set(value, kind):
            return value
    return None
