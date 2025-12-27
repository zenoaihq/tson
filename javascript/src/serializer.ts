/**
 * TSON Serializer
 *
 * Converts JavaScript data structures to TSON format.
 */

import type { TSONValue, TSONObject, TSONArray, SchemaMap } from './types';
import {
  formatPrimitive,
  needsQuoting,
  escapeString,
  isUniformObjectArray,
} from './utils';

/**
 * Serialize JavaScript object to TSON formatted string.
 *
 * @example
 * dumps({ name: "Alice", age: 30 })
 * // Returns: '{@name,age|Alice,30}'
 *
 * @example
 * dumps([{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }])
 * // Returns: '{@id,name#2|1,Alice|2,Bob}'
 */
export function dumps(data: TSONValue): string {
  return serializeValue(data);
}

/**
 * Serialize JavaScript object to TSON formatted file (Node.js only).
 *
 * @param data - JavaScript object to serialize
 * @param filePath - Path to file to write
 */
export async function dump(data: TSONValue, filePath: string): Promise<void> {
  // Dynamic import for Node.js fs module
  const fs = await import('fs/promises');
  await fs.writeFile(filePath, dumps(data), 'utf-8');
}

/**
 * Serialize any JavaScript value to TSON format.
 *
 * Dispatches to appropriate serializer based on type.
 */
export function serializeValue(value: TSONValue): string {
  // Handle primitives
  if (
    value === null ||
    typeof value === 'boolean' ||
    typeof value === 'number' ||
    typeof value === 'string'
  ) {
    return formatPrimitive(value);
  }

  // Handle arrays
  if (Array.isArray(value)) {
    // Check if it's a uniform array of objects (tabular optimization)
    if (isUniformObjectArray(value)) {
      return serializeTabular(value);
    } else {
      return serializeArray(value);
    }
  }

  // Handle objects
  if (typeof value === 'object' && value !== null) {
    return serializeObject(value as TSONObject);
  }

  throw new TypeError(`Cannot serialize type: ${typeof value}`);
}

/**
 * Serialize a JavaScript object to TSON object format.
 *
 * Format: {@key1,key2|value1,value2}
 */
export function serializeObject(obj: TSONObject): string {
  const keys = Object.keys(obj);

  if (keys.length === 0) {
    return '{@}';
  }

  // Format keys
  const keyParts: string[] = [];
  for (const key of keys) {
    let keyStr = String(key);
    if (needsQuoting(keyStr)) {
      keyStr = `"${escapeString(keyStr)}"`;
    }
    keyParts.push(keyStr);
  }

  // Format values
  const valueParts: string[] = [];
  for (const key of keys) {
    valueParts.push(serializeValue(obj[key]));
  }

  // Build object string
  const keysStr = keyParts.join(',');
  const valuesStr = valueParts.join(',');

  return `{@${keysStr}|${valuesStr}}`;
}

/**
 * Serialize a JavaScript array to TSON array format.
 *
 * Format: [value1,value2,value3]
 */
export function serializeArray(arr: TSONArray): string {
  if (arr.length === 0) {
    return '[]';
  }

  // Serialize each element
  const valueParts: string[] = [];
  for (const value of arr) {
    valueParts.push(serializeValue(value));
  }

  return '[' + valueParts.join(',') + ']';
}

/**
 * Serialize a uniform array of objects in tabular format.
 *
 * Format: {@key1,key2#N|val1,val2|val1,val2}
 *
 * This is the key optimization: keys are declared once instead of repeated
 * for each object in the array.
 */
export function serializeTabular(arr: TSONObject[]): string {
  if (arr.length === 0) {
    return '[]';
  }

  if (!isUniformObjectArray(arr)) {
    throw new Error('Array is not uniform - cannot use tabular format');
  }

  // Get keys from first object
  const keys = Object.keys(arr[0]);
  const count = arr.length;

  // Check if any values are objects with uniform structure (nested schema opportunity)
  const nestedSchemas = detectNestedSchemas(arr, keys);

  // Format keys (with nested schemas if applicable)
  const keyParts: string[] = [];
  for (const key of keys) {
    let keyStr = String(key);
    if (needsQuoting(keyStr)) {
      keyStr = `"${escapeString(keyStr)}"`;
    }

    // Add nested schema notation if applicable
    if (key in nestedSchemas) {
      const schemaKeys = nestedSchemas[key]!;
      // Quote schema keys that need quoting (contain special chars)
      const formattedSchemaKeys = schemaKeys.map(sk => {
        if (needsQuoting(sk)) {
          return `"${escapeString(sk)}"`;
        }
        return sk;
      });
      const schemaStr = formattedSchemaKeys.join(',');
      keyStr = `${keyStr}(@${schemaStr})`;
    }

    keyParts.push(keyStr);
  }

  const keysStr = keyParts.join(',');

  // Format rows
  const rowParts: string[] = [];
  for (const obj of arr) {
    const valueParts: string[] = [];
    for (const key of keys) {
      const value = obj[key];

      // If this key has a nested schema, serialize as schematized object
      if (key in nestedSchemas) {
        valueParts.push(serializeSchematizedObject(value as TSONObject, nestedSchemas[key]!));
      } else {
        valueParts.push(serializeValue(value));
      }
    }
    rowParts.push(valueParts.join(','));
  }

  const rowsStr = rowParts.join('|');

  return `{@${keysStr}#${count}|${rowsStr}}`;
}

/**
 * Detect if any fields contain uniform nested objects that can use schema notation.
 *
 * For each key, checks if all values are objects with identical keys.
 * If so, that field can use nested schema notation.
 */
export function detectNestedSchemas(arr: TSONObject[], keys: string[]): SchemaMap {
  const nestedSchemas: SchemaMap = {};

  for (const key of keys) {
    // Get all values for this key
    const values = arr.map(obj => obj[key]);

    // Check if all values are plain objects
    if (!values.every(v => typeof v === 'object' && v !== null && !Array.isArray(v))) {
      continue;
    }

    if (values.length === 0) {
      continue;
    }

    // Check if all objects have the same keys
    const firstKeys = Object.keys(values[0] as TSONObject);
    const allSame = values.slice(1).every(v => {
      const objKeys = Object.keys(v as TSONObject);
      return (
        objKeys.length === firstKeys.length &&
        objKeys.every((k, i) => k === firstKeys[i])
      );
    });

    if (allSame) {
      // This field can use nested schema
      nestedSchemas[key] = firstKeys;
    }
  }

  return nestedSchemas;
}

/**
 * Serialize an object using a pre-declared schema.
 *
 * Format: {value1,value2} (no @ marker, values only)
 *
 * The @ marker is omitted because the schema was already declared in the
 * parent structure.
 */
export function serializeSchematizedObject(obj: TSONObject, schema: string[]): string {
  if (Object.keys(obj).length === 0) {
    return '{}';
  }

  // Serialize values in schema order
  const valueParts: string[] = [];
  for (const key of schema) {
    const value = obj[key];
    valueParts.push(serializeValue(value));
  }

  return '{' + valueParts.join(',') + '}';
}
