"""
Debug tools for lib-binary programming language
Provides IR instruction display and debugging utilities
"""

from typing import List, Dict, Any
from ir import *
from bytecode import *


class IRDebugger:
    """Debugger for IR instructions"""
    
    def __init__(self, module: IRModule):
        self.module = module
    
    def print_detailed_ir(self):
        """Print detailed IR with analysis"""
        print("=== Detailed IR Analysis ===")
        print(f"Module: {self.module}")
        print(f"Constants: {self.module.constants}")
        print(f"Strings: {self.module.strings}")
        print(f"Structs: {self.module.structs}")
        print()
        
        for func_name, func in self.module.functions.items():
            print(f"Function: {func_name}")
            print(f"  Parameters: {func.params}")
            print(f"  Locals: {func.locals}")
            if func.return_type:
                print(f"  Return type: {func.return_type}")
            
            # Analyze instructions
            self._analyze_function(func)
            print()
    
    def _analyze_function(self, func: IRFunction):
        """Analyze a single function"""
        print("  Instructions:")
        
        # Track variable usage
        var_usage = {}
        const_usage = {}
        label_usage = {}
        call_targets = {}
        
        for i, instr in enumerate(func.instructions):
            prefix = f"    {i:3d}: {instr}"
            
            # Track variable usage
            if instr.result:
                if instr.result not in var_usage:
                    var_usage[instr.result] = {'defined': [], 'used': []}
                var_usage[instr.result]['defined'].append(i)
            
            for op in instr.operands:
                if isinstance(op, str):
                    if op in var_usage:
                        var_usage[op]['used'].append(i)
                    elif op.startswith('L'):
                        if op not in label_usage:
                            label_usage[op] = []
                        label_usage[op].append(i)
                elif isinstance(op, int) and op < len(self.module.constants):
                    if op not in const_usage:
                        const_usage[op] = []
                    const_usage[op].append(i)
            
            # Track function calls
            if instr.type == IRInstructionType.CALL and instr.operands:
                func_name = instr.operands[0]
                if func_name not in call_targets:
                    call_targets[func_name] = []
                call_targets[func_name].append(i)
            
            print(prefix)
        
        # Print analysis
        print("  Analysis:")
        
        if var_usage:
            print("    Variable usage:")
            for var, usage in var_usage.items():
                if var in func.params:
                    var_type = "parameter"
                elif var.startswith('t'):
                    var_type = "temporary"
                else:
                    var_type = "local"
                
                print(f"      {var} ({var_type}): defined at {usage['defined']}, used at {usage['used']}")
        
        if const_usage:
            print("    Constant usage:")
            for idx, positions in const_usage.items():
                const_val = self.module.constants[idx]
                print(f"      [{idx}] {const_val}: used at {positions}")
        
        if label_usage:
            print("    Label usage:")
            for label, positions in label_usage.items():
                print(f"      {label}: used at {positions}")
        
        if call_targets:
            print("    Function calls:")
            for target, positions in call_targets.items():
                print(f"      {target}: called at {positions}")


class BytecodeDebugger:
    """Debugger for bytecode instructions"""
    
    def __init__(self, module: BytecodeModule):
        self.module = module
    
    def print_detailed_bytecode(self):
        """Print detailed bytecode with analysis"""
        print("=== Detailed Bytecode Analysis ===")
        print(f"Module: {self.module}")
        print(f"Constants: {self.module.constants}")
        print(f"Strings: {self.module.strings}")
        print(f"Structs: {self.module.structs}")
        print(f"Entry point: {self.module.entry_point}")
        print()
        
        for func_name, func in self.module.functions.items():
            print(f"Function: {func_name}")
            print(f"  Parameters: {func.params}")
            print(f"  Locals count: {func.locals_count}")
            if func.return_type:
                print(f"  Return type: {func.return_type}")
            
            self._analyze_bytecode_function(func)
            print()
    
    def _analyze_bytecode_function(self, func: BytecodeFunction):
        """Analyze a single bytecode function"""
        print("  Instructions:")
        
        # Track instruction types
        instr_types = {}
        jump_targets = {}
        
        for i, instr in enumerate(func.instructions):
            prefix = f"    {i:3d}: {instr}"
            
            # Count instruction types
            if instr.opcode not in instr_types:
                instr_types[instr.opcode] = 0
            instr_types[instr.opcode] += 1
            
            # Track jump targets
            if instr.opcode in [BytecodeOpcode.JUMP, BytecodeOpcode.JUMP_IF_TRUE, BytecodeOpcode.JUMP_IF_FALSE]:
                if len(instr.operands) > 0 and isinstance(instr.operands[0], int):
                    target = instr.operands[0]
                    if target not in jump_targets:
                        jump_targets[target] = []
                    jump_targets[target].append(i)
            
            print(prefix)
        
        # Print analysis
        print("  Analysis:")
        
        if instr_types:
            print("    Instruction distribution:")
            for opcode, count in instr_types.items():
                print(f"      {opcode.name}: {count}")
        
        if jump_targets:
            print("    Jump targets:")
            for target, sources in jump_targets.items():
                print(f"      {target}: jumped from {sources}")


