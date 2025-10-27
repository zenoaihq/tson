"""
TSON Deserializer

Parses TSON format back to Python data structures.
"""

from typing import Any, List, Dict, TextIO, Optional
from .utils import (
    parse_primitive,
    split_by_delimiter,
    build_schema_map,
)


def loads(s: str) -> Any:
    """
    Deserialize TSON formatted string to Python object.

    Args:
        s: TSON formatted string

    Returns:
        Python object (dict, list, or primitive)

    Examples:
        >>> loads('{@name,age|Alice,30}')
        {'name': 'Alice', 'age': 30}

        >>> loads('{@id,name#2|1,Alice|2,Bob}')
        [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    """
    s = s.strip()
    if not s:
        return None

    return parse_value(s)


def load(fp: TextIO) -> Any:
    """
    Deserialize TSON formatted file to Python object.

    Args:
        fp: File-like object to read from

    Returns:
        Python object
    """
    return loads(fp.read())


def parse_value(text: str) -> Any:
    """
    Parse a TSON value of any type.

    Determines the type by looking at the first character and dispatches
    to the appropriate parser.

    Args:
        text: TSON value string

    Returns:
        Parsed Python value
    """
    text = text.strip()

    if not text:
        return ""

    # Check first character to determine type
    first_char = text[0]

    if first_char == '{':
        # Object (with @ marker) or schematized object
        return parse_object(text)

    elif first_char == '[':
        # Array
        return parse_array(text)

    else:
        # Primitive value
        return parse_primitive(text)


def parse_object(text: str) -> Any:
    """
    Parse TSON object format.

    Handles both:
    - {@key1,key2|val1,val2} - Single object or array of objects
    - {val1,val2} - Schematized object (no @ marker)

    Args:
        text: TSON object string

    Returns:
        Python dict or list of dicts

    Raises:
        ValueError: If format is invalid
    """
    text = text.strip()

    if not text.startswith('{') or not text.endswith('}'):
        raise ValueError(f"Invalid object format: {text}")

    # Extract content between braces
    content = text[1:-1].strip()

    # Empty object
    if content == '@' or content == '':
        if content == '@':
            return {}
        else:
            # {} without @ is technically invalid for empty object but we'll be lenient
            return {}

    # Check if this has @ marker (object with keys)
    if content.startswith('@'):
        return parse_keyed_object(content[1:])  # Remove @ marker

    else:
        # Schematized object without @ marker (just values)
        # This shouldn't happen at top level but can occur as nested value
        # Parse as comma-separated values
        values = split_by_delimiter(content, ',')
        parsed_values = [parse_value(v) for v in values]

        # Return as list (since we don't have keys)
        # In practice, this shouldn't be hit at top level
        return parsed_values


def parse_keyed_object(content: str) -> Any:
    """
    Parse content after @ marker in object.

    Format: key1,key2|val1,val2 or key1,key2#N|val1,val2|val1,val2

    Args:
        content: Content string (without @ marker)

    Returns:
        Python dict or list of dicts (if tabular format)
    """
    # Split by pipe to separate keys from values
    parts = split_by_delimiter(content, '|')

    if len(parts) < 1:
        raise ValueError("Invalid object format: missing keys")

    # First part contains keys (and possibly row count)
    keys_part = parts[0]

    # Parse keys and extract count if present
    keys, count = parse_keys(keys_part)

    # Build schema map (maps field names to nested schemas)
    schema_map = build_schema_map(keys)

    # Get actual field names (without schema notation)
    field_names = [k.split('(')[0] for k in keys]

    # If only one part, it's an error (no values)
    if len(parts) == 1:
        raise ValueError("Invalid object format: missing values")

    # If two parts, could be single object or array with one row
    # If more than two parts, definitely array (multiple rows)
    value_parts = parts[1:]

    # Check if this is tabular format (array) or single object
    # If count is specified or multiple value parts, it's tabular
    is_tabular = count is not None or len(value_parts) > 1

    if is_tabular:
        # Array of objects (tabular format)
        return parse_tabular_array(field_names, value_parts, schema_map, count)
    else:
        # Single object
        return parse_single_object(field_names, value_parts[0], schema_map)


