"""
TSON - Token-efficient Structured Object Notation

A compact, delimiter-based serialization format designed for efficient
data exchange with Large Language Models.

Basic usage:
    >>> import tson
    >>> data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    >>> encoded = tson.dumps(data)
    >>> decoded = tson.loads(encoded)
    >>> assert data == decoded

Key features:
    - Token-efficient: 30-60% fewer tokens than JSON for typical data
    - Single syntax: One consistent format for all JSON types
    - Schema notation: Nested schemas for maximum compression
    - LLM-friendly: Clear structure that models can parse and generate
"""

__version__ = "1.1.0"
__author__ = "TSON Contributors"
__license__ = "MIT"

from .serializer import dumps, dump
from .deserializer import loads, load
from .prettify import prettify, minify
from .fileio import (
    load_json,
    load_tson,
    save_tson,
    save_tson_string,
    json_to_tson,
    tson_to_json,
    read_tson_string,
    prettify_file,
    minify_file,
)

__all__ = [
    # Core serialization
    "dumps",
    "dump",
    "loads",
    "load",
    # Formatting
    "prettify",
    "minify",
    # File I/O
    "load_json",
    "load_tson",
    "save_tson",
    "save_tson_string",
    "json_to_tson",
    "tson_to_json",
    "read_tson_string",
    "prettify_file",
    "minify_file",
]

