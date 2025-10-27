"""
TSON String Tester

Interactive tool to test TSON strings:
1. Parse TSON → JSON
2. Convert JSON → TSON
3. Verify round-trip
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import tson
import json


def test_tson_string(tson_string):
    """
    Test a TSON string: parse to JSON and convert back.

    Args:
        tson_string: TSON formatted string to test
    """
    print("\n" + "=" * 70)
    print("TSON String Test")
    print("=" * 70)

    print("\nInput TSON:")
    print(tson_string)
    print(f"Length: {len(tson_string)} characters")

    try:
        # Parse TSON to Python
        parsed_data = tson.loads(tson_string)

        print("\n" + "-" * 70)
        print("Parsed as JSON:")
        json_str = json.dumps(parsed_data, indent=2)
        print(json_str)
        print(f"Length: {len(json.dumps(parsed_data))} characters (minified)")

        # Convert back to TSON
        print("\n" + "-" * 70)
        print("Converted back to TSON:")
        tson_back = tson.dumps(parsed_data)
        print(tson_back)
        print(f"Length: {len(tson_back)} characters")

        # Verify round-trip
        print("\n" + "-" * 70)
        print("Round-trip verification:")
        round_trip_data = tson.loads(tson_back)

        if parsed_data == round_trip_data:
            print("[SUCCESS] Round-trip successful!")
        else:
            print("[FAILED] Data changed during round-trip")
            print(f"Original: {parsed_data}")
            print(f"After round-trip: {round_trip_data}")

        # Show token savings
        json_minified = json.dumps(parsed_data)
        savings = len(json_minified) - len(tson_back)
        percent = (savings / len(json_minified) * 100) if len(json_minified) > 0 else 0

        print("\n" + "-" * 70)
        print("Token Savings:")
        print(f"  JSON:    {len(json_minified)} characters")
        print(f"  TSON:    {len(tson_back)} characters")
        print(f"  Saved:   {savings} characters ({percent:.1f}%)")

    except Exception as e:
        print("\n" + "-" * 70)
        print(f"[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 70 + "\n")


def run_example_tests():
    """Run predefined example tests."""
    print("\n" + "=" * 70)
    print("TSON String Tester - Example Tests")
    print("=" * 70)

    examples = [
        # Simple object
        "{@name,age,active|Alice,30,true}",

        # Array
        "[1,2,3,4,5]",

        # Tabular format
        "{@id,name,email#3|1,Alice,alice@ex.com|2,Bob,bob@ex.com|3,Carol,carol@ex.com}",

        # Nested schema
        "{@id,address(@city,zip)#2|1,{NYC,10001}|2,{LA,90001}}",

        # Nested Tough
        "{@id,address#2|1,{@city,zip(@zip1,zip2)#2|NYC,{10001,1002}|NYC,{10001,1002}}|2,{@city,zip(@zip1,zip2)#2|NYC,{10001,1002}|NYC,{10001,1002}}}",

        # Nested Nested

        # Complex structure
        "{@name,tags,meta|Alice,[python,go],{@created|2025-01-27}}",
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n--- Example {i}/{len(examples)} ---")
        test_tson_string(example)

        if i < len(examples):
            input("Press Enter to continue to next example...")


def interactive_mode():
    """Interactive mode - enter TSON strings to test."""
    print("\n" + "=" * 70)
    print("TSON String Tester - Interactive Mode")
    print("=" * 70)
    print("\nEnter TSON strings to test.")
    print("Commands:")
    print("  - Type 'examples' to see example tests")
    print("  - Type 'quit' or 'exit' to quit")
    print("  - Type 'help' for TSON syntax help")
    print("=" * 70)

    while True:
        print("\n")
        tson_input = input("Enter TSON string (or command): ").strip()

        if not tson_input:
            continue

        if tson_input.lower() in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break

        if tson_input.lower() == 'examples':
            run_example_tests()
            continue

        if tson_input.lower() == 'help':
            print_help()
            continue

        test_tson_string(tson_input)


def print_help():
    """Print TSON syntax help."""
    print("\n" + "=" * 70)
    print("TSON Syntax Quick Reference")
    print("=" * 70)
    print("""
Objects:
  {@key1,key2|value1,value2}
  Example: {@name,age|Alice,30}

Arrays:
  [value1,value2,value3]
  Example: [1,2,3]

Tabular (array of objects):
  {@key1,key2#N|val1,val2|val1,val2}
  Example: {@id,name#2|1,Alice|2,Bob}

Nested schema:
  {@field1,field2(@subkey1,subkey2)|value,{subval1,subval2}}
  Example: {@id,address(@city,zip)|1,{NYC,10001}}

Primitives:
  - Strings: Alice or "quoted string"
  - Numbers: 42, 3.14
  - Booleans: true, false
  - Null: null

Delimiters:
  @ = object marker
  , = field/value separator
  | = row separator
  # = row count (optional)
""")
    print("=" * 70)


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("TSON String Tester")
    print("=" * 70)
    print("\nWhat would you like to do?")
    print("  1. Test example TSON strings")
    print("  2. Interactive mode (enter your own strings)")
    print("  3. Test a specific string")
    print("=" * 70)

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == '1':
        run_example_tests()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        tson_input = input("\nEnter TSON string: ").strip()
        if tson_input:
            test_tson_string(tson_input)
    else:
        print("Invalid choice. Running examples...")
        run_example_tests()


if __name__ == "__main__":
    # Check if TSON string provided as command-line argument
    if len(sys.argv) > 1:
        # Test the provided string
        tson_string = sys.argv[1]
        test_tson_string(tson_string)
    else:
        # Interactive mode
        main()

    # test_1 = json.loads(open("test1.json").read())
    # print(test_1)
    # encoded_1 = tson.dumps(test_1)
    # print(encoded_1)
    # decoded_1 = tson.loads(encoded_1)
    # print(decoded_1)
    # print(test_1 == decoded_1)
    # print(len(str(test_1)))
    # print(len(encoded_1))
