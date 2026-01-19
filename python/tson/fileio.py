"""
TSON File Utilities

Convenience functions for working with TSON and JSON files.
Includes support for:
- Loading JSON/TSON files
- Saving to TSON with formatting options
- Optional gzip compression (uses stdlib, no extra dependencies)
"""

import json
import gzip
from pathlib import Path
from typing import Any, Union, Optional, Literal

from .serializer import dumps
from .deserializer import loads
from .prettify import prettify, minify


# Type alias for file paths
PathLike = Union[str, Path]
FormatOption = Literal["compact", "pretty"]


def load_json(filepath: PathLike, encoding: str = "utf-8") -> Any:
    """
    Load a JSON file and return Python data structure.
    
    Args:
        filepath: Path to JSON file (.json or .json.gz)
        encoding: File encoding (default: utf-8)
    
    Returns:
        Parsed Python object
    
    Examples:
        >>> data = load_json("data.json")
        >>> data = load_json("data.json.gz")  # gzipped
    """
    filepath = Path(filepath)
    
    if filepath.suffix == '.gz':
        with gzip.open(filepath, 'rt', encoding=encoding) as f:
            return json.load(f)
    else:
        with open(filepath, 'r', encoding=encoding) as f:
            return json.load(f)


def load_tson(filepath: PathLike, encoding: str = "utf-8") -> Any:
    """
    Load a TSON file and return Python data structure.
    
    Args:
        filepath: Path to TSON file (.tson or .tson.gz)
        encoding: File encoding (default: utf-8)
    
    Returns:
        Parsed Python object
    
    Examples:
        >>> data = load_tson("data.tson")
        >>> data = load_tson("data.tson.gz")  # gzipped
    """
    filepath = Path(filepath)
    
    if filepath.suffix == '.gz':
        with gzip.open(filepath, 'rt', encoding=encoding) as f:
            return loads(f.read())
    else:
        with open(filepath, 'r', encoding=encoding) as f:
            return loads(f.read())


def save_tson(
    data: Any,
    filepath: PathLike,
    format: FormatOption = "compact",
    indent: str = "  ",
    compress: bool = False,
    encoding: str = "utf-8"
) -> None:
    """
    Save Python data to a TSON file.
    
    Args:
        data: Python object to serialize
        filepath: Output file path
        format: "compact" (default) or "pretty"
        indent: Indentation for pretty format (default: 2 spaces)
        compress: If True, gzip compress the output
        encoding: File encoding (default: utf-8)
    
    Examples:
        >>> save_tson(data, "output.tson")
        >>> save_tson(data, "output.tson", format="pretty")
        >>> save_tson(data, "output.tson.gz", compress=True)
    """
    filepath = Path(filepath)
    
    # Serialize to TSON
    tson_str = dumps(data)
    
    # Apply formatting
    if format == "pretty":
        tson_str = prettify(tson_str, indent=indent)
    
    # Write to file
    if compress or filepath.suffix == '.gz':
        with gzip.open(filepath, 'wt', encoding=encoding) as f:
            f.write(tson_str)
    else:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(tson_str)


def save_tson_string(
    tson_str: str,
    filepath: PathLike,
    format: Optional[FormatOption] = None,
    indent: str = "  ",
    compress: bool = False,
    encoding: str = "utf-8"
) -> None:
    """
    Save a TSON string directly to file.
    
    Args:
        tson_str: TSON formatted string
        filepath: Output file path
        format: None (keep as-is), "compact", or "pretty"
        indent: Indentation for pretty format (default: 2 spaces)
        compress: If True, gzip compress the output
        encoding: File encoding (default: utf-8)
    
    Examples:
        >>> save_tson_string(tson_data, "output.tson")
        >>> save_tson_string(tson_data, "output.tson", format="pretty")
    """
    filepath = Path(filepath)
    
    # Apply formatting if requested
    if format == "pretty":
        tson_str = prettify(tson_str, indent=indent)
    elif format == "compact":
        tson_str = minify(tson_str)
    
    # Write to file
    if compress or filepath.suffix == '.gz':
        with gzip.open(filepath, 'wt', encoding=encoding) as f:
            f.write(tson_str)
    else:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(tson_str)


def json_to_tson(
    input_path: PathLike,
    output_path: Optional[PathLike] = None,
    format: FormatOption = "compact",
    compress: bool = False
) -> str:
    """
    Convert a JSON file to TSON format.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path to output TSON file (optional)
        format: "compact" (default) or "pretty"
        compress: If True, gzip compress the output
    
    Returns:
        TSON string representation
    
    Examples:
        >>> tson_str = json_to_tson("data.json")
        >>> json_to_tson("data.json", "data.tson")
        >>> json_to_tson("data.json", "data.tson.gz", compress=True)
    """
    data = load_json(input_path)
    tson_str = dumps(data)
    
    if format == "pretty":
        tson_str = prettify(tson_str)
    
    if output_path:
        save_tson_string(tson_str, output_path, compress=compress)
    
    return tson_str


def tson_to_json(
    input_path: PathLike,
    output_path: Optional[PathLike] = None,
    indent: Optional[int] = 2,
    compress: bool = False
) -> str:
    """
    Convert a TSON file to JSON format.
    
    Args:
        input_path: Path to input TSON file
        output_path: Path to output JSON file (optional)
        indent: JSON indentation (default: 2, None for compact)
        compress: If True, gzip compress the output
    
    Returns:
        JSON string representation
    
    Examples:
        >>> json_str = tson_to_json("data.tson")
        >>> tson_to_json("data.tson", "data.json")
    """
    data = load_tson(input_path)
    json_str = json.dumps(data, indent=indent, ensure_ascii=False)
    
    if output_path:
        output_path = Path(output_path)
        if compress or output_path.suffix == '.gz':
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.write(json_str)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
    
    return json_str


def read_tson_string(filepath: PathLike, encoding: str = "utf-8") -> str:
    """
    Read a TSON file as raw string (without parsing).
    
    Useful when you want to prettify/minify without deserializing.
    
    Args:
        filepath: Path to TSON file
        encoding: File encoding (default: utf-8)
    
    Returns:
        Raw TSON string
    """
    filepath = Path(filepath)
    
    if filepath.suffix == '.gz':
        with gzip.open(filepath, 'rt', encoding=encoding) as f:
            return f.read()
    else:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()


def prettify_file(
    input_path: PathLike,
    output_path: Optional[PathLike] = None,
    indent: str = "  "
) -> str:
    """
    Prettify a TSON file in place or to a new file.
    
    Args:
        input_path: Path to input TSON file
        output_path: Path to output file (default: overwrite input)
        indent: Indentation string (default: 2 spaces)
    
    Returns:
        Prettified TSON string
    """
    tson_str = read_tson_string(input_path)
    pretty_str = prettify(tson_str, indent=indent)
    
    target = output_path or input_path
    save_tson_string(pretty_str, target)
    
    return pretty_str


def minify_file(
    input_path: PathLike,
    output_path: Optional[PathLike] = None
) -> str:
    """
    Minify a TSON file in place or to a new file.
    
    Args:
        input_path: Path to input TSON file
        output_path: Path to output file (default: overwrite input)
    
    Returns:
        Minified TSON string
    """
    tson_str = read_tson_string(input_path)
    compact_str = minify(tson_str)
    
    target = output_path or input_path
    save_tson_string(compact_str, target)
    
    return compact_str
