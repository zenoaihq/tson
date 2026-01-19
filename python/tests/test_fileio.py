"""
Test suite for TSON file I/O utilities.
"""

import sys
import os
import tempfile
import json
import gzip
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tson


class TestLoadFunctions:
    """Tests for load functions."""

    def test_load_json(self):
        """Test loading a JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "Alice", "age": 30}, f)
            filepath = f.name
        
        try:
            data = tson.load_json(filepath)
            assert data == {"name": "Alice", "age": 30}
        finally:
            os.unlink(filepath)

    def test_load_json_gzipped(self):
        """Test loading a gzipped JSON file."""
        filepath = tempfile.mktemp(suffix='.json.gz')
        with gzip.open(filepath, 'wt') as f:
            json.dump({"x": 1, "y": 2}, f)
        
        try:
            data = tson.load_json(filepath)
            assert data == {"x": 1, "y": 2}
        finally:
            os.unlink(filepath)

    def test_load_tson(self):
        """Test loading a TSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tson', delete=False) as f:
            f.write('{@id,name#2|1,Alice|2,Bob}')
            filepath = f.name
        
        try:
            data = tson.load_tson(filepath)
            assert data == [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        finally:
            os.unlink(filepath)

    def test_load_tson_gzipped(self):
        """Test loading a gzipped TSON file."""
        filepath = tempfile.mktemp(suffix='.tson.gz')
        with gzip.open(filepath, 'wt') as f:
            f.write('{@a,b|1,2}')
        
        try:
            data = tson.load_tson(filepath)
            assert data == {"a": 1, "b": 2}
        finally:
            os.unlink(filepath)


class TestSaveFunctions:
    """Tests for save functions."""

    def test_save_tson_compact(self):
        """Test saving data as compact TSON."""
        filepath = tempfile.mktemp(suffix='.tson')
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        
        try:
            tson.save_tson(data, filepath, format="compact")
            content = open(filepath).read()
            assert '@id,name#2' in content
            assert '\n' not in content  # Compact = single line
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_tson_pretty(self):
        """Test saving data as pretty TSON."""
        filepath = tempfile.mktemp(suffix='.tson')
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        
        try:
            tson.save_tson(data, filepath, format="pretty")
            content = open(filepath).read()
            assert '\n' in content  # Pretty = multiple lines
            assert '|1,Alice' in content
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_tson_gzipped(self):
        """Test saving data as gzipped TSON."""
        filepath = tempfile.mktemp(suffix='.tson.gz')
        data = {"key": "value"}
        
        try:
            tson.save_tson(data, filepath, compress=True)
            # Verify it's actually gzipped
            with gzip.open(filepath, 'rt') as f:
                content = f.read()
            assert 'key' in content
            assert 'value' in content
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_tson_string(self):
        """Test saving a TSON string directly."""
        filepath = tempfile.mktemp(suffix='.tson')
        tson_str = '{@a,b,c|1,2,3}'
        
        try:
            tson.save_tson_string(tson_str, filepath)
            content = open(filepath).read()
            assert content == tson_str
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)

    def test_save_tson_string_pretty(self):
        """Test saving TSON string with prettify."""
        filepath = tempfile.mktemp(suffix='.tson')
        tson_str = '{@a,b#2|1,2|3,4}'
        
        try:
            tson.save_tson_string(tson_str, filepath, format="pretty")
            content = open(filepath).read()
            assert '\n' in content
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)


class TestConversionFunctions:
    """Tests for format conversion functions."""

    def test_json_to_tson(self):
        """Test converting JSON file to TSON."""
        json_path = tempfile.mktemp(suffix='.json')
        tson_path = tempfile.mktemp(suffix='.tson')
        
        with open(json_path, 'w') as f:
            json.dump([{"id": 1}, {"id": 2}], f)
        
        try:
            result = tson.json_to_tson(json_path, tson_path)
            assert '@id#2' in result
            
            # Verify file was created
            assert os.path.exists(tson_path)
            content = open(tson_path).read()
            assert content == result
        finally:
            for p in [json_path, tson_path]:
                if os.path.exists(p):
                    os.unlink(p)

    def test_tson_to_json(self):
        """Test converting TSON file to JSON."""
        tson_path = tempfile.mktemp(suffix='.tson')
        json_path = tempfile.mktemp(suffix='.json')
        
        with open(tson_path, 'w') as f:
            f.write('{@name,value|test,123}')
        
        try:
            result = tson.tson_to_json(tson_path, json_path)
            data = json.loads(result)
            assert data == {"name": "test", "value": 123}
            
            # Verify file was created
            assert os.path.exists(json_path)
        finally:
            for p in [tson_path, json_path]:
                if os.path.exists(p):
                    os.unlink(p)

    def test_json_to_tson_no_output(self):
        """Test json_to_tson returns string without saving."""
        json_path = tempfile.mktemp(suffix='.json')
        
        with open(json_path, 'w') as f:
            json.dump({"a": 1}, f)
        
        try:
            result = tson.json_to_tson(json_path)  # No output path
            assert '@a|1' in result
        finally:
            os.unlink(json_path)


class TestFileOperations:
    """Tests for file prettify/minify operations."""

    def test_read_tson_string(self):
        """Test reading TSON as raw string."""
        filepath = tempfile.mktemp(suffix='.tson')
        content = '{@foo,bar|1,2}'
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        try:
            result = tson.read_tson_string(filepath)
            assert result == content
        finally:
            os.unlink(filepath)

    def test_prettify_file(self):
        """Test prettifying a file in place."""
        filepath = tempfile.mktemp(suffix='.tson')
        
        with open(filepath, 'w') as f:
            f.write('{@a,b#2|1,2|3,4}')
        
        try:
            result = tson.prettify_file(filepath)
            assert '\n' in result
            
            # Check file was updated
            content = open(filepath).read()
            assert '\n' in content
        finally:
            os.unlink(filepath)

    def test_minify_file(self):
        """Test minifying a file."""
        filepath = tempfile.mktemp(suffix='.tson')
        
        with open(filepath, 'w') as f:
            f.write('{@a,b#2\n  |1,2\n  |3,4}')
        
        try:
            result = tson.minify_file(filepath)
            assert '\n' not in result
            
            # Check file was updated
            content = open(filepath).read()
            assert '\n' not in content
        finally:
            os.unlink(filepath)

    def test_prettify_file_to_new_path(self):
        """Test prettifying to a different output file."""
        input_path = tempfile.mktemp(suffix='.tson')
        output_path = tempfile.mktemp(suffix='.pretty.tson')
        
        with open(input_path, 'w') as f:
            f.write('{@x,y|1,2}')
        
        try:
            tson.prettify_file(input_path, output_path)
            
            # Original unchanged
            original = open(input_path).read()
            assert '\n' not in original
            
            # Output is prettified
            pretty = open(output_path).read()
            assert '\n' in pretty
        finally:
            for p in [input_path, output_path]:
                if os.path.exists(p):
                    os.unlink(p)


def run_tests():
    """Run all tests and print results."""
    test_classes = [
        TestLoadFunctions,
        TestSaveFunctions,
        TestConversionFunctions,
        TestFileOperations,
    ]
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
