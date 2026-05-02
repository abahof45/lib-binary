#!/usr/bin/env python3
"""
Debug parser to see where it's failing
"""

from lexer import tokenize_source
from parser import parse_source

def debug_parser(source):
    print("Source code:")
    print(source)
    print("\nParsing...")
    
    try:
        ast = parse_source(source)
        print("✓ Parsing successful!")
        print(f"AST: {ast}")
        
        # Print AST structure
        def print_ast(node, indent=0):
            prefix = "  " * indent
            print(f"{prefix}{repr(node)}")
            if hasattr(node, 'statements'):
                for stmt in node.statements:
                    print_ast(stmt, indent + 1)
            elif hasattr(node, 'body'):
                for stmt in node.body:
                    print_ast(stmt, indent + 1)
        
        print("\nAST structure:")
        print_ast(ast)
        
    except Exception as e:
        print(f"✗ Parsing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test simple function
    source = """func main():
    print("Hello")
    x = 10
    y = 20
    print(x + y)"""
    
    debug_parser(source)
