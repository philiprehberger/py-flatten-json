# philiprehberger-flatten-json

[![Tests](https://github.com/philiprehberger/py-flatten-json/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-flatten-json/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-flatten-json.svg)](https://pypi.org/project/philiprehberger-flatten-json/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-flatten-json)](https://github.com/philiprehberger/py-flatten-json/commits/main)

Flatten nested JSON/dicts into dot-notation keys and unflatten back.

## Installation

```bash
pip install philiprehberger-flatten-json
```

## Usage

```python
from philiprehberger_flatten_json import flatten, unflatten

nested = {"a": {"b": {"c": 1}}, "d": [2, 3]}

flatten(nested)
# {"a.b.c": 1, "d.0": 2, "d.1": 3}

unflatten({"a.b.c": 1, "d.0": 2, "d.1": 3})
# {"a": {"b": {"c": 1}}, "d": [2, 3]}

# Custom separator
flatten(nested, separator="/")
# {"a/b/c": 1, "d/0": 2, "d/1": 3}

# Max depth
flatten(nested, max_depth=1)
# {"a": {"b": {"c": 1}}, "d": [2, 3]}

# Prefix
flatten(nested, prefix="root")
# {"root.a.b.c": 1, "root.d.0": 2, "root.d.1": 3}

# Keep numeric keys as dict
unflatten({"a.0": 1, "a.1": 2}, list_as_dict=True)
# {"a": {"0": 1, "1": 2}}
```

### Roundtrip

```python
from philiprehberger_flatten_json import flatten, unflatten

data = {"users": [{"name": "Alice", "age": 30}], "meta": {"version": 2}}

flat = flatten(data)
# {"users.0.name": "Alice", "users.0.age": 30, "meta.version": 2}

restored = unflatten(flat)
# {"users": [{"name": "Alice", "age": 30}], "meta": {"version": 2}}
```

## API

| Function | Description |
|---|---|
| `flatten(data, *, separator=".", max_depth=0, prefix="")` | Flatten nested dict/list into dot-notation keys |
| `unflatten(data, *, separator=".", list_as_dict=False)` | Restore nested structure from flat dict |

### Parameters

**`flatten()`**
- `data` — Nested dict or list
- `separator` — Key separator (default `"."`)
- `max_depth` — Max depth to flatten, 0 = unlimited
- `prefix` — String to prepend to all keys

**`unflatten()`**
- `data` — Flat dict with composite keys
- `separator` — Key separator used during flattening
- `list_as_dict` — When `True`, numeric keys stay as dict keys instead of converting to lists

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-flatten-json)

🐛 [Report issues](https://github.com/philiprehberger/py-flatten-json/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-flatten-json/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
