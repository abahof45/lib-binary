"""
Intermediate Representation (IR) for lib-binary programming language
IR is a low-level, platform-independent representation that sits between AST and bytecode
"""

from enum import Enum
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass
import uuid


class IRInstructionType(Enum):
    # Control flow
    LABEL = "LABEL"
    JUMP = "JUMP"
    JUMP_IF_TRUE = "JUMP_IF_TRUE"
    JUMP_IF_FALSE = "JUMP_IF_FALSE"
    CALL = "CALL"
    RETURN = "RETURN"
    
    # Stack operations
    PUSH = "PUSH"
    POP = "POP"
    DUP = "DUP"
    
    # Memory operations
    LOAD_CONST = "LOAD_CONST"
    LOAD_VAR = "LOAD_VAR"
    STORE_VAR = "STORE_VAR"
    ALLOC = "ALLOC"
    FREE = "FREE"
    LOAD_PTR = "LOAD_PTR"
    STORE_PTR = "STORE_PTR"
    
    # Arithmetic operations
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    NEG = "NEG"
    
    # Bitwise operations
    BIT_AND = "BIT_AND"
    BIT_OR = "BIT_OR"
    BIT_XOR = "BIT_XOR"
    BIT_LEFT_SHIFT = "BIT_LEFT_SHIFT"
    BIT_RIGHT_SHIFT = "BIT_RIGHT_SHIFT"
    
    # Comparison operations
    EQ = "EQ"
    NEQ = "NEQ"
    LT = "LT"
    GT = "GT"
    LTE = "LTE"
    GTE = "GTE"
    
    # Logical operations
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Standard library calls
    PRINT = "PRINT"
    INPUT = "INPUT"
    LEN = "LEN"
    RANGE = "RANGE"
    
    # Type operations
    CAST_INT = "CAST_INT"
    CAST_FLOAT = "CAST_FLOAT"
    CAST_STR = "CAST_STR"


@dataclass
class IRInstruction:
    """Single IR instruction"""
    type: IRInstructionType
    operands: List[Any]
    result: Optional[str] = None
    comment: Optional[str] = None
    
    def __repr__(self):
        if self.result:
            return f"{self.result} = {self.type.value}({', '.join(map(str, self.operands))})"
        else:
            return f"{self.type.value}({', '.join(map(str, self.operands))})"


@dataclass
class IRFunction:
    """IR function definition"""
    name: str
    params: List[str]
    instructions: List[IRInstruction]
    locals: List[str]
    return_type: Optional[str] = None
    
    def __repr__(self):
        return f"IRFunction({self.name}, params={self.params}, {len(self.instructions)} instructions)"


@dataclass
class IRModule:
    """Complete IR module containing all functions and data"""
    functions: Dict[str, IRFunction]
    constants: List[Any]
    strings: List[str]
    structs: Dict[str, List[tuple]]  # struct name -> list of (field_name, field_type)
    
    def __repr__(self):
        return f"IRModule({len(self.functions)} functions, {len(self.constants)} constants)"


