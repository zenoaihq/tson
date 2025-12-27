# TSON Specification v1.1

**Token-efficient Structured Object Notation**

A compact, delimiter-based serialization format designed for efficient data exchange with Large Language Models.

## Design Principles

1. **Token Efficiency** - Minimize redundancy through schema declarations
2. **Single Syntax** - One consistent format for all JSON types
3. **Delimiter-Based** - Explicit separators, not whitespace-dependent
4. **LLM-Friendly** - Clear structure that models can parse and generate
5. **Universal** - Complete JSON compatibility with lossless round-trips

---

## Core Data Types

TSON supports all JSON data types:

| Type | Example | Notes |
|------|---------|-------|
| Object | `{@name,age\|Alice,30}` | Key-value pairs |
| Array | `[1,2,3]` | Ordered values |
| String | `Alice` or `"Hello, World"` | Quoted if contains special chars |
| Number | `42`, `3.14`, `-17` | Integer or float |
| Boolean | `true`, `false` | Lowercase |
| Null | `null` | Represents no value |

---

## Syntax Rules

### 1. Objects

**Format:**
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

**Format:**
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

This is the **key optimization** - keys are declared once instead of repeated.

**Format:**
```
{@key1,key2#N|value1,value2|value1,value2|...}
```

**Components:**
- `@key1,key2` - Schema (keys declared once)
- `#N` - Row count (optional but recommended)
- `|` - Row separator
- Each row: comma-separated values matching schema order

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

### 4. Nested Schema Notation

For arrays of objects containing nested objects with uniform structure:

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
1. `address(@city,zip)` declares that `address` contains objects with `city` and `zip` keys
2. In row data: `{NYC,"10001"}` is interpreted using that schema
3. No need to repeat key declarations for each row

**Nested Schema Keys with Special Characters:**
```
{@id,info(@"key,comma","key|pipe")#2|1,{Alice,value1}|2,{Bob,value2}}
```

Keys within nested schemas that contain special characters must be quoted.

---

## Delimiters

| Character | Purpose | Must Quote If In Value |
|-----------|---------|-----------------------|
| `{` | Start object | Yes |
| `}` | End object | Yes |
| `[` | Start array | Yes |
| `]` | End array | Yes |
| `@` | Object marker | Yes |
| `,` | Value separator | Yes |
| `|` | Row separator | Yes |
| `#` | Count marker | Yes |
| `"` | String quote | Yes (use `\"`) |
| `(` | Schema notation | Yes |
| `)` | Schema notation | Yes |

---

## String Handling

### When to Quote Strings

Strings **must be quoted** when they:

1. **Are empty** - `""`
2. **Contain delimiters** - `,` `|` `@` `#` `{` `}` `[` `]` `(` `)`
3. **Contain double quotes** - Escape as `\"`
4. **Contain whitespace** - Spaces, tabs, newlines
5. **Look like numbers** - `"10001"` to preserve as string
6. **Look like reserved words** - `"true"` `"false"` `"null"` as strings

### Unquoted Strings (Safe Characters)

These characters are safe without quotes: `a-z A-Z 0-9 _ - . / : + =`

**Examples:**
```
Alice
hello_world
2025-01-27
user@example.com    // @ is special but common in emails - MUST quote
```

Wait - `@` requires quoting! Correct example:
```
Alice              // OK - no special chars
hello_world        // OK
2025-01-27         // OK
"user@example.com" // Must quote - contains @
```

### String Escaping

Inside quoted strings, use JSON-style escape sequences:

| Escape | Meaning |
|--------|---------|
| `\"` | Double quote |
| `\\` | Backslash |
| `\n` | Newline |
| `\r` | Carriage return |
| `\t` | Tab |

**Examples:**
```
"She said \"hello\""      // Contains quotes
"Line 1\nLine 2"          // Contains newline
"C:\\Users\\file"         // Windows path with backslashes
"literal\\ntext"          // Literal backslash + n (not newline)
```

### Type Preservation

**Numeric Strings vs Numbers:**
```
{@zip_string,zip_number|"10001",10001}
```
- `"10001"` - String (quoted)
- `10001` - Number (unquoted)

**Empty Values:**
```
{@str,arr,obj|"",[],{@}}
```
- `""` - Empty string
- `[]` - Empty array
- `{@}` - Empty object

---

## Keys with Special Characters

Keys follow the same quoting rules as values:

**Simple keys (unquoted):**
```
{@name,age,active|...}
```

