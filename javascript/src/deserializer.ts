/**
 * TSON Deserializer
 *
 * Parses TSON format back to JavaScript data structures.
 */

import type { TSONValue, TSONObject, TSONArray, SchemaMap } from './types';
import {
  parsePrimitive,
  splitByDelimiter,
  buildSchemaMap,
  parseKeys,
} from './utils';

/**
 * Deserialize TSON formatted string to JavaScript object.
 *
 * @example
 * loads('{@name,age|Alice,30}')
 * // Returns: { name: 'Alice', age: 30 }
 *
 * @example
 * loads('{@id,name#2|1,Alice|2,Bob}')
 * // Returns: [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]
 */
export function loads(s: string): TSONValue {
  const trimmed = s.trim();
  if (trimmed.length === 0) {
    return null;
  }

  return parseValue(trimmed);
}

/**
 * Deserialize TSON formatted file to JavaScript object (Node.js only).
 *
 * @param filePath - Path to file to read
 * @returns Parsed JavaScript object
 */
export async function load(filePath: string): Promise<TSONValue> {
  // Dynamic import for Node.js fs module
  const fs = await import('fs/promises');
  const content = await fs.readFile(filePath, 'utf-8');
  return loads(content);
}

/**
 * Parse a TSON value of any type.
 *
 * Determines the type by looking at the first character and dispatches
 * to the appropriate parser.
 */
export function parseValue(text: string): TSONValue {
  const trimmed = text.trim();

  if (trimmed.length === 0) {
    return '';
  }

  // Check first character to determine type
  const firstChar = trimmed[0];

  if (firstChar === '{') {
    // Object (with @ marker) or schematized object
    return parseObject(trimmed);
  } else if (firstChar === '[') {
    // Array
    return parseArray(trimmed);
  } else {
    // Primitive value
    return parsePrimitive(trimmed);
  }
}

/**
 * Parse TSON object format.
 *
 * Handles both:
 * - {@key1,key2|val1,val2} - Single object or array of objects
 * - {val1,val2} - Schematized object (no @ marker)
 */
export function parseObject(text: string): TSONValue {
  const trimmed = text.trim();

  if (!trimmed.startsWith('{') || !trimmed.endsWith('}')) {
    throw new Error(`Invalid object format: ${text}`);
  }

  // Extract content between braces
  const content = trimmed.slice(1, -1).trim();

  // Empty object
  if (content === '@' || content === '') {
    return {};
  }

  // Check if this has @ marker (object with keys)
  if (content.startsWith('@')) {
    return parseKeyedObject(content.slice(1)); // Remove @ marker
  } else {
    // Schematized object without @ marker (just values)
    // This shouldn't happen at top level but can occur as nested value
    // Parse as comma-separated values
    const values = splitByDelimiter(content, ',');
    const parsedValues = values.map(v => parseValue(v));

    // Return as array (since we don't have keys)
    // In practice, this shouldn't be hit at top level
    return parsedValues;
  }
}

/**
 * Parse content after @ marker in object.
 *
 * Format: key1,key2|val1,val2 or key1,key2#N|val1,val2|val1,val2
 */
export function parseKeyedObject(content: string): TSONValue {
  // Split by pipe to separate keys from values
  const parts = splitByDelimiter(content, '|');

  if (parts.length < 1) {
    throw new Error('Invalid object format: missing keys');
  }

  // First part contains keys (and possibly row count)
  const keysPart = parts[0];

  // Parse keys and extract count if present
  const { keys, count } = parseKeys(keysPart);

  // Build schema map (maps field names to nested schemas)
  const schemaMap = buildSchemaMap(keys);

  // Get actual field names (without schema notation)
  const fieldNames = keys.map(k => k.split('(')[0]);

  // If only one part, it's an error (no values)
  if (parts.length === 1) {
    throw new Error('Invalid object format: missing values');
  }

  // If two parts, could be single object or array with one row
  // If more than two parts, definitely array (multiple rows)
  const valueParts = parts.slice(1);

  // Check if this is tabular format (array) or single object
  // If count is specified or multiple value parts, it's tabular
  const isTabular = count !== null || valueParts.length > 1;

  if (isTabular) {
    // Array of objects (tabular format)
    return parseTabularArray(fieldNames, valueParts, schemaMap, count);
  } else {
    // Single object
    return parseSingleObject(fieldNames, valueParts[0], schemaMap);
  }
}

