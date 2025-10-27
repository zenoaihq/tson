"""
TSON Round-Trip Tests

Verify that data can be serialized and deserialized correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tson


def test_simple_object():
    """Test simple object serialization."""
    data = {"name": "Alice", "age": 30, "active": True}

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Simple object")


def test_simple_array():
    """Test simple array serialization."""
    data = [1, 2, 3, 4, 5]

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Simple array")


def test_array_of_objects():
    """Test array of uniform objects (tabular format)."""
    data = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Carol", "age": 35}
    ]

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Array of objects (tabular)")


def test_nested_object():
    """Test nested objects."""
    data = {
        "user": {
            "profile": {
                "name": "Alice",
                "age": 30
            },
            "settings": {
                "theme": "dark"
            }
        }
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Nested object")


def test_mixed_array():
    """Test array with mixed types."""
    data = [1, "string", True, None, 3.14]

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Mixed array")


def test_empty_values():
    """Test empty strings, arrays, and objects."""
    data = {
        "empty_string": "",
        "empty_array": [],
        "empty_object": {},
        "null_value": None
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Empty values")


def test_special_characters():
    """Test strings with special characters."""
    data = {
        "comma": "hello, world",
        "pipe": "a|b|c",
        "quotes": 'She said "hello"',
        "newline": "line1\nline2",
        "at_sign": "@username"
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Special characters")


def test_numeric_strings():
    """Test preservation of numeric strings vs numbers."""
    data = {
        "zip_string": "10001",
        "zip_number": 10001,
        "version_string": "1.0",
        "version_number": 1.0
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    assert isinstance(decoded["zip_string"], str), "zip_string should be string"
    assert isinstance(decoded["zip_number"], int), "zip_number should be int"
    print("[PASS] Numeric strings")


def test_nested_arrays():
    """Test nested arrays."""
    data = {
        "matrix": [[1, 2, 3], [4, 5, 6]],
        "mixed": [1, [2, 3], [[4, 5]]]
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Nested arrays")


def test_array_with_nested_objects():
    """Test array of objects containing nested objects (nested schema)."""
    data = [
        {
            "id": 1,
            "name": "Alice",
            "address": {"city": "NYC", "zip": "10001"}
        },
        {
            "id": 2,
            "name": "Bob",
            "address": {"city": "LA", "zip": "90001"}
        }
    ]

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Array with nested objects (nested schema)")


def test_complex_structure():
    """Test complex real-world-like structure."""
    data = {
        "company": "Acme Corp",
        "employees": [
            {
                "id": 1,
                "name": "Alice",
                "skills": ["Python", "Go"],
                "contact": {"email": "alice@example.com", "phone": "555-0101"}
            },
            {
                "id": 2,
                "name": "Bob",
                "skills": ["Java"],
                "contact": {"email": "bob@example.com", "phone": "555-0102"}
            }
        ],
        "metadata": {
            "created": "2025-01-27",
            "version": "1.0"
        }
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)
    print(decoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Complex structure")


def test_boolean_values():
    """Test boolean values."""
    data = [
        {"id": 1, "active": True, "verified": False},
        {"id": 2, "active": False, "verified": True}
    ]

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Boolean values")


def test_numeric_types():
    """Test various numeric types."""
    data = {
        "int": 42,
        "negative_int": -17,
        "float": 3.14159,
        "negative_float": -2.5,
        "zero": 0,
        "large": 1000000
    }

    encoded = tson.dumps(data)
    print(f"Encoded: {encoded}")
    decoded = tson.loads(encoded)

    assert decoded == data, f"Round-trip failed:\nOriginal: {data}\nDecoded: {decoded}"
    print("[PASS] Numeric types")


def run_all_tests():
    """Run all round-trip tests."""
    print("\n" + "=" * 70)
    print("TSON Round-Trip Tests")
    print("=" * 70 + "\n")

    tests = [
        test_simple_object,
        test_simple_array,
        test_array_of_objects,
        test_nested_object,
        test_mixed_array,
        test_empty_values,
        test_special_characters,
        test_numeric_strings,
        test_nested_arrays,
        test_array_with_nested_objects,
        test_complex_structure,
        test_boolean_values,
        test_numeric_types,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}")
            print(f"  {e}")
            failed.append(test.__name__)
        except Exception as e:
            print(f"[ERROR] {test.__name__}")
            print(f"  {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed.append(test.__name__)

    print("\n" + "=" * 70)
    if failed:
        print(f"FAILED: {len(failed)} test(s) failed")
        for name in failed:
            print(f"  - {name}")
    else:
        print(f"SUCCESS: All {len(tests)} tests passed!")
    print("=" * 70 + "\n")

    return len(failed) == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


