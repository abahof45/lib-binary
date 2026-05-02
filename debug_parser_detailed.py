#!/usr/bin/env python3
"""
Debug parser with detailed token tracking
"""

from lexer import tokenize_source, Lexer, Token, TokenType

def debug_parser_detailed(source):
    print("Source code:")
    print(source)
    print("\nTokens:")
    
    # Get tokens
    lexer = Lexer(source)
    tokens = []
    for token in lexer.tokenize():
        tokens.append(token)
        print(f"  {token.type.value:15} '{token.value:10}' Line: {token.line:2} Col: {token.column:2}")
    
    print("\nSimulating parser:")
    
    # Simulate the parser logic
    pos = 0
    current_token = tokens[pos] if pos < len(tokens) else None
    
    print(f"Current token: {current_token.type.value if current_token else 'None'}")
    
    # Expect FUNC
    if current_token and current_token.type == TokenType.FUNC:
        print("✓ Found FUNC")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Next token: {current_token.type.value if current_token else 'None'}")
    
    # Expect IDENTIFIER (function name)
    if current_token and current_token.type == TokenType.IDENTIFIER:
        print(f"✓ Found function name: {current_token.value}")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Next token: {current_token.type.value if current_token else 'None'}")
    
    # Expect LPAREN
    if current_token and current_token.type == TokenType.LPAREN:
        print("✓ Found LPAREN")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Next token: {current_token.type.value if current_token else 'None'}")
    
    # Expect RPAREN (no parameters)
    if current_token and current_token.type == TokenType.RPAREN:
        print("✓ Found RPAREN")
        pos += 1
        current_token = tokens[pos] if pos < len(tokens) else None
        print(f"Next token: {current_token.type.value if current_token else 'None'}")
        
        # Check for optional return type colon
        if current_token and current_token.type == TokenType.COLON:
            print("✓ Found COLON (potential return type)")
            pos += 1
            current_token = tokens[pos] if pos < len(tokens) else None
            print(f"Next token: {current_token.type.value if current_token else 'None'}")
            
            # Check if next token is a type
            if current_token and current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR, TokenType.STR]:
                print(f"✓ Found return type: {current_token.value}")
                pos += 1
                current_token = tokens[pos] if pos < len(tokens) else None
                print(f"Next token: {current_token.type.value if current_token else 'None'}")
                
                # Expect another COLON for function body
                if current_token and current_token.type == TokenType.COLON:
                    print("✓ Found COLON (function body)")
                    pos += 1
                    current_token = tokens[pos] if pos < len(tokens) else None
                    print(f"Next token: {current_token.type.value if current_token else 'None'}")
                else:
                    print("✗ Expected COLON for function body")
            else:
                print("✗ Expected type after return type colon")
        else:
            # No return type, expect COLON for function body
            print("Looking for COLON for function body...")
            if current_token and current_token.type == TokenType.COLON:
                print("✓ Found COLON (function body)")
                pos += 1
                current_token = tokens[pos] if pos < len(tokens) else None
                print(f"Next token: {current_token.type.value if current_token else 'None'}")
            else:
                print(f"✗ Expected COLON for function body, got {current_token.type.value if current_token else 'None'}")
    else:
        print(f"✗ Expected RPAREN, got {current_token.type.value if current_token else 'None'}")

if __name__ == "__main__":
    # Test simple function
    source = """func main():
    print("Hello")
    x = 10
    y = 20
    print(x + y)"""
    
    debug_parser_detailed(source)
