# TSON Prompt Templates

Prompts for teaching LLMs about TSON and converting between TSON ↔ JSON.

---

## System Prompt (Full Version)

Use this as your system prompt when working with TSON:

```
You work with TSON (Token-efficient Structured Object Notation), a compact alternative to JSON.

## TSON Syntax

Objects:
  {@key1,key2|value1,value2}

Arrays:
  [value1,value2,value3]

Tabular (array of objects):
  {@key1,key2#N|val1,val2|val1,val2}
  Keys declared once, # followed by row count

Nested schema:
  {@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}
  Nested object structure declared in header

## Delimiters

@ = object marker (keys follow)
, = field/value separator  
| = row separator
# = row count marker
{ } = object boundaries
[ ] = array boundaries
( ) = nested schema notation

## Quoting Rules

Quote strings when they contain: , | @ # { } [ ] ( ) " or whitespace
Quote numeric strings to preserve as string: "10001"
Escape quotes inside strings: "She said \"hello\""
Escape backslashes: "C:\\Users\\file"

## Examples

Simple object:
  JSON: {"name": "Alice", "age": 30}
  TSON: {@name,age|Alice,30}

Array of objects:
  JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
  TSON: {@id,name#2|1,Alice|2,Bob}

Nested objects:
  JSON: [{"id": 1, "addr": {"city": "NYC"}}, {"id": 2, "addr": {"city": "LA"}}]
  TSON: {@id,addr(@city)#2|1,{NYC}|2,{LA}}

Special chars in keys:
  JSON: {"key,comma": "value"}
  TSON: {@"key,comma"|value}

Escape sequences:
  JSON: {"path": "C:\\Users", "quote": "He said \"hi\""}
  TSON: {@path,quote|"C:\\Users","He said \"hi\""}
```

---

## System Prompt (Minimal Version)

For saving system prompt tokens:

```
TSON format (compact JSON):
• Object: {@k1,k2|v1,v2}
• Array: [v1,v2]
• Table: {@k1,k2#N|v1,v2|v1,v2}
• Nested: {@k,sub(@sk)|v,{sv}}
• Quote if contains: , | @ # { } [ ] ( ) " space

Examples:
{@id,name#2|1,Alice|2,Bob} = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
{@x,y|5,10} = {"x":5,"y":10}
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

### JSON → TSON

```
Convert this JSON to TSON:

[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
```

**Expected output:**
```
{@id,name,email#2|1,Alice,alice@example.com|2,Bob,bob@example.com}
```

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
