"""
TSON Basic Usage Examples

Demonstrates core features and common use cases.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tson
import json


def example_1_simple_object():
    """Example 1: Simple Object"""
    print("\n" + "=" * 70)
    print("Example 1: Simple Object")
    print("=" * 70)

    data = {"name": "Alice", "age": 30, "active": True}

    print("\nOriginal data:")
    print(data)

    print("\nJSON:")
    json_str = json.dumps(data)
    print(json_str)
    print(f"Length: {len(json_str)} characters")

    print("\nTSON:")
    tson_str = tson.dumps(data)
    print(tson_str)
    print(f"Length: {len(tson_str)} characters")

    savings = len(json_str) - len(tson_str)
    percent = (savings / len(json_str) * 100) if len(json_str) > 0 else 0
    print(f"\nSavings: {savings} characters ({percent:.1f}%)")

    # Verify round-trip
    decoded = tson.loads(tson_str)
    print(f"Round-trip successful: {data == decoded}")


def example_2_array_of_objects():
    """Example 2: Array of Objects (Tabular Format)"""
    print("\n" + "=" * 70)
    print("Example 2: Array of Objects - Tabular Optimization")
    print("=" * 70)

    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Carol", "email": "carol@example.com"}
    ]

    print("\nOriginal data:")
    for item in data:
        print(f"  {item}")

    print("\nJSON:")
    json_str = json.dumps(data)
    print(json_str)
    print(f"Length: {len(json_str)} characters")

    print("\nTSON (keys written once!):")
    tson_str = tson.dumps(data)
    print(tson_str)
    print(f"Length: {len(tson_str)} characters")

    savings = len(json_str) - len(tson_str)
    percent = (savings / len(json_str) * 100) if len(json_str) > 0 else 0
    print(f"\nSavings: {savings} characters ({percent:.1f}%)")
    print("Note: Savings increase with more rows!")


def example_3_nested_schema():
    """Example 3: Nested Schema Notation"""
    print("\n" + "=" * 70)
    print("Example 3: Nested Schema Notation (Advanced)")
    print("=" * 70)

    data = [
        {"id": 1, "name": "Alice", "address": {"city": "NYC", "zip": "10001"}},
        {"id": 2, "name": "Bob", "address": {"city": "LA", "zip": "90001"}},
        {"id": 3, "name": "Carol", "address": {"city": "Chicago", "zip": "60601"}}
    ]

    print("\nOriginal data:")
    for item in data:
        print(f"  {item}")

    print("\nJSON:")
    json_str = json.dumps(data)
    print(json_str[:100] + "..." if len(json_str) > 100 else json_str)
    print(f"Length: {len(json_str)} characters")

    print("\nTSON (nested schema - address keys declared once!):")
    tson_str = tson.dumps(data)
    print(tson_str)
    print(f"Length: {len(tson_str)} characters")

    savings = len(json_str) - len(tson_str)
    percent = (savings / len(json_str) * 100) if len(json_str) > 0 else 0
    print(f"\nSavings: {savings} characters ({percent:.1f}%)")
    print("Schema notation: address(@city,zip) declares the structure once!")


def example_4_mixed_types():
    """Example 4: Mixed Types and Nesting"""
    print("\n" + "=" * 70)
    print("Example 4: Mixed Types and Nesting")
    print("=" * 70)

    data = {
        "name": "Alice",
        "age": 30,
        "tags": ["python", "go", "rust"],
        "meta": {
            "created": "2025-01-27",
            "active": True
        }
    }

    print("\nOriginal data:")
    print(json.dumps(data, indent=2))

    print("\nTSON:")
    tson_str = tson.dumps(data)
    print(tson_str)

    decoded = tson.loads(tson_str)
    print(f"\nRound-trip successful: {data == decoded}")


def example_5_real_world():
    """Example 5: Real-World Data Structure"""
    print("\n" + "=" * 70)
    print("Example 5: Real-World Employee Data")
    print("=" * 70)

    data = {
        "company": "Acme Corp",
        "employees": [
            {
                "id": 1,
                "name": "Alice Johnson",
                "department": "Engineering",
                "skills": ["Python", "Go", "Docker"],
                "contact": {
                    "email": "alice@acme.com",
                    "phone": "555-0101"
                }
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "department": "Design",
                "skills": ["Figma", "Illustrator"],
                "contact": {
                    "email": "bob@acme.com",
                    "phone": "555-0102"
                }
            }
        ],
        "metadata": {
            "updated": "2025-01-27",
            "version": "1.0"
        }
    }

    print("\nJSON:")
    json_str = json.dumps(data)
    print(json_str[:150] + "..." if len(json_str) > 150 else json_str)
    print(f"Length: {len(json_str)} characters")

    print("\nTSON:")
    tson_str = tson.dumps(data)
    print(tson_str[:150] + "..." if len(tson_str) > 150 else tson_str)
    print(f"Length: {len(tson_str)} characters")

    savings = len(json_str) - len(tson_str)
    percent = (savings / len(json_str) * 100) if len(json_str) > 0 else 0
    print(f"\nSavings: {savings} characters ({percent:.1f}%)")


def example_6_special_values():
    """Example 6: Special Values and Edge Cases"""
    print("\n" + "=" * 70)
    print("Example 6: Special Values and Edge Cases")
    print("=" * 70)

    data = {
        "null_value": None,
        "empty_string": "",
        "empty_array": [],
        "empty_object": {},
        "numeric_string": "12345",
        "actual_number": 12345,
        "boolean": True,
        "special_chars": "hello, world | @ # {}"
    }

    print("\nOriginal data:")
    print(json.dumps(data, indent=2))

    print("\nTSON:")
    tson_str = tson.dumps(data)
    print(tson_str)

    decoded = tson.loads(tson_str)
    print(f"\nRound-trip successful: {data == decoded}")
    print(f"Type preserved: numeric_string is {type(decoded['numeric_string']).__name__}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("TSON Basic Usage Examples")
    print("=" * 70)

    examples = [
        example_1_simple_object,
        example_2_array_of_objects,
        example_3_nested_schema,
        example_4_mixed_types,
        example_5_real_world,
        example_6_special_values,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("Examples Complete!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_all_examples()
