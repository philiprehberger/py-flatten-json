from philiprehberger_flatten_json import flatten, unflatten


def test_flatten_simple():
    result = flatten({"a": {"b": 1}})
    assert result == {"a.b": 1}


def test_flatten_deep():
    result = flatten({"a": {"b": {"c": 1}}})
    assert result == {"a.b.c": 1}


def test_flatten_with_list():
    result = flatten({"a": [1, 2]})
    assert result == {"a.0": 1, "a.1": 2}


def test_flatten_mixed():
    result = flatten({"a": {"b": [1, 2]}, "c": 3})
    assert result == {"a.b.0": 1, "a.b.1": 2, "c": 3}


def test_flatten_custom_separator():
    result = flatten({"a": {"b": 1}}, separator="/")
    assert result == {"a/b": 1}


def test_flatten_max_depth():
    result = flatten({"a": {"b": {"c": 1}}}, max_depth=1)
    assert result == {"a": {"b": {"c": 1}}}


def test_unflatten_simple():
    result = unflatten({"a.b": 1})
    assert result == {"a": {"b": 1}}


def test_unflatten_with_list():
    result = unflatten({"a.0": 1, "a.1": 2})
    assert result == {"a": [1, 2]}


def test_round_trip():
    original = {"a": {"b": {"c": 1}}, "d": [2, 3]}
    flat = flatten(original)
    restored = unflatten(flat)
    assert restored == original


def test_empty_dict():
    assert flatten({}) == {}
    assert unflatten({}) == {}


def test_flat_input():
    data = {"a": 1, "b": 2}
    assert flatten(data) == data


def test_empty_nested_dict():
    result = flatten({"a": {}})
    assert result == {"a": {}}


def test_empty_nested_list():
    result = flatten({"a": []})
    assert result == {"a": []}
