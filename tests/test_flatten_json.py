from __future__ import annotations

import pytest

from philiprehberger_flatten_json import flatten, unflatten


# --- Flatten basics ---

def test_flatten_nested_dict():
    data = {"a": {"b": {"c": 1}}}
    assert flatten(data) == {"a.b.c": 1}

def test_flatten_nested_list():
    data = {"a": [1, 2, 3]}
    assert flatten(data) == {"a.0": 1, "a.1": 2, "a.2": 3}

def test_flatten_mixed():
    data = {"a": {"b": 1}, "c": [2, 3]}
    result = flatten(data)
    assert result == {"a.b": 1, "c.0": 2, "c.1": 3}


# --- Empty structures ---

def test_flatten_empty_dict():
    assert flatten({}) == {}

def test_flatten_empty_list_preserved():
    data = {"a": []}
    assert flatten(data) == {"a": []}

def test_flatten_empty_nested_dict():
    data = {"a": {}}
    assert flatten(data) == {"a": {}}


# --- Scalar values ---

def test_flatten_string_leaf():
    data = {"a": "hello"}
    assert flatten(data) == {"a": "hello"}

def test_flatten_none_leaf():
    data = {"a": None}
    assert flatten(data) == {"a": None}

def test_flatten_bool_leaf():
    data = {"a": True, "b": False}
    assert flatten(data) == {"a": True, "b": False}


# --- Custom separator ---

def test_flatten_custom_separator():
    data = {"a": {"b": 1}}
    assert flatten(data, separator="/") == {"a/b": 1}

def test_unflatten_custom_separator():
    data = {"a/b": 1}
    assert unflatten(data, separator="/") == {"a": {"b": 1}}


# --- Max depth ---

def test_max_depth_1():
    data = {"a": {"b": {"c": 1}}}
    result = flatten(data, max_depth=1)
    assert result == {"a": {"b": {"c": 1}}}

def test_max_depth_2():
    data = {"a": {"b": {"c": 1}}}
    result = flatten(data, max_depth=2)
    assert result == {"a.b": {"c": 1}}

def test_max_depth_0_unlimited():
    data = {"a": {"b": {"c": 1}}}
    assert flatten(data, max_depth=0) == {"a.b.c": 1}


# --- Prefix ---

def test_flatten_with_prefix():
    data = {"a": {"b": 1}}
    assert flatten(data, prefix="root") == {"root.a.b": 1}

def test_flatten_prefix_with_separator():
    data = {"a": {"b": 1}}
    assert flatten(data, prefix="root", separator="/") == {"root/a/b": 1}


# --- Round-trip ---

def test_round_trip_dict():
    data = {"a": {"b": 1}, "c": 2}
    assert unflatten(flatten(data)) == data

def test_round_trip_list():
    data = {"items": [1, 2, 3]}
    assert unflatten(flatten(data)) == data


# --- Unflatten basics ---

def test_unflatten_dot_notation():
    data = {"a.b.c": 1}
    assert unflatten(data) == {"a": {"b": {"c": 1}}}

def test_unflatten_numeric_keys_become_lists():
    data = {"a.0": 1, "a.1": 2}
    assert unflatten(data) == {"a": [1, 2]}


# --- Unflatten list_as_dict ---

def test_unflatten_list_as_dict():
    data = {"a.0": 1, "a.1": 2}
    result = unflatten(data, list_as_dict=True)
    assert result == {"a": {"0": 1, "1": 2}}


# --- Deeply nested ---

def test_deeply_nested():
    data = {"a": {"b": {"c": {"d": {"e": 1}}}}}
    flat = flatten(data)
    assert flat == {"a.b.c.d.e": 1}
    assert unflatten(flat) == data


# --- List of dicts ---

def test_list_of_dicts():
    data = {"items": [{"a": 1}, {"a": 2}]}
    flat = flatten(data)
    assert flat == {"items.0.a": 1, "items.1.a": 2}
    assert unflatten(flat) == data


# --- Single key ---

def test_single_key():
    data = {"a": 1}
    assert flatten(data) == {"a": 1}


# --- Unflatten empty ---

def test_unflatten_empty():
    assert unflatten({}) == {}