class IRVisualizer:
    """Visualizer for IR control flow"""
    
    def __init__(self, module: IRModule):
        self.module = module
    
    def generate_dot_graph(self, func_name: str) -> str:
        """Generate DOT graph for function control flow"""
        if func_name not in self.module.functions:
            return f"Function {func_name} not found"
        
        func = self.module.functions[func_name]
        
        # Build basic blocks
        blocks = self._build_basic_blocks(func)
        
        # Generate DOT
        dot = ["digraph G {"]
        dot.append("  node [shape=box];")
        dot.append("")
        
        # Add nodes
        for i, block in enumerate(blocks):
            label = f"Block {i}\\n"
            for instr in block:
                label += f"  {instr}\\n"
            dot.append(f'  block{i} [label="{label}"];')
        
        dot.append("")
        
        # Add edges
        for i, block in enumerate(blocks):
            # Find jumps from this block
            for instr in block:
                if instr.type in [IRInstructionType.JUMP, IRInstructionType.JUMP_IF_TRUE, IRInstructionType.JUMP_IF_FALSE]:
                    if len(instr.operands) > 0:
                        target_label = instr.operands[0]
                        target_block = self._find_block_for_label(blocks, target_label)
                        if target_block is not None:
                            dot.append(f"  block{i} -> block{target_block};")
                    
                    # For conditional jumps, also add fall-through edge
                    if instr.type in [IRInstructionType.JUMP_IF_TRUE, IRInstructionType.JUMP_IF_FALSE]:
                        next_block = i + 1 if i + 1 < len(blocks) else None
                        if next_block is not None:
                            dot.append(f"  block{i} -> block{next_block} [style=dashed];")
                        break
        
        dot.append("}")
        return "\n".join(dot)
    
    def _build_basic_blocks(self, func: IRFunction) -> List[List[IRInstruction]]:
        """Build basic blocks from function instructions"""
        blocks = []
        current_block = []
        
        # Find all labels
        labels = set()
        for instr in func.instructions:
            if instr.type == IRInstructionType.LABEL:
                labels.add(instr.operands[0])
        
        for instr in func.instructions:
            # Start new block at labels
            if instr.type == IRInstructionType.LABEL:
                if current_block:
                    blocks.append(current_block)
                current_block = [instr]
            # Start new block after jumps
            elif instr.type in [IRInstructionType.JUMP, IRInstructionType.JUMP_IF_TRUE, IRInstructionType.JUMP_IF_FALSE, IRInstructionType.RETURN]:
                current_block.append(instr)
                blocks.append(current_block)
                current_block = []
            else:
                current_block.append(instr)
        
        # Add final block
        if current_block:
            blocks.append(current_block)
        
        return blocks
    
    def _find_block_for_label(self, blocks: List[List[IRInstruction]], label: str) -> Optional[int]:
        """Find which block contains a label"""
        for i, block in enumerate(blocks):
            for instr in block:
                if instr.type == IRInstructionType.LABEL and instr.operands[0] == label:
                    return i
        return None


def debug_ir_module(module: IRModule, detailed: bool = True):
    """Debug IR module with optional detailed analysis"""
    debugger = IRDebugger(module)
    if detailed:
        debugger.print_detailed_ir()
    else:
        from ir import print_ir
        print_ir(module)


def debug_bytecode_module(module: BytecodeModule, detailed: bool = True):
    """Debug bytecode module with optional detailed analysis"""
    debugger = BytecodeDebugger(module)
    if detailed:
        debugger.print_detailed_bytecode()
    else:
        print(f"BytecodeModule({len(module.functions)} functions, {len(module.constants)} constants)")
        for func_name, func in module.functions.items():
            print(f"  {func_name}: {len(func.instructions)} instructions")


if __name__ == "__main__":
    # Test debug tools
    from ast_to_ir import convert_ast_to_ir
    from parser import parse_source
    
    test_code = """
func main():
    x = 10
    y = 20
    if x < y:
        print("x is less than y")
    else:
        print("x is not less than y")
    return x + y
"""
    
    try:
        # Parse and convert to IR
        ast = parse_source(test_code)
        ir_module = convert_ast_to_ir(ast)
        
        print("=== IR Debug ===")
        debug_ir_module(ir_module, detailed=True)
        
        # Generate control flow graph
        visualizer = IRVisualizer(ir_module)
        dot_graph = visualizer.generate_dot_graph("main")
        print("\n=== Control Flow Graph (DOT) ===")
        print(dot_graph)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
