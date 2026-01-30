"""
Tests for Cost Analyzer
"""

import unittest
import tempfile
import os
from pathlib import Path
from codeflash.cost_analyzer import CostAnalyzer


class TestCostAnalyzer(unittest.TestCase):
    """Test cases for the CostAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_detect_heavy_import(self):
        """Test detection of heavy library imports."""
        # Create a test file with pandas import
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""
import pandas as pd

df = pd.read_csv('data.csv')
""")
        
        analyzer = CostAnalyzer(str(test_file))
        results = analyzer.analyze()
        
        # Should detect pandas as heavy import
        self.assertTrue(len(results) > 0)
        self.assertTrue(any('pandas' in r['issue'].lower() for r in results))
    
    def test_detect_list_comprehension(self):
        """Test detection of list comprehensions that could be generators."""
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""
numbers = [x * 2 for x in range(1000000)]
""")
        
        analyzer = CostAnalyzer(str(test_file))
        results = analyzer.analyze()
        
        # Should detect list comprehension
        self.assertTrue(any('comprehension' in r['issue'].lower() for r in results))
    
    def test_detect_string_concatenation(self):
        """Test detection of augmented assignment in loops."""
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""
result = ""
for item in range(10):
    result += str(item)
""")
        
        analyzer = CostAnalyzer(str(test_file))
        results = analyzer.analyze()
        
        # Should detect augmented assignment issue
        self.assertTrue(any('+=' in r['issue'] or 'augmented' in r['issue'].lower() for r in results))
    
    def test_analyze_directory(self):
        """Test analyzing a directory of Python files."""
        # Create multiple test files
        file1 = Path(self.temp_dir) / "file1.py"
        file1.write_text("import pandas as pd")
        
        file2 = Path(self.temp_dir) / "file2.py"
        file2.write_text("import numpy as np")
        
        analyzer = CostAnalyzer(self.temp_dir)
        results = analyzer.analyze()
        
        # Should find issues in both files
        self.assertTrue(len(results) >= 2)
    
    def test_skip_invalid_files(self):
        """Test that invalid Python files are skipped gracefully."""
        test_file = Path(self.temp_dir) / "invalid.py"
        test_file.write_text("this is not valid python {{{")
        
        analyzer = CostAnalyzer(str(test_file))
        # Should not raise an exception
        results = analyzer.analyze()
        
        # May return empty or partial results, but shouldn't crash
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()
