# TSON Quick Start Guide

Get up and running with TSON in 5 minutes.

## Installation

```bash
cd tson
pip install -e .
```

## Basic Usage

```python
import tson

# 1. Simple object
data = {"name": "Alice", "age": 30}
encoded = tson.dumps(data)
print(encoded)  # {@name,age|Alice,30}

decoded = tson.loads(encoded)
print(decoded)  # {'name': 'Alice', 'age': 30}
```

## Key Features

### 1. Tabular Format (Big Win!)

```python
# Array of uniform objects
data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Carol"}
]

encoded = tson.dumps(data)
print(encoded)
# {@id,name#3|1,Alice|2,Bob|3,Carol}
#  ^keys written once!  ^rows separated by |
```

**Why this matters:** Keys written once = huge token savings for large datasets.

### 2. Nested Schema (Advanced)

```python
# Array with nested objects
data = [
    {"id": 1, "address": {"city": "NYC", "zip": "10001"}},
    {"id": 2, "address": {"city": "LA", "zip": "90001"}}
]

encoded = tson.dumps(data)
print(encoded)
# {@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}
#        ^nested schema!    ^just values in rows
```

**Why this matters:** Nested structure declared once, then only values = scales with row count.

### 3. All JSON Types Supported

```python
data = {
    "string": "hello",
    "number": 42,
    "float": 3.14,
    "boolean": True,
    "null": None,
    "array": [1, 2, 3],
    "object": {"nested": "value"}
}

encoded = tson.dumps(data)
decoded = tson.loads(encoded)
assert data == decoded  # Perfect round-trip!
```

## Syntax Cheat Sheet

```
Objects:   {@key1,key2|val1,val2}
Arrays:    [val1,val2,val3]
Tabular:   {@key1,key2#N|val1,val2|val1,val2}
Nested:    {@id,field(@subkey1,subkey2)|val,{subval1,subval2}}

Primitives:
- Strings: Alice or "hello, world"
- Numbers: 42, 3.14
- Booleans: true, false
- Null: null

Delimiters:
@ = object marker
, = field/value separator
| = row separator
# = row count (optional)
```

## When to Quote Strings

**Unquoted (safe):**
```
Alice
hello_world
data-2025
```

**Quoted (necessary):**
```
"hello, world"     # Contains comma
"user@example.com" # Contains @
"10001"            # Looks like number
```

## File I/O

```python
# Write to file
with open('data.tson', 'w') as f:
    tson.dump(data, f)

# Read from file
with open('data.tson', 'r') as f:
    data = tson.load(f)
```

## Testing

```bash
# Run tests
python tests/test_roundtrip.py

# Run examples
python examples/basic_usage.py
```

## Real-World Example

```python
import tson

# Employee database
employees = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "dept": "Engineering",
        "skills": ["Python", "Go", "Docker"],
        "contact": {
            "email": "alice@example.com",
            "phone": "555-0101"
        }
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "dept": "Design",
        "skills": ["Figma", "Illustrator"],
        "contact": {
            "email": "bob@example.com",
            "phone": "555-0102"
        }
    }
]

# Serialize
encoded = tson.dumps(employees)

# Nested schema notation automatically applied:
# contact(@email,phone) declared once, values in each row

# Deserialize
decoded = tson.loads(encoded)

assert employees == decoded  # Perfect round-trip
```

## Token Savings Examples

From `basic_usage.py`:

| Data | JSON | TSON | Savings |
|------|------|------|---------|
| Simple object | 44 chars | 32 chars | 27% |
| 3 objects | 170 chars | 98 chars | 42% |
| 3 nested objects | 217 chars | 98 chars | 55% |

**Note:** Savings increase with more rows!

## Next Steps

- Read [SPEC.md](SPEC.md) for complete specification
- Read [README.md](README.md) for detailed documentation
- Run `python examples/basic_usage.py` for more examples
- Try it with your own data!

## Common Patterns

### Pattern 1: Database Results
```python
# Perfect for tabular data
rows = cursor.fetchall()
tson_data = tson.dumps(rows)
# Send to LLM with 40-60% fewer tokens
```

### Pattern 2: LLM Function Arguments
```python
def analyze_data(data_tson: str):
    """Function that takes TSON-encoded data"""
    data = tson.loads(data_tson)
    # Process data...
```

### Pattern 3: Configuration Files
```python
config = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"ttl": 3600}
}

# Save
with open('config.tson', 'w') as f:
    tson.dump(config, f)
```

---

**That's it!** You're ready to use TSON.

For questions or issues, see [README.md](README.md) or the [specification](SPEC.md).
