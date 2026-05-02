"""
IR to Bytecode converter for lib-binary programming language
Converts IR instructions to bytecode format
"""

from typing import Dict, List, Optional
from ir import *
from bytecode import *


class IRToBytecodeConverter:
    """Converts IR to bytecode"""
    
    def __init__(self):
        self.label_addresses: Dict[str, int] = {}
        self.current_function: Optional[str] = None
        self.instruction_counter = 0
    
    def convert(self, ir_module: IRModule) -> BytecodeModule:
        """Convert IR module to bytecode module"""
        bytecode_module = BytecodeModule()
        
        # Copy constants and strings
        bytecode_module.constants = ir_module.constants
        bytecode_module.strings = ir_module.strings
        bytecode_module.structs = ir_module.structs
        
        # Convert functions
        for func_name, ir_func in ir_module.functions.items():
            bytecode_func = self.convert_function(ir_func)
            bytecode_module.functions[func_name] = bytecode_func
        
        # Set entry point (look for main function)
        if "main" in bytecode_module.functions:
            bytecode_module.entry_point = "main"
        
        return bytecode_module
    
    def convert_function(self, ir_func: IRFunction) -> BytecodeFunction:
        """Convert IR function to bytecode function"""
        self.current_function = ir_func.name
        self.instruction_counter = 0
        self.label_addresses.clear()
        
        # First pass: collect label addresses
        instructions = []
        for ir_instr in ir_func.instructions:
            if ir_instr.type == IRInstructionType.LABEL:
                self.label_addresses[ir_instr.operands[0]] = self.instruction_counter
            else:
                self.instruction_counter += 1
        
        # Second pass: convert instructions
        self.instruction_counter = 0
        instructions = []
        
        for ir_instr in ir_func.instructions:
            if ir_instr.type != IRInstructionType.LABEL:
                bytecode_instr = self.convert_instruction(ir_instr)
                if bytecode_instr:
                    instructions.append(bytecode_instr)
                    self.instruction_counter += 1
        
        # Calculate locals count (excluding parameters)
        locals_count = len(ir_func.locals) - len(ir_func.params)
        if locals_count < 0:
            locals_count = 0
        
        return BytecodeFunction(
            ir_func.name,
            ir_func.params,
            instructions,
            locals_count,
            ir_func.return_type
        )
    
    def convert_instruction(self, ir_instr: IRInstruction) -> Optional[BytecodeInstruction]:
        """Convert single IR instruction to bytecode"""
        opcode = self._get_opcode(ir_instr.type)
        if opcode is None:
            return None
        
        operands = []
        
        # Convert operands based on instruction type
        if ir_instr.type == IRInstructionType.LABEL:
            operands.append(ir_instr.operands[0])
        elif ir_instr.type in [IRInstructionType.JUMP, IRInstructionType.JUMP_IF_TRUE, IRInstructionType.JUMP_IF_FALSE]:
            # Convert label to address
            label = ir_instr.operands[-1]
            if label in self.label_addresses:
                operands.append(self.label_addresses[label])
            else:
                operands.append(0)  # Will be fixed later
        elif ir_instr.type == IRInstructionType.CALL:
            # Function name and arguments
            operands.append(ir_instr.operands[0])  # function name
            # Arguments are handled at runtime
        elif ir_instr.type in [IRInstructionType.LOAD_CONST, IRInstructionType.LOAD_VAR, IRInstructionType.STORE_VAR]:
            # Single operand (index or name)
            operands.append(ir_instr.operands[0])
        elif ir_instr.type in [IRInstructionType.ADD, IRInstructionType.SUB, IRInstructionType.MUL, IRInstructionType.DIV,
                              IRInstructionType.MOD, IRInstructionType.BIT_AND, IRInstructionType.BIT_OR, IRInstructionType.BIT_XOR,
                              IRInstructionType.BIT_LEFT_SHIFT, IRInstructionType.BIT_RIGHT_SHIFT, IRInstructionType.EQ,
                              IRInstructionType.NEQ, IRInstructionType.LT, IRInstructionType.GT, IRInstructionType.LTE,
                              IRInstructionType.GTE, IRInstructionType.AND, IRInstructionType.OR]:
            # Binary operations: two operands
            operands.extend(ir_instr.operands[:2])
        elif ir_instr.type in [IRInstructionType.NEG, IRInstructionType.NOT, IRInstructionType.ALLOC,
                              IRInstructionType.FREE, IRInstructionType.LOAD_PTR, IRInstructionType.STORE_PTR,
                              IRInstructionType.PRINT, IRInstructionType.INPUT, IRInstructionType.LEN,
                              IRInstructionType.RANGE]:
            # Unary operations: one operand
            if ir_instr.operands:
                operands.append(ir_instr.operands[0])
        elif ir_instr.type == IRInstructionType.RETURN:
            # Optional operand
            if ir_instr.operands:
                operands.append(ir_instr.operands[0])
        
        return BytecodeInstruction(opcode, operands)
    
    def _get_opcode(self, ir_type: IRInstructionType) -> Optional[BytecodeOpcode]:
        """Map IR instruction type to bytecode opcode"""
        mapping = {
            IRInstructionType.LABEL: BytecodeOpcode.LABEL,
            IRInstructionType.JUMP: BytecodeOpcode.JUMP,
            IRInstructionType.JUMP_IF_TRUE: BytecodeOpcode.JUMP_IF_TRUE,
            IRInstructionType.JUMP_IF_FALSE: BytecodeOpcode.JUMP_IF_FALSE,
            IRInstructionType.CALL: BytecodeOpcode.CALL,
            IRInstructionType.RETURN: BytecodeOpcode.RETURN,
            
            IRInstructionType.PUSH: BytecodeOpcode.PUSH,
            IRInstructionType.POP: BytecodeOpcode.POP,
            IRInstructionType.DUP: BytecodeOpcode.DUP,
            
            IRInstructionType.LOAD_CONST: BytecodeOpcode.LOAD_CONST,
            IRInstructionType.LOAD_VAR: BytecodeOpcode.LOAD_VAR,
            IRInstructionType.STORE_VAR: BytecodeOpcode.STORE_VAR,
            IRInstructionType.ALLOC: BytecodeOpcode.ALLOC,
            IRInstructionType.FREE: BytecodeOpcode.FREE,
            IRInstructionType.LOAD_PTR: BytecodeOpcode.LOAD_PTR,
            IRInstructionType.STORE_PTR: BytecodeOpcode.STORE_PTR,
            
            IRInstructionType.ADD: BytecodeOpcode.ADD,
            IRInstructionType.SUB: BytecodeOpcode.SUB,
            IRInstructionType.MUL: BytecodeOpcode.MUL,
            IRInstructionType.DIV: BytecodeOpcode.DIV,
            IRInstructionType.MOD: BytecodeOpcode.MOD,
            IRInstructionType.NEG: BytecodeOpcode.NEG,
            
            IRInstructionType.BIT_AND: BytecodeOpcode.BIT_AND,
            IRInstructionType.BIT_OR: BytecodeOpcode.BIT_OR,
            IRInstructionType.BIT_XOR: BytecodeOpcode.BIT_XOR,
            IRInstructionType.BIT_LEFT_SHIFT: BytecodeOpcode.BIT_LEFT_SHIFT,
            IRInstructionType.BIT_RIGHT_SHIFT: BytecodeOpcode.BIT_RIGHT_SHIFT,
            
            IRInstructionType.EQ: BytecodeOpcode.EQ,
            IRInstructionType.NEQ: BytecodeOpcode.NEQ,
            IRInstructionType.LT: BytecodeOpcode.LT,
            IRInstructionType.GT: BytecodeOpcode.GT,
            IRInstructionType.LTE: BytecodeOpcode.LTE,
            IRInstructionType.GTE: BytecodeOpcode.GTE,
            
            IRInstructionType.AND: BytecodeOpcode.AND,
            IRInstructionType.OR: BytecodeOpcode.OR,
            IRInstructionType.NOT: BytecodeOpcode.NOT,
            
            IRInstructionType.PRINT: BytecodeOpcode.PRINT,
            IRInstructionType.INPUT: BytecodeOpcode.INPUT,
            IRInstructionType.LEN: BytecodeOpcode.LEN,
            IRInstructionType.RANGE: BytecodeOpcode.RANGE,
            
            IRInstructionType.CAST_INT: BytecodeOpcode.CAST_INT,
            IRInstructionType.CAST_FLOAT: BytecodeOpcode.CAST_FLOAT,
            IRInstructionType.CAST_STR: BytecodeOpcode.CAST_STR,
        }
        
        return mapping.get(ir_type)


