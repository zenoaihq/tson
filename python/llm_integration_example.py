"""
TSON LLM Integration Example

Demonstrates how to use TSON with LLM APIs for token-efficient data exchange.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import tson
import json


# =============================================================================
# SYSTEM PROMPT - Use this with your LLM
# =============================================================================

TSON_SYSTEM_PROMPT = """
You are working with TSON (Token-efficient Structured Object Notation), a compact alternative to JSON.

TSON Syntax:
• Objects: {@key1,key2|value1,value2}
• Arrays: [value1,value2,value3]
• Tabular (array of objects): {@key1,key2#N|val1,val2|val1,val2}
• Nested schema: {@field,nested(@subkey1,subkey2)|value,{subval1,subval2}}

Delimiters:
• @ = object marker
• , = field/value separator
• | = row separator
• # = row count

Examples:

1. Simple object:
   JSON: {"name": "Alice", "age": 30}
   TSON: {@name,age|Alice,30}

2. Array of objects (tabular):
   JSON: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
   TSON: {@id,name#2|1,Alice|2,Bob}

3. Nested objects with schema:
   JSON: [{"id": 1, "address": {"city": "NYC", "zip": "10001"}}]
   TSON: {@id,address(@city,zip)#1|1,{NYC,"10001"}}

Key Rules:
• Keys are written ONCE in header, then only values in rows
• Use | to separate rows, , to separate values
• Include #N to specify row count
• Quote strings if they contain: , | @ # { } [ ]
"""


# Minimal version (for token-constrained scenarios)
TSON_SYSTEM_PROMPT_MINIMAL = """
TSON format (compact JSON):
• {@k1,k2|v1,v2} = object
• {@k1,k2#N|v1,v2|v1,v2} = array of objects 
• {@k,sub(@sk)|v,{sv}} = nested
• [v1,v2,v3] = array

Examples:
{@id,name#2|1,Alice|2,Bob} = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
"""


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

def create_tson_to_json_prompt(tson_data: str) -> str:
    """Create prompt to convert TSON to JSON."""
    return f"""
Convert this TSON data to JSON format:

TSON:
{tson_data}

Return only the JSON, no explanation.
"""


def create_json_to_tson_prompt(json_data: str) -> str:
    """Create prompt to convert JSON to TSON."""
    return f"""
Convert this JSON data to TSON format:

JSON:
{json_data}

Return only the TSON, no explanation.
"""


def create_task_with_tson_data_prompt(tson_data: str, task: str) -> str:
    """Create prompt for a task with TSON data as input."""
    return f"""
The following data is in TSON format:

{tson_data}

Task: {task}
"""


def create_task_expecting_tson_output_prompt(task: str, fields: list, count: int = None) -> str:
    """Create prompt expecting TSON output."""
    count_hint = f" (exactly {count} rows)" if count else ""
    return f"""
{task}

Return the result in TSON format with fields: {', '.join(fields)}{count_hint}

Format: {{@{','.join(fields)}#{count or 'N'}|...}}
"""


# =============================================================================
# EXAMPLE USAGE FUNCTIONS
# =============================================================================

def example_1_send_tson_to_llm():
    """
    Example 1: Send data in TSON format to LLM for analysis.

    Use case: You have large data and want to save tokens on input.
    """
    print("\n" + "=" * 70)
    print("Example 1: Send TSON to LLM for Analysis")
    print("=" * 70)

    # Your data
    data = [
        {"date": "2025-01-01", "sales": 5000, "region": "North"},
        {"date": "2025-01-02", "sales": 6000, "region": "South"},
        {"date": "2025-01-03", "sales": 5500, "region": "East"},
        {"date": "2025-01-04", "sales": 7200, "region": "West"},
        {"date": "2025-01-05", "sales": 6800, "region": "North"},
    ]

    # Convert to TSON
    tson_data = tson.dumps(data)

    # Compare sizes
    json_data = json.dumps(data)
    print(f"\nJSON size: {len(json_data)} characters")
    print(f"TSON size: {len(tson_data)} characters")
    print(f"Savings: {len(json_data) - len(tson_data)} characters ({(1 - len(tson_data)/len(json_data))*100:.1f}%)")

    # Create prompt
    prompt = create_task_with_tson_data_prompt(
        tson_data=tson_data,
        task="What is the average sales amount? Which region had the highest sales?"
    )

    print("\n--- PROMPT TO SEND TO LLM ---")
    print("System:", TSON_SYSTEM_PROMPT_MINIMAL)
    print("\nUser:", prompt)

    print("\n--- WHAT LLM WOULD SEE ---")
    print("Data in compact format:", tson_data)

    # Note: In real usage, you would call your LLM API here:
    # response = openai.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": TSON_SYSTEM_PROMPT},
    #         {"role": "user", "content": prompt}
    #     ]
    # )


def example_2_request_tson_from_llm():
    """
    Example 2: Request LLM to generate data in TSON format.

    Use case: You want the LLM's output in compact format.
    """
    print("\n" + "=" * 70)
    print("Example 2: Request TSON Output from LLM")
    print("=" * 70)

    prompt = create_task_expecting_tson_output_prompt(
        task="Generate 5 sample employee records with realistic data.",
        fields=["id", "name", "department", "salary"],
        count=5
    )

    print("\n--- PROMPT TO SEND TO LLM ---")
    print("System:", TSON_SYSTEM_PROMPT_MINIMAL)
    print("\nUser:", prompt)

    print("\n--- EXPECTED LLM RESPONSE ---")
    expected = "{@id,name,department,salary#5|1,Alice,Engineering,120000|2,Bob,Sales,95000|3,Carol,Marketing,85000|4,Dave,Engineering,115000|5,Eve,Design,90000}"
    print(expected)

    print("\n--- THEN PARSE IT ---")
    try:
        parsed = tson.loads(expected)
        print("Parsed successfully:")
        print(json.dumps(parsed[:2], indent=2), "...")
    except Exception as e:
        print(f"Error: {e}")


def example_3_function_calling_with_tson():
    """
    Example 3: Use TSON in function calling for efficiency.

    Use case: Function arguments are large and repeated across many calls.
    """
    print("\n" + "=" * 70)
    print("Example 3: Function Calling with TSON")
    print("=" * 70)

    # Define function that accepts TSON
    function_definition = {
        "name": "analyze_sales_data",
        "description": "Analyze sales data and return insights",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Sales data in TSON format: {@date,region,sales#N|...}"
                }
            },
            "required": ["data"]
        }
    }

    # Prepare data
    data = [
        {"date": "2025-01-01", "region": "North", "sales": 5000},
        {"date": "2025-01-02", "region": "South", "sales": 6000},
        {"date": "2025-01-03", "region": "East", "sales": 5500},
    ]

    tson_data = tson.dumps(data)

    print("\n--- FUNCTION DEFINITION ---")
    print(json.dumps(function_definition, indent=2))

    print("\n--- FUNCTION CALL (what LLM would generate) ---")
    print(f'analyze_sales_data("{tson_data}")')

    print("\n--- TOKEN COMPARISON ---")
    json_data = json.dumps(data)
    print(f"With JSON: ~{len(json_data)} chars")
    print(f"With TSON: ~{len(tson_data)} chars")
    print(f"Savings: {len(json_data) - len(tson_data)} chars per call")
    print(f"\nOver 100 calls: {(len(json_data) - len(tson_data)) * 100} chars saved!")


def example_4_bidirectional_conversation():
    """
    Example 4: Bidirectional conversation using TSON.

    Use case: Multi-turn conversation with data exchange.
    """
    print("\n" + "=" * 70)
    print("Example 4: Bidirectional TSON Conversation")
    print("=" * 70)

    print("\n--- TURN 1: User sends TSON data ---")
    user_data = [
        {"product": "Widget", "price": 29.99, "stock": 100},
        {"product": "Gadget", "price": 49.99, "stock": 50},
        {"product": "Doohickey", "price": 19.99, "stock": 200},
    ]

    tson_input = tson.dumps(user_data)
    print(f"User: Here's our inventory: {tson_input}")
    print(f"        Filter for items with stock > 75")

    print("\n--- TURN 2: LLM responds with filtered TSON ---")
    filtered_tson = "{@product,price,stock#2|Widget,29.99,100|Doohickey,19.99,200}"
    print(f"Assistant: Filtered results: {filtered_tson}")

    print("\n--- TURN 3: User asks for JSON version ---")
    print("User: Convert that to JSON format")

    print("\n--- TURN 4: LLM converts ---")
    parsed = tson.loads(filtered_tson)
    print(f"Assistant: {json.dumps(parsed, indent=2)}")


def example_5_with_validation():
    """
    Example 5: TSON with validation and retry.

    Use case: Production system that validates LLM output.
    """
    print("\n" + "=" * 70)
    print("Example 5: TSON with Validation")
    print("=" * 70)

    # Simulate LLM responses (some valid, some invalid)
    llm_responses = [
        "{@id,name#2|1,Alice|2,Bob}",                    # Valid
        "{@id,name:2|1:Alice|2:Bob}",                    # Invalid (wrong delimiter)
        "[{@id|1},{@id|2}]",                              # Valid but different format
        "{@id,name#2|1,Alice,30|2,Bob,25}",               # Invalid (extra field)
    ]

    print("\nTesting LLM responses:")
    for i, response in enumerate(llm_responses, 1):
        print(f"\n--- Response {i} ---")
        print(f"Output: {response}")

        try:
            parsed = tson.loads(response)
            print(f"✓ Valid TSON!")
            print(f"  Parsed: {parsed}")
        except Exception as e:
            print(f"✗ Invalid TSON: {e}")
            print(f"  Would retry with: 'Your TSON had an error. Return as JSON instead.'")


# =============================================================================
# INTEGRATION WITH POPULAR LLM APIs
# =============================================================================

def openai_example():
    """
    Example integration with OpenAI API.

    Note: Requires 'openai' package and API key.
    """
    code = '''
from openai import OpenAI
import tson

client = OpenAI(api_key="your-api-key")

# Prepare data in TSON
data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
tson_data = tson.dumps(data)

# Call with system prompt
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": TSON_SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze this data: {tson_data}\\nHow many records?"}
    ]
)

print(response.choices[0].message.content)
# Expected: "There are 2 records"
'''

    print("\n" + "=" * 70)
    print("OpenAI Integration Example")
    print("=" * 70)
    print(code)


def anthropic_example():
    """
    Example integration with Anthropic Claude API.

    Note: Requires 'anthropic' package and API key.
    """
    code = '''
from anthropic import Anthropic
import tson

client = Anthropic(api_key="your-api-key")

# Prepare data in TSON
data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
tson_data = tson.dumps(data)

# Call with system prompt
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=TSON_SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": f"Analyze: {tson_data}\\nHow many records?"}
    ]
)

print(response.content[0].text)
'''

    print("\n" + "=" * 70)
    print("Anthropic Claude Integration Example")
    print("=" * 70)
    print(code)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("TSON LLM Integration Examples")
    print("=" * 70)
    print("\nThese examples show how to use TSON with LLMs for token efficiency.")
    print("All examples are ready to copy into your code.")

    examples = [
        example_1_send_tson_to_llm,
        example_2_request_tson_from_llm,
        example_3_function_calling_with_tson,
        example_4_bidirectional_conversation,
        example_5_with_validation,
    ]

    for example in examples:
        try:
            example()
            input("\n[Press Enter to continue to next example...]")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
            import traceback
            traceback.print_exc()

    # Show API integration examples
    openai_example()
    anthropic_example()

    print("\n" + "=" * 70)
    print("Examples Complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Copy the system prompt (TSON_SYSTEM_PROMPT)")
    print("2. Use prompt templates for your use case")
    print("3. Add validation for LLM-generated TSON")
    print("4. Measure token savings in production")
    print("\nSee prompts.md for more prompt templates!")


if __name__ == "__main__":
    main()
