# TSON Specification v1.0

**Token-efficient Structured Object Notation**

A compact, delimiter-based serialization format designed for efficient data exchange with Large Language Models.

## Design Principles

1. **Token Efficiency** - Minimize redundancy through schema declarations
2. **Single Syntax** - One consistent format for all JSON types
3. **Delimiter-Based** - Explicit separators, not whitespace-dependent
4. **LLM-Friendly** - Clear structure that models can parse and generate
5. **Universal** - Complete JSON compatibility

## Core Data Types

TSON supports all JSON data types:

| Type | Example | Notes |
|------|---------|-------|
| Object | `{@name,age\|Alice,30}` | Key-value pairs |
| Array | `[1,2,3]` | Ordered values |
| String | `Alice` or `"Hello, World"` | Quoted if needed |
| Number | `42`, `3.14`, `-17` | Integer or float |
| Boolean | `true`, `false` | Lowercase |
| Null | `null` | Represents no value |

## Syntax Rules

### 1. Objects

**Simple Object:**
```
{@key1,key2,key3|value1,value2,value3}
```

**Components:**
- `{` - Start delimiter
- `@` - Object marker (indicates keys follow)
- `key1,key2,key3` - Comma-separated key names
- `|` - Separator between keys and values
- `value1,value2,value3` - Comma-separated values
- `}` - End delimiter

**Example:**
```
{@name,age,active|Alice,30,true}
```

Equivalent JSON:
```json
{"name": "Alice", "age": 30, "active": true}
```

**Empty Object:**
```
{@}
```

### 2. Arrays

**Simple Array:**
```
[value1,value2,value3]
```

**Example:**
```
[1,2,3]
```

Equivalent JSON:
```json
[1, 2, 3]
```

**Empty Array:**
```
[]
```

### 3. Array of Objects (Tabular Format)

**Format:**
```
{@key1,key2#N|value1,value2|value1,value2}
```

**Components:**
- `@key1,key2` - Schema (keys declared once)
- `#N` - Optional row count
- `|` - Row separator
- Each row: comma-separated values matching the schema

**Example:**
```
{@id,name,age#3|1,Alice,30|2,Bob,25|3,Carol,35}
```

Equivalent JSON:
```json
[
  {"id": 1, "name": "Alice", "age": 30},
  {"id": 2, "name": "Bob", "age": 25},
  {"id": 3, "name": "Carol", "age": 35}
]
```

**Key Benefit:** Keys written once instead of repeated per object.

### 4. Nested Schema Notation

For objects containing nested objects with uniform structure:

**Format:**
```
{@key1,nested_key(@subkey1,subkey2)#N|value,{subval1,subval2}|...}
```

**Example:**
```
{@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}
```

Equivalent JSON:
```json
[
  {"id": 1, "address": {"city": "NYC", "zip": "10001"}},
  {"id": 2, "address": {"city": "LA", "zip": "90001"}}
]
```

**How It Works:**
1. `address(@city,zip)` declares that the `address` field contains objects with `city` and `zip` keys
2. In row data: `{NYC,"10001"}` is interpreted as an object using that schema
3. No need to repeat `@city,zip` for each row

**Token Savings:** Scales with number of rows - more rows = greater savings

### 5. Nested Structures

**Objects can nest:**
```
{@user|{@profile|{@name|Alice}}}
```

**Arrays can nest:**
```
[[1,2],[3,4]]
```

**Mixed nesting:**
```
{@name,tags,meta|Alice,[python,go],{@created|2025-01-27}}
```

## Delimiters

| Character | Purpose | Context |
|-----------|---------|---------|
| `{` | Start object | All objects |
| `}` | End object | All objects |
| `[` | Start array | All arrays |
| `]` | End array | All arrays |
| `@` | Object marker | Indicates keys follow |
| `,` | Separator | Keys, values, array elements |
| `|` | Row separator | Between key list and values, between rows |
| `#` | Count marker | Optional row count |

## Value Representation

### Primitives

**Numbers:**
- Integers: `42`, `-17`, `0`
- Floats: `3.14`, `-2.5`, `0.001`
- Scientific: `2.5e10`, `1.23e-5`

**Booleans:**
- `true`
- `false`

**Null:**
- `null`

### Strings

**Unquoted** (when safe):
```
Alice
hello_world
data-2025
```

Allowed characters: `a-z A-Z 0-9 _ -`

**Quoted** (when necessary):
```
"Hello, World"
"user@example.com"
"10001"
```

Quote when string contains:
- Delimiters: `,` `|` `@` `#` `{` `}` `[` `]`
- Whitespace or newlines
- Looks like a number (to preserve as string)
- Special characters

### String Escaping

Inside quoted strings, use standard JSON escapes:

| Escape | Meaning |
|--------|---------|
| `\"` | Double quote |
| `\\` | Backslash |
| `\n` | Newline |
| `\t` | Tab |
| `\r` | Carriage return |