class BytecodeOptimizer:
    """Optimizes bytecode instructions"""
    
    def __init__(self, module: BytecodeModule):
        self.module = module
    
    def optimize(self) -> BytecodeModule:
        """Run bytecode optimizations"""
        self.constant_folding()
        self.dead_code_elimination()
        self.jump_optimization()
        return self.module
    
    def constant_folding(self):
        """Fold constant operations in bytecode"""
        for func in self.module.functions.values():
            i = 0
            while i < len(func.instructions):
                instr = func.instructions[i]
                
                # Check if this is a binary operation with constant operands
                if (instr.opcode in [BytecodeOpcode.ADD, BytecodeOpcode.SUB, BytecodeOpcode.MUL, BytecodeOpcode.DIV] and
                    len(instr.operands) >= 2 and
                    all(isinstance(op, int) and op < len(self.module.constants) for op in instr.operands[:2])):
                    
                    const1 = self.module.constants[instr.operands[0]]
                    const2 = self.module.constants[instr.operands[1]]
                    
                    # Compute result
                    try:
                        if instr.opcode == BytecodeOpcode.ADD:
                            result = const1 + const2
                        elif instr.opcode == BytecodeOpcode.SUB:
                            result = const1 - const2
                        elif instr.opcode == BytecodeOpcode.MUL:
                            result = const1 * const2
                        elif instr.opcode == BytecodeOpcode.DIV:
                            if const2 == 0:
                                i += 1
                                continue
                            result = const1 / const2
                        else:
                            i += 1
                            continue
                        
                        # Add result to constants
                        const_idx = len(self.module.constants)
                        self.module.constants.append(result)
                        
                        # Replace instruction
                        func.instructions[i] = BytecodeInstruction(
                            BytecodeOpcode.LOAD_CONST, [const_idx]
                        )
                    except:
                        i += 1
                
                i += 1
    
    def dead_code_elimination(self):
        """Remove unreachable code"""
        for func in self.module.functions.values():
            # Mark reachable instructions
            reachable = [False] * len(func.instructions)
            
            # Start from first instruction
            if len(func.instructions) > 0:
                self._mark_reachable(func, 0, reachable)
            
            # Remove unreachable instructions
            func.instructions = [
                instr for i, instr in enumerate(func.instructions)
                if reachable[i]
            ]
    
    def _mark_reachable(self, func: BytecodeFunction, start_idx: int, reachable: List[bool]):
        """Mark reachable instructions recursively"""
        if start_idx >= len(func.instructions) or reachable[start_idx]:
            return
        
        reachable[start_idx] = True
        instr = func.instructions[start_idx]
        
        # Follow jumps
        if instr.opcode == BytecodeOpcode.JUMP and len(instr.operands) > 0:
            target = instr.operands[0]
            if isinstance(target, int) and target < len(func.instructions):
                self._mark_reachable(func, target, reachable)
        elif instr.opcode in [BytecodeOpcode.JUMP_IF_TRUE, BytecodeOpcode.JUMP_IF_FALSE]:
            # Both next instruction and jump target are reachable
            if start_idx + 1 < len(func.instructions):
                self._mark_reachable(func, start_idx + 1, reachable)
            if len(instr.operands) > 0:
                target = instr.operands[0]
                if isinstance(target, int) and target < len(func.instructions):
                    self._mark_reachable(func, target, reachable)
        elif instr.opcode != BytecodeOpcode.RETURN:
            # Continue to next instruction
            if start_idx + 1 < len(func.instructions):
                self._mark_reachable(func, start_idx + 1, reachable)
    
    def jump_optimization(self):
        """Optimize jump instructions"""
        for func in self.module.functions.values():
            i = 0
            while i < len(func.instructions):
                instr = func.instructions[i]
                
                # Remove jumps to next instruction
                if (instr.opcode == BytecodeOpcode.JUMP and 
                    len(instr.operands) > 0 and
                    isinstance(instr.operands[0], int) and
                    instr.operands[0] == i + 1):
                    func.instructions.pop(i)
                    continue
                
                # Convert jump-if-false to jump-if-true with negated condition
                if (instr.opcode == BytecodeOpcode.JUMP_IF_FALSE and
                    len(instr.operands) > 1 and
                    i + 1 < len(func.instructions) and
                    func.instructions[i + 1].opcode == BytecodeOpcode.JUMP):
                    
                    # This is a complex optimization that would need more context
                    # For now, we'll skip it
                    pass
                
                i += 1


