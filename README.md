# TSON

**Token-efficient Structured Object Notation**

A compact, delimiter-based serialization format designed for efficient data exchange with Large Language Models.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![npm version](https://img.shields.io/npm/v/@zenoaihq/tson.svg)](https://www.npmjs.com/package/@zenoaihq/tson)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/zenoaihq/tson)

---

## Table of Contents

- [Why TSON?](#why-tson)
- [Benchmarks](#benchmarks)
- [When NOT to Use TSON](#when-not-to-use-tson)
- [Quick Start](#quick-start)
- [Implementations](#implementations)
- [Core Features](#core-features)
- [Use Cases](#use-cases)
- [Playground](#playground)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Why TSON?

When working with Large Language Models, every token counts. JSON's verbose syntax—with repeated keys, excessive punctuation, and mandatory quotes—wastes tokens on formatting rather than meaningful data.

**TSON solves this through:**
- 🎯 **Schema Declarations** - Write keys once, not for every object
- 🔄 **Nested Schema Notation** - Declare nested object structures upfront
- ⚡ **Single Syntax** - One consistent format for all data types
- 🤖 **LLM-Friendly** - Delimiter-based structure that models can reliably parse and generate
- 🔒 **Lossless** - Perfect round-trip conversion to/from JSON

### Quick Example

**JSON (138 characters):**
```json
[{"id":1,"name":"Alice","email":"alice@example.com"},{"id":2,"name":"Bob","email":"bob@example.com"},{"id":3,"name":"Carol","email":"carol@example.com"}]
```

**TSON (92 characters, 33% smaller):**
```
{@id,name,email#3|1,Alice,alice@example.com|2,Bob,bob@example.com|3,Carol,carol@example.com}
```

Field names (`id`, `name`, `email`) written **once** instead of repeated for each object.

---

## Benchmarks

Benchmarks run on [JsonSchemaBench](https://github.com/guidance-ai/jsonschemabench) - a comprehensive dataset of 9,558 real-world JSON schemas.

### Size Reduction vs JSON

```
📊 JsonSchemaBench Results (9,558 schemas, 100% roundtrip pass)

Dataset              │ Schemas │  JSON Size │  TSON Size │ Savings
─────────────────────┼─────────┼────────────┼────────────┼─────────
Github Trivial       │     444 │    319 KB  │    261 KB  │  18.2%
Github Easy          │   1,943 │  1,106 KB  │    911 KB  │  17.6%
Github Medium        │   1,976 │  3,513 KB  │  2,876 KB  │  18.1%
Github Hard          │   1,240 │  8,946 KB  │  7,548 KB  │  15.6%
Github Ultra         │     164 │  6,429 KB  │  5,607 KB  │  12.8%
Glaiveai2K           │   1,707 │    958 KB  │    795 KB  │  17.1%
JsonSchemaStore      │     492 │ 12,320 KB  │ 10,590 KB  │  14.0%
Kubernetes           │   1,064 │ 19,589 KB  │ 18,592 KB  │   5.1%
Snowplow             │     403 │    688 KB  │    565 KB  │  17.8%
WashingtonPost       │     125 │  1,571 KB  │  1,407 KB  │  10.4%
─────────────────────┼─────────┼────────────┼────────────┼─────────
TOTAL                │   9,558 │ 55,439 KB  │ 49,151 KB  │  11.3%
```

**Key findings:**
- ✅ **100% roundtrip success** - All 9,558 schemas convert losslessly
- ✅ **11-18% savings** on typical structured data
- ✅ **~50% savings** on formatted/pretty-printed JSON

### LLM Accuracy

We use [StructEval](https://github.com/zenoaihq/structeval) to test TSON generation accuracy with LLMs. Results show **accuracy at par with JSON** for structured output tasks.

---

## When NOT to Use TSON

TSON excels with arrays of uniform objects, but there are cases where other formats may be better:

| Scenario | Recommendation |
|----------|----------------|
| **Deeply nested, non-uniform structures** | JSON-compact may use fewer tokens for highly irregular data |
| **Very small payloads (<100 tokens)** | Overhead of teaching TSON syntax may exceed savings |
| **Pure flat tabular data** | CSV is smaller (~5-10%) but lacks structure |
| **Existing JSON pipelines** | If integration cost exceeds token savings |

**Use TSON when:**
- ✅ Arrays of objects with repeated keys
- ✅ Nested objects with uniform structure
- ✅ LLM function calling / structured output
- ✅ Context window optimization
- ✅ Saving json data to save memory

---

## Quick Start

### Python

```bash
pip install tson
```

```python
import tson

data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
encoded = tson.dumps(data)  # {@id,name#2|1,Alice|2,Bob}
decoded = tson.loads(encoded)  # Perfect round-trip
```

### JavaScript/TypeScript

```bash
npm install @zenoaihq/tson
```

```typescript
import { dumps, loads } from '@zenoaihq/tson';

const data = [{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }];
const encoded = dumps(data); // {@id,name#2|1,Alice|2,Bob}
const decoded = loads(encoded); // Perfect round-trip
```

---

## Implementations

| Language | Status | Package |
|----------|--------|---------|
| **Python** | ✅ Stable | `pip install tson` |
| **JavaScript/TypeScript** | ✅ Stable | `npm install @zenoaihq/tson` |

Both implementations include:
- `dumps()` / `loads()` - Core serialization
- `prettify()` / `minify()` - Formatting
- File I/O utilities
- 100% roundtrip compatibility

**[→ Python Documentation](python/README.md)** | **[→ JavaScript Documentation](javascript/README.md)**

---

## Core Features

### 1. Tabular Format
Array of objects with keys declared once:
```
{@key1,key2#N|val1,val2|val1,val2}
```

### 2. Nested Schema Notation
Nested objects with schema in header:
```
{@id,address(@city,zip)#2|1,{NYC,10001}|2,{LA,90001}}
```

### 3. Nested Arrays (v1.2)
Arrays inside objects with count inside parentheses:
```
{@name,items(@x,y#2)#2|Alice,[{1,a},{2,b}]|Bob,[{3,c},{4,d}]}
```

### 4. Type Preservation
Correctly distinguishes strings from numbers:
```
{@zip_string,zip_number|"10001",10001}
```

---

## Use Cases

| Use Case | Token Savings |
|----------|---------------|
| **LLM Function Calling** | 30-50% on arguments |
| **Context Windows** | Fit more data in limited context |
| **Structured Output** | Easier for LLMs to generate valid data |
| **Batch Processing** | Compact storage and transfer |

---

## Playground

Explore TSON tokenization interactively:

🔗 **[Token Playground](https://www.curiouslychase.com/playground/format-tokenization-exploration?mode=preset&size=small-simple&structure=uniform-flat)**

---

## Documentation

- **[SPEC.md](SPEC.md)** - Complete format specification (v1.2)
- **[prompts.md](prompts.md)** - LLM integration guide and prompt templates
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

---

## Comparison with Alternatives

TSON offers **more token savings** than similar formats while remaining simple and delimiter-based:

| Format | Universal | Token Savings | LLM Generation | Nested Schema |
|--------|-----------|---------------|----------------|---------------|
| JSON | ✅ | 0% (baseline) | ✅ Easy | ✅ Yes |
| YAML | ✅ | ~5-10% | ⚠️ Whitespace-dependent | ✅ Yes |
| TOON | ✅ | ~15-20% | ⚠️ Whitespace-dependent | ✅ Yes |
| XML | ✅ | -50% (larger) | ✅ Easy | ✅ Yes |
| CSV | ❌ Tabular only | 50-60% | ✅ Easy | ❌ No |
| **TSON** | ✅ | **11-18%** vs compact JSON | ✅ Delimiter-based | ✅ Yes |

**Key advantages over alternatives:**
- ✅ **Delimiter-based** - More reliable than indentation for LLM generation
- ✅ **Compact** - More savings than YAML/TOON vs compact JSON
- ✅ **Simple** - Fewer rules than YAML, no whitespace sensitivity
- ✅ **Lossless** - 100% roundtrip compatibility with JSON

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](LICENSE)

**Version:** 1.1.0 | **Status:** Production Ready

*Built for efficiency. Optimized for LLMs.*

Developed by [Zeno AI](https://zenoai.tech) | Contact: shubham@zenoai.tech
