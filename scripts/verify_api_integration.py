#!/usr/bin/env python3
"""Verify exact public API-to-condensed-MCP action parity without imports."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _public_api_methods(root: Path) -> set[str]:
    methods: set[str] = set()
    api_dir = root / "firefly_iii_mcp" / "api"
    for path in sorted(api_dir.glob("api_client_*.py")):
        if path.name in {"api_client_base.py", "api_client_firefly_iii.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not (
                    item.name.startswith("_")
                    or item.name in {"authenticate", "close", "request"}
                ):
                    methods.add(item.name)
    return methods


def _condensed_actions(root: Path) -> set[str]:
    actions: set[str] = set()
    mcp_dir = root / "firefly_iii_mcp" / "mcp"
    for path in sorted(mcp_dir.glob("mcp_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id == "resolve_action":
                if len(node.args) < 2 or not isinstance(
                    node.args[1], (ast.Set, ast.List, ast.Tuple)
                ):
                    continue
                for element in node.args[1].elts:
                    if isinstance(element, ast.Constant) and isinstance(
                        element.value, str
                    ):
                        actions.add(element.value)
            if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in {"client", "api"}
            ):
                actions.add(node.func.attr)
    return actions


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    methods = _public_api_methods(root)
    actions = _condensed_actions(root)
    missing = sorted(methods - actions)
    unknown = sorted(actions - methods)

    print("Firefly III API-to-MCP parity")
    print(f"API methods: {len(methods)}")
    print(f"Condensed actions: {len(actions)}")
    if missing:
        print("Missing actions: " + ", ".join(missing))
    if unknown:
        print("Unknown actions: " + ", ".join(unknown))
    if missing or unknown or not methods:
        return 1
    print("Coverage: 100.0%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