**Keys with special characters (quoted):**
```
{@"with,comma","with|pipe","at@sign","with space"|value,value,value,value}
```

**Keys with parentheses:**
```
{@"func()","name(test)"|value,another}
```

Note: A key like `address(@city,zip)` is **nested schema notation**, not a key with parentheses. To have a key literally named `address()`, quote it: `"address()"`.

---

## Nested Structures

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

---

## Whitespace

Whitespace is **optional** but can improve readability:

**Compact:**
```
{@id,name#2|1,Alice|2,Bob}
```

**Readable:**
```
{@id,name#2 | 1,Alice | 2,Bob}
```

**Multi-line:**
```
{@id,name#3|
1,Alice|
2,Bob|
3,Carol}
```

Parsers should trim whitespace around delimiters.

---

## Examples

### Example 1: Simple Object
```
TSON: {@name,age|Alice,30}
JSON: {"name": "Alice", "age": 30}
```

### Example 2: Array of Objects
```
TSON: {@id,name#2|1,Alice|2,Bob}
JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
```

### Example 3: Nested Schema
```
TSON: {@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}
JSON: [
  {"id": 1, "address": {"city": "NYC", "zip": "10001"}},
  {"id": 2, "address": {"city": "LA", "zip": "90001"}}
]
```

### Example 4: Special Characters in Values
```
TSON: {@path,quote,comma|"C:\\Users\\file","He said \"hello\"","a,b,c"}
JSON: {"path": "C:\\Users\\file", "quote": "He said \"hello\"", "comma": "a,b,c"}
```

### Example 5: Special Characters in Keys
```
TSON: {@"key,comma","key|pipe"|value1,value2}
JSON: {"key,comma": "value1", "key|pipe": "value2"}
```

### Example 6: Nested Schema with Special Char Keys
```
TSON: {@id,info(@"key,comma","key|pipe")#2|1,{Alice,val1}|2,{Bob,val2}}
JSON: [
  {"id": 1, "info": {"key,comma": "Alice", "key|pipe": "val1"}},
  {"id": 2, "info": {"key,comma": "Bob", "key|pipe": "val2"}}
]
```

### Example 7: Complex Real-World
```
TSON: {@company,employees|Acme,{@id,name,skills#2|1,Alice,[Python,Go]|2,Bob,[Java]}}
JSON: {
  "company": "Acme",
  "employees": [
    {"id": 1, "name": "Alice", "skills": ["Python", "Go"]},
    {"id": 2, "name": "Bob", "skills": ["Java"]}
  ]
}
```

---

## Grammar (Informal BNF)

```
document   := value
value      := object | array | primitive
object     := "{@" keys "|" values "}" | "{@}"
array      := "[" values "]" | "[]"
keys       := key ("," key)* ("#" count)?
key        := identifier | quoted_string | identifier "(@" schema_keys ")"
schema_keys := key ("," key)*
values     := value ("," value)* ("|" value ("," value)*)*
primitive  := string | number | boolean | null
string     := unquoted_string | '"' escaped_chars '"'
number     := integer | float
boolean    := "true" | "false"
null       := "null"
count      := digit+
```

---

## Implementation Notes

### Parsing Keys
1. If a key starts and ends with `"`, treat it as a quoted key (unescape contents)
2. If a key contains `(@`, parse as nested schema notation
3. Otherwise, treat as plain key name

### Detecting Tabular Format
An object is tabular (array of objects) if:
- Row count `#N` is present, OR
- Multiple `|` separators exist after the keys

### Escape Sequence Processing
When unescaping strings, process character-by-character to correctly handle:
- `\\n` = literal backslash + 'n'
- `\n` = newline character

---

## Limitations

1. **No Comments** - TSON is a data format, not configuration
2. **No Circular References** - Tree structures only
3. **Schema Depth** - Nested schemas recommended for 1-2 levels
4. **No Special Numbers** - `NaN`, `Infinity` not supported (v1.x)

---

## Compatibility

### JSON → TSON
All JSON converts losslessly:
- Objects → `{@key1,key2|val1,val2}`
- Arrays of uniform objects → `{@key#N|...}` (tabular)
- Other arrays → `[val1,val2]`
- Primitives → Same representation (quote if needed)

### TSON → JSON
All TSON converts losslessly:
- Parse structure
- Apply schemas to nested objects
- Output standard JSON

---

**Version:** 1.1
**Date:** 2025-12-27
**Status:** Stable

*Built for efficiency. Optimized for LLMs.*
