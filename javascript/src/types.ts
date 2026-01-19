/**
 * TSON Type Definitions
 *
 * TypeScript type definitions for TSON serialization/deserialization.
 */

/**
 * Primitive TSON value types
 */
export type TSONPrimitive = string | number | boolean | null;

/**
 * TSON array type
 */
export type TSONArray = TSONValue[];

/**
 * TSON object type
 */
export type TSONObject = { [key: string]: TSONValue };

/**
 * Any valid TSON value
 */
export type TSONValue = TSONPrimitive | TSONArray | TSONObject;

/**
 * Schema info for nested object/array structures
 * - schema: nested schema keys (or null if no schema)
 * - count: array count (or null if single object)
 */
export interface SchemaInfo {
  schema: string[] | null;
  count: number | null;
}

/**
 * Schema map for nested object structures
 * Maps field names to their schema info
 */
export type SchemaMap = Record<string, SchemaInfo>;

/**
 * Result of parsing a key with optional schema notation
 */
export interface KeySchema {
  keyName: string;
  schema: string[] | null;
  count: number | null;
}

/**
 * Result of parsing keys with optional row count
 */
export interface ParsedKeys {
  keys: string[];
  count: number | null;
}
