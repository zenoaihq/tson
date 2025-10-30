# TSON Quick Start Guide (JavaScript/TypeScript)

**Get started with TSON in 5 minutes!**

## What is TSON?

TSON (Token-efficient Structured Object Notation) is a compact data format designed for LLMs. It's like JSON, but uses **30-70% fewer tokens**.

## Installation

```bash
npm install @zenoaihq/tson
```

## Basic Usage

### 1. Import

```typescript
import { dumps, loads } from '@zenoaihq/tson';
```

### 2. Serialize (JavaScript → TSON)

```typescript
const data = { name: 'Alice', age: 30 };
const tson = dumps(data);
console.log(tson);
// {@name,age|Alice,30}
```

### 3. Deserialize (TSON → JavaScript)

```typescript
const tson = '{@name,age|Alice,30}';
const data = loads(tson);
console.log(data);
// { name: 'Alice', age: 30 }
```

## Key Features

### Tabular Format (The Magic!)

**The Problem with JSON:**

```json
[
  {"id": 1, "name": "Alice"},
  {"id": 2, "name": "Bob"},
  {"id": 3, "name": "Carol"}
]
```

Keys `id` and `name` are repeated 3 times. Wasteful!

**TSON Solution:**

```typescript
const data = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Carol' },
];

dumps(data);
// {@id,name#3|1,Alice|2,Bob|3,Carol}
```

Keys written **once**. Values in rows. Token savings scale with data size!

### Nested Schema Notation

**Nested objects in arrays:**

```typescript
const data = [
  { id: 1, name: 'Alice', address: { city: 'NYC', zip: '10001' } },
  { id: 2, name: 'Bob', address: { city: 'LA', zip: '90001' } },
];

dumps(data);
// {@id,name,address(@city,zip)#2|1,Alice,{NYC,"10001"}|2,Bob,{LA,"90001"}}
```

The `address(@city,zip)` declares the structure once. Then only values in rows!

### Type Preservation

```typescript
const data = {
  zip_code: '10001', // String
  zip_number: 10001, // Number
};

const tson = dumps(data);
// {@zip_code,zip_number|"10001",10001}

const decoded = loads(tson);
console.log(typeof decoded.zip_code); // "string"
console.log(typeof decoded.zip_number); // "number"
```

Numbers, strings, booleans, and null are all preserved correctly!

## Syntax Cheat Sheet

| Format                  | TSON Syntax                             | Notes                    |
| ----------------------- | --------------------------------------- | ------------------------ |
| Simple object           | `{@key1,key2|val1,val2}`                | Keys then values         |
| Array                   | `[1,2,3]`                               | Like JSON                |
| Array of objects        | `{@key1,key2#N|v1,v2|v1,v2}`            | Tabular (keys once!)     |
| Nested objects          | `{@k1,k2|{@k3|v3},v2}`                  | Objects can nest         |
| Nested schema           | `{@k1,k2(@k3,k4)#N|v1,{v3,v4}}`         | Schema notation          |
| Strings with specials   | `"hello, world"`                        | Quoted when needed       |
| Numbers                 | `42`, `3.14`, `-17`                     | Unquoted                 |
| Booleans                | `true`, `false`                         | Lowercase                |
| Null                    | `null`                                  | Lowercase                |
| Empty values            | `""`, `[]`, `{@}`                       | Explicit empties         |

## File I/O (Node.js)

### Write to file:

```typescript
import { dump } from '@zenoaihq/tson';

const data = { users: [{ id: 1, name: 'Alice' }] };
await dump(data, 'data.tson');
```

### Read from file:

```typescript
import { load } from '@zenoaihq/tson';

const data = await load('data.tson');
console.log(data);
```

## Real-World Example

### Employee Database

```typescript
import { dumps, loads } from '@zenoaihq/tson';

const employees = [
  {
    id: 1,
    name: 'Alice Johnson',
    email: 'alice@acme.com',
    department: 'Engineering',
    salary: 120000,
  },
  {
    id: 2,
    name: 'Bob Smith',
    email: 'bob@acme.com',
    department: 'Design',
    salary: 95000,
  },
  {
    id: 3,
    name: 'Carol Davis',
    email: 'carol@acme.com',
    department: 'Marketing',
    salary: 85000,
  },
];

// Serialize
const tson = dumps(employees);
console.log(tson);
// {@id,name,email,department,salary#3|1,Alice Johnson,alice@acme.com,Engineering,120000|2,Bob Smith,bob@acme.com,Design,95000|3,Carol Davis,carol@acme.com,Marketing,85000}

console.log(`JSON size: ${JSON.stringify(employees).length} chars`);
console.log(`TSON size: ${tson.length} chars`);
// Savings: ~45%!

// Deserialize
const decoded = loads(tson);
console.log(decoded[0].name); // "Alice Johnson"
```

