"""Flatten nested JSON/dicts into dot-notation keys and unflatten back."""

from __future__ import annotations

from typing import Any


__all__ = [
    "flatten",
    "unflatten",
]


def flatten(
    data: dict | list,
    *,
    separator: str = ".",
    max_depth: int = 0,
    prefix: str = "",
) -> dict[str, Any]:
    """Flatten a nested dict/list into a flat dict with dot-notation keys.

    Args:
        data: Nested dict or list.
        separator: Key separator. Defaults to ``"."``.
        max_depth: Maximum nesting depth to flatten. 0 means unlimited.
        prefix: String to prepend to all keys.

    Returns:
        Flat dict with composite keys.
    """
    result: dict[str, Any] = {}
    _flatten_recursive(data, prefix, separator, max_depth, 0, result)
    return result


def _flatten_recursive(
    data: Any,
    prefix: str,
    separator: str,
    max_depth: int,
    current_depth: int,
    result: dict[str, Any],
) -> None:
    if max_depth > 0 and current_depth >= max_depth:
        result[prefix] = data
        return

    if isinstance(data, dict):
        if not data:
            if prefix:
                result[prefix] = data
            return
        for key, value in data.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            _flatten_recursive(value, new_key, separator, max_depth, current_depth + 1, result)
    elif isinstance(data, list):
        if not data:
            if prefix:
                result[prefix] = data
            return
        for i, value in enumerate(data):
            new_key = f"{prefix}{separator}{i}" if prefix else str(i)
            _flatten_recursive(value, new_key, separator, max_depth, current_depth + 1, result)
    else:
        result[prefix] = data


def unflatten(data: dict[str, Any], *, separator: str = ".", list_as_dict: bool = False) -> dict | list:
    """Unflatten a flat dict with dot-notation keys back to nested structure.

    Args:
        data: Flat dict with composite keys.
        separator: Key separator used during flattening.
        list_as_dict: When True, numeric keys stay as dict keys instead of
            converting to lists.

    Returns:
        Nested dict or list.
    """
    if not data:
        return {}

    result: dict[str, Any] = {}

    for compound_key, value in data.items():
        keys = compound_key.split(separator)
        _set_nested(result, keys, value)

    if list_as_dict:
        return result
    return _convert_numeric_dicts(result)


def _set_nested(container: dict, keys: list[str], value: Any) -> None:
    for key in keys[:-1]:
        if key not in container:
            container[key] = {}
        container = container[key]
    container[keys[-1]] = value


def _convert_numeric_dicts(data: Any) -> Any:
    """Recursively convert dicts with all-numeric keys to lists."""
    if not isinstance(data, dict):
        return data

    # Check if all keys are numeric
    if data and all(_is_int(k) for k in data):
        max_idx = max(int(k) for k in data)
        if max_idx < len(data) * 2:  # reasonable density check
            lst = [None] * (max_idx + 1)
            for k, v in data.items():
                lst[int(k)] = _convert_numeric_dicts(v)
            return lst

    return {k: _convert_numeric_dicts(v) for k, v in data.items()}


def _is_int(s: str) -> bool:
    try:
        int(s)
    except ValueError:
        return False
    return True
