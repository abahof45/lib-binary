"""
Virtual Machine for lib-binary programming language
Executes bytecode instructions with stack-based execution model
"""

import sys
from typing import Dict, List, Any, Optional, Callable
from bytecode import *


class VMError(Exception):
    """Virtual machine runtime error"""
    def __init__(self, message: str, instruction_index: int = -1):
        self.message = message
        self.instruction_index = instruction_index
        super().__init__(f"VM Error at instruction {instruction_index}: {message}")


class MemoryManager:
    """Simple memory manager for heap simulation"""
    
    def __init__(self, heap_size: int = 1024 * 1024):  # 1MB default
        self.heap_size = heap_size
        self.heap = [0] * heap_size
        self.allocated_blocks = {}  # pointer -> size
        self.next_pointer = 0
    
    def alloc(self, size: int) -> int:
        """Allocate memory block"""
        if size <= 0:
            return 0
        
        # Simple linear allocation
        if self.next_pointer + size > self.heap_size:
            raise VMError("Out of memory")
        
        pointer = self.next_pointer
        self.allocated_blocks[pointer] = size
        self.next_pointer += size
        
        return pointer
    
    def free(self, pointer: int):
        """Free memory block"""
        if pointer in self.allocated_blocks:
            del self.allocated_blocks[pointer]
            # Note: This simple implementation doesn't actually free the space
            # In a real implementation, you'd need a proper memory allocator
    
    def store(self, pointer: int, value: Any):
        """Store value at pointer"""
        if pointer < 0 or pointer >= self.heap_size:
            raise VMError(f"Invalid pointer: {pointer}")
        
        self.heap[pointer] = value
    
    def load(self, pointer: int) -> Any:
        """Load value from pointer"""
        if pointer < 0 or pointer >= self.heap_size:
            raise VMError(f"Invalid pointer: {pointer}")
        
        return self.heap[pointer]