def convert_ir_to_bytecode(ir_module: IRModule) -> BytecodeModule:
    """Convenience function to convert IR to bytecode"""
    converter = IRToBytecodeConverter()
    return converter.convert(ir_module)


def optimize_bytecode(bytecode_module: BytecodeModule) -> BytecodeModule:
    """Convenience function to optimize bytecode"""
    optimizer = BytecodeOptimizer(bytecode_module)
    return optimizer.optimize()


if __name__ == "__main__":
    # Test the converter
    from ir import *
    from ast_to_ir import convert_ast_to_ir
    from parser import parse_source
    
    test_code = """
func main():
    x = 10
    y = 20
    print(x + y)
"""
    
    try:
        # Parse and convert to IR
        ast = parse_source(test_code)
        ir_module = convert_ast_to_ir(ast)
        
        # Optimize IR
        optimizer = IROptimizer(ir_module)
        ir_module = optimizer.optimize()
        
        # Convert to bytecode
        bytecode_module = convert_ir_to_bytecode(ir_module)
        
        # Optimize bytecode
        bytecode_module = optimize_bytecode(bytecode_module)
        
        print("Bytecode generated successfully:")
        print(f"Functions: {list(bytecode_module.functions.keys())}")
        print(f"Constants: {bytecode_module.constants}")
        print(f"Entry point: {bytecode_module.entry_point}")
        
        # Print instructions for main function
        if "main" in bytecode_module.functions:
            main_func = bytecode_module.functions["main"]
            print(f"\nMain function ({len(main_func.instructions)} instructions):")
            for i, instr in enumerate(main_func.instructions):
                print(f"  {i:3d}: {instr}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
