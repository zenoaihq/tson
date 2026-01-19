"""
TSON Prettify

Format TSON strings for human readability.
CSV-like format: schema on top, one row/value per line.
"""

from typing import Optional


def prettify(tson_str: str, indent: str = "  ") -> str:
    """
    Format a compact TSON string for human readability.
    
    Uses CSV-like formatting:
    - Schema declaration on first line
    - Each row/value on its own line with leading delimiter
    
    Args:
        tson_str: Compact TSON string
        indent: Indentation string (default: 2 spaces)
    
    Returns:
        Pretty-formatted TSON string
    
    Examples:
        >>> prettify('{@id,name#2|1,Alice|2,Bob}')
        '{@id,name#2\\n|1,Alice\\n|2,Bob}'
        
        >>> prettify('{@a,b|1,2}')
        '{@a,b\\n|1,2}'
    """
    if not tson_str or not tson_str.strip():
        return tson_str
    
    return _prettify_value(tson_str.strip(), indent, depth=0)


def _prettify_value(text: str, indent: str, depth: int) -> str:
    """
    Recursively prettify a TSON value.
    
    Args:
        text: TSON value string
        indent: Indentation string
        depth: Current nesting depth
    
    Returns:
        Pretty-formatted string
    """
    text = text.strip()
    
    if not text:
        return text
    
    # Object with schema: {@...}
    if text.startswith('{@'):
        return _prettify_object(text, indent, depth)
    
    # Schematized object (no @): {...}
    elif text.startswith('{'):
        return text  # Keep schematized values compact
    
    # Array: [...]
    elif text.startswith('['):
        return _prettify_array(text, indent, depth)
    
    # Primitive value
    else:
        return text


def _prettify_object(text: str, indent: str, depth: int) -> str:
    """
    Prettify a TSON object.
    
    Format:
        {@key1,key2,key3#N
        |value1,value2,value3
        |value4,value5,value6}
    
    Args:
        text: TSON object string starting with '{@'
        indent: Indentation string
        depth: Current nesting depth
    
    Returns:
        Pretty-formatted object
    """
    if not text.startswith('{@') or not text.endswith('}'):
        return text
    
    # Extract content between {@ and }
    content = text[2:-1]
    
    if not content:
        return '{@}'
    
    # Split by | to get schema and values
    parts = _split_top_level(content, '|')
    
    if len(parts) == 0:
        return text
    
    schema = parts[0]
    value_rows = parts[1:]
    
    # Build pretty output
    current_indent = indent * depth
    next_indent = indent * (depth + 1)
    
    if not value_rows:
        # Schema only, no values
        return f'{{{current_indent}@{schema}}}'
    
    lines = [f'{{@{schema}']
    
    for row in value_rows:
        # Prettify nested objects/arrays within each row
        prettified_row = _prettify_row_values(row, indent, depth + 1)
        lines.append(f'{next_indent}|{prettified_row}')
    
    # Close brace on same line as last value
    lines[-1] = lines[-1] + '}'
    
    return '\n'.join(lines)


def _prettify_array(text: str, indent: str, depth: int) -> str:
    """
    Prettify a TSON array.
    
    Format:
        [value1
        ,value2
        ,value3]
    
    Args:
        text: TSON array string starting with '['
        indent: Indentation string
        depth: Current nesting depth
    
    Returns:
        Pretty-formatted array
    """
    if not text.startswith('[') or not text.endswith(']'):
        return text
    
    content = text[1:-1]
    
    if not content:
        return '[]'
    
    # Split array elements
    elements = _split_top_level(content, ',')
    
    if len(elements) <= 1:
        # Single element or empty, keep compact
        return text
    
    next_indent = indent * (depth + 1)
    
    lines = []
    for i, elem in enumerate(elements):
        prettified = _prettify_value(elem.strip(), indent, depth + 1)
        if i == 0:
            lines.append(f'[{prettified}')
        else:
            lines.append(f'{next_indent},{prettified}')
    
    lines[-1] = lines[-1] + ']'
    
    return '\n'.join(lines)


def _prettify_row_values(row: str, indent: str, depth: int) -> str:
    """
    Prettify values within a row, handling nested structures.
    
    Args:
        row: Comma-separated row values
        indent: Indentation string
        depth: Current nesting depth
    
    Returns:
        Row with nested values prettified (inline)
    """
    # For Level-1 formatting, we keep rows compact but prettify
    # nested objects/arrays that appear within
    values = _split_top_level(row, ',')
    
    prettified_values = []
    for val in values:
        val = val.strip()
        # Only prettify nested objects at depth 0 (top level)
        # Keep row values compact for CSV-like appearance
        prettified_values.append(val)
    
    return ','.join(prettified_values)


def _split_top_level(text: str, delimiter: str) -> list:
    """
    Split text by delimiter, respecting nested brackets and quotes.
    
    Args:
        text: Text to split
        delimiter: Character to split on
    
    Returns:
        List of parts
    """
    parts = []
    current = []
    depth = 0
    in_string = False
    escape_next = False
    
    i = 0
    while i < len(text):
        char = text[i]
        
        if escape_next:
            current.append(char)
            escape_next = False
            i += 1
            continue
        
        if char == '\\':
            current.append(char)
            escape_next = True
            i += 1
            continue
        
        if char == '"':
            in_string = not in_string
            current.append(char)
            i += 1
            continue
        
        if in_string:
            current.append(char)
            i += 1
            continue
        
        if char in '{[':
            depth += 1
            current.append(char)
        elif char in '}]':
            depth -= 1
            current.append(char)
        elif char == delimiter and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(char)
        
        i += 1
    
    if current:
        parts.append(''.join(current))
    
    return parts


def minify(tson_str: str) -> str:
    """
    Remove all formatting from a TSON string.
    
    Args:
        tson_str: Pretty-formatted TSON string
    
    Returns:
        Compact single-line TSON string
    """
    if not tson_str:
        return tson_str
    
    lines = tson_str.split('\n')
    result = []
    
    for line in lines:
        # Remove leading/trailing whitespace but preserve content
        stripped = line.strip()
        result.append(stripped)
    
    return ''.join(result)