**Example:**
```
"She said \"hello\""
"Line 1\nLine 2"
```

## Type Preservation

**Numeric Strings:**

To distinguish string `"123"` from number `123`:

```
{@zip,count|"10001",10001}
```
- `"10001"` - String (quoted because looks like number)
- `10001` - Number (unquoted)

**Empty Values:**

```
{@str,arr,obj|"",[],{@}}
```
- `""` - Empty string
- `[]` - Empty array
- `{@}` - Empty object

## Whitespace

**Whitespace is optional** for compactness but can be added for readability:

**Compact:**
```
{@id,name#2|1,Alice|2,Bob}
```

**Readable:**
```
{@id,name#2 | 1,Alice | 2,Bob}
```

Both are equivalent. Parsers ignore whitespace around delimiters.

**Newlines:** Can be used between rows for readability:
```
{@id,name#3|
1,Alice|
2,Bob|
3,Carol}
```

## Grammar (Informal)

```
value      := object | array | primitive
object     := "{@" keys "|" values "}" | "{@}"
array      := "[" values "]" | "[]"
keys       := key ("," key)* ("#" count)?
key        := identifier | identifier "(" keys ")"
values     := value ("," value)* ("|" value ("," value)*)*
primitive  := string | number | boolean | null
string     := unquoted | '"' escaped '"'
number     := integer | float
boolean    := "true" | "false"
null       := "null"
```

## Examples

### Example 1: Simple Object
```
TSON: {@name,age|Alice,30}
JSON: {"name": "Alice", "age": 30}
```

### Example 2: Simple Array
```
TSON: [1,2,3]
JSON: [1, 2, 3]
```

### Example 3: Nested Object
```
TSON: {@user|{@profile|{@name|Alice}}}
JSON: {"user": {"profile": {"name": "Alice"}}}
```

### Example 4: Array of Objects
```
TSON: {@id,name#2|1,Alice|2,Bob}
JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
```

### Example 5: Nested Schema
```
TSON: {@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}
JSON: [
  {"id": 1, "address": {"city": "NYC", "zip": "10001"}},
  {"id": 2, "address": {"city": "LA", "zip": "90001"}}
]
```

### Example 6: Mixed Types
```
TSON: {@name,tags,count|Alice,[python,go],5}
JSON: {"name": "Alice", "tags": ["python", "go"], "count": 5}
```

### Example 7: Complex Real-World
```
TSON: {@company,employees(@id,name,skills)#2|Acme,{1,Alice,[Python,Go]}|{2,Bob,[Java]}}
JSON: {
  "company": "Acme",
  "employees": [
    {"id": 1, "name": "Alice", "skills": ["Python", "Go"]},
    {"id": 2, "name": "Bob", "skills": ["Java"]}
  ]
}
```

## Design Decisions

### Why `@` for objects?

- Clear visual marker that keys follow
- Distinguishes objects from arrays at a glance
- Single character = minimal overhead

### Why `|` for row separator?

- Visually distinct from `,` (value separator)
- Common in data formats (CSV variants)
- Single character = compact

### Why nested schema notation?

- Massive token savings for repeated structures
- Scales: 100 rows with nested objects = ~40% token reduction
- Schema declared upfront helps LLMs understand structure

### Why curly braces for both single objects and arrays of objects?

- `{@key|value}` - Single object
- `{@key#N|val|val}` - Array of objects (presence of `#N` or multiple `|` indicates array)
- Consistent: `@` always means "keys follow"

## Limitations

1. **No Comments** - TSON is a data format, not a configuration language
2. **No References** - Cannot represent circular structures or shared references
3. **Tree Structure Only** - Like JSON, TSON represents trees, not graphs
4. **Schema Depth** - Nested schemas recommended for 1-2 levels (deeper nesting becomes complex)

## Extensions (Future)

Potential additions for v2.0+:

- Extended types: `NaN`, `Infinity`, `-Infinity`
- Datetime notation: `@date(2025-01-27)`
- Binary data: `@binary(base64...)`
- Comments: `// comment`
- Schema references: `@schema(user)` to reuse schemas
- Value references: Deduplication for repeated values

## Compatibility

### Converting from JSON

All JSON can be converted to TSON losslessly:
1. Objects → `{@key1,key2|val1,val2}`
2. Arrays → `[val1,val2]`
3. Array of uniform objects → `{@key#N|...}` (tabular optimization)
4. Primitives → Same representation

### Converting to JSON

All TSON can be converted to JSON losslessly:
1. Parse TSON structure
2. Reconstruct JSON tree
3. Apply schemas to nested objects
4. Output standard JSON

## Formal Specification Status

This specification defines TSON v1.0. Future versions may add features but will maintain backward compatibility with v1.0 syntax for core types.

## References

- JSON Specification: RFC 8259
- Design inspiration: TOON, MessagePack, CSV

## License

This specification is released under MIT License.

---

**Version:** 1.0
**Date:** 2025-01-27
**Status:** Stable
