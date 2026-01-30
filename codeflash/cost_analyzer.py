"""
Cloud Cost Analyzer
Identifies optimization opportunities to reduce cloud computing costs
"""

import ast
import os
from pathlib import Path
from typing import List, Dict


class CostAnalyzer:
    """
    Analyzes Python code for cloud cost optimization opportunities.
    
    Focuses on:
    - Memory usage optimization
    - Heavy library import reduction
    - Data structure efficiency
    - Resource allocation patterns
    """
    
    # Heavy libraries that could have lighter alternatives
    HEAVY_LIBRARIES = {
        'pandas': {
            'weight': 'heavy',
            'alternatives': ['csv (stdlib)', 'polars (lighter & faster)'],
            'use_cases': {
                'read_csv': 'For simple CSV reading, use csv.DictReader from stdlib',
                'DataFrame': 'For large datasets, consider polars or Apache Arrow',
            }
        },
        'numpy': {
            'weight': 'medium',
            'alternatives': ['array (stdlib) for simple arrays'],
            'use_cases': {
                'array': 'For simple arrays without complex operations',
            }
        },
        'requests': {
            'weight': 'medium',
            'alternatives': ['urllib (stdlib) for simple HTTP requests'],
            'use_cases': {}
        },
    }
    
    def __init__(self, path: str):
        self.path = Path(path)
        self.results = []
    
    def analyze(self) -> List[Dict]:
        """
        Analyze the code and return optimization opportunities.
        
        Returns:
            List of dictionaries with optimization suggestions
        """
        if self.path.is_file():
            self._analyze_file(self.path)
        elif self.path.is_dir():
            for py_file in self.path.rglob('*.py'):
                self._analyze_file(py_file)
        
        return self.results
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            self._check_imports(tree, file_path)
            self._check_data_structures(tree, file_path)
            self._check_memory_patterns(tree, file_path)
            
        except SyntaxError:
            # Skip files with syntax errors
            pass
        except (UnicodeDecodeError, IOError):
            # Skip files that can't be read
            pass
    
    def _check_imports(self, tree: ast.AST, file_path: Path):
        """Check for heavy library imports that could be optimized."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._check_library_usage(alias.name, node.lineno, file_path)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._check_library_usage(node.module, node.lineno, file_path)
    
    def _check_library_usage(self, lib_name: str, line_no: int, file_path: Path):
        """Check if a library import could be optimized."""
        # Check if this is a heavy library
        base_lib = lib_name.split('.')[0]
        
        if base_lib in self.HEAVY_LIBRARIES:
            lib_info = self.HEAVY_LIBRARIES[base_lib]
            alternatives = ', '.join(lib_info['alternatives'])
            
            self.results.append({
                'file': str(file_path),
                'line': line_no,
                'issue': f'Heavy import: {lib_name}',
                'impact': f'Increases memory footprint and cold-start time (Library is {lib_info["weight"]})',
                'suggestion': f'Consider lighter alternatives: {alternatives}',
                'type': 'import_optimization',
                'library': base_lib,
            })
    
    def _check_data_structures(self, tree: ast.AST, file_path: Path):
        """Check for inefficient data structure usage."""
        for node in ast.walk(tree):
            # Check for list comprehensions that could be generators
            if isinstance(node, ast.ListComp):
                # Note: This is a heuristic - only suggests generators for large iterations
                # In practice, list comprehensions are fine for small datasets or when
                # the list is needed for multiple iterations or indexing
                self.results.append({
                    'file': str(file_path),
                    'line': node.lineno,
                    'issue': 'List comprehension could be a generator',
                    'impact': 'Stores entire list in memory (O(n) space)',
                    'suggestion': 'Use generator expression () instead of [] if only iterating once',
                    'type': 'data_structure',
                })
    
    def _check_memory_patterns(self, tree: ast.AST, file_path: Path):
        """Check for memory-intensive patterns."""
        for node in ast.walk(tree):
            # Check for augmented assignments (+=) in loops
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add):
                            # Potential string concatenation or list concatenation in a loop
                            # Both can be inefficient - strings create new objects, lists copy data
                            self.results.append({
                                'file': str(file_path),
                                'line': child.lineno,
                                'issue': 'Augmented assignment (+= operator) in loop',
                                'impact': 'May create new objects each iteration if used with strings (O(n²) memory)',
                                'suggestion': 'If concatenating strings: use list.append() and "".join(). If adding numbers: this is fine.',
                                'type': 'memory_pattern',
                            })
    
    def apply_optimizations(self, results: List[Dict]) -> int:
        """
        Apply the suggested optimizations to the code.
        
        Note: This is currently a placeholder implementation.
        In production, this would use AST transformation to safely
        apply code modifications.
        
        Args:
            results: List of optimization suggestions
            
        Returns:
            Number of optimizations that would be applied (placeholder)
        """
        # TODO: Implement actual code transformations using AST
        # For now, this is a placeholder that doesn't modify files
        # to avoid breaking user code
        return 0  # Indicate no actual changes were made
