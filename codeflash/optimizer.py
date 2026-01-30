"""
General Code Optimizer
Handles speed and memory optimization goals
"""

import ast
from pathlib import Path
from typing import List, Dict


class CodeOptimizer:
    """
    General code optimizer for speed and memory optimizations.
    """
    
    def __init__(self, path: str, goal: str = 'speed'):
        self.path = Path(path)
        self.goal = goal
        self.results = []
    
    def analyze(self) -> List[Dict]:
        """
        Analyze code for optimization opportunities.
        
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
            
            if self.goal == 'speed':
                self._check_speed_optimizations(tree, file_path)
            elif self.goal == 'memory':
                self._check_memory_optimizations(tree, file_path)
            
        except (SyntaxError, Exception):
            # Skip files that can't be analyzed
            pass
    
    def _check_speed_optimizations(self, tree: ast.AST, file_path: Path):
        """Check for speed optimization opportunities."""
        for node in ast.walk(tree):
            # Check for list membership tests that could use sets
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.In):
                        self.results.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'issue': 'List membership test (O(n) complexity)',
                            'impact': 'Slower lookups for large lists',
                            'suggestion': 'Convert to set for O(1) lookup if checking membership frequently',
                            'type': 'speed',
                        })
    
    def _check_memory_optimizations(self, tree: ast.AST, file_path: Path):
        """Check for memory optimization opportunities."""
        for node in ast.walk(tree):
            # Check for list comprehensions
            if isinstance(node, ast.ListComp):
                self.results.append({
                    'file': str(file_path),
                    'line': node.lineno,
                    'issue': 'List comprehension stores all items in memory',
                    'impact': 'High memory usage for large datasets',
                    'suggestion': 'Use generator expression if items are processed once',
                    'type': 'memory',
                })
    
    def apply_optimizations(self, results: List[Dict]) -> int:
        """
        Apply the suggested optimizations.
        
        Args:
            results: List of optimization suggestions
            
        Returns:
            Number of optimizations applied
        """
        # Placeholder for actual implementation
        # In production, this would modify the code
        return len(results)
