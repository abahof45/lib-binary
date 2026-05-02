"""
AST to IR converter for lib-binary programming language
Converts AST nodes to IR instructions
"""

from typing import Dict, List, Optional
from parser import *
from ir import *


class ASTToIRConverter:
    """Converts AST to IR"""
    
    def __init__(self):
        self.builder = IRBuilder()
        self.current_function: Optional[str] = None
        self.symbol_tables: Dict[str, Dict[str, str]] = {}  # function -> variable -> temp
        self.loop_stack: List[tuple] = []  # (continue_label, break_label)
    
    def convert(self, ast: Program) -> IRModule:
        """Convert AST program to IR module"""
        # Convert all functions
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDef):
                self.convert_function(stmt)
            elif isinstance(stmt, StructDef):
                self.convert_struct(stmt)
        
        return self.builder.build_module()
    
    def convert_function(self, func: FunctionDef):
        """Convert a function definition to IR"""
        self.current_function = func.name
        self.symbol_tables[func.name] = {}
        
        # Start function
        self.builder.start_function(func.name, func.params, func.return_type)
        
        # Add parameters to symbol table
        for param in func.params:
            self.symbol_tables[func.name][param] = param
        
        # Convert function body
        for stmt in func.body:
            self.convert_statement(stmt)
        
        # Add implicit return if none exists
        if not func.body or not any(isinstance(s, ReturnStatement) for s in func.body):
            self.builder.emit_return()
        
        # End function
        self.builder.end_function()
        self.current_function = None
    
    def convert_struct(self, struct: StructDef):
        """Convert a struct definition to IR"""
        self.builder.add_struct(struct.name, struct.fields)
    
    def convert_statement(self, stmt: ASTNode):
        """Convert a statement to IR"""
        if isinstance(stmt, VariableDecl):
            self.convert_variable_decl(stmt)
        elif isinstance(stmt, Assignment):
            self.convert_assignment(stmt)
        elif isinstance(stmt, FunctionCall):
            self.convert_function_call(stmt)
        elif isinstance(stmt, IfStatement):
            self.convert_if_statement(stmt)
        elif isinstance(stmt, WhileStatement):
            self.convert_while_statement(stmt)
        elif isinstance(stmt, ForStatement):
            self.convert_for_statement(stmt)
        elif isinstance(stmt, ReturnStatement):
            self.convert_return_statement(stmt)
        elif isinstance(stmt, LowBlock):
            self.convert_low_block(stmt)
        elif isinstance(stmt, MemoryOp):
            self.convert_memory_op(stmt)
        else:
            # Expression statement
            result = self.convert_expression(stmt)
            if result:
                # Result is computed but not used (side effects only)
                pass
    
    def convert_variable_decl(self, var_decl: VariableDecl):
        """Convert variable declaration to IR"""
        var_name = var_decl.name
        
        if var_decl.value:
            # Variable with initialization
            value_temp = self.convert_expression(var_decl.value)
            self.symbol_tables[self.current_function][var_name] = value_temp
            self.builder.emit_store_var(var_name, value_temp)
        else:
            # Variable without initialization
            temp = self.builder.new_temp()
            self.symbol_tables[self.current_function][var_name] = temp
            # Initialize with default value
            self.builder.emit_load_const(0, temp)
            self.builder.emit_store_var(var_name, temp)
    
    def convert_assignment(self, assignment: Assignment):
        """Convert assignment to IR"""
        value_temp = self.convert_expression(assignment.value)
        
        # Store to variable
        self.builder.emit_store_var(assignment.target, value_temp)
        
        # Update symbol table
        self.symbol_tables[self.current_function][assignment.target] = value_temp
    
    def convert_function_call(self, call: FunctionCall, result_var: Optional[str] = None) -> Optional[str]:
        """Convert function call to IR"""
        # Convert arguments
        arg_temps = []
        for arg in call.args:
            arg_temp = self.convert_expression(arg)
            arg_temps.append(arg_temp)
        
        # Generate result variable if not provided
        if result_var is None:
            result_var = self.builder.new_temp()
        
        # Emit call
        if call.name in ["print", "input", "len", "range"]:
            # Standard library function
            if call.name == "print":
                self.builder.emit_print(arg_temps[0])
                return None
            elif call.name == "input":
                self.builder.emit_input(result_var)
            elif call.name == "len":
                self.builder.emit_len(arg_temps[0], result_var)
            elif call.name == "range":
                self.builder.emit_range(arg_temps[0], arg_temps[1], result_var)
        else:
            # User-defined function
            self.builder.emit_call(call.name, arg_temps, result_var)
        
        return result_var
    
    def convert_if_statement(self, if_stmt: IfStatement):
        """Convert if statement to IR"""
        # Convert condition
        cond_temp = self.convert_expression(if_stmt.condition)
        
        # Create labels
        else_label = self.builder.new_label()
        end_label = self.builder.new_label()
        
        # Jump to else if condition is false
        self.builder.emit_jump_if_false(cond_temp, else_label)
        
        # Convert then body
        for stmt in if_stmt.then_body:
            self.convert_statement(stmt)
        
        # Jump to end if there's an else block
        if if_stmt.else_body:
            self.builder.emit_jump(end_label)
        
        # Else label
        self.builder.emit_label(else_label)
        
        # Convert else body if present
        if if_stmt.else_body:
            for stmt in if_stmt.else_body:
                self.convert_statement(stmt)
        
        # End label
        if if_stmt.else_body:
            self.builder.emit_label(end_label)
        else:
            self.builder.emit_label(else_label)
    
    def convert_while_statement(self, while_stmt: WhileStatement):
        """Convert while statement to IR"""
        # Create labels
        start_label = self.builder.new_label()
        end_label = self.builder.new_label()
        
        # Add to loop stack
        self.loop_stack.append((start_label, end_label))
        
        # Start label
        self.builder.emit_label(start_label)
        
        # Convert condition
        cond_temp = self.convert_expression(while_stmt.condition)
        
        # Jump to end if condition is false
        self.builder.emit_jump_if_false(cond_temp, end_label)
        
        # Convert body
        for stmt in while_stmt.body:
            self.convert_statement(stmt)
        
        # Jump back to start
        self.builder.emit_jump(start_label)
        
        # End label
        self.builder.emit_label(end_label)
        
        # Remove from loop stack
        self.loop_stack.pop()
    
    def convert_for_statement(self, for_stmt: ForStatement):
        """Convert for statement to IR"""
        # Convert iterable (should be range)
        iterable_temp = self.convert_expression(for_stmt.iterable)
        
        # Create labels
        start_label = self.builder.new_label()
        end_label = self.builder.new_label()
        
        # Add to loop stack
        self.loop_stack.append((start_label, end_label))
        
        # Create iterator variable
        iterator_temp = self.builder.new_temp()
        self.builder.emit_load_const(0, iterator_temp)
        
        # Store loop variable
        self.symbol_tables[self.current_function][for_stmt.var] = iterator_temp
        self.builder.emit_store_var(for_stmt.var, iterator_temp)
        
        # Start label
        self.builder.emit_label(start_label)
        
        # Check condition (iterator < end)
        end_temp = self.builder.new_temp()
        self.builder.emit_load_var(for_stmt.var, end_temp)
        
        # Get range end (assuming range(start, end))
        # For simplicity, we'll use a basic approach
        cond_temp = self.builder.new_temp()
        self.builder.emit_lt(iterator_temp, iterable_temp, cond_temp)
        
        # Jump to end if condition is false
        self.builder.emit_jump_if_false(cond_temp, end_label)
        
        # Convert body
        for stmt in for_stmt.body:
            self.convert_statement(stmt)
        
        # Increment iterator
        inc_temp = self.builder.new_temp()
        self.builder.emit_load_const(1, inc_temp)
        self.builder.emit_add(iterator_temp, inc_temp, iterator_temp)
        self.builder.emit_store_var(for_stmt.var, iterator_temp)
        
        # Jump back to start
        self.builder.emit_jump(start_label)
        
        # End label
        self.builder.emit_label(end_label)
        
        # Remove from loop stack
        self.loop_stack.pop()
    
    def convert_return_statement(self, return_stmt: ReturnStatement):
        """Convert return statement to IR"""
        if return_stmt.value:
            value_temp = self.convert_expression(return_stmt.value)
            self.builder.emit_return(value_temp)
        else:
            self.builder.emit_return()
    
    def convert_low_block(self, low_block: LowBlock):
        """Convert low-level block to IR"""
        for stmt in low_block.statements:
            self.convert_statement(stmt)
    
    def convert_memory_op(self, mem_op: MemoryOp):
        """Convert memory operation to IR"""
        if mem_op.op == "alloc":
            size_temp = self.convert_expression(mem_op.args[0])
            result_temp = self.builder.new_temp()
            self.builder.emit_alloc(size_temp, result_temp)
            return result_temp
        elif mem_op.op == "free":
            ptr_temp = self.convert_expression(mem_op.args[0])
            self.builder.emit_free(ptr_temp)
        elif mem_op.op == "store":
            ptr_temp = self.convert_expression(mem_op.args[0])
            value_temp = self.convert_expression(mem_op.args[1])
            self.builder.emit_store_ptr(ptr_temp, value_temp)
        elif mem_op.op == "load":
            ptr_temp = self.convert_expression(mem_op.args[0])
            result_temp = self.builder.new_temp()
            self.builder.emit_load_ptr(ptr_temp, result_temp)
            return result_temp
    
    def convert_expression(self, expr: ASTNode) -> str:
        """Convert expression to IR and return temporary variable"""
        if isinstance(expr, Literal):
            temp = self.builder.new_temp()
            self.builder.emit_load_const(expr.value, temp)
            return temp
        
        elif isinstance(expr, Identifier):
            # Check if variable exists in symbol table
            if expr.name in self.symbol_tables[self.current_function]:
                var_temp = self.symbol_tables[self.current_function][expr.name]
                # Load variable into new temp
                temp = self.builder.new_temp()
                self.builder.emit_load_var(expr.name, temp)
                return temp
            else:
                # Undefined variable, treat as error
                raise ValueError(f"Undefined variable: {expr.name}")
        
        elif isinstance(expr, BinaryOp):
            left_temp = self.convert_expression(expr.left)
            right_temp = self.convert_expression(expr.right)
            result_temp = self.builder.new_temp()
            
            # Emit appropriate operation
            if expr.op == "+":
                self.builder.emit_add(left_temp, right_temp, result_temp)
            elif expr.op == "-":
                self.builder.emit_sub(left_temp, right_temp, result_temp)
            elif expr.op == "*":
                self.builder.emit_mul(left_temp, right_temp, result_temp)
            elif expr.op == "/":
                self.builder.emit_div(left_temp, right_temp, result_temp)
            elif expr.op == "%":
                self.builder.emit_mod(left_temp, right_temp, result_temp)
            elif expr.op == "&":
                self.builder.emit_bit_and(left_temp, right_temp, result_temp)
            elif expr.op == "|":
                self.builder.emit_bit_or(left_temp, right_temp, result_temp)
            elif expr.op == "^":
                self.builder.emit_bit_xor(left_temp, right_temp, result_temp)
            elif expr.op == "<<":
                self.builder.emit_bit_left_shift(left_temp, right_temp, result_temp)
            elif expr.op == ">>":
                self.builder.emit_bit_right_shift(left_temp, right_temp, result_temp)
            elif expr.op == "==":
                self.builder.emit_eq(left_temp, right_temp, result_temp)
            elif expr.op == "!=":
                self.builder.emit_neq(left_temp, right_temp, result_temp)
            elif expr.op == "<":
                self.builder.emit_lt(left_temp, right_temp, result_temp)
            elif expr.op == ">":
                self.builder.emit_gt(left_temp, right_temp, result_temp)
            elif expr.op == "<=":
                self.builder.emit_lte(left_temp, right_temp, result_temp)
            elif expr.op == ">=":
                self.builder.emit_gte(left_temp, right_temp, result_temp)
            elif expr.op == "and":
                self.builder.emit_and(left_temp, right_temp, result_temp)
            elif expr.op == "or":
                self.builder.emit_or(left_temp, right_temp, result_temp)
            else:
                raise ValueError(f"Unsupported binary operator: {expr.op}")
            
            return result_temp
        
        elif isinstance(expr, UnaryOp):
            operand_temp = self.convert_expression(expr.operand)
            result_temp = self.builder.new_temp()
            
            if expr.op == "-":
                self.builder.emit_neg(operand_temp, result_temp)
            elif expr.op == "!":
                self.builder.emit_not(operand_temp, result_temp)
            else:
                raise ValueError(f"Unsupported unary operator: {expr.op}")
            
            return result_temp
        
        elif isinstance(expr, FunctionCall):
            return self.convert_function_call(expr)
        
        else:
            raise ValueError(f"Unsupported expression type: {type(expr)}")


def convert_ast_to_ir(ast: Program) -> IRModule:
    """Convenience function to convert AST to IR"""
    converter = ASTToIRConverter()
    return converter.convert(ast)


if __name__ == "__main__":
    # Test the converter
    from parser import parse_source
    
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
        ir_module = convert_ast_to_ir(ast)
        
        print("IR generated successfully:")
        from ir import print_ir
        print_ir(ir_module)
        
    except Exception as e:
        print(f"Error: {e}")
