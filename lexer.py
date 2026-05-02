"""
Lexer for lib-binary programming language
Tokenizes .wd source files into tokens for parsing
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    FUNC = "FUNC"
    LOW = "LOW"
    STRUCT = "STRUCT"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"
    INT = "INT"
    FLOAT = "FLOAT"
    CHAR = "CHAR"
    PTR = "PTR"
    STR = "STR"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    
    # Bitwise operators
    BIT_AND = "BIT_AND"
    BIT_OR = "BIT_OR"
    BIT_XOR = "BIT_XOR"
    BIT_LEFT_SHIFT = "BIT_LEFT_SHIFT"
    BIT_RIGHT_SHIFT = "BIT_RIGHT_SHIFT"
    
    # Comparison operators
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Assignment operators
    ASSIGN = "ASSIGN"
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    COLON = "COLON"
    DOT = "DOT"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"
    
    # Memory operations
    ALLOC = "ALLOC"
    FREE = "FREE"
    STORE = "STORE"
    LOAD = "LOAD"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]  # Stack for tracking indentation levels
        
        # Define token patterns
        self.token_patterns = [
            # Comments
            (r'//.*', None),
            (r'/\*[\s\S]*?\*/', None),
            (r'#.*', None),
            
            # Numbers
            (r'\d+\.\d+', TokenType.NUMBER),
            (r'\d+', TokenType.NUMBER),
            
            # Strings
            (r'"[^"]*"', TokenType.STRING),
            (r"'[^']*'", TokenType.STRING),
            
            # Keywords and identifiers
            (r'func\b', TokenType.FUNC),
            (r'low\b', TokenType.LOW),
            (r'struct\b', TokenType.STRUCT),
            (r'if\b', TokenType.IF),
            (r'else\b', TokenType.ELSE),
            (r'while\b', TokenType.WHILE),
            (r'for\b', TokenType.FOR),
            (r'return\b', TokenType.RETURN),
            (r'int\b', TokenType.INT),
            (r'float\b', TokenType.FLOAT),
            (r'char\b', TokenType.CHAR),
            (r'ptr\b', TokenType.PTR),
            (r'str\b', TokenType.STR),
            (r'alloc\b', TokenType.ALLOC),
            (r'free\b', TokenType.FREE),
            (r'store\b', TokenType.STORE),
            (r'load\b', TokenType.LOAD),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # Multi-character operators
            (r'==', TokenType.EQUAL),
            (r'!=', TokenType.NOT_EQUAL),
            (r'<=', TokenType.LESS_EQUAL),
            (r'>=', TokenType.GREATER_EQUAL),
            (r'<<', TokenType.BIT_LEFT_SHIFT),
            (r'>>', TokenType.BIT_RIGHT_SHIFT),
            (r'\+=', TokenType.PLUS_ASSIGN),
            (r'-=', TokenType.MINUS_ASSIGN),
            
            # Single-character operators
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULTIPLY),
            (r'/', TokenType.DIVIDE),
            (r'%', TokenType.MODULO),
            (r'&', TokenType.BIT_AND),
            (r'\|', TokenType.BIT_OR),
            (r'\^', TokenType.BIT_XOR),
            (r'<', TokenType.LESS_THAN),
            (r'>', TokenType.GREATER_THAN),
            (r'=', TokenType.ASSIGN),
            
            # Delimiters
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\{', TokenType.LBRACE),
            (r'\}', TokenType.RBRACE),
            (r'\[', TokenType.LBRACKET),
            (r'\]', TokenType.RBRACKET),
            (r',', TokenType.COMMA),
            (r':', TokenType.COLON),
            (r'\.', TokenType.DOT),
        ]
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def handle_indentation(self) -> List[Token]:
        tokens = []
        indent_level = 0
        
        # Count leading whitespace
        while self.current_char() and self.current_char() in ' \t':
            if self.current_char() == ' ':
                indent_level += 1
            else:  # Tab
                indent_level += 4  # Assume tab = 4 spaces
            self.advance()
        
        # Compare with current indentation level
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # New indentation level
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, "", self.line, self.column))
        elif indent_level < current_indent:
            # Dedent to appropriate level
            while indent_level < self.indent_stack[-1]:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
        
        return tokens
    
    def next_token(self) -> Token:
        # Handle indentation at the beginning of lines
        if self.column == 1:
            indent_tokens = self.handle_indentation()
            if indent_tokens:
                return indent_tokens[0]
        
        # Skip regular whitespace
        self.skip_whitespace()
        
        # Handle newlines
        if self.current_char() == '\n':
            token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
            self.advance()
            return token
        
        # End of file
        if not self.current_char():
            # Generate remaining DEDENT tokens
            if len(self.indent_stack) > 1:
                self.indent_stack.pop()
                return Token(TokenType.DEDENT, "", self.line, self.column)
            return Token(TokenType.EOF, "", self.line, self.column)
        
        # Try to match patterns
        for pattern, token_type in self.token_patterns:
            regex = re.compile(pattern)
            match = regex.match(self.source, self.position)
            
            if match:
                value = match.group(0)
                
                # Skip comments
                if token_type is None:
                    self.position = match.end()
                    self.column += len(value)
                    return self.next_token()
                
                token = Token(token_type, value, self.line, self.column)
                self.position = match.end()
                self.column += len(value)
                return token
        
        # Unknown character
        char = self.current_char()
        token = Token(TokenType.IDENTIFIER, char, self.line, self.column)
        self.advance()
        return token
    
    def tokenize(self) -> List[Token]:
        tokens = []
        
        while True:
            token = self.next_token()
            tokens.append(token)
            
            if token.type == TokenType.EOF:
                break
        
        return tokens


def tokenize_source(source: str) -> List[Token]:
    """Convenience function to tokenize source code"""
    lexer = Lexer(source)
    return lexer.tokenize()


if __name__ == "__main__":
    # Test the lexer
    test_code = """
func main():
    x = 10
    y = 20
    print(x + y)
    
    low:
        ptr a = alloc(10)
        store(a, 5)
"""
    
    tokens = tokenize_source(test_code)
    for token in tokens:
        print(f"{token.type.value:15} {token.value:15} Line: {token.line:2} Col: {token.column:2}")
