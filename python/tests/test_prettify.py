"""
Test suite for TSON prettify module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tson
from tson.prettify import prettify, minify


class TestPrettify:
    """Tests for the prettify function."""

    def test_simple_object(self):
        """Test prettifying a simple object."""
        compact = '{@a,b|1,2}'
        expected = '{@a,b\n  |1,2}'
        assert prettify(compact) == expected

    def test_tabular_format(self):
        """Test prettifying tabular data (array of objects)."""
        compact = '{@id,name#3|1,Alice|2,Bob|3,Carol}'
        expected = '{@id,name#3\n  |1,Alice\n  |2,Bob\n  |3,Carol}'
        assert prettify(compact) == expected

    def test_nested_object_stays_compact(self):
        """Nested objects within rows should stay compact (Level-1 only)."""
        compact = '{@user,meta|{@id,name|1,Alice},{@count|5}}'
        pretty = prettify(compact)
        # Should only split at top-level |
        lines = pretty.split('\n')
        assert len(lines) == 2
        assert lines[0] == '{@user,meta'
        assert '|{@id,name|1,Alice},{@count|5}}' in lines[1]

    def test_empty_object(self):
        """Test empty object stays unchanged."""
        assert prettify('{@}') == '{@}'

    def test_empty_array(self):
        """Test empty array stays unchanged."""
        assert prettify('[]') == '[]'

    def test_array_of_objects(self):
        """Test prettifying an array of objects."""
        compact = '[{@a|1},{@b|2},{@c|3}]'
        pretty = prettify(compact)
        assert pretty.startswith('[{@a')
        assert ',{@b' in pretty
        assert ',{@c' in pretty

    def test_quoted_strings(self):
        """Test that quoted strings are handled correctly."""
        compact = '{@name,desc|"Alice","Hello, World!"}'
        pretty = prettify(compact)
        assert '"Alice"' in pretty
        assert '"Hello, World!"' in pretty

    def test_with_nested_arrays(self):
        """Test tabular data with nested arrays."""
        compact = '{@name,scores#2|Alice,[90,85]|Bob,[88,91]}'
        expected = '{@name,scores#2\n  |Alice,[90,85]\n  |Bob,[88,91]}'
        assert prettify(compact) == expected


class TestMinify:
    """Tests for the minify function."""

    def test_round_trip(self):
        """Test that minify reverses prettify."""
        original = '{@id,name#3|1,Alice|2,Bob|3,Carol}'
        pretty = prettify(original)
        minified = minify(pretty)
        assert minified == original

    def test_minify_multiline(self):
        """Test minifying a multiline string."""
        pretty = '{@a,b\n  |1,2\n  |3,4}'
        expected = '{@a,b|1,2|3,4}'
        assert minify(pretty) == expected

    def test_minify_already_compact(self):
        """Test minifying already compact string."""
        compact = '{@a,b|1,2}'
        assert minify(compact) == compact


class TestRoundTrip:
    """Tests for round-trip integrity (content preservation)."""

    def test_simple_round_trip_parsing(self):
        """Ensure parsed content is identical after prettify/minify."""
        original = '{@id,name,active#2|1,Alice,true|2,Bob,false}'
        
        # Parse original
        data1 = tson.loads(original)
        
        # Prettify, minify, parse
        pretty = prettify(original)
        minified = minify(pretty)
        data2 = tson.loads(minified)
        data2 = tson.loads(pretty)
        
        assert data1 == data2

    def test_complex_nested_round_trip(self):
        """Test round-trip with nested structures."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ],
            "count": 2
        }
        
        # Serialize → Prettify → Minify → Parse
        compact = tson.dumps(data)
        pretty = prettify(compact)
        minified = minify(pretty)
        parsed = tson.loads(minified)
        
        assert parsed == data


def run_tests():
    """Run all tests and print results."""
    test_classes = [TestPrettify, TestMinify, TestRoundTrip]
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        print(f"\n{'='*50}")
        print(f"Running: {test_class.__name__}")
        print('='*50)
        
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                    failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print('='*50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
