# TSON Format Prompts

Prompts for teaching LLMs about TSON and converting between TSON ↔ JSON.

---

## System Prompt: TSON Format Explanation

**Use this as your system prompt when working with TSON:**

```
You are working with TSON (Token-efficient Structured Object Notation), a compact alternative to JSON.

TSON Syntax:
• Objects: {@key1,key2|value1,value2}
• Arrays: [value1,value2,value3]
• Tabular (array of objects): {@key1,key2#N|val1,val2|val1,val2}
• Nested schema: {@field,nested(@subkey1,subkey2)|value,{subval1,subval2}}

Delimiters:
• @ = object marker
• , = field/value separator
• | = row separator
• # = row count

Primitives:
• Strings: Alice or "quoted string"
• Numbers: 42, 3.14
• Booleans: true, false
• Null: null

Examples:

1. Simple object:
   JSON: {"name": "Alice", "age": 30}
   TSON: {@name,age|Alice,30}

2. Array:
   JSON: [1, 2, 3]
   TSON: [1,2,3]

3. Array of objects (tabular):
   JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
   TSON: {@id,name#2|1,Alice|2,Bob}

4. Nested objects with schema:
   JSON: [{"id": 1, "address": {"city": "NYC", "zip": "10001"}}, {"id": 2, "address": {"city": "LA", "zip": "90001"}}]
   TSON: {@id,address(@city,zip)#2|1,{NYC,"10001"}|2,{LA,"90001"}}

Key Rules:
• Keys are written ONCE in header, then only values in rows
• Use | to separate rows, , to separate values
• Include #N to specify row count
• Quote strings only if they contain special characters: , | @ # { } [ ]
• Nested objects with repeated structure use (@key1,key2) notation
```

---

## Prompt 1: Convert TSON to JSON

**User prompt template:**

```
Convert this TSON data to JSON format:

TSON:
{@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}

Return as valid JSON.
```

**Expected output:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"},
  {"id": 3, "name": "Carol", "email": "carol@example.com"}
]
```

---

## Prompt 2: Convert JSON to TSON

**User prompt template:**

```
Convert this JSON data to TSON format:

JSON:
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"},
  {"id": 3, "name": "Carol", "email": "carol@example.com"}
]

Return as TSON.
```

**Expected output:**
```
{@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}
```

---

## Prompt 3: TSON with Task (Parsing Input)

**User prompt template:**

```
The following data is in TSON format. Parse it and answer the question.

