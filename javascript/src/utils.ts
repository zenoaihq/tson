/**
 * TSON Utility Functions
 *
 * Helper functions for serialization, deserialization, and validation.
 */

import type { TSONValue, TSONObject, SchemaMap, KeySchema, ParsedKeys } from './types';

/**
 * Special characters that require string quoting
 */
export const SPECIAL_CHARS = new Set([',', '|', '@', '#', '{', '}', '[', ']', '\n', '\r', '\t', ' ']);

/**
 * Determine if a string value needs to be quoted in TSON format.
 *
 * Strings need quoting if they:
 * - Are empty
 * - Contain special delimiter characters
 * - Have leading/trailing whitespace
 * - Look like numbers (to preserve them as strings)
 * - Look like reserved words (true/false/null) when we want them as strings
 */
export function needsQuoting(value: string): boolean {
  if (value.length === 0) {
    return true;
  }

  // Check for reserved words that we want to keep as strings
  if (value === 'true' || value === 'false' || value === 'null') {
    return true;
  }

  // Check for leading/trailing whitespace
  if (value[0].trim() === '' || value[value.length - 1].trim() === '') {
    return true;
  }

  // Check if it looks like a number (preserve type distinction)
  if (looksLikeNumber(value)) {
    return true;
  }

  // Check for special characters
  for (const char of value) {
    if (SPECIAL_CHARS.has(char)) {
      return true;
    }
  }

  return false;
}

/**
 * Check if a string looks like a numeric value.
 *
 * Used to determine if we should quote a string to preserve it as a string
 * rather than having it parsed as a number.
 */
export function looksLikeNumber(value: string): boolean {
  if (value.length === 0) {
    return false;
  }

  // Try parsing as number
  const num = Number(value);
  return !isNaN(num) && value.trim() === value && isFinite(num);
}

/**
 * Escape special characters in a string for quoted representation.
 *
 * Uses standard JSON escape sequences.
 */
export function escapeString(value: string): string {
  // Order matters: backslash first to avoid double-escaping
  return value
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/\t/g, '\\t');
}

/**
 * Unescape a quoted string back to its original form.
 *
 * Reverses the escaping done by escapeString().
 */
export function unescapeString(value: string): string {
  // Order matters: process in reverse order of escaping
  return value
    .replace(/\\t/g, '\t')
    .replace(/\\r/g, '\r')
    .replace(/\\n/g, '\n')
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, '\\');
}

/**
 * Format a primitive value as TSON string.
 */
export function formatPrimitive(value: TSONValue): string {
  if (value === null) {
    return 'null';
  }

  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }

  if (typeof value === 'number') {
    return String(value);
  }

  if (typeof value === 'string') {
    if (needsQuoting(value)) {
      return `"${escapeString(value)}"`;
    }
    return value;
  }

  throw new Error(`Cannot format non-primitive type: ${typeof value}`);
}

/**
 * Parse a TSON primitive value string to JavaScript type.
 */
export function parsePrimitive(value: string): TSONValue {
  const trimmed = value.trim();

  if (trimmed.length === 0) {
    return '';
  }

  // Check for boolean
  if (trimmed === 'true') {
    return true;
  }
  if (trimmed === 'false') {
    return false;
  }

  // Check for null
  if (trimmed === 'null') {
    return null;
  }

  // Check for quoted string
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    return unescapeString(trimmed.slice(1, -1));
  }

  // Try to parse as number
  if (looksLikeNumber(trimmed)) {
    const num = Number(trimmed);
    if (!isNaN(num)) {
      return num;
    }
  }

  // Otherwise it's an unquoted string
  return trimmed;
}

/**
 * Check if a value is an array of objects with identical keys.
 *
 * This determines if we can use tabular format optimization.
 */
export function isUniformObjectArray(data: unknown): data is TSONObject[] {
  if (!Array.isArray(data) || data.length === 0) {
    return false;
  }

  // All elements must be plain objects
  if (!data.every(item => isPlainObject(item))) {
    return false;
  }

  // Get keys from first element
  const firstKeys = Object.keys(data[0]);

  // Check that all elements have the same keys in the same order
  for (let i = 1; i < data.length; i++) {
    const keys = Object.keys(data[i]);
    if (keys.length !== firstKeys.length) {
      return false;
    }
    for (let j = 0; j < keys.length; j++) {
      if (keys[j] !== firstKeys[j]) {
        return false;
      }
    }
  }

  return true;
}

/**
 * Check if value is a plain object (not array, null, or other special object)
 */
