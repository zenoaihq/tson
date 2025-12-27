"""
TSON Utility Functions

Helper functions for serialization, deserialization, and validation.
"""

from typing import Any, List, Dict, Optional


# Special characters that require string quoting
SPECIAL_CHARS = {',', '|', '@', '#', '{', '}', '[', ']', '\n', '\r', '\t', ' ',"\"", "(", ")"}


def needs_quoting(value: str) -> bool:
    """
    Determine if a string value needs to be quoted in TSON format.

    Strings need quoting if they:
    - Are empty
    - Contain special delimiter characters
    - Have leading/trailing whitespace
    - Look like numbers (to preserve them as strings)
    - Look like reserved words (true/false/null) when we want them as strings

    Args:
        value: String to check

    Returns:
        True if quoting is required, False otherwise
    """
    if not value:
        return True

    # Check for reserved words that we want to keep as strings
    # (If value is exactly "true", "false", or "null" and we're calling this,
    #  we want to preserve it as a string, so quote it)
    if value in ('true', 'false', 'null'):
        return True

    # Check for leading/trailing whitespace
    if value[0].isspace() or value[-1].isspace():
        return True

    # Check if it looks like a number (preserve type distinction)
    if looks_like_number(value):
        return True

    # Check for special characters
    for char in value:
        if char in SPECIAL_CHARS:
            return True

    return False


def looks_like_number(value: str) -> bool:
    """
    Check if a string looks like a numeric value.

    Used to determine if we should quote a string to preserve it as a string
    rather than having it parsed as a number.

    Args:
        value: String to check

    Returns:
        True if value could be parsed as a number, False otherwise
    """
    if not value:
        return False

    try:
        # Try parsing as float (covers int and float)
        float(value)
        return True
    except ValueError:
        return False


def escape_string(value: str) -> str:
    """
    Escape special characters in a string for quoted representation.

    Uses standard JSON escape sequences.

    Args:
        value: String to escape

    Returns:
        Escaped string
    """
    # Order matters: backslash first to avoid double-escaping
    value = value.replace('\\', '\\\\')
    value = value.replace('"', '\\"')
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\t', '\\t')
    return value


def unescape_string(value: str) -> str:
    """
    Unescape a quoted string back to its original form.

    Reverses the escaping done by escape_string().

    Args:
        value: Escaped string

    Returns:
        Unescaped string
    """
    # Must process character by character to handle escape sequences correctly
    # Simple replace() can corrupt sequences like \\n (literal backslash + n)
    result = []
    i = 0
    while i < len(value):
        if value[i] == '\\' and i + 1 < len(value):
            next_char = value[i + 1]
            if next_char == '\\':
                result.append('\\')
                i += 2
            elif next_char == '"':
                result.append('"')
                i += 2
            elif next_char == 'n':
                result.append('\n')
                i += 2
            elif next_char == 'r':
                result.append('\r')
                i += 2
            elif next_char == 't':
                result.append('\t')
                i += 2
            else:
                # Unknown escape, keep as-is
                result.append(value[i])
                i += 1
        else:
            result.append(value[i])
            i += 1
    return ''.join(result)


def format_primitive(value: Any) -> str:
    """
    Format a primitive Python value as TSON string.

    Args:
        value: Primitive value (None, bool, int, float, str)

    Returns:
        TSON string representation

    Raises:
        ValueError: If value is not a primitive type
    """
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        # Must check bool before int (bool is subclass of int in Python)
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        if needs_quoting(value):
            return f'"{escape_string(value)}"'
        return value
    else:
        raise ValueError(f"Cannot format non-primitive type: {type(value).__name__}")


def parse_primitive(value: str) -> Any:
    """
    Parse a TSON primitive value string to Python type.

    Args:
        value: String representation of primitive

    Returns:
        Parsed Python value (None, bool, int, float, or str)
    """
    value = value.strip()

    if not value:
        return ""

    # Check for boolean
    if value == 'true':
        return True
    elif value == 'false':
        return False

    # Check for null
    elif value == 'null':
        return None

    # Check for quoted string
    elif value.startswith('"') and value.endswith('"'):
        return unescape_string(value[1:-1])

    # Try to parse as number
    elif looks_like_number(value):
        try:
            # Try int first
            if '.' not in value and 'e' not in value.lower():
                return int(value)
            else:
                return float(value)
        except ValueError:
            # Shouldn't happen if looks_like_number returned True, but be safe
            return value

    # Otherwise it's an unquoted string
    else:
        return value


