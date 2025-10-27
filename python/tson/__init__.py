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

__version__ = "1.0.0"
__author__ = "TSON Contributors"
__license__ = "MIT"

from .serializer import dumps, dump
from .deserializer import loads, load

__all__ = [
    "dumps",
    "dump",
    "loads",
    "load",
]