function isPlainObject(value: unknown): value is TSONObject {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value) &&
    Object.prototype.toString.call(value) === '[object Object]'
  );
}

/**
 * Split text by delimiter, respecting quoted strings and nested structures.
 *
 * This is more sophisticated than string.split() because it handles:
 * - Quoted strings (don't split on delimiters inside quotes)
 * - Nested braces/brackets/parentheses (don't split inside nested structures)
 * - Escaped characters
 */
export function splitByDelimiter(text: string, delimiter: string): string[] {
  const result: string[] = [];
  const current: string[] = [];
  let inQuotes = false;
  let escapeNext = false;
  let depthCurly = 0;
  let depthSquare = 0;
  let depthParen = 0;

  for (const char of text) {
    // Handle escape sequences
    if (escapeNext) {
      current.push(char);
      escapeNext = false;
      continue;
    }

    if (char === '\\') {
      current.push(char);
      escapeNext = true;
      continue;
    }

    // Handle quotes
    if (char === '"') {
      inQuotes = !inQuotes;
      current.push(char);
      continue;
    }

    // Inside quotes, add everything
    if (inQuotes) {
      current.push(char);
      continue;
    }

    // Track nesting depth
    if (char === '{') {
      depthCurly++;
      current.push(char);
    } else if (char === '}') {
      depthCurly--;
      current.push(char);
    } else if (char === '[') {
      depthSquare++;
      current.push(char);
    } else if (char === ']') {
      depthSquare--;
      current.push(char);
    } else if (char === '(') {
      depthParen++;
      current.push(char);
    } else if (char === ')') {
      depthParen--;
      current.push(char);
    } else if (
      char === delimiter &&
      depthCurly === 0 &&
      depthSquare === 0 &&
      depthParen === 0
    ) {
      // Found unquoted, unnested delimiter - split here
      result.push(current.join('').trim());
      current.length = 0;
    } else {
      current.push(char);
    }
  }

  // Add final segment
  if (current.length > 0) {
    result.push(current.join('').trim());
  }

  return result;
}

/**
 * Parse a key which may include nested schema notation.
 *
 * Examples:
 *   "name" -> { keyName: "name", schema: null }
 *   "address(@city,zip)" -> { keyName: "address", schema: ["city", "zip"] }
 *   "location(@coords(@lat,lng))" -> { keyName: "location", schema: ["coords(@lat,lng)"] }
 */
export function parseKeySchema(keyString: string): KeySchema {
  const trimmed = keyString.trim();

  // Check if key has nested schema
  if (!trimmed.includes('(')) {
    return { keyName: trimmed, schema: null };
  }

  // Find the opening parenthesis
  const parenIdx = trimmed.indexOf('(');
  const keyName = trimmed.slice(0, parenIdx).trim();

  // Extract schema (everything between outermost parentheses)
  if (!trimmed.endsWith(')')) {
    throw new Error(`Invalid key schema syntax: ${keyString}`);
  }

  let schemaStr = trimmed.slice(parenIdx + 1, -1).trim();

  // Strip leading @ if present (part of notation, not key name)
  if (schemaStr.startsWith('@')) {
    schemaStr = schemaStr.slice(1);
  }

  // Split schema by commas (respecting nested parentheses)
  const schemaKeys = splitByDelimiter(schemaStr, ',');

  return { keyName, schema: schemaKeys };
}

/**
 * Build a mapping of field names to their nested schemas.
 *
 * Example:
 *   ["id", "address(@city,zip)"]
 *   -> { id: null, address: ["city", "zip"] }
 */
export function buildSchemaMap(keys: string[]): SchemaMap {
  const schemaMap: SchemaMap = {};

  for (const key of keys) {
    const { keyName, schema } = parseKeySchema(key);
    schemaMap[keyName] = schema;
  }

  return schemaMap;
}

/**
 * Parse keys string and extract row count if present.
 *
 * Format: key1,key2,key3 or key1,key2,key3#N
 */
export function parseKeys(keysStr: string): ParsedKeys {
  // Check for row count marker
  if (keysStr.includes('#')) {
    // Split from right in case # appears in key name
    const lastHashIdx = keysStr.lastIndexOf('#');
    const keysPart = keysStr.slice(0, lastHashIdx);
    const countPart = keysStr.slice(lastHashIdx + 1).trim();

    const count = parseInt(countPart, 10);
    if (isNaN(count)) {
      throw new Error(`Invalid row count: ${countPart}`);
    }

    const keys = splitByDelimiter(keysPart, ',');
    return { keys, count };
  } else {
    const keys = splitByDelimiter(keysStr, ',');
    return { keys, count: null };
  }
}
