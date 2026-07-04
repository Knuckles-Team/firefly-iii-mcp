import importlib

import pytest


@pytest.mark.concept("FF-OS.config.ff")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:FF-OS.config.ff"""
    module = importlib.import_module("firefly_iii_mcp")
    assert hasattr(module, "__all__")
