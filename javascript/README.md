# TSON for JavaScript/TypeScript

**Token-efficient Structured Object Notation - JavaScript/TypeScript Implementation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![npm version](https://img.shields.io/npm/v/@zenoaihq/tson.svg)](https://www.npmjs.com/package/@zenoaihq/tson)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-blue.svg)](https://www.typescriptlang.org/)

A compact serialization format designed for efficient data exchange with Large Language Models (LLMs). TSON achieves **25-70% token savings** compared to JSON while maintaining perfect round-trip conversion.

## Why TSON?

When working with LLMs, every token costs money and context space. JSON's verbose syntax wastes tokens on formatting rather than data:

- Repeated keys in arrays of objects
- Excessive punctuation (quotes, colons, brackets)
- Unnecessary whitespace in compact mode

TSON solves this with a delimiter-based format optimized for token efficiency.

## Installation

```bash
npm install @zenoaihq/tson
```

```bash
pnpm add @zenoaihq/tson
```

```bash
yarn add @zenoaihq/tson
```

## Quick Start

```typescript
import { dumps, loads } from '@zenoaihq/tson';

// Simple object
const data = { name: 'Alice', age: 30, active: true };
const encoded = dumps(data);
console.log(encoded);
// Output: {@name,age,active|Alice,30,true}

// Perfect round-trip
const decoded = loads(encoded);
console.log(decoded); // { name: 'Alice', age: 30, active: true }
```

## Token Savings Example

```typescript
import { dumps } from '@zenoaihq/tson';

const data = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
  { id: 3, name: 'Carol', email: 'carol@example.com' },
];

// JSON: 153 characters
const json = JSON.stringify(data);
console.log(json.length); // 153

// TSON: 90 characters (41% savings!)
const tson = dumps(data);
console.log(tson.length); // 90
console.log(tson);
// {@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}
```

Keys are written **once**, not repeated for each row!

## API Reference

### Serialization

```typescript
import { dumps, dump } from '@zenoaihq/tson';

// Serialize JavaScript data to TSON string
const tsonString = dumps(data);

// Serialize to file (Node.js only)
await dump(data, 'data.tson');
```

### Deserialization

```typescript
import { loads, load } from '@zenoaihq/tson';

// Deserialize TSON string to JavaScript data
const data = loads(tsonString);

// Deserialize from file (Node.js only)
const data = await load('data.tson');
```

## TypeScript Support

Full TypeScript support with comprehensive type definitions:

```typescript
import { dumps, loads, TSONValue, TSONObject, TSONArray } from '@zenoaihq/tson';

const data: TSONObject = {
  name: 'Alice',
  age: 30,
  tags: ['developer', 'typescript'],
};

const encoded: string = dumps(data);
const decoded: TSONValue = loads(encoded);
```

## Examples

### 1. Simple Objects

```typescript
const data = { name: 'Alice', age: 30, active: true };
const encoded = dumps(data);
// {@name,age,active|Alice,30,true}
```

### 2. Arrays

```typescript
const data = [1, 2, 3, 4, 5];
const encoded = dumps(data);
// [1,2,3,4,5]
```

### 3. Array of Objects (Tabular Format)

```typescript
const data = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
  { id: 3, name: 'Carol', email: 'carol@example.com' },
];
const encoded = dumps(data);
// {@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}

const decoded = loads(encoded);
// Perfect round-trip!
```

### 4. Nested Schema Notation

```typescript
const data = [
  { id: 1, name: 'Alice', address: { city: 'NYC', zip: '10001' } },
  { id: 2, name: 'Bob', address: { city: 'LA', zip: '90001' } },
];
const encoded = dumps(data);
// {@id,name,address(@city,zip)#2|1,Alice,{NYC,"10001"}|2,Bob,{LA,"90001"}}
```

Address keys (`city`, `zip`) are declared once in the schema notation `address(@city,zip)`, then only values appear in rows!

### 5. Complex Nested Structures

```typescript
const data = {
  company: 'Acme Corp',
  employees: [
    {
      id: 1,
      name: 'Alice',
      skills: ['Python', 'Go'],
      contact: { email: 'alice@acme.com', phone: '555-0101' },
    },
    {
      id: 2,
      name: 'Bob',
      skills: ['Java'],
      contact: { email: 'bob@acme.com', phone: '555-0102' },
    },
  ],
  metadata: {
    created: '2025-01-27',
    version: '1.0',
  },
};

const encoded = dumps(data);
const decoded = loads(encoded);
// Perfect round-trip with complex nesting!
```

### 6. Type Preservation

```typescript
const data = {
  zip_string: '10001', // String
  zip_number: 10001, // Number
  version_string: '1.0', // String
  version_number: 1.0, // Float
};

const encoded = dumps(data);
// {@zip_string,zip_number,version_string,version_number|"10001",10001,"1.0",1.0}

const decoded = loads(encoded);
console.log(typeof decoded.zip_string); // "string"
console.log(typeof decoded.zip_number); // "number"
```

### 7. Empty Values

```typescript
const data = {
  empty_string: '',
  empty_array: [],
  empty_object: {},
  null_value: null,
};

const encoded = dumps(data);
// {@empty_string,empty_array,empty_object,null_value|"",[],{@},null}
```

### 8. Special Characters

```typescript
const data = {
  comma: 'hello, world',
  pipe: 'a|b|c',
  quotes: 'She said "hello"',
  newline: 'line1\nline2',
  at_sign: '@username',
};

const encoded = dumps(data);
const decoded = loads(encoded);
// Special characters are automatically escaped and preserved
```

## LLM Integration

### Quick Example

```typescript
import { dumps } from '@zenoaihq/tson';

// Prepare data for LLM
const data = [
  { date: '2025-01-01', sales: 5000, region: 'North' },
  { date: '2025-01-02', sales: 6000, region: 'South' },
  { date: '2025-01-03', sales: 5500, region: 'East' },
];

const tsonData = dumps(data);

// System prompt for LLM
const systemPrompt = `
TSON format (compact JSON):
• {@k1,k2|v1,v2} = object
• {@k1,k2#N|v1,v2|v1,v2} = array of objects
• Delimiters: @ (keys), | (rows), , (fields), # (count)
`;

const userPrompt = `Analyze this sales data: ${tsonData}`;

// Send to LLM API...
// Token savings: 30-50% compared to JSON!
```

See [../prompts.md](../prompts.md) for complete LLM prompt templates.

## Platform Support

- **Node.js**: 16.0.0 or higher
- **Browser**: All modern browsers (ES2020+)
- **Deno**: Compatible (use npm: specifier)
- **Bun**: Compatible

### Node.js

```typescript
import { dumps, loads, dump, load } from '@zenoaihq/tson';

// File I/O available
await dump(data, 'data.tson');
const data = await load('data.tson');
```

### Browser

```typescript
import { dumps, loads } from '@zenoaihq/tson';

// File I/O not available in browser
// Use dumps/loads for string serialization
const encoded = dumps(data);
const decoded = loads(encoded);
```

## Type Support

TSON supports all JSON-compatible types:

| JavaScript Type | TSON Representation      | Example                     |
| --------------- | ------------------------ | --------------------------- |
| `string`        | String (quoted if needed)| `Alice` or `"Hello, World"` |
| `number`        | Number                   | `42`, `3.14`, `-17`         |
| `boolean`       | Boolean                  | `true`, `false`             |
| `null`          | Null                     | `null`                      |
| `Array`         | Array                    | `[1,2,3]`                   |
| `Object`        | Object                   | `{@key|value}`              |

## Performance

TSON is optimized for:

- **Token efficiency**: 25-70% savings vs JSON
- **Fast parsing**: Simple delimiter-based parsing
- **Low memory**: Minimal overhead
- **Zero dependencies**: Pure TypeScript implementation
- **Tree-shakeable**: ESM with no side effects

## Syntax Guide

See [../SPEC.md](../SPEC.md) for complete syntax specification.

**Quick reference:**

| Delimiter | Purpose              | Example                |
| --------- | -------------------- | ---------------------- |
| `{` `}`   | Object boundaries    | `{@name|Alice}`        |
| `[` `]`   | Array boundaries     | `[1,2,3]`              |
| `@`       | Object marker        | `{@key1,key2|...}`     |
| `,`       | Field/value separator| `name,age,city`        |
| `|`       | Row separator        | `val1,val2|val1,val2`  |
| `#`       | Row count (optional) | `#3`                   |

## Testing

Run the test suite:

```bash
npm test
```

All 13 tests should pass:

```
✓ should handle simple objects
✓ should handle simple arrays
✓ should handle array of objects in tabular format
✓ should handle nested objects
✓ should handle mixed type arrays
✓ should handle empty values
✓ should handle special characters
✓ should preserve numeric strings vs numbers
✓ should handle nested arrays
✓ should handle array with nested objects using nested schema
✓ should handle complex real-world-like structures
✓ should handle boolean values
✓ should handle various numeric types

Test Files  1 passed (1)
     Tests  13 passed (13)
```

## Examples

Run the examples:

```bash
npm run dev examples/basic-usage.ts
```

Or with ts-node:

```bash
npx tsx examples/basic-usage.ts
```

## Building

Build the package:

```bash
npm run build
```

This generates:

- `dist/index.js` - ESM build
- `dist/index.cjs` - CommonJS build
- `dist/index.d.ts` - TypeScript declarations

## Development

```bash
# Install dependencies
npm install

# Run tests in watch mode
npm run test:watch

# Type check
npm run typecheck

# Lint
npm run lint

# Format
npm run format
```

## Contributing

Contributions are welcome! Please see [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Documentation

- **[../SPEC.md](../SPEC.md)** - Complete format specification (v1.0)
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[../prompts.md](../prompts.md)** - LLM integration guide
- **[examples/](examples/)** - Usage examples

## Comparison with JSON

**Example: Array of 100 user objects**

```typescript
// JSON: ~8,500 characters
// TSON: ~4,200 characters
// Savings: 50%+ (scales with more rows!)
```

**Why TSON wins:**

- Keys written once (tabular format)
- No quotes around simple strings
- No colons, minimal brackets
- Optional whitespace
- Nested schema notation for complex structures

## Related Projects

- [Python Implementation](../python/) - Production ready
- [TOON by Johann Schopplich](https://github.com/johannschopplich/toon) - Alternative format

## License

MIT License - see [LICENSE](../LICENSE) file for details.

---

**Package:** `@zenoaihq/tson`
**Version:** 1.0.0
**Status:** Production Ready
**Node.js:** 16.0.0+
**TypeScript:** 5.3+
**Dependencies:** 0

*Built by [Zeno AI](https://zenoai.tech) for efficient LLM communication*
