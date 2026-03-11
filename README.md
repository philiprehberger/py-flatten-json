# philiprehberger-flatten-json

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
```

## API

- `flatten(data, separator=".", max_depth=0)` — Flatten nested structure
- `unflatten(data, separator=".")` — Restore nested structure

## License

MIT