def parse_keys(keys_str: str) -> tuple:
    """
    Parse keys string and extract row count if present.

    Format: key1,key2,key3 or key1,key2,key3#N

    Args:
        keys_str: Keys string

    Returns:
        Tuple of (keys_list, count or None)
    """
    # Check for row count marker
    if '#' in keys_str:
        parts = keys_str.rsplit('#', 1)  # Split from right in case # in key name
        keys_part = parts[0]
        count_part = parts[1].strip()

        try:
            count = int(count_part)
        except ValueError:
            raise ValueError(f"Invalid row count: {count_part}")

        keys = split_by_delimiter(keys_part, ',')
        return (keys, count)
    else:
        keys = split_by_delimiter(keys_str, ',')
        return (keys, None)


def parse_single_object(field_names: List[str], values_str: str, schema_map: Dict) -> Dict:
    """
    Parse a single object from keys and values.

    Args:
        field_names: List of field names
        values_str: Comma-separated values string
        schema_map: Map of field names to nested schemas

    Returns:
        Python dict
    """
    # Split values
    values = split_by_delimiter(values_str, ',')

    if len(values) != len(field_names):
        raise ValueError(
            f"Field count mismatch: {len(field_names)} fields but {len(values)} values"
        )

    # Build object
    obj = {}
    for field_name, value_str in zip(field_names, values):
        # Check if this field has a nested schema
        schema = schema_map.get(field_name)

        if schema:
            # Parse as schematized object
            obj[field_name] = parse_schematized_value(value_str, schema)
        else:
            # Parse as regular value
            obj[field_name] = parse_value(value_str)

    return obj


def parse_tabular_array(field_names: List[str], row_parts: List[str],
                       schema_map: Dict, expected_count: Optional[int]) -> List[Dict]:
    """
    Parse tabular format into list of dicts.

    Args:
        field_names: List of field names
        row_parts: List of row value strings
        schema_map: Map of field names to nested schemas
        expected_count: Expected number of rows (or None)

    Returns:
        List of Python dicts

    Raises:
        ValueError: If row count doesn't match expected
    """
    result = []

    for row_str in row_parts:
        if not row_str.strip():
            continue

        obj = parse_single_object(field_names, row_str, schema_map)
        result.append(obj)

    # Verify count if specified
    if expected_count is not None and len(result) != expected_count:
        raise ValueError(
            f"Row count mismatch: expected {expected_count} rows but got {len(result)}"
        )

    return result


def parse_schematized_value(value_str: str, schema: List[str]) -> Dict:
    """
    Parse a value that uses a nested schema.

    The value should be in format {val1,val2} where values correspond to
    the keys in the schema.

    Args:
        value_str: Value string (e.g. "{NYC,10001}")
        schema: List of key names or nested schema strings

    Returns:
        Python dict

    Raises:
        ValueError: If format is invalid
    """
    value_str = value_str.strip()

    # Should be wrapped in braces
    if not value_str.startswith('{') or not value_str.endswith('}'):
        raise ValueError(f"Schematized value must be wrapped in braces: {value_str}")

    # Extract content
    content = value_str[1:-1].strip()

    # Empty object
    if not content:
        return {}

    # Split by comma
    values = split_by_delimiter(content, ',')

    if len(values) != len(schema):
        raise ValueError(
            f"Schema mismatch: {len(schema)} keys but {len(values)} values"
        )

    # Build nested schema map for recursive schemas
    nested_schema_map = build_schema_map(schema)

    # Get field names (without schema notation)
    field_names = [k.split('(')[0] for k in schema]

    # Build object
    obj = {}
    for field_name, value_str, schema_key in zip(field_names, values, schema):
        # Check if this field itself has a nested schema
        nested_schema = nested_schema_map.get(field_name)

        if nested_schema:
            # Recursively parse with nested schema
            obj[field_name] = parse_schematized_value(value_str, nested_schema)
        else:
            # Parse as regular value
            obj[field_name] = parse_value(value_str)

    return obj


def parse_array(text: str) -> List:
    """
    Parse TSON array format.

    Format: [value1,value2,value3]

    Args:
        text: TSON array string

    Returns:
        Python list

    Raises:
        ValueError: If format is invalid
    """
    text = text.strip()

    if not text.startswith('[') or not text.endswith(']'):
        raise ValueError(f"Invalid array format: {text}")

    # Extract content between brackets
    content = text[1:-1].strip()

    # Empty array
    if not content:
        return []

    # Split by comma
    values = split_by_delimiter(content, ',')

    # Parse each value
    result = []
    for value_str in values:
        if value_str.strip():  # Skip empty strings from trailing commas
            result.append(parse_value(value_str))

    return result