TSON Data:
{@id,name,department,salary#5|1,Alice,Engineering,120000|2,Bob,Sales,95000|3,Carol,Engineering,115000|4,Dave,Marketing,85000|5,Eve,Engineering,125000}

Question: What is the average salary for Engineering department employees?
```

**Expected output:**
```
The Engineering department has 3 employees:
- Alice: $120,000
- Carol: $115,000
- Eve: $125,000

Average salary: $120,000
```

---

## Prompt 4: Generate TSON Output

**User prompt template:**

```
Generate sample employee data with the following fields: id, name, department, hire_date.

Create 5 employees.

Return in TSON format.
```

**Expected output:**
```
{@id,name,department,hire_date#5|1,Alice,Engineering,2023-01-15|2,Bob,Sales,2023-02-20|3,Carol,Marketing,2023-03-10|4,Dave,Engineering,2023-04-05|5,Eve,Design,2023-05-12}
```

---

## Prompt 5: Complex Nested TSON

**User prompt template:**

```
Convert this JSON with nested objects to TSON:

JSON:
[
  {
    "id": 1,
    "name": "Alice",
    "contact": {
      "email": "alice@example.com",
      "phone": "555-0101"
    }
  },
  {
    "id": 2,
    "name": "Bob",
    "contact": {
      "email": "bob@example.com",
      "phone": "555-0102"
    }
  }
]

Use nested schema notation for the contact field.
```

**Expected output:**
```
{@id,name,contact(@email,phone)#2|1,Alice,{alice@example.com,555-0101}|2,Bob,{bob@example.com,555-0102}}
```

---

## Prompt 6: TSON to JSON with Validation

**User prompt template:**

```
Convert this TSON to JSON and validate the structure:

TSON:
{@user_id,username,is_active,last_login#3|101,alice,true,2025-01-27|102,bob,false,2025-01-20|103,carol,true,2025-01-26}

Requirements:
1. Convert to valid JSON
2. Ensure all data types are correct (numbers, booleans, strings)
3. Format the JSON with proper indentation
```

**Expected output:**
```json
[
  {
    "user_id": 101,
    "username": "alice",
    "is_active": true,
    "last_login": "2025-01-27"
  },
  {
    "user_id": 102,
    "username": "bob",
    "is_active": false,
    "last_login": "2025-01-20"
  },
  {
    "user_id": 103,
    "username": "carol",
    "is_active": true,
    "last_login": "2025-01-26"
  }
]
```

---

## Prompt 7: Bidirectional Conversion Test

**User prompt template:**

```
Test your understanding of TSON:

1. Convert this JSON to TSON:
{"product": "Widget", "price": 29.99, "in_stock": true}

2. Then convert this TSON to JSON:
{@order_id,product,quantity#2|1001,Widget,5|1002,Gadget,3}

Show both conversions.
```

**Expected output:**
```
1. JSON to TSON:
{@product,price,in_stock|Widget,29.99,true}

2. TSON to JSON:
[
  {"order_id": 1001, "product": "Widget", "quantity": 5},
  {"order_id": 1002, "product": "Gadget", "quantity": 3}
]
```

---

## Prompt 8: Working with TSON in Function Calls

**System prompt + function definition:**

```
You have access to a function that accepts data in TSON format for efficiency.

Function:
analyze_sales_data(data: string in TSON format) -> analysis results

The data parameter should be in TSON tabular format.

Example usage:
analyze_sales_data("{@date,region,sales#3|2025-01-01,North,5000|2025-01-02,South,6000|2025-01-03,East,5500}")
```

**User prompt:**
```
I have sales data for 5 days:
- 2025-01-01, North region, $5,000
- 2025-01-02, South region, $6,000
- 2025-01-03, East region, $5,500
- 2025-01-04, West region, $7,200
- 2025-01-05, North region, $6,800

Call the analyze_sales_data function with this data in TSON format.
```

**Expected output:**
```
analyze_sales_data("{@date,region,sales#5|2025-01-01,North,5000|2025-01-02,South,6000|2025-01-03,East,5500|2025-01-04,West,7200|2025-01-05,North,6800}")
```

---

## Shortened System Prompt (Minimal Version)

**For when you need to save system prompt tokens:**

```
TSON format (compact JSON):
• Object: {@k1,k2|v1,v2}
• Array: [v1,v2,v3]
• Table: {@k1,k2#N|v1,v2|v1,v2}
• Nested: {@k,sub(@sk1,sk2)|v,{sv1,sv2}}

Examples:
{@id,name#2|1,Alice|2,Bob} = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
{@x,y|5,10} = {"x":5,"y":10}
[1,2,3] = [1,2,3]
```

---

## Best Practices for Prompting

### DO:
✅ Provide 2-3 examples in system prompt
✅ Use nested schema notation for repeated structures
✅ Include #N row counts when generating TSON
✅ Specify "Return as TSON" or "Return as JSON" explicitly

### DON'T:
❌ Mix TSON and JSON in same data structure
❌ Expect perfect syntax on first try (use validation)
❌ Use TSON for tiny data (<100 tokens)
❌ Forget to quote strings with special characters

---

## Testing Your Model

**Quick test prompt:**

```
Test 1: Parse this TSON and tell me how many records there are:
{@id,name#3|1,Alice|2,Bob|3,Carol}

Test 2: Convert this JSON to TSON:
[{"x": 10, "y": 20}, {"x": 30, "y": 40}]

Test 3: What is the value of the "name" field in the second record?
{@id,name,age#3|1,Alice,30|2,Bob,25|3,Carol,35}
```

**Expected answers:**
```
Test 1: There are 3 records
Test 2: {@x,y#2|10,20|30,40}
Test 3: Bob
```

---

## Token Savings Example

**Before (JSON):**
```
Prompt: "Analyze this data: [{"id":1,"name":"Alice","dept":"Eng"},{"id":2,"name":"Bob","dept":"Sales"},...]"
Tokens: ~45 per 3 records
```

**After (TSON):**
```
System: "Data in TSON format..." (300 tokens, cached)
Prompt: "Analyze: {@id,name,dept#3|1,Alice,Eng|2,Bob,Sales|...}"
Tokens: ~25 per 3 records (45% savings on data)
```

**Savings scale with data size!**

---

## Ready-to-Use Prompt Template

```python
SYSTEM_PROMPT = """
You work with TSON (Token-efficient Structured Object Notation).

Syntax:
• {@key1,key2|val1,val2} = object
• [@key1,key2#N|v1,v2|v1,v2} = array of objects
• [v1,v2,v3] = array

Examples:
{@name,age|Alice,30} = {"name":"Alice","age":30}
{@id,name#2|1,Alice|2,Bob} = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
{@id,address(@city,zip)|1,{NYC,10001}} = [{"id":1,"address":{"city":"NYC","zip":10001}}]
"""

USER_PROMPT_TSON_TO_JSON = """
Convert to JSON:

TSON: {your_tson_here}
JSON:
"""

USER_PROMPT_JSON_TO_TSON = """
Convert to TSON:

JSON: {your_json_here}
TSON:
"""
```

---

**These prompts are production-ready. Copy and use them!**
