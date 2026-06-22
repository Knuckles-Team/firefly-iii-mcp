import importlib

import pytest


@pytest.mark.concept("FF-001")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:FF-001"""
    module = importlib.import_module("firefly_iii_mcp")
    assert hasattr(module, "__all__")
