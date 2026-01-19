/**
 * TSON - Token-efficient Structured Object Notation
 *
 * A compact serialization format designed for efficient data exchange with LLMs.
 * Achieves 25-70% token savings compared to JSON.
 *
 * @packageDocumentation
 */

// Export main API functions
export { dumps, dump } from './serializer';
export { loads, load } from './deserializer';

// Export formatting functions
export { prettify, minify } from './prettify';

// Export file I/O functions (Node.js only)
export {
  loadJson,
  loadTson,
  saveTson,
  saveTsonString,
  jsonToTson,
  tsonToJson,
  readTsonString,
  prettifyFile,
  minifyFile,
} from './fileio';

// Export types for TypeScript users
export type {
  TSONValue,
  TSONPrimitive,
  TSONArray,
  TSONObject,
  SchemaMap,
  SchemaInfo,
  KeySchema,
  ParsedKeys,
} from './types';

// Re-export utility functions for advanced usage
export {
  needsQuoting,
  looksLikeNumber,
  escapeString,
  unescapeString,
  formatPrimitive,
  parsePrimitive,
  isUniformObjectArray,
  splitByDelimiter,
  parseKeySchema,
  buildSchemaMap,
  parseKeys,
} from './utils';
