#!/usr/bin/env python3
import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import your test modules
from test_leafnode import TestLeafNode
from test_htmlnode import TestHTMLNode
from test_textnode import *
from test_parentnode import TestParentNode

def create_test_suite():
    """Create a test suite with the specific tests you want to run."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Define all your test classes here
    test_classes = [
        # TestTextNode,
        # TestHTMLNode,
        # TestLeafNode,
        # TestParentNode,
        # TestTextNodeToHtmlNode,
        TestSplitNodesDelimeter
    ]
    
    # Add all test classes to the suite
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    return suite

if __name__ == "__main__":
    # Create and run the test suite
    test_suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful()) 