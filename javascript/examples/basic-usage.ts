/**
 * TSON Basic Usage Examples
 *
 * Demonstrates core features and common use cases.
 */

import { dumps, loads } from '../src';

function example1SimpleObject() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 1: Simple Object');
  console.log('='.repeat(70));

  const data = { name: 'Alice', age: 30, active: true };

  console.log('\nOriginal data:');
  console.log(data);

  console.log('\nJSON:');
  const jsonStr = JSON.stringify(data);
  console.log(jsonStr);
  console.log(`Length: ${jsonStr.length} characters`);

  console.log('\nTSON:');
  const tsonStr = dumps(data);
  console.log(tsonStr);
  console.log(`Length: ${tsonStr.length} characters`);

  const savings = jsonStr.length - tsonStr.length;
  const percent = jsonStr.length > 0 ? (savings / jsonStr.length) * 100 : 0;
  console.log(`\nSavings: ${savings} characters (${percent.toFixed(1)}%)`);

  // Verify round-trip
  const decoded = loads(tsonStr);
  console.log(`Round-trip successful: ${JSON.stringify(data) === JSON.stringify(decoded)}`);
}

function example2ArrayOfObjects() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 2: Array of Objects - Tabular Optimization');
  console.log('='.repeat(70));

  const data = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' },
    { id: 3, name: 'Carol', email: 'carol@example.com' },
  ];

  console.log('\nOriginal data:');
  data.forEach((item) => console.log(` `, item));

  console.log('\nJSON:');
  const jsonStr = JSON.stringify(data);
  console.log(jsonStr);
  console.log(`Length: ${jsonStr.length} characters`);

  console.log('\nTSON (keys written once!):');
  const tsonStr = dumps(data);
  console.log(tsonStr);
  console.log(`Length: ${tsonStr.length} characters`);

  const savings = jsonStr.length - tsonStr.length;
  const percent = jsonStr.length > 0 ? (savings / jsonStr.length) * 100 : 0;
  console.log(`\nSavings: ${savings} characters (${percent.toFixed(1)}%)`);
  console.log('Note: Savings increase with more rows!');
}

function example3NestedSchema() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 3: Nested Schema Notation (Advanced)');
  console.log('='.repeat(70));

  const data = [
    { id: 1, name: 'Alice', address: { city: 'NYC', zip: '10001' } },
    { id: 2, name: 'Bob', address: { city: 'LA', zip: '90001' } },
    { id: 3, name: 'Carol', address: { city: 'Chicago', zip: '60601' } },
  ];

  console.log('\nOriginal data:');
  data.forEach((item) => console.log(`  `, item));

  console.log('\nJSON:');
  const jsonStr = JSON.stringify(data);
  const jsonDisplay = jsonStr.length > 100 ? jsonStr.slice(0, 100) + '...' : jsonStr;
  console.log(jsonDisplay);
  console.log(`Length: ${jsonStr.length} characters`);

  console.log('\nTSON (nested schema - address keys declared once!):');
  const tsonStr = dumps(data);
  console.log(tsonStr);
  console.log(`Length: ${tsonStr.length} characters`);

  const savings = jsonStr.length - tsonStr.length;
  const percent = jsonStr.length > 0 ? (savings / jsonStr.length) * 100 : 0;
  console.log(`\nSavings: ${savings} characters (${percent.toFixed(1)}%)`);
  console.log('Schema notation: address(@city,zip) declares the structure once!');
}

function example4MixedTypes() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 4: Mixed Types and Nesting');
  console.log('='.repeat(70));

  const data = {
    name: 'Alice',
    age: 30,
    tags: ['python', 'go', 'rust'],
    meta: {
      created: '2025-01-27',
      active: true,
    },
  };

  console.log('\nOriginal data:');
  console.log(JSON.stringify(data, null, 2));

  console.log('\nTSON:');
  const tsonStr = dumps(data);
  console.log(tsonStr);

  const decoded = loads(tsonStr);
  console.log(`\nRound-trip successful: ${JSON.stringify(data) === JSON.stringify(decoded)}`);
}

function example5RealWorld() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 5: Real-World Employee Data');
  console.log('='.repeat(70));

  const data = {
    company: 'Acme Corp',
    employees: [
      {
        id: 1,
        name: 'Alice Johnson',
        department: 'Engineering',
        skills: ['Python', 'Go', 'Docker'],
        contact: {
          email: 'alice@acme.com',
          phone: '555-0101',
        },
      },
      {
        id: 2,
        name: 'Bob Smith',
        department: 'Design',
        skills: ['Figma', 'Illustrator'],
        contact: {
          email: 'bob@acme.com',
          phone: '555-0102',
        },
      },
    ],
    metadata: {
      updated: '2025-01-27',
      version: '1.0',
    },
  };

  console.log('\nJSON:');
  const jsonStr = JSON.stringify(data);
  const jsonDisplay = jsonStr.length > 150 ? jsonStr.slice(0, 150) + '...' : jsonStr;
  console.log(jsonDisplay);
  console.log(`Length: ${jsonStr.length} characters`);

  console.log('\nTSON:');
  const tsonStr = dumps(data);
  const tsonDisplay = tsonStr.length > 150 ? tsonStr.slice(0, 150) + '...' : tsonStr;
  console.log(tsonDisplay);
  console.log(`Length: ${tsonStr.length} characters`);

  const savings = jsonStr.length - tsonStr.length;
  const percent = jsonStr.length > 0 ? (savings / jsonStr.length) * 100 : 0;
  console.log(`\nSavings: ${savings} characters (${percent.toFixed(1)}%)`);
}

function example6SpecialValues() {
  console.log('\n' + '='.repeat(70));
  console.log('Example 6: Special Values and Edge Cases');
  console.log('='.repeat(70));

  const data = {
    null_value: null,
    empty_string: '',
    empty_array: [] as any[],
    empty_object: {},
    numeric_string: '12345',
    actual_number: 12345,
    boolean: true,
    special_chars: 'hello, world | @ # {}',
  };

  console.log('\nOriginal data:');
  console.log(JSON.stringify(data, null, 2));

  console.log('\nTSON:');
  const tsonStr = dumps(data);
  console.log(tsonStr);

  const decoded = loads(tsonStr);
  console.log(`\nRound-trip successful: ${JSON.stringify(data) === JSON.stringify(decoded)}`);
  console.log(`Type preserved: numeric_string is ${typeof (decoded as any).numeric_string}`);
}

function runAllExamples() {
  console.log('\n' + '='.repeat(70));
  console.log('TSON Basic Usage Examples');
  console.log('='.repeat(70));

  const examples = [
    example1SimpleObject,
    example2ArrayOfObjects,
    example3NestedSchema,
    example4MixedTypes,
    example5RealWorld,
    example6SpecialValues,
  ];

  for (const example of examples) {
    try {
      example();
    } catch (e) {
      console.log(`\nError in ${example.name}: ${e}`);
      console.error(e);
    }
  }

  console.log('\n' + '='.repeat(70));
  console.log('Examples Complete!');
  console.log('='.repeat(70) + '\n');
}

// Run all examples
runAllExamples();