class IRBuilder:
    """Builder class for constructing IR"""
    
    def __init__(self):
        self.current_function: Optional[IRFunction] = None
        self.instructions: List[IRInstruction] = []
        self.locals: List[str] = []
        self.label_counter = 0
        self.temp_counter = 0
        self.constants: List[Any] = []
        self.strings: List[str] = []
        self.functions: Dict[str, IRFunction] = {}
        self.structs: Dict[str, List[tuple]] = {}
    
    def new_label(self) -> str:
        """Generate a new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def new_temp(self) -> str:
        """Generate a new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        self.locals.append(temp)
        return temp
    
    def add_constant(self, value: Any) -> int:
        """Add a constant to the constant pool"""
        if value not in self.constants:
            self.constants.append(value)
        return self.constants.index(value)
    
    def add_string(self, value: str) -> int:
        """Add a string to the string pool"""
        if value not in self.strings:
            self.strings.append(value)
        return self.strings.index(value)
    
    def add_instruction(self, instruction: IRInstruction):
        """Add an instruction to the current function"""
        if self.current_function:
            self.current_function.instructions.append(instruction)
        else:
            self.instructions.append(instruction)
    
    def emit_label(self, label: str):
        """Emit a label instruction"""
        self.add_instruction(IRInstruction(IRInstructionType.LABEL, [label]))
    
    def emit_jump(self, label: str):
        """Emit an unconditional jump"""
        self.add_instruction(IRInstruction(IRInstructionType.JUMP, [label]))
    
    def emit_jump_if_true(self, condition: str, label: str):
        """Emit a conditional jump (jump if true)"""
        self.add_instruction(IRInstruction(IRInstructionType.JUMP_IF_TRUE, [condition, label]))
    
    def emit_jump_if_false(self, condition: str, label: str):
        """Emit a conditional jump (jump if false)"""
        self.add_instruction(IRInstruction(IRInstructionType.JUMP_IF_FALSE, [condition, label]))
    
    def emit_call(self, func_name: str, args: List[str], result: Optional[str] = None):
        """Emit a function call"""
        self.add_instruction(IRInstruction(IRInstructionType.CALL, [func_name] + args, result))
    
    def emit_return(self, value: Optional[str] = None):
        """Emit a return instruction"""
        operands = [value] if value else []
        self.add_instruction(IRInstruction(IRInstructionType.RETURN, operands))
    
    def emit_push(self, value: str):
        """Push a value onto the stack"""
        self.add_instruction(IRInstruction(IRInstructionType.PUSH, [value]))
    
    def emit_pop(self, target: Optional[str] = None):
        """Pop a value from the stack"""
        self.add_instruction(IRInstruction(IRInstructionType.POP, [], target))
    
    def emit_load_const(self, value: Any, result: str):
        """Load a constant"""
        const_idx = self.add_constant(value)
        self.add_instruction(IRInstruction(IRInstructionType.LOAD_CONST, [const_idx], result))
    
    def emit_load_var(self, var_name: str, result: str):
        """Load a variable"""
        self.add_instruction(IRInstruction(IRInstructionType.LOAD_VAR, [var_name], result))
    
    def emit_store_var(self, var_name: str, value: str):
        """Store a value to a variable"""
        self.add_instruction(IRInstruction(IRInstructionType.STORE_VAR, [var_name, value]))
    
    def emit_alloc(self, size: str, result: str):
        """Allocate memory"""
        self.add_instruction(IRInstruction(IRInstructionType.ALLOC, [size], result))
    
    def emit_free(self, ptr: str):
        """Free memory"""
        self.add_instruction(IRInstruction(IRInstructionType.FREE, [ptr]))
    
    def emit_load_ptr(self, ptr: str, result: str):
        """Load value from pointer"""
        self.add_instruction(IRInstruction(IRInstructionType.LOAD_PTR, [ptr], result))
    
    def emit_store_ptr(self, ptr: str, value: str):
        """Store value to pointer"""
        self.add_instruction(IRInstruction(IRInstructionType.STORE_PTR, [ptr, value]))
    
    def emit_add(self, left: str, right: str, result: str):
        """Addition"""
        self.add_instruction(IRInstruction(IRInstructionType.ADD, [left, right], result))
    
    def emit_sub(self, left: str, right: str, result: str):
        """Subtraction"""
        self.add_instruction(IRInstruction(IRInstructionType.SUB, [left, right], result))
    
    def emit_mul(self, left: str, right: str, result: str):
        """Multiplication"""
        self.add_instruction(IRInstruction(IRInstructionType.MUL, [left, right], result))
    
    def emit_div(self, left: str, right: str, result: str):
        """Division"""
        self.add_instruction(IRInstruction(IRInstructionType.DIV, [left, right], result))
    
    def emit_mod(self, left: str, right: str, result: str):
        """Modulo"""
        self.add_instruction(IRInstruction(IRInstructionType.MOD, [left, right], result))
    
    def emit_neg(self, operand: str, result: str):
        """Negation"""
        self.add_instruction(IRInstruction(IRInstructionType.NEG, [operand], result))
    
    def emit_bit_and(self, left: str, right: str, result: str):
        """Bitwise AND"""
        self.add_instruction(IRInstruction(IRInstructionType.BIT_AND, [left, right], result))
    
    def emit_bit_or(self, left: str, right: str, result: str):
        """Bitwise OR"""
        self.add_instruction(IRInstruction(IRInstructionType.BIT_OR, [left, right], result))
    
    def emit_bit_xor(self, left: str, right: str, result: str):
        """Bitwise XOR"""
        self.add_instruction(IRInstruction(IRInstructionType.BIT_XOR, [left, right], result))
    
    def emit_bit_left_shift(self, left: str, right: str, result: str):
        """Bitwise left shift"""
        self.add_instruction(IRInstruction(IRInstructionType.BIT_LEFT_SHIFT, [left, right], result))
    
    def emit_bit_right_shift(self, left: str, right: str, result: str):
        """Bitwise right shift"""
        self.add_instruction(IRInstruction(IRInstructionType.BIT_RIGHT_SHIFT, [left, right], result))
    
    def emit_eq(self, left: str, right: str, result: str):
        """Equality comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.EQ, [left, right], result))
    
    def emit_neq(self, left: str, right: str, result: str):
        """Inequality comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.NEQ, [left, right], result))
    
    def emit_lt(self, left: str, right: str, result: str):
        """Less than comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.LT, [left, right], result))
    
    def emit_gt(self, left: str, right: str, result: str):
        """Greater than comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.GT, [left, right], result))
    
    def emit_lte(self, left: str, right: str, result: str):
        """Less than or equal comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.LTE, [left, right], result))
    
    def emit_gte(self, left: str, right: str, result: str):
        """Greater than or equal comparison"""
        self.add_instruction(IRInstruction(IRInstructionType.GTE, [left, right], result))
    
    def emit_and(self, left: str, right: str, result: str):
        """Logical AND"""
        self.add_instruction(IRInstruction(IRInstructionType.AND, [left, right], result))
    
    def emit_or(self, left: str, right: str, result: str):
        """Logical OR"""
        self.add_instruction(IRInstruction(IRInstructionType.OR, [left, right], result))
    
    def emit_not(self, operand: str, result: str):
        """Logical NOT"""
        self.add_instruction(IRInstruction(IRInstructionType.NOT, [operand], result))
    
    def emit_print(self, value: str):
        """Print value"""
        self.add_instruction(IRInstruction(IRInstructionType.PRINT, [value]))
    
    def emit_input(self, result: str):
        """Read input"""
        self.add_instruction(IRInstruction(IRInstructionType.INPUT, [], result))
    
    def emit_len(self, value: str, result: str):
        """Get length"""
        self.add_instruction(IRInstruction(IRInstructionType.LEN, [value], result))
    
    def emit_range(self, start: str, end: str, result: str):
        """Create range"""
        self.add_instruction(IRInstruction(IRInstructionType.RANGE, [start, end], result))
    
    def start_function(self, name: str, params: List[str], return_type: Optional[str] = None):
        """Start defining a new function"""
        self.current_function = IRFunction(name, params, [], list(params), return_type)
        self.locals = list(params)
        self.instructions = []
    
    def end_function(self) -> IRFunction:
        """End current function definition"""
        if self.current_function:
            func = self.current_function
            self.functions[func.name] = func
            self.current_function = None
            return func
        raise ValueError("No function currently being defined")
    
    def add_struct(self, name: str, fields: List[tuple]):
        """Add a struct definition"""
        self.structs[name] = fields
    
    def build_module(self) -> IRModule:
        """Build the complete IR module"""
        return IRModule(
            functions=self.functions,
            constants=self.constants,
            strings=self.strings,
            structs=self.structs
        )


class IROptimizer:
    """Optimizer for IR code"""
    
    def __init__(self, module: IRModule):
        self.module = module
    
    def optimize(self) -> IRModule:
        """Run all optimizations"""
        self.constant_folding()
        self.dead_code_elimination()
        self.constant_propagation()
        return self.module
    
    def constant_folding(self):
        """Fold constant expressions"""
        for func in self.module.functions.values():
            i = 0
            while i < len(func.instructions):
                instr = func.instructions[i]
                
                # Check if this is a binary operation with constant operands
                if (instr.type in [IRInstructionType.ADD, IRInstructionType.SUB, IRInstructionType.MUL, IRInstructionType.DIV] and
                    len(instr.operands) == 2 and
                    all(isinstance(op, int) and op < len(self.module.constants) for op in instr.operands)):
                    
                    const1 = self.module.constants[instr.operands[0]]
                    const2 = self.module.constants[instr.operands[1]]
                    
                    # Compute result
                    if instr.type == IRInstructionType.ADD:
                        result = const1 + const2
                    elif instr.type == IRInstructionType.SUB:
                        result = const1 - const2
                    elif instr.type == IRInstructionType.MUL:
                        result = const1 * const2
                    elif instr.type == IRInstructionType.DIV:
                        if const2 == 0:
                            i += 1
                            continue
                        result = const1 / const2
                    else:
                        i += 1
                        continue
                    
                    # Replace with constant load
                    const_idx = self.add_constant(result)
                    func.instructions[i] = IRInstruction(
                        IRInstructionType.LOAD_CONST, [const_idx], instr.result
                    )
                
                i += 1
    
    def dead_code_elimination(self):
        """Remove dead code"""
        for func in self.module.functions.values():
            # Mark used instructions
            used = set()
            
            # Mark all labels that are jumped to
            for instr in func.instructions:
                if instr.type in [IRInstructionType.JUMP, IRInstructionType.JUMP_IF_TRUE, IRInstructionType.JUMP_IF_FALSE]:
                    if len(instr.operands) > 0:
                        used.add(instr.operands[-1])
            
            # Remove unused labels
            func.instructions = [
                instr for instr in func.instructions
                if not (instr.type == IRInstructionType.LABEL and instr.operands[0] not in used)
            ]
    
    def constant_propagation(self):
        """Propagate constants"""
        for func in self.module.functions.values():
            const_values = {}
            
            for instr in func.instructions:
                # Track constant assignments
                if (instr.type == IRInstructionType.LOAD_CONST and instr.result):
                    const_values[instr.result] = self.module.constants[instr.operands[0]]
                
                # Replace variable loads with constants if possible
                elif (instr.type == IRInstructionType.LOAD_VAR and instr.result and
                      instr.operands[0] in const_values):
                    
                    const_val = const_values[instr.operands[0]]
                    const_idx = self.add_constant(const_val)
                    func.instructions[func.instructions.index(instr)] = IRInstruction(
                        IRInstructionType.LOAD_CONST, [const_idx], instr.result
                    )
    
    def add_constant(self, value: Any) -> int:
        """Add a constant to the module"""
        if value not in self.module.constants:
            self.module.constants.append(value)
        return self.module.constants.index(value)


def print_ir(module: IRModule):
    """Print IR module in human-readable format"""
    print("=== IR Module ===")
    print(f"Constants: {module.constants}")
    print(f"Strings: {module.strings}")
    print(f"Structs: {module.structs}")
    print()
    
    for func_name, func in module.functions.items():
        print(f"Function: {func_name}({', '.join(func.params)})")
        if func.return_type:
            print(f"  Returns: {func.return_type}")
        print("  Locals:", func.locals)
        print("  Instructions:")
        
        for instr in func.instructions:
            if instr.comment:
                print(f"    {instr}  # {instr.comment}")
            else:
                print(f"    {instr}")
        print()
