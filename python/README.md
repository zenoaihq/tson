# TSON for Python

**Token-efficient Structured Object Notation - Python Implementation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-13%2F13%20passing-brightgreen.svg)]()

## Installation

```bash
cd python
pip install -e .
```

Or install from PyPI:
```bash
pip install tson
```

## Quick Start

```python
import tson

# Simple object
data = {"name": "Alice", "age": 30, "active": True}
encoded = tson.dumps(data)
print(encoded)
# Output: {@name,age,active|Alice,30,true}

# Perfect round-trip
decoded = tson.loads(encoded)
assert data == decoded  # True
```

## API Reference

### Serialization

```python
import tson

# Serialize Python data to TSON string
tson_string = tson.dumps(data)

# Serialize to file
with open('data.tson', 'w') as f:
    tson.dump(data, f)
```

### Deserialization

```python
# Deserialize TSON string to Python data
data = tson.loads(tson_string)

# Deserialize from file
with open('data.tson', 'r') as f:
    data = tson.load(f)
```

## Examples

### 1. Simple Objects

```python
data = {"name": "Alice", "age": 30, "active": True}
encoded = tson.dumps(data)
# {@name,age,active|Alice,30,true}
```

### 2. Arrays

```python
data = [1, 2, 3, 4, 5]
encoded = tson.dumps(data)
# [1,2,3,4,5]
```

### 3. Array of Objects (Tabular Format)

```python
data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Carol", "email": "carol@example.com"}
]
encoded = tson.dumps(data)
# {@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}

decoded = tson.loads(encoded)
assert data == decoded  # Perfect round-trip
```

### 4. Nested Schema Notation

```python
data = [
    {"id": 1, "name": "Alice", "address": {"city": "NYC", "zip": "10001"}},
    {"id": 2, "name": "Bob", "address": {"city": "LA", "zip": "90001"}}
]
encoded = tson.dumps(data)
# {@id,name,address(@city,zip)#2|1,Alice,{NYC,"10001"}|2,Bob,{LA,"90001"}}
```

### 5. Complex Nested Structures

```python
data = {
    "company": "Acme Corp",
    "employees": [
        {
            "id": 1,
            "name": "Alice",
            "skills": ["Python", "Go"],
            "contact": {"email": "alice@acme.com", "phone": "555-0101"}
        },
        {
            "id": 2,
            "name": "Bob",
            "skills": ["Java"],
            "contact": {"email": "bob@acme.com", "phone": "555-0102"}
        }
    ]
}

encoded = tson.dumps(data)
decoded = tson.loads(encoded)
assert data == decoded  # Perfect round-trip
```

### 6. Type Preservation

```python
data = {
    "zip_string": "10001",  # String
    "zip_number": 10001,    # Number
    "version_string": "1.0", # String
    "version_number": 1.0   # Float
}

encoded = tson.dumps(data)
# {@zip_string,zip_number,version_string,version_number|"10001",10001,"1.0",1.0}

decoded = tson.loads(encoded)
assert isinstance(decoded["zip_string"], str)   # True
assert isinstance(decoded["zip_number"], int)   # True
assert isinstance(decoded["version_string"], str)  # True
assert isinstance(decoded["version_number"], float)  # True
```

### 7. Empty Values

```python
data = {
    "empty_string": "",
    "empty_array": [],
    "empty_object": {},
    "null_value": None
}

encoded = tson.dumps(data)
# {@empty_string,empty_array,empty_object,null_value|"",[],{@},null}
```

### 8. Special Characters

```python
data = {
    "comma": "hello, world",
    "pipe": "a|b|c",
    "quotes": 'She said "hello"',
    "newline": "line1\nline2"
}

encoded = tson.dumps(data)
decoded = tson.loads(encoded)
assert data == decoded  # Special characters preserved
```

## Testing

Run the comprehensive test suite (13 tests):

```bash
python tests/test_round\ trip.py
```

All tests should pass:
```
[PASS] Simple object
[PASS] Simple array
[PASS] Array of objects (tabular)
[PASS] Nested object
[PASS] Mixed array
[PASS] Empty values
[PASS] Special characters
[PASS] Numeric strings
[PASS] Nested arrays
[PASS] Array with nested objects (nested schema)
[PASS] Complex structure
[PASS] Boolean values
[PASS] Numeric types

SUCCESS: All 13 tests passed!
```

## Interactive Testing

Test TSON strings interactively:

```bash
python test_tson_string.py
```

This tool lets you:
- Enter TSON strings and see the JSON conversion
- Verify round-trip conversion
- See token savings
- Run example tests

## LLM Integration

See [llm_integration_example.py](llm_integration_example.py) for complete examples of using TSON with LLMs.

### Quick Example

```python
import tson

# Prepare data for LLM
data = [
    {"date": "2025-01-01", "sales": 5000, "region": "North"},
    {"date": "2025-01-02", "sales": 6000, "region": "South"},
    {"date": "2025-01-03", "sales": 5500, "region": "East"},
]

tson_data = tson.dumps(data)

# Include TSON system prompt (see prompts.md)
system_prompt = """
TSON format (compact JSON):
• {@k1,k2|v1,v2} = object
• {@k1,k2#N|v1,v2|v1,v2} = array of objects
"""

user_prompt = f"Analyze this sales data: {tson_data}"

# Send to LLM API...
# Token savings: 30-50% compared to JSON
```

See [../prompts.md](../prompts.md) for complete LLM prompt templates.

## Examples

Run the basic usage examples:

```bash
python examples/basic_usage.py
```

This demonstrates:
- Simple objects
- Array of objects (tabular format)
- Nested schema notation
- Mixed types
- Real-world data structures
- Special values

## Type Support

TSON supports all JSON types:

| Python Type | TSON Representation | Example |
|-------------|---------------------|---------|
| `str` | String (quoted if needed) | `Alice` or `"Hello, World"` |
| `int` | Number | `42`, `-17` |
| `float` | Number | `3.14`, `-2.5` |
| `bool` | Boolean | `true`, `false` |
| `None` | Null | `null` |
| `list` | Array | `[1,2,3]` |
| `dict` | Object | `{@key\|value}` |

## Performance

TSON is optimized for:
- **Token efficiency** - 30-55% savings vs JSON
- **Fast parsing** - Simple delimiter-based parsing
- **Low memory** - Minimal overhead
- **No dependencies** - Pure Python implementation

## Syntax Guide

See the main [SPEC.md](../SPEC.md) for complete syntax specification.

**Quick reference:**

| Delimiter | Purpose | Example |
|-----------|---------|---------|
| `{` `}` | Object boundaries | `{@name\|Alice}` |
| `[` `]` | Array boundaries | `[1,2,3]` |
| `@` | Object marker | `{@key1,key2\|...}` |
| `,` | Field/value separator | `name,age,city` |
| `\|` | Row separator | `val1,val2\|val1,val2` |
| `#` | Row count (optional) | `#3` |

## Requirements

- Python 3.7 or higher
- No external dependencies

## Development

Install in editable mode for development:

```bash
pip install -e .
```

Run tests:
```bash
python tests/test_round\ trip.py
```

## Contributing

Contributions to the Python implementation are welcome! Please see [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Documentation

- **[../SPEC.md](../SPEC.md)** - Complete format specification
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[../prompts.md](../prompts.md)** - LLM integration guide
- **[llm_integration_example.py](llm_integration_example.py)** - Working LLM examples

## License

MIT License - see [../LICENSE](../LICENSE) file for details.

---

**Version:** 1.0.0
**Status:** Production Ready
**Python:** 3.7+
**Dependencies:** None

*Part of the TSON project by Zeno AI*
