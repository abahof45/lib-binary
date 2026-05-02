#!/usr/bin/env python3
"""
Debug lexer to see what tokens are generated
"""

from lexer import tokenize_source

def debug_tokens(source):
    print("Source code:")
    print(source)
    print("\nTokens:")
    
    tokens = tokenize_source(source)
    for token in tokens:
        print(f"  {token.type.value:15} '{token.value:10}' Line: {token.line:2} Col: {token.column:2}")

if __name__ == "__main__":
    # Test simple function
    source = """func main():
    print("Hello")
    x = 10
    y = 20
    print(x + y)"""
    
    debug_tokens(source)