## Token Savings Examples

### Small Dataset (3 rows)

```typescript
const data = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 3, name: 'Carol' },
];

// JSON: 71 characters
// TSON: 36 characters
// Savings: 49%
```

### Medium Dataset (10 rows)

```typescript
// 10 user objects with id, name, email
// JSON: ~450 characters
// TSON: ~270 characters
// Savings: 40%
```

### Large Dataset (100 rows)

```typescript
// 100 user objects
// JSON: ~8,500 characters
// TSON: ~4,200 characters
// Savings: 51%
```

**Savings increase with more rows!**

## TypeScript Integration

```typescript
import { dumps, loads, TSONObject, TSONArray, TSONValue } from '@zenoaihq/tson';

// Type your data
interface User {
  id: number;
  name: string;
  email: string;
}

const users: User[] = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
];

// Serialize
const tson: string = dumps(users);

// Deserialize (type assertion needed)
const decoded = loads(tson) as User[];
console.log(decoded[0].name); // TypeScript knows this is a User
```

## Using with LLMs

### Sending Data to LLM

```typescript
import { dumps } from '@zenoaihq/tson';

const salesData = [
  { date: '2025-01-01', revenue: 5000, region: 'North' },
  { date: '2025-01-02', revenue: 6200, region: 'South' },
  { date: '2025-01-03', revenue: 4800, region: 'East' },
];

// Convert to TSON
const tsonData = dumps(salesData);

// Include in prompt
const prompt = `
Analyze this sales data and provide insights:

${tsonData}

What trends do you see?
`;

// Send to your LLM API
// Uses 30-50% fewer tokens than JSON!
```

### System Prompt for LLM

Include this in your system message to teach the LLM about TSON:

```
TSON Format Guide:
• {@key1,key2|val1,val2} - Object with keys and values
• {@key1,key2#N|v1,v2|v1,v2} - Array of N objects (tabular)
• [1,2,3] - Simple array
• Delimiters: @ (keys), | (rows), , (fields), # (count)
• Quotes only when needed (spaces, special chars, looks like number)
```

## Common Patterns

### 1. Config Objects

```typescript
const config = {
  api_key: 'sk-abc123',
  timeout: 5000,
  retries: 3,
  enabled: true,
};

dumps(config);
// {@api_key,timeout,retries,enabled|sk-abc123,5000,3,true}
```

### 2. API Responses

```typescript
const response = {
  status: 'success',
  data: [
    { id: 1, value: 100 },
    { id: 2, value: 200 },
  ],
  timestamp: '2025-01-27T10:30:00Z',
};

dumps(response);
// Compact format, perfect for caching or logging
```

### 3. Form Data

```typescript
const formData = {
  username: 'alice',
  email: 'alice@example.com',
  age: 30,
  newsletter: true,
  interests: ['tech', 'books', 'travel'],
};

const tson = dumps(formData);
// Store or transmit efficiently
```

## Best Practices

### ✅ DO

- Use TSON for LLM prompts (huge token savings)
- Use tabular format for arrays of uniform objects
- Use TSON for data storage when space matters
- Keep data JSON-compatible for portability

### ❌ DON'T

- Don't use TSON for human-readable config files (use JSON/YAML)
- Don't mix different object structures in arrays (breaks tabular optimization)
- Don't expect TSON to be human-friendly (it's machine-optimized)

## Troubleshooting

### Issue: Type mismatch after deserialization

```typescript
// Problem: "10001" becomes 10001
const data = { zip: '10001' };
const tson = dumps(data);
const decoded = loads(tson);
console.log(typeof decoded.zip); // "number" 😱

// Solution: Strings that look like numbers are automatically quoted
// This shouldn't happen! If it does, it's a bug - please report it.
```

### Issue: Special characters not preserved

```typescript
// TSON automatically escapes special characters
const data = { text: 'hello, world | special @ chars' };
const tson = dumps(data); // Quotes and escapes automatically
const decoded = loads(tson); // Unescapes automatically
// Works perfectly!
```

## Next Steps

- Read the [complete README](README.md) for full API reference
- Check out [examples/](examples/) for more use cases
- See [../SPEC.md](../SPEC.md) for format specification
- Learn about [LLM integration](../prompts.md)

## Quick Reference Card

```typescript
// Import
import { dumps, loads, dump, load } from '@zenoaihq/tson';

// Serialize
const tson = dumps(data); // object → TSON string
await dump(data, 'file.tson'); // object → file (Node.js)

// Deserialize
const data = loads(tson); // TSON string → object
const data = await load('file.tson'); // file → object (Node.js)

// Types (TypeScript)
import type { TSONValue, TSONObject, TSONArray } from '@zenoaihq/tson';
```

---

**Ready to save tokens?** Start using TSON today!

For questions or issues, visit: https://github.com/zenoaihq/tson
