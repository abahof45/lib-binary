#!/usr/bin/env python3
"""
lib-binary compiler and runtime
Main CLI interface for compiling and running lib-binary programs
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Import all compiler components
from lexer import tokenize_source
from parser import parse_source
from ast_to_ir import convert_ast_to_ir
from ir import IROptimizer, print_ir
from ir_to_bytecode import convert_ir_to_bytecode, optimize_bytecode
from bytecode import serialize_bytecode, deserialize_bytecode
from vm import run_bytecode, VirtualMachine


class CompilerError(Exception):
    """Compilation error"""
    pass


class LibBinaryCompiler:
    """Main compiler class"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
    
    def compile_file(self, input_file: str, output_file: str, optimize: bool = True) -> bool:
        """Compile a .wd file to .bin bytecode"""
        try:
            # Read source file
            if not os.path.exists(input_file):
                raise CompilerError(f"Input file not found: {input_file}")
            
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            if self.debug:
                print(f"Compiling {input_file}...")
            
            # Step 1: Lexical analysis
            tokens = tokenize_source(source_code)
            if self.debug:
                print(f"Lexical analysis: {len(tokens)} tokens")
            
            # Step 2: Parse to AST
            ast = parse_source(source_code)
            if self.debug:
                print(f"Parsing: {len(ast.statements)} statements")
            
            # Step 3: Convert to IR
            ir_module = convert_ast_to_ir(ast)
            if self.debug:
                print(f"IR generation: {len(ir_module.functions)} functions")
                if self.debug > 1:
                    print_ir(ir_module)
            
            # Step 4: Optimize IR
            if optimize:
                optimizer = IROptimizer(ir_module)
                ir_module = optimizer.optimize()
                if self.debug:
                    print("IR optimization completed")
            
            # Step 5: Convert to bytecode
            bytecode_module = convert_ir_to_bytecode(ir_module)
            if self.debug:
                print(f"Bytecode generation: {len(bytecode_module.functions)} functions")
            
            # Step 6: Optimize bytecode
            if optimize:
                bytecode_module = optimize_bytecode(bytecode_module)
                if self.debug:
                    print("Bytecode optimization completed")
            
            # Step 7: Serialize to binary
            bytecode_data = serialize_bytecode(bytecode_module)
            
            # Write output file
            with open(output_file, 'wb') as f:
                f.write(bytecode_data)
            
            if self.debug:
                print(f"Compiled successfully: {output_file} ({len(bytecode_data)} bytes)")
            
            return True
            
        except Exception as e:
            print(f"Compilation error: {e}", file=sys.stderr)
            if self.debug:
                import traceback
                traceback.print_exc()
            return False
    
    def run_bytecode_file(self, bytecode_file: str, debug: bool = False) -> bool:
        """Run a .bin bytecode file"""
        try:
            # Read bytecode file
            if not os.path.exists(bytecode_file):
                raise CompilerError(f"Bytecode file not found: {bytecode_file}")
            
            with open(bytecode_file, 'rb') as f:
                bytecode_data = f.read()
            
            if debug:
                print(f"Loading bytecode: {bytecode_file} ({len(bytecode_data)} bytes)")
            
            # Deserialize bytecode
            module = deserialize_bytecode(bytecode_data)
            
            if debug:
                print(f"Loaded module: {module}")
                print(f"Functions: {list(module.functions.keys())}")
                print(f"Constants: {module.constants}")
                print(f"Entry point: {module.entry_point}")
            
            # Run bytecode
            result = run_bytecode(module, debug=debug)
            
            if result is not None:
                if debug:
                    print(f"Program returned: {result}")
            
            return True
            
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)
            if debug:
                import traceback
                traceback.print_exc()
            return False
    
    def disassemble_bytecode(self, bytecode_file: str, output_file: Optional[str] = None) -> bool:
        """Disassemble bytecode to human-readable format"""
        try:
            # Read bytecode file
            with open(bytecode_file, 'rb') as f:
                bytecode_data = f.read()
            
            # Deserialize bytecode
            module = deserialize_bytecode(bytecode_data)
            
            # Generate disassembly
            disassembly = []
            disassembly.append("=== lib-binary Bytecode Disassembly ===\n")
            disassembly.append(f"Module: {module}")
            disassembly.append(f"Constants: {module.constants}")
            disassembly.append(f"Strings: {module.strings}")
            disassembly.append(f"Structs: {module.structs}")
            disassembly.append(f"Entry point: {module.entry_point}\n")
            
            for func_name, func in module.functions.items():
                disassembly.append(f"Function: {func_name}")
                disassembly.append(f"  Parameters: {func.params}")
                disassembly.append(f"  Locals: {func.locals_count}")
                if func.return_type:
                    disassembly.append(f"  Returns: {func.return_type}")
                disassembly.append("  Instructions:")
                
                for i, instr in enumerate(func.instructions):
                    disassembly.append(f"    {i:3d}: {instr}")
                
                disassembly.append("")
            
            disassembly_text = "\n".join(disassembly)
            
            # Output
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(disassembly_text)
                print(f"Disassembly written to: {output_file}")
            else:
                print(disassembly_text)
            
            return True
            
        except Exception as e:
            print(f"Disassembly error: {e}", file=sys.stderr)
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="lib-binary compiler and runtime",
        prog="lib-binary"
    )
    
    parser.add_argument(
        "input",
        help="Input file (.wd source or .bin bytecode)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file"
    )
    
    parser.add_argument(
        "-d", "--debug",
        action="count",
        default=0,
        help="Enable debug output (use -dd for more verbose)"
    )
    
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Disable optimizations"
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["run", "compile", "disassemble"],
        help="Command to execute (if not specified, inferred from file extension)"
    )
    
    parser.add_argument(
        "--ir-debug",
        action="store_true",
        help="Show IR instructions during compilation"
    )
    
    args = parser.parse_args()
    
    # Create compiler
    compiler = LibBinaryCompiler(debug=args.debug > 0)
    
    # Determine command and files
    input_path = Path(args.input)
    
    if args.command:
        command = args.command
    else:
        # Infer command from file extension
        if input_path.suffix == '.wd':
            command = 'compile'
        elif input_path.suffix == '.bin':
            command = 'run'
        else:
            print(f"Error: Cannot determine command for file extension '{input_path.suffix}'", file=sys.stderr)
            print("Use .wd for source files or .bin for bytecode files", file=sys.stderr)
            sys.exit(1)
    
    # Determine output file
    output_file = args.output
    if not output_file:
        if command == 'compile':
            output_file = input_path.with_suffix('.bin')
        elif command == 'disassemble':
            output_file = input_path.with_suffix('.disasm')
    
    # Execute command
    if command == 'compile':
        if input_path.suffix != '.wd':
            print(f"Error: Compile command expects .wd source file", file=sys.stderr)
            sys.exit(1)
        
        success = compiler.compile_file(
            str(input_path),
            str(output_file),
            optimize=not args.no_optimize
        )
        
        if success:
            print(f"Compiled {input_path} -> {output_file}")
        else:
            sys.exit(1)
    
    elif command == 'run':
        if input_path.suffix != '.bin':
            print(f"Error: Run command expects .bin bytecode file", file=sys.stderr)
            sys.exit(1)
        
        success = compiler.run_bytecode_file(
            str(input_path),
            debug=args.debug > 0
        )
        
        if not success:
            sys.exit(1)
    
    elif command == 'disassemble':
        if input_path.suffix != '.bin':
            print(f"Error: Disassemble command expects .bin bytecode file", file=sys.stderr)
            sys.exit(1)
        
        success = compiler.disassemble_bytecode(
            str(input_path),
            str(output_file) if output_file else None
        )
        
        if not success:
            sys.exit(1)
    
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
