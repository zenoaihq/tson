"""
TSON Serializer

Converts Python data structures to TSON format.
"""

from typing import Any, List, Dict, TextIO
from .utils import (
    format_primitive,
    needs_quoting,
    escape_string,
    is_uniform_object_array,
)


def dumps(data: Any) -> str:
    """
    Serialize Python object to TSON formatted string.

    Args:
        data: Python object to serialize (dict, list, or primitive)

    Returns:
        TSON formatted string

    Examples:
        >>> dumps({"name": "Alice", "age": 30})
        '{@name,age|Alice,30}'

        >>> dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
        '{@id,name#2|1,Alice|2,Bob}'
    """
    return serialize_value(data)


def dump(data: Any, fp: TextIO) -> None:
    """
    Serialize Python object to TSON formatted file.

    Args:
        data: Python object to serialize
        fp: File-like object to write to
    """
    fp.write(dumps(data))


def serialize_value(value: Any) -> str:
    """
    Serialize any Python value to TSON format.

    Dispatches to appropriate serializer based on type.

    Args:
        value: Value to serialize

    Returns:
        TSON string representation
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return format_primitive(value)

    elif isinstance(value, dict):
        return serialize_object(value)

    elif isinstance(value, list):
        # Check if it's a uniform array of objects (tabular optimization)
        if is_uniform_object_array(value):
            return serialize_tabular(value)
        else:
            return serialize_array(value)

    else:
        raise TypeError(f"Cannot serialize type: {type(value).__name__}")


def serialize_object(obj: Dict) -> str:
    """
    Serialize a Python dictionary to TSON object format.

    Format: {@key1,key2|value1,value2}

    Args:
        obj: Dictionary to serialize

    Returns:
        TSON object string
    """
    if not obj:
        return '{@}'

    keys = list(obj.keys())
    values = [obj[k] for k in keys]

    # Format keys
    key_parts = []
    for key in keys:
        key_str = str(key)
        if needs_quoting(key_str):
            key_str = f'"{escape_string(key_str)}"'
        key_parts.append(key_str)

    # Format values
    value_parts = []
    for value in values:
        value_parts.append(serialize_value(value))

    # Build object string
    keys_str = ','.join(key_parts)
    values_str = ','.join(value_parts)

    return f'{{@{keys_str}|{values_str}}}'


def serialize_array(arr: List) -> str:
    """
    Serialize a Python list to TSON array format.

    Format: [value1,value2,value3]

    Args:
        arr: List to serialize

    Returns:
        TSON array string
    """
    if not arr:
        return '[]'

    # Serialize each element
    value_parts = []
    for value in arr:
        value_parts.append(serialize_value(value))

    return '[' + ','.join(value_parts) + ']'


def serialize_tabular(arr: List[Dict]) -> str:
    """
    Serialize a uniform array of dictionaries in tabular format.

    Format: {@key1,key2#N|val1,val2|val1,val2}

    This is the key optimization: keys are declared once instead of repeated
    for each object in the array.

    Args:
        arr: List of dictionaries with identical keys

    Returns:
        TSON tabular string

    Raises:
        ValueError: If array is not uniform
    """
    if not arr:
        return '[]'

    if not is_uniform_object_array(arr):
        raise ValueError("Array is not uniform - cannot use tabular format")

    # Get keys from first object
    keys = list(arr[0].keys())
    count = len(arr)

    # Check if any values are objects with uniform structure (nested schema opportunity)
    nested_schemas = detect_nested_schemas(arr, keys)

    # Format keys (with nested schemas if applicable)
    key_parts = []
    for key in keys:
        key_str = str(key)
        if needs_quoting(key_str):
            key_str = f'"{escape_string(key_str)}"'

        # Add nested schema notation if applicable
        if key in nested_schemas:
            schema_keys = nested_schemas[key]
            # Quote schema keys that need quoting (contain special chars)
            formatted_schema_keys = []
            for sk in schema_keys:
                if needs_quoting(sk):
                    formatted_schema_keys.append(f'"{escape_string(sk)}"')
                else:
                    formatted_schema_keys.append(sk)
            schema_str = ','.join(formatted_schema_keys)
            key_str = f'{key_str}(@{schema_str})'

        key_parts.append(key_str)

    keys_str = ','.join(key_parts)

    # Format rows
    row_parts = []
    for obj in arr:
        value_parts = []
        for key in keys:
            value = obj[key]

            # If this key has a nested schema, serialize as schematized object
            if key in nested_schemas:
                value_parts.append(serialize_schematized_object(value, nested_schemas[key]))
            else:
                value_parts.append(serialize_value(value))

        row_parts.append(','.join(value_parts))

    rows_str = '|'.join(row_parts)

    return f'{{@{keys_str}#{count}|{rows_str}}}'


def detect_nested_schemas(arr: List[Dict], keys: List[str]) -> Dict[str, List[str]]:
    """
    Detect if any fields contain uniform nested objects that can use schema notation.

    For each key, checks if all values are dictionaries with identical keys.
    If so, that field can use nested schema notation.

    Args:
        arr: Array of objects
        keys: List of keys to check

    Returns:
        Dictionary mapping key names to their nested schemas
    """
    nested_schemas = {}

    for key in keys:
        # Get all values for this key
        values = [obj[key] for obj in arr]

        # Check if all values are dicts
        if not all(isinstance(v, dict) for v in values):
            continue

        # Check if all dicts have the same keys
        if len(values) == 0:
            continue

        first_keys = list(values[0].keys())
        if not all(list(v.keys()) == first_keys for v in values[1:]):
            continue

        # This field can use nested schema
        nested_schemas[key] = first_keys

    return nested_schemas


def serialize_schematized_object(obj: Dict, schema: List[str]) -> str:
    """
    Serialize an object using a pre-declared schema.

    Format: {value1,value2} (no @ marker, values only)

    The @ marker is omitted because the schema was already declared in the
    parent structure.

    Args:
        obj: Dictionary to serialize
        schema: List of keys in order

    Returns:
        TSON string with values only
    """
    if not obj:
        return '{}'

    # Serialize values in schema order
    value_parts = []
    for key in schema:
        value = obj.get(key)
        value_parts.append(serialize_value(value))

    return '{' + ','.join(value_parts) + '}'
