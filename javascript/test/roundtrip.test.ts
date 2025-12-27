/**
 * TSON Round-Trip Tests
 *
 * Verify that data can be serialized and deserialized correctly.
 */

import { describe, it, expect } from 'vitest';
import { dumps, loads } from '../src';

describe('TSON Round-Trip Tests', () => {
  it('should handle simple objects', () => {
    const data = { name: 'Alice', age: 30, active: true };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle simple arrays', () => {
    const data = [1, 2, 3, 4, 5];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle array of objects in tabular format', () => {
    const data = [
      { id: 1, name: 'Alice', age: 30 },
      { id: 2, name: 'Bob', age: 25 },
      { id: 3, name: 'Carol', age: 35 },
    ];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle nested objects', () => {
    const data = {
      user: {
        profile: {
          name: 'Alice',
          age: 30,
        },
        settings: {
          theme: 'dark',
        },
      },
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle mixed type arrays', () => {
    const data = [1, 'string', true, null, 3.14];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle empty values', () => {
    const data = {
      empty_string: '',
      empty_array: [],
      empty_object: {},
      null_value: null,
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle special characters', () => {
    const data = {
      comma: 'hello, world',
      pipe: 'a|b|c',
      quotes: 'She said "hello"',
      newline: 'line1\nline2',
      at_sign: '@username',
      "at@sign": '@username',
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should preserve numeric strings vs numbers', () => {
    const data = {
      zip_string: '10001',
      zip_number: 10001,
      version_string: '1.0',
      version_number: 1.0,
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
    expect(typeof decoded.zip_string).toBe('string');
    expect(typeof decoded.zip_number).toBe('number');
  });

  it('should handle nested arrays', () => {
    const data = {
      matrix: [
        [1, 2, 3],
        [4, 5, 6],
      ],
      mixed: [1, [2, 3], [[4, 5]]],
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle array with nested objects using nested schema', () => {
    const data = [
      {
        id: 1,
        name: 'Alice',
        address: { city: 'NYC', zip: '10001' },
      },
      {
        id: 2,
        name: 'Bob',
        address: { city: 'LA', zip: '90001' },
      },
    ];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle complex real-world-like structures', () => {
    const data = {
      company: 'Acme Corp',
      employees: [
        {
          id: 1,
          name: 'Alice',
          skills: ['Python', 'Go'],
          contact: { email: 'alice@example.com', phone: '555-0101' },
        },
        {
          id: 2,
          name: 'Bob',
          skills: ['Java'],
          contact: { email: 'bob@example.com', phone: '555-0102' },
        },
      ],
      metadata: {
        created: '2025-01-27',
        version: '1.0',
      },
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle boolean values', () => {
    const data = [
      { id: 1, active: true, verified: false },
      { id: 2, active: false, verified: true },
    ];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle various numeric types', () => {
    const data = {
      int: 42,
      negative_int: -17,
      float: 3.14159,
      negative_float: -2.5,
      zero: 0,
      large: 1000000,
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });


  it('should handle keys containing hash symbol', () => {
    const data = {
      "key#1": "value",
      "normal": "data"
    };

    const encoded = dumps(data);
    console.log(`Encoded hash test: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle backslash in values', () => {
    const data = {
      path: 'C:\\Users\\file',
      escaped_n: 'literal\\ntext',
      double_backslash: 'a\\\\b',
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle parentheses in keys', () => {
    const data = {
      'func()': 'value',
      'name(test)': 'another',
      '(leading': 'val1',
      'trailing)': 'val2',
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle double quotes in values', () => {
    const data = {
      quote: 'He said "hello"',
      mixed: 'Text with "quotes" and more',
      only_quote: '"',
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle nested schema with special char keys', () => {
    const data = [
      { id: 1, info: { 'key,comma': 'Alice', 'key|pipe': 'value1' } },
      { id: 2, info: { 'key,comma': 'Bob', 'key|pipe': 'value2' } },
    ];

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });

  it('should handle keys with special characters', () => {
    const data = {
      'with,comma': 'value',
      'with|pipe': 'value',
      'at@sign': '@username',
      'with space': 'value',
    };

    const encoded = dumps(data);
    console.log(`Encoded: ${encoded}`);
    const decoded = loads(encoded);

    expect(decoded).toEqual(data);
  });
});
