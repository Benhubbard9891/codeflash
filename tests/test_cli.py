"""
Tests for CLI
"""

import unittest
from click.testing import CliRunner
from codeflash.cli import main


class TestCLI(unittest.TestCase):
    """Test cases for the CLI."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(main, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('0.1.0', result.output)
    
    def test_help(self):
        """Test help command."""
        result = self.runner.invoke(main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Codeflash', result.output)
    
    def test_optimize_help(self):
        """Test optimize command help."""
        result = self.runner.invoke(main, ['optimize', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('--goal', result.output)
        self.assertIn('speed', result.output)
        self.assertIn('cost', result.output)


if __name__ == '__main__':
    unittest.main()
