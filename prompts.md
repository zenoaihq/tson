# TSON Prompt Templates

Prompts for teaching LLMs about TSON and converting between TSON ↔ JSON.

---

## System Prompt (Full Version - Recommended)

Use this as your system prompt when working with TSON:

```
You convert JSON to TSON (Token-efficient Structured Object Notation).

## CONVERSION RULES (Follow in order)

### Rule 1: Identify the Structure Type
- Single object → {@keys|values}
- Array of uniform objects → {@keys#N|row1|row2|...}  
- Simple array → [val1,val2,val3]

### Rule 2: For Objects, Declare Keys First
Format: {@key1,key2,key3|value1,value2,value3}

Example:
  JSON: {"name": "Alice", "age": 30}
  TSON: {@name,age|Alice,30}

### Rule 3: For Arrays of Uniform Objects, Use Tabular Format
Format: {@key1,key2#N|val1,val2|val1,val2}
- Keys declared ONCE with #N (N = number of rows)
- Rows separated by |

Example:
  JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
  TSON: {@id,name#2|1,Alice|2,Bob}

### Rule 4: Nested Objects - Declare Schema in Header
When a field contains an OBJECT, use (@schema) notation:
Format: key(@subkey1,subkey2)

Example:
  JSON: [{"id": 1, "addr": {"city": "NYC", "zip": "10001"}}, {"id": 2, "addr": {"city": "LA", "zip": "90210"}}]
  TSON: {@id,addr(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90210"}}
  
  Note: addr values are {city_val,zip_val} - just values, no keys!

### Rule 5: Nested Arrays - Use #N INSIDE Parentheses + Brackets
When a field contains an ARRAY OF OBJECTS, put count INSIDE ():
Format: key(@subkey1,subkey2#M)  ← #M inside means array of M items
Values use BRACKETS: [{...},{...}]  ← NOT pipes!

Example:
  JSON: [
    {"user": "Alice", "orders": [{"product": "Apple", "qty": 2}, {"product": "Banana", "qty": 3}]},
    {"user": "Bob", "orders": [{"product": "Orange", "qty": 1}, {"product": "Grape", "qty": 5}]}
  ]
  TSON: {@user,orders(@product,qty#2)#2|Alice,[{Apple,2},{Banana,3}]|Bob,[{Orange,1},{Grape,5}]}
  
  Breaking it down:
  - orders(@product,qty#2) → "orders" is array of 2 objects with keys product,qty
  - #2 at end → 2 top-level rows (Alice and Bob)
  - [{Apple,2},{Banana,3}] → brackets for nested arrays, not pipes!

### Rule 6: String Quoting
Quote strings ONLY if they contain special characters: , | @ # { } [ ] ( ) " or whitespace
Quote numeric strings to preserve type: "10001" vs 10001

### Rule 7: Non-Uniform Arrays
If array elements have different keys, use standard JSON-like format:
[{@k1|v1},{@k2|v2}]

## COMMON MISTAKES TO AVOID

❌ WRONG: Using pipes for nested arrays
   {@user,items(@x)#2|Alice,{1}|{2}|Bob,...}
   
✅ RIGHT: Using brackets for nested arrays  
   {@user,items(@x#2)#2|Alice,[{1},{2}]|Bob,[{3},{4}]}

❌ WRONG: Putting #N outside parentheses for nested arrays
   {@user,items(@x)#2#2|...}  ← ambiguous!
   
✅ RIGHT: #N inside for nested, #N outside for top-level
   {@user,items(@x#2)#2|...}

❌ WRONG: Repeating keys in nested values
   {@id,addr(@city)|1,{@city|NYC}}  ← don't repeat @city
   
✅ RIGHT: Just values in nested objects
   {@id,addr(@city)|1,{NYC}}

## QUICK DECISION TREE

Is this field value...
├── A primitive (string/number/bool/null)? → Just write the value
├── A simple array [1,2,3]? → Write as [1,2,3]
├── A single object? → {@keys|values}
├── An array of uniform objects?
│   └── Is it a TOP-LEVEL array? → {@keys#N|row|row}
│   └── Is it a NESTED field? → key(@schema#N) with values as [{...},{...}]
└── A nested object? → key(@schema) with value as {...}
```

---

## System Prompt (Concise Version)

For contexts where token efficiency matters:

