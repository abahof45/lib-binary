"""
Parser for lib-binary programming language
Builds AST from tokens produced by the lexer
"""

from typing import List, Optional, Union, Any
from abc import ABC, abstractmethod
from lexer import Token, TokenType, tokenize_source


class ASTNode(ABC):
    """Base class for all AST nodes"""
    pass


class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


class FunctionDef(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode], return_type: Optional[str] = None):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type
    
    def __repr__(self):
        return f"FunctionDef({self.name}, params={self.params})"


class StructDef(ASTNode):
    def __init__(self, name: str, fields: List[tuple]):
        self.name = name
        self.fields = fields  # List of (name, type) tuples
    
    def __repr__(self):
        return f"StructDef({self.name}, fields={self.fields})"


class LowBlock(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements
    
    def __repr__(self):
        return f"LowBlock({len(self.statements)} statements)"


class VariableDecl(ASTNode):
    def __init__(self, name: str, var_type: Optional[str], value: Optional[ASTNode]):
        self.name = name
        self.var_type = var_type
        self.value = value
    
    def __repr__(self):
        return f"VariableDecl({self.name}, type={self.var_type})"


class Assignment(ASTNode):
    def __init__(self, target: str, value: ASTNode, op: str = "="):
        self.target = target
        self.value = value
        self.op = op
    
    def __repr__(self):
        return f"Assignment({self.target} {self.op} {self.value})"


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"


class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.op}{self.operand})"


class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"FunctionCall({self.name}, args={len(self.args)})"


class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    
    def __repr__(self):
        return f"IfStatement(condition={self.condition})"


class WhileStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStatement(condition={self.condition})"


class ForStatement(ASTNode):
    def __init__(self, var: str, iterable: ASTNode, body: List[ASTNode]):
        self.var = var
        self.iterable = iterable
        self.body = body
    
    def __repr__(self):
        return f"ForStatement({self.var} in {self.iterable})"


class ReturnStatement(ASTNode):
    def __init__(self, value: Optional[ASTNode] = None):
        self.value = value
    
    def __repr__(self):
        return f"ReturnStatement({self.value})"


class Literal(ASTNode):
    def __init__(self, value: Any):
        self.value = value
    
    def __repr__(self):
        return f"Literal({self.value})"


class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"