class VirtualMachine:
    """Virtual machine for executing bytecode"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.stack: List[Any] = []
        self.call_stack: List[tuple] = []  # (function_name, instruction_index, base_pointer)
        self.variables: Dict[str, Any] = {}
        self.memory = MemoryManager()
        self.module: Optional[BytecodeModule] = None
        self.current_function: Optional[BytecodeFunction] = None
        self.instruction_index: int = 0
        self.base_pointer: int = 0
        
        # Standard library functions
        self.stdlib: Dict[str, Callable] = {
            'print': self._std_print,
            'input': self._std_input,
            'len': self._std_len,
            'range': self._std_range,
        }
    
    def load_module(self, module: BytecodeModule):
        """Load bytecode module"""
        self.module = module
        self.variables.clear()
        self.stack.clear()
        self.call_stack.clear()
    
    def run(self, entry_point: Optional[str] = None) -> Any:
        """Run the loaded module"""
        if not self.module:
            raise VMError("No module loaded")
        
        # Determine entry point
        if entry_point is None:
            entry_point = self.module.entry_point
        
        if entry_point is None:
            entry_point = "main"  # Default to main
        
        if entry_point not in self.module.functions:
            raise VMError(f"Entry point '{entry_point}' not found")
        
        # Start execution
        self.call_function(entry_point, [])
        return self.execute()
    
    def call_function(self, func_name: str, args: List[Any]):
        """Call a function"""
        if func_name not in self.module.functions:
            raise VMError(f"Function '{func_name}' not found")
        
        func = self.module.functions[func_name]
        
        # Check argument count
        if len(args) != len(func.params):
            raise VMError(f"Function '{func_name}' expects {len(func.params)} arguments, got {len(args)}")
        
        # Save current state
        if self.current_function:
            self.call_stack.append((self.current_function.name, self.instruction_index, self.base_pointer))
        
        # Set up new function state
        self.current_function = func
        self.instruction_index = 0
        self.base_pointer = len(self.stack)
        
        # Push arguments onto stack
        for arg in args:
            self.stack.append(arg)
        
        # Initialize local variables
        for i in range(func.locals_count):
            self.stack.append(0)  # Default value
    
    def execute(self) -> Any:
        """Execute the current function"""
        if not self.current_function:
            raise VMError("No function to execute")
        
        while self.instruction_index < len(self.current_function.instructions):
            instr = self.current_function.instructions[self.instruction_index]
            
            if self.debug:
                print(f"Executing: {instr} (stack: {self.stack[-5:] if len(self.stack) > 5 else self.stack})")
            
            try:
                self.execute_instruction(instr)
            except VMError as e:
                e.instruction_index = self.instruction_index
                raise e
            
            self.instruction_index += 1
        
        # Function finished
        result = self.stack.pop() if self.stack else None
        
        # Restore previous state
        if self.call_stack:
            func_name, instr_index, base_pointer = self.call_stack.pop()
            self.current_function = self.module.functions[func_name]
            self.instruction_index = instr_index
            self.base_pointer = base_pointer
        else:
            self.current_function = None
        
        return result
    
    def execute_instruction(self, instr: BytecodeInstruction):
        """Execute a single instruction"""
        opcode = instr.opcode
        
        if opcode == BytecodeOpcode.LABEL:
            # Labels are handled by jumps, no action needed
            pass
        
        elif opcode == BytecodeOpcode.JUMP:
            if len(instr.operands) > 0:
                target = instr.operands[0]
                if isinstance(target, int):
                    self.instruction_index = target - 1  # -1 because we increment after execution
        
        elif opcode == BytecodeOpcode.JUMP_IF_TRUE:
            if len(instr.operands) > 1:
                condition = self.stack.pop()
                target = instr.operands[0]
                if condition and isinstance(target, int):
                    self.instruction_index = target - 1
        
        elif opcode == BytecodeOpcode.JUMP_IF_FALSE:
            if len(instr.operands) > 1:
                condition = self.stack.pop()
                target = instr.operands[0]
                if not condition and isinstance(target, int):
                    self.instruction_index = target - 1
        
        elif opcode == BytecodeOpcode.CALL:
            if len(instr.operands) >= 1:
                func_name = instr.operands[0]
                
                # Check if it's a standard library function
                if func_name in self.stdlib:
                    # Handle standard library call
                    arg_count = len(instr.operands) - 1 if len(instr.operands) > 1 else 0
                    args = []
                    for _ in range(arg_count):
                        args.append(self.stack.pop())
                    args.reverse()  # Reverse to get correct order
                    
                    result = self.stdlib[func_name](*args)
                    if result is not None:
                        self.stack.append(result)
                else:
                    # Handle user-defined function call
                    arg_count = len(instr.operands) - 1 if len(instr.operands) > 1 else 0
                    args = []
                    for _ in range(arg_count):
                        args.append(self.stack.pop())
                    args.reverse()
                    
                    # Save current state and call function
                    old_func = self.current_function
                    old_index = self.instruction_index
                    old_base = self.base_pointer
                    
                    self.call_function(func_name, args)
                    result = self.execute()
                    
                    # Restore state
                    self.current_function = old_func
                    self.instruction_index = old_index
                    self.base_pointer = old_base
                    
                    if result is not None:
                        self.stack.append(result)
        
        elif opcode == BytecodeOpcode.RETURN:
            if instr.operands:
                # Return value is already on stack
                pass
            else:
                # No return value, push None
                self.stack.append(None)
            
            # Jump to end of function
            self.instruction_index = len(self.current_function.instructions) - 1
        
        elif opcode == BytecodeOpcode.PUSH:
            if len(instr.operands) > 0:
                value = instr.operands[0]
                self.stack.append(value)
        
        elif opcode == BytecodeOpcode.POP:
            if self.stack:
                self.stack.pop()
        
        elif opcode == BytecodeOpcode.DUP:
            if self.stack:
                self.stack.append(self.stack[-1])
        
        elif opcode == BytecodeOpcode.LOAD_CONST:
            if len(instr.operands) > 0:
                const_idx = instr.operands[0]
                if isinstance(const_idx, int) and const_idx < len(self.module.constants):
                    self.stack.append(self.module.constants[const_idx])
                else:
                    raise VMError(f"Invalid constant index: {const_idx}")
        
        elif opcode == BytecodeOpcode.LOAD_VAR:
            if len(instr.operands) > 0:
                var_name = instr.operands[0]
                if isinstance(var_name, str) and var_name in self.variables:
                    self.stack.append(self.variables[var_name])
                else:
                    raise VMError(f"Undefined variable: {var_name}")
        
        elif opcode == BytecodeOpcode.STORE_VAR:
            if len(instr.operands) >= 2:
                var_name = instr.operands[0]
                value = instr.operands[1] if isinstance(instr.operands[1], Any) else self.stack.pop()
                self.variables[var_name] = value
        
        elif opcode == BytecodeOpcode.ALLOC:
            if len(instr.operands) > 0:
                size = instr.operands[0] if isinstance(instr.operands[0], int) else self.stack.pop()
                pointer = self.memory.alloc(size)
                self.stack.append(pointer)
        
        elif opcode == BytecodeOpcode.FREE:
            if len(instr.operands) > 0:
                pointer = instr.operands[0] if isinstance(instr.operands[0], int) else self.stack.pop()
                self.memory.free(pointer)
        
        elif opcode == BytecodeOpcode.LOAD_PTR:
            if len(instr.operands) > 0:
                pointer = instr.operands[0] if isinstance(instr.operands[0], int) else self.stack.pop()
                value = self.memory.load(pointer)
                self.stack.append(value)
        
        elif opcode == BytecodeOpcode.STORE_PTR:
            if len(instr.operands) >= 2:
                pointer = instr.operands[0] if isinstance(instr.operands[0], int) else self.stack.pop()
                value = instr.operands[1] if isinstance(instr.operands[1], Any) else self.stack.pop()
                self.memory.store(pointer, value)
        
        # Arithmetic operations
        elif opcode == BytecodeOpcode.ADD:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
        
        elif opcode == BytecodeOpcode.SUB:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
        
        elif opcode == BytecodeOpcode.MUL:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
        
        elif opcode == BytecodeOpcode.DIV:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise VMError("Division by zero")
                self.stack.append(a / b)
        
        elif opcode == BytecodeOpcode.MOD:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise VMError("Modulo by zero")
                self.stack.append(a % b)
        
        elif opcode == BytecodeOpcode.NEG:
            if len(self.stack) >= 1:
                a = self.stack.pop()
                self.stack.append(-a)
        
        # Bitwise operations
        elif opcode == BytecodeOpcode.BIT_AND:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a & b)
        
        elif opcode == BytecodeOpcode.BIT_OR:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a | b)
        
        elif opcode == BytecodeOpcode.BIT_XOR:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a ^ b)
        
        elif opcode == BytecodeOpcode.BIT_LEFT_SHIFT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a << b)
        
        elif opcode == BytecodeOpcode.BIT_RIGHT_SHIFT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >> b)
        
        # Comparison operations
        elif opcode == BytecodeOpcode.EQ:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
        
        elif opcode == BytecodeOpcode.NEQ:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)
        
        elif opcode == BytecodeOpcode.LT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
        
        elif opcode == BytecodeOpcode.GT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
        
        elif opcode == BytecodeOpcode.LTE:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)
        
        elif opcode == BytecodeOpcode.GTE:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)
        
        # Logical operations
        elif opcode == BytecodeOpcode.AND:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a and b)
        
        elif opcode == BytecodeOpcode.OR:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a or b)
        
        elif opcode == BytecodeOpcode.NOT:
            if len(self.stack) >= 1:
                a = self.stack.pop()
                self.stack.append(not a)
        
        # Standard library calls (handled in CALL)
        elif opcode in [BytecodeOpcode.PRINT, BytecodeOpcode.INPUT, BytecodeOpcode.LEN, BytecodeOpcode.RANGE]:
            # These should be handled by the CALL instruction
            pass
        
        # Type operations
        elif opcode == BytecodeOpcode.CAST_INT:
            if len(self.stack) >= 1:
                a = self.stack.pop()
                self.stack.append(int(a))
        
        elif opcode == BytecodeOpcode.CAST_FLOAT:
            if len(self.stack) >= 1:
                a = self.stack.pop()
                self.stack.append(float(a))
        
        elif opcode == BytecodeOpcode.CAST_STR:
            if len(self.stack) >= 1:
                a = self.stack.pop()
                self.stack.append(str(a))
        
        else:
            raise VMError(f"Unknown opcode: {opcode}")
    
    def _std_print(self, *args):
        """Standard library print function"""
        if len(args) == 1:
            print(args[0])
        else:
            print(*args)
        return None
    
    def _std_input(self, prompt: str = "") -> str:
        """Standard library input function"""
        return input(prompt)
    
    def _std_len(self, obj) -> int:
        """Standard library len function"""
        return len(obj)
    
    def _std_range(self, start: int, end: int) -> List[int]:
        """Standard library range function"""
        return list(range(start, end))


def run_bytecode(module: BytecodeModule, debug: bool = False) -> Any:
    """Convenience function to run bytecode module"""
    vm = VirtualMachine(debug)
    vm.load_module(module)
    return vm.run()


if __name__ == "__main__":
    # Test VM with a simple module
    from ir_to_bytecode import convert_ir_to_bytecode
    from ast_to_ir import convert_ast_to_ir
    from parser import parse_source
    
    test_code = """
func main():
    x = 10
    y = 20
    result = x + y
    print(result)
    return result
"""
    
    try:
        # Parse and compile
        ast = parse_source(test_code)
        ir_module = convert_ast_to_ir(ast)
        bytecode_module = convert_ir_to_bytecode(ir_module)
        
        print("Running bytecode...")
        result = run_bytecode(bytecode_module, debug=True)
        print(f"Program finished with result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