```
TSON converts JSON to compact format. Follow these rules:

STRUCTURE:
• Object: {@key1,key2|val1,val2}
• Array of objects: {@key1,key2#N|row1|row2}  (N=count, rows split by |)
• Simple array: [v1,v2,v3]

NESTED STRUCTURES:
• Nested object: declare schema in key - addr(@city,zip) → value is {NYC,"10001"}
• Nested array: put count INSIDE parens - items(@x,y#2) → value is [{1,a},{2,b}]
  CRITICAL: nested arrays use BRACKETS [...], not pipes!

EXAMPLES:
{"name":"Alice","age":30}
→ {@name,age|Alice,30}

[{"id":1,"name":"A"},{"id":2,"name":"B"}]  
→ {@id,name#2|1,A|2,B}

{"user":"A","items":[{"x":1},{"x":2}]}
→ {@user,items(@x#2)|A,[{1},{2}]}

[{"name":"A","orders":[{"p":"X","q":1},{"p":"Y","q":2}]},{"name":"B","orders":[{"p":"Z","q":3},{"p":"W","q":4}]}]
→ {@name,orders(@p,q#2)#2|A,[{X,1},{Y,2}]|B,[{Z,3},{W,4}]}

QUOTING: Only quote strings with special chars (, | @ # { } [ ] ( ) " space)
```

---

## Conversion Prompts

### TSON → JSON

```
Convert this TSON to JSON:

{@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}
```

**Expected output:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"},
  {"id": 3, "name": "Carol", "email": "carol@example.com"}
]
```

### JSON → TSON (Complex Nested Example)

This is the most challenging conversion. Follow step-by-step:

```
Convert this JSON to TSON:

