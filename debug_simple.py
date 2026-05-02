#!/usr/bin/env python3
"""
Simple debug without Unicode
"""

from lexer import tokenize_source, Lexer, Token, TokenType

def debug_simple(source):
    print("Source code:")
    print(source)
    print("\nTokens:")
    
    # Get tokens
    lexer = Lexer(source)
    tokens = []
    for token in lexer.tokenize():
        tokens.append(token)
        print(f"  {token.type.value:15} '{token.value:10}' Line: {token.line:2} Col: {token.column:2}")
    
    print("\nParser simulation:")
    
    # Simulate the parser logic step by step
    pos = 0
    current_token = tokens[pos] if pos < len(tokens) else None
    
    print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
    
    # Expect FUNC
    if current_token and current_token.type == TokenType.FUNC:
        print("Found FUNC")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
    
    # Expect IDENTIFIER (function name)
    if current_token and current_token.type == TokenType.IDENTIFIER:
        print(f"Found function name: {current_token.value}")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
    
    # Expect LPAREN
    if current_token and current_token.type == TokenType.LPAREN:
        print("Found LPAREN")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
    
    # Expect RPAREN (no parameters)
    if current_token and current_token.type == TokenType.RPAREN:
        print("Found RPAREN")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
        
        # Now check what we have after RPAREN
        print(f"After RPAREN: {current_token.type.value if current_token else 'None'}")
        
        # The issue: we have COLON here, which should be the function body colon
        if current_token and current_token.type == TokenType.COLON:
            print("Found COLON - this should be function body colon")
            pos += 1
            current_token = tokens[pos] if pos < len(tokens) else None
            print(f"Position {pos}: {current_token.type.value if current_token else 'None'}")
        else:
            print(f"Expected COLON for function body, got {current_token.type.value if current_token else 'None'}")
    else:
        print(f"Expected RPAREN, got {current_token.type.value if current_token else 'None'}")

if __name__ == "__main__":
    # Test simple function
    source = """func main():
    print("Hello")
    x = 10
    y = 20
    print(x + y)"""
    
    debug_simple(source)