class MemoryOp(ASTNode):
    def __init__(self, op: str, args: List[ASTNode]):
        self.op = op  # alloc, free, store, load
        self.args = args
    
    def __repr__(self):
        return f"MemoryOp({self.op}, args={self.args})"


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse error at line {token.line}, column {token.column}: {message}")


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        raise ParseError(f"Expected {token_type.value}, got {self.current_token.type.value if self.current_token else 'EOF'}", 
                        self.current_token or Token(TokenType.EOF, "", 0, 0))
    
    def skip_newlines(self):
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse_program(self) -> Program:
        statements = []
        self.skip_newlines()
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        if not self.current_token:
            return None
        
        # Skip newlines and indents (these are handled at block level)
        if self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT]:
            self.advance()
            return None
        
        # Function definition
        if self.current_token.type == TokenType.FUNC:
            return self.parse_function_def()
        
        # Struct definition
        elif self.current_token.type == TokenType.STRUCT:
            return self.parse_struct_def()
        
        # Low block
        elif self.current_token.type == TokenType.LOW:
            return self.parse_low_block()
        
        # If statement
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        
        # While statement
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        
        # For statement
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for_statement()
        
        # Return statement
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        
        # Variable declaration or assignment
        else:
            return self.parse_variable_or_assignment()
    
    def parse_function_def(self) -> FunctionDef:
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENTIFIER).value
        
        # Parameters
        self.expect(TokenType.LPAREN)
        params = []
        if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        
        # Return type (optional) - check if we have a type after colon
        return_type = None
        if self.current_token and self.current_token.type == TokenType.COLON:
            # Look ahead to see if next token is a type
            if (self.peek() and self.peek().type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR, TokenType.STR]):
                # This is a return type declaration
                self.advance()  # Consume the colon
                return_type = self.expect(TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR, TokenType.STR).value
                # Now expect colon for function body
                self.expect(TokenType.COLON)
            else:
                # This is the function body colon
                return_type = None
                # The current token is already the function body colon
                self.advance()  # Consume the colon
        else:
            # No colon found, this is an error
            self.expect(TokenType.COLON)
        
        # Function body
        body = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        return FunctionDef(name, params, body, return_type)
    
    def parse_struct_def(self) -> StructDef:
        self.expect(TokenType.STRUCT)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COLON)
        
        fields = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
            field_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            
            # Field type
            if self.current_token and self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR, TokenType.STR]:
                field_type = self.current_token.value
                self.advance()
            else:
                field_type = "auto"  # Default to auto
            
            fields.append((field_name, field_type))
            
            if self.current_token and self.current_token.type == TokenType.NEWLINE:
                self.advance()
        
        return StructDef(name, fields)
    
    def parse_low_block(self) -> LowBlock:
        self.expect(TokenType.LOW)
        self.expect(TokenType.COLON)
        
        statements = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
            stmt = self.parse_low_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return LowBlock(statements)
    
    def parse_low_statement(self) -> ASTNode:
        # Memory operations
        if self.current_token and self.current_token.type in [TokenType.ALLOC, TokenType.FREE, TokenType.STORE, TokenType.LOAD]:
            op = self.current_token.value
            self.advance()
            
            args = []
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                self.advance()
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token and self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
            
            return MemoryOp(op, args)
        
        # Variable declaration with type
        elif (self.current_token and self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR] and
              self.peek() and self.peek().type == TokenType.IDENTIFIER):
            var_type = self.current_token.value
            self.advance()
            name = self.expect(TokenType.IDENTIFIER).value
            
            value = None
            if self.current_token and self.current_token.type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
            
            return VariableDecl(name, var_type, value)
        
        # Regular statement
        else:
            return self.parse_variable_or_assignment()
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        
        # Then body
        then_body = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.ELSE, TokenType.EOF]):
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
            self.skip_newlines()
        
        # Else body (optional)
        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            if self.current_token and self.current_token.type == TokenType.COLON:
                self.advance()
                else_body = []
                self.skip_newlines()
                
                while (self.current_token and 
                       self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                    self.skip_newlines()
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        
        body = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        return WhileStatement(condition, body)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        var = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IDENTIFIER)  # 'in' keyword (treated as identifier for now)
        iterable = self.parse_expression()
        self.expect(TokenType.COLON)
        
        body = []
        self.skip_newlines()
        
        while (self.current_token and 
               self.current_token.type not in [TokenType.DEDENT, TokenType.EOF]):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        return ForStatement(var, iterable, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        value = None
        if self.current_token and self.current_token.type not in [TokenType.NEWLINE, TokenType.EOF]:
            value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_variable_or_assignment(self) -> ASTNode:
        # Check if this is a type declaration
        if (self.current_token and self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.PTR, TokenType.STR] and
            self.peek() and self.peek().type == TokenType.IDENTIFIER):
            var_type = self.current_token.value
            self.advance()
            name = self.expect(TokenType.IDENTIFIER).value
            
            value = None
            if self.current_token and self.current_token.type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN]:
                op = self.current_token.value
                self.advance()
                value = self.parse_expression()
                return Assignment(name, value, op)
            
            return VariableDecl(name, var_type, value)
        
        # Check if this is an assignment
        elif (self.current_token and self.current_token.type == TokenType.IDENTIFIER and
              self.peek() and self.peek().type in [TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN]):
            name = self.current_token.value
            self.advance()
            op = self.current_token.value
            self.advance()
            value = self.parse_expression()
            return Assignment(name, value, op)
        
        # Otherwise, it's an expression statement (function call, etc.)
        else:
            return self.parse_expression()
    
    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "or":
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, "or", right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "and":
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, "and", right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.current_token and self.current_token.type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            op = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_bitwise_shift()
        
        while self.current_token and self.current_token.type in [TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]:
            op = self.current_token.value
            self.advance()
            right = self.parse_bitwise_shift()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_shift(self) -> ASTNode:
        left = self.parse_bitwise_and()
        
        while self.current_token and self.current_token.type in [TokenType.BIT_LEFT_SHIFT, TokenType.BIT_RIGHT_SHIFT]:
            op = self.current_token.value
            self.advance()
            right = self.parse_bitwise_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_and(self) -> ASTNode:
        left = self.parse_bitwise_xor()
        
        while self.current_token and self.current_token.type == TokenType.BIT_AND:
            op = self.current_token.value
            self.advance()
            right = self.parse_bitwise_xor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_xor(self) -> ASTNode:
        left = self.parse_bitwise_or()
        
        while self.current_token and self.current_token.type == TokenType.BIT_XOR:
            op = self.current_token.value
            self.advance()
            right = self.parse_bitwise_or()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_or(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.current_token and self.current_token.type == TokenType.BIT_OR:
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token and self.current_token.type in [TokenType.MINUS, TokenType.NOT_EQUAL]:
            op = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        if not self.current_token:
            raise ParseError("Unexpected end of input", Token(TokenType.EOF, "", 0, 0))
        
        # Literals
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.value) if '.' in self.current_token.value else int(self.current_token.value)
            token = self.current_token
            self.advance()
            return Literal(value)
        
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value[1:-1]  # Remove quotes
            token = self.current_token
            self.advance()
            return Literal(value)
        
        # Identifiers and function calls
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            # Function call
            if self.current_token and self.current_token.type == TokenType.LPAREN:
                self.advance()
                args = []
                if self.current_token and self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token and self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return FunctionCall(name, args)
            
            # Simple identifier
            return Identifier(name)
        
        # Parenthesized expression
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            raise ParseError(f"Unexpected token: {self.current_token.type.value}", self.current_token)


def parse_source(source: str) -> Program:
    """Convenience function to parse source code"""
    tokens = tokenize_source(source)
    parser = Parser(tokens)
    return parser.parse_program()


if __name__ == "__main__":
    # Test the parser
    test_code = """
func main():
    x = 10
    y = 20
    print(x + y)
    
    low:
        ptr a = alloc(10)
        store(a, 5)
"""
    
    try:
        ast = parse_source(test_code)
        print("AST parsed successfully:")
        print(ast)
        
        # Print detailed AST
        def print_ast(node, indent=0):
            prefix = "  " * indent
            print(f"{prefix}{repr(node)}")
            if hasattr(node, 'statements'):
                for stmt in node.statements:
                    print_ast(stmt, indent + 1)
            elif hasattr(node, 'body'):
                for stmt in node.body:
                    print_ast(stmt, indent + 1)
        
        print_ast(ast)
        
    except ParseError as e:
        print(f"Parse error: {e}")
