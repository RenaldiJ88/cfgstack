# Copyright (c) 2026 The cfgstack authors
# SPDX-License-Identifier: MIT
"""cfgstack: layered configuration resolution."""
from cfgstack.resolver import (
    KIND_SCALAR,
    KIND_SEQUENCE,
    KINDS,
    resolve,
)

__all__ = ["KIND_SCALAR", "KIND_SEQUENCE", "KINDS", "resolve"]
__version__ = "0.3.1"