[
  {
    "company": "Acme",
    "employees": [
      {"id": 1, "name": "Alice", "skills": ["Python", "Go"]},
      {"id": 2, "name": "Bob", "skills": ["Java"]}
    ]
  },
  {
    "company": "Beta",
    "employees": [
      {"id": 3, "name": "Carol", "skills": ["Rust", "C++"]},
      {"id": 4, "name": "Dave", "skills": ["JavaScript"]}
    ]
  }
]
```

**Step-by-step conversion:**

1. **Identify structure**: Array of 2 companies → `{@...#2|company1|company2}`

2. **Top-level keys**: `company`, `employees`
   - `company` is string → just a value
   - `employees` is array of 2 objects → nested array schema!

3. **Nested employees schema**: Each employee has `id`, `name`, `skills`
   - `skills` is a simple array, not uniform objects → stays as [...]
   - Schema: `employees(@id,name,skills#2)` (2 employees per company)

4. **Assemble**:
   ```
   {@company,employees(@id,name,skills#2)#2|Acme,[{1,Alice,[Python,Go]},{2,Bob,[Java]}]|Beta,[{3,Carol,[Rust,C++]},{4,Dave,[JavaScript]}]}
   ```

**Breaking down the result:**
- `employees(@id,name,skills#2)` → nested array with schema
- `#2` inside `()` → 2 employees per company
- `#2` at very end → 2 companies total
- `[{...},{...}]` → brackets for nested arrays
- `[Python,Go]` → simple arrays stay as brackets with values

---

## Task Prompts

### Data Analysis with TSON Input

```
Here is employee data in TSON format:

{@id,name,dept,salary#5|1,Alice,Engineering,120000|2,Bob,Sales,95000|3,Carol,Engineering,115000|4,Dave,Marketing,85000|5,Eve,Engineering,125000}

Question: What is the average salary for Engineering department?
```

**Expected output:**
```
Engineering employees: Alice ($120,000), Carol ($115,000), Eve ($125,000)
Average: $120,000
```

### Generate TSON Output

```
Create sample product data with fields: id, name, price, in_stock.
Generate 4 products. Return in TSON format.
```

**Expected output:**
```
{@id,name,price,in_stock#4|1,Widget,29.99,true|2,Gadget,49.99,true|3,Gizmo,19.99,false|4,Thingamajig,39.99,true}
```

---

## Edge Case Prompts

### Special Characters in Values

```
Convert to TSON:

{
  "path": "C:\\Users\\Documents",
  "message": "He said \"hello\"",
  "list": "a,b,c"
}
```

**Expected output:**
```
{@path,message,list|"C:\\Users\\Documents","He said \"hello\"","a,b,c"}
```

### Special Characters in Keys

```
Convert to TSON:

{
  "key,with,commas": "value1",
  "key|with|pipes": "value2",
  "normal_key": "value3"
}
```

**Expected output:**
```
{@"key,with,commas","key|with|pipes",normal_key|value1,value2,value3}
```

### Nested Schema with Special Keys

```
Convert to TSON:

[
  {"id": 1, "data": {"field,one": "a", "field|two": "b"}},
  {"id": 2, "data": {"field,one": "c", "field|two": "d"}}
]
```

**Expected output:**
```
{@id,data(@"field,one","field|two")#2|1,{a,b}|2,{c,d}}
```

### Nested Arrays (v1.2)

```
Convert to TSON:

[
  {"user": "Alice", "orders": [{"product": "Apple", "qty": 2}, {"product": "Banana", "qty": 3}]},
  {"user": "Bob", "orders": [{"product": "Orange", "qty": 1}, {"product": "Grape", "qty": 5}]}
]
```

**Expected output:**
```
{@user,orders(@product,qty#2)#2|Alice,[{Apple,2},{Banana,3}]|Bob,[{Orange,1},{Grape,5}]}
```

**Key points:**
- `#2` inside `(@product,qty#2)` = each user has 2 orders
- `#2` after the schema = 2 users total
- Nested arrays use `[{...},{...}]` brackets

### Preserving String vs Number Types

```
Convert to TSON, preserving types:

{"zip_code": "10001", "count": 10001, "version": "1.0", "price": 1.0}
```

**Expected output:**
```
{@zip_code,count,version,price|"10001",10001,"1.0",1.0}
```

---

## Function Calling Prompts

### TSON as Function Parameter

```
You have access to a function that accepts TSON data:

analyze_data(data: TSON string) -> results

User: I have sales data:
- 2025-01-01: North $5000
- 2025-01-02: South $6000
- 2025-01-03: East $5500

Call analyze_data with this data.
```

**Expected output:**
```
analyze_data("{@date,region,sales#3|2025-01-01,North,5000|2025-01-02,South,6000|2025-01-03,East,5500}")
```

---

## Test Prompts

### Quick Validation Test

```
Test 1: How many records in this TSON?
{@id,name#3|1,Alice|2,Bob|3,Carol}

Test 2: Convert to TSON:
[{"x": 10, "y": 20}, {"x": 30, "y": 40}]

Test 3: What is "name" in the 2nd record?
{@id,name,age#3|1,Alice,30|2,Bob,25|3,Carol,35}
```

**Expected answers:**
```
Test 1: 3 records
Test 2: {@x,y#2|10,20|30,40}
Test 3: Bob
```

### Edge Case Validation

```
Verify these TSON strings are correct:

1. Key with parentheses: {@"func()"|value}
2. Backslash in value: {@path|"C:\\Users"}
3. Quote in value: {@msg|"He said \"hi\""}
4. Nested schema special keys: {@id,info(@"a,b")#1|1,{val}}

For each, show the equivalent JSON.
```

**Expected:**
```
1. {"func()": "value"}
2. {"path": "C:\\Users"}
3. {"msg": "He said \"hi\""}
4. [{"id": 1, "info": {"a,b": "val"}}]
```

---

## Best Practices

### DO ✅
- Provide 2-3 examples in prompts
- Use `#N` row counts for clarity
- Specify "Return as TSON" or "Return as JSON"
- Quote strings with special characters
- Escape quotes and backslashes properly

### DON'T ❌
- Mix TSON and JSON in same structure
- Use TSON for tiny data (<100 tokens)
- Forget to quote strings with delimiters
- Assume unquoted strings with @ or # are valid

---

## Token Savings Comparison

**JSON (verbose):**
```json
[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"},{"id":3,"name":"Carol"}]
```
~65 characters

**TSON (compact):**
```
{@id,name#3|1,Alice|2,Bob|3,Carol}
```
~35 characters (46% smaller)

**Savings scale with data size!**

---

## Python Template

```python
SYSTEM_PROMPT = """
You work with TSON (Token-efficient Structured Object Notation).

Syntax:
• {@key1,key2|val1,val2} = object
• {@key1,key2#N|v1,v2|v1,v2} = array of objects
• [v1,v2,v3] = array
• Quote strings containing: , | @ # { } [ ] ( ) " space

Examples:
{@name,age|Alice,30} = {"name":"Alice","age":30}
{@id,name#2|1,Alice|2,Bob} = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
"""

def convert_to_tson_prompt(json_data):
    return f"Convert to TSON:\n\n{json_data}"

def convert_to_json_prompt(tson_data):
    return f"Convert to JSON:\n\n{tson_data}"
```

---

**These prompts are production-ready. Copy and use them!**