/**
 * Parse a single object from keys and values.
 */
export function parseSingleObject(
  fieldNames: string[],
  valuesStr: string,
  schemaMap: SchemaMap
): TSONObject {
  // Split values
  const values = splitByDelimiter(valuesStr, ',');

  if (values.length !== fieldNames.length) {
    throw new Error(
      `Field count mismatch: ${fieldNames.length} fields but ${values.length} values`
    );
  }

  // Build object
  const obj: TSONObject = {};
  for (let i = 0; i < fieldNames.length; i++) {
    const fieldName = fieldNames[i];
    const valueStr = values[i];

    // Check if this field has a nested schema
    const schema = schemaMap[fieldName];

    if (schema) {
      // Parse as schematized object
      obj[fieldName] = parseSchematizedValue(valueStr, schema);
    } else {
      // Parse as regular value
      obj[fieldName] = parseValue(valueStr);
    }
  }

  return obj;
}

/**
 * Parse tabular format into array of objects.
 */
export function parseTabularArray(
  fieldNames: string[],
  rowParts: string[],
  schemaMap: SchemaMap,
  expectedCount: number | null
): TSONObject[] {
  const result: TSONObject[] = [];

  for (const rowStr of rowParts) {
    if (rowStr.trim().length === 0) {
      continue;
    }

    const obj = parseSingleObject(fieldNames, rowStr, schemaMap);
    result.push(obj);
  }

  // Verify count if specified
  if (expectedCount !== null && result.length !== expectedCount) {
    throw new Error(
      `Row count mismatch: expected ${expectedCount} rows but got ${result.length}`
    );
  }

  return result;
}

/**
 * Parse a value that uses a nested schema.
 *
 * The value should be in format {val1,val2} where values correspond to
 * the keys in the schema.
 */
export function parseSchematizedValue(valueStr: string, schema: string[]): TSONObject {
  const trimmed = valueStr.trim();

  // Should be wrapped in braces
  if (!trimmed.startsWith('{') || !trimmed.endsWith('}')) {
    throw new Error(`Schematized value must be wrapped in braces: ${valueStr}`);
  }

  // Extract content
  const content = trimmed.slice(1, -1).trim();

  // Empty object
  if (content.length === 0) {
    return {};
  }

  // Split by comma
  const values = splitByDelimiter(content, ',');

  if (values.length !== schema.length) {
    throw new Error(
      `Schema mismatch: ${schema.length} keys but ${values.length} values`
    );
  }

  // Build nested schema map for recursive schemas
  const nestedSchemaMap = buildSchemaMap(schema);

  // Get field names (without schema notation)
  const fieldNames = schema.map(k => k.split('(')[0]);

  // Build object
  const obj: TSONObject = {};
  for (let i = 0; i < fieldNames.length; i++) {
    const fieldName = fieldNames[i];
    const valueStr = values[i];

    // Check if this field itself has a nested schema
    const nestedSchema = nestedSchemaMap[fieldName];

    if (nestedSchema) {
      // Recursively parse with nested schema
      obj[fieldName] = parseSchematizedValue(valueStr, nestedSchema);
    } else {
      // Parse as regular value
      obj[fieldName] = parseValue(valueStr);
    }
  }

  return obj;
}

/**
 * Parse TSON array format.
 *
 * Format: [value1,value2,value3]
 */
export function parseArray(text: string): TSONArray {
  const trimmed = text.trim();

  if (!trimmed.startsWith('[') || !trimmed.endsWith(']')) {
    throw new Error(`Invalid array format: ${text}`);
  }

  // Extract content between brackets
  const content = trimmed.slice(1, -1).trim();

  // Empty array
  if (content.length === 0) {
    return [];
  }

  // Split by comma
  const values = splitByDelimiter(content, ',');

  // Parse each value
  const result: TSONArray = [];
  for (const valueStr of values) {
    if (valueStr.trim().length > 0) {
      // Skip empty strings from trailing commas
      result.push(parseValue(valueStr));
    }
  }

  return result;
}