def is_uniform_object_array(data: List) -> bool:
    """
    Check if a list is an array of objects with identical keys.

    This determines if we can use tabular format optimization.

    Args:
        data: List to check

    Returns:
        True if list contains uniform objects, False otherwise
    """
    if not isinstance(data, list) or len(data) == 0:
        return False

    # All elements must be dictionaries
    if not all(isinstance(item, dict) for item in data):
        return False

    # Get keys from first element
    first_keys = list(data[0].keys())

    # Check that all elements have the same keys in the same order
    for item in data[1:]:
        if list(item.keys()) != first_keys:
            return False

    return True


def split_by_delimiter(text: str, delimiter: str) -> List[str]:
    """
    Split text by delimiter, respecting quoted strings and nested structures.

    This is more sophisticated than str.split() because it handles:
    - Quoted strings (don't split on delimiters inside quotes)
    - Nested braces/brackets/parentheses (don't split inside nested structures)
    - Escaped characters

    Args:
        text: Text to split
        delimiter: Single character delimiter

    Returns:
        List of split segments
    """
    result = []
    current = []
    in_quotes = False
    escape_next = False
    depth_curly = 0
    depth_square = 0
    depth_paren = 0

    for char in text:
        # Handle escape sequences
        if escape_next:
            current.append(char)
            escape_next = False
            continue

        if char == '\\':
            current.append(char)
            escape_next = True
            continue

        # Handle quotes
        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
            continue

        # Inside quotes, add everything
        if in_quotes:
            current.append(char)
            continue

        # Track nesting depth
        if char == '{':
            depth_curly += 1
            current.append(char)
        elif char == '}':
            depth_curly -= 1
            current.append(char)
        elif char == '[':
            depth_square += 1
            current.append(char)
        elif char == ']':
            depth_square -= 1
            current.append(char)
        elif char == '(':
            depth_paren += 1
            current.append(char)
        elif char == ')':
            depth_paren -= 1
            current.append(char)
        elif char == delimiter and depth_curly == 0 and depth_square == 0 and depth_paren == 0:
            # Found unquoted, unnested delimiter - split here
            result.append(''.join(current).strip())
            current = []
        else:
            current.append(char)

    # Add final segment
    if current:
        result.append(''.join(current).strip())

    return result


def parse_key_schema(key_string: str) -> tuple:
    """
    Parse a key which may include nested schema notation.

    Examples:
        "name" -> ("name", None)
        "address(@city,zip)" -> ("address", ["city", "zip"])
        "location(@coords(@lat,lng))" -> ("location", ["coords(@lat,lng)"])

    Args:
        key_string: Key string potentially with nested schema

    Returns:
        Tuple of (key_name, schema_keys or None)
    """
    key_string = key_string.strip()

    # If the entire key is quoted, it's a simple key (any parens inside are literal)
    # Must check this BEFORE looking for '(' to handle keys like "company("
    if key_string.startswith('"') and key_string.endswith('"'):
        return (unescape_string(key_string[1:-1]), None)

    # Check if key has nested schema (only for unquoted keys)
    if '(' not in key_string:
        return (key_string, None)

    # Find the opening parenthesis
    paren_idx = key_string.index('(')
    key_name = key_string[:paren_idx].strip()

    # Unquote the key name if it's quoted
    if key_name.startswith('"') and key_name.endswith('"'):
        key_name = unescape_string(key_name[1:-1])

    # Extract schema (everything between outermost parentheses)
    # Need to handle nested parentheses
    if not key_string.endswith(')'):
        raise ValueError(f"Invalid key schema syntax: {key_string}")

    schema_str = key_string[paren_idx + 1:-1].strip()

    # Strip leading @ if present (part of notation, not key name)
    if schema_str.startswith('@'):
        schema_str = schema_str[1:]

    # Split schema by commas (respecting nested parentheses)
    schema_keys = split_by_delimiter(schema_str, ',')

    return (key_name, schema_keys)


def build_schema_map(keys: List[str]) -> Dict[str, Optional[List[str]]]:
    """
    Build a mapping of field names to their nested schemas.

    Args:
        keys: List of key strings (may include nested schemas)

    Returns:
        Dictionary mapping key names to their schemas (or None if no schema)

    Example:
        ["id", "address(@city,zip)"]
        -> {"id": None, "address": ["city", "zip"]}
    """
    schema_map = {}

    for key in keys:
        key_name, schema = parse_key_schema(key)
        schema_map[key_name] = schema

    return schema_map
