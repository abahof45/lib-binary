# lib-binary Usage Guide

## Installation

The lib-binary system is implemented as a set of Python modules. No installation required - just ensure you have Python 3.6+ installed.

## Quick Start

### 1. Write a lib-binary program

Create a file `hello.wd`:
```python
func main():
    print("Hello, lib-binary!")
    x = 10
    y = 20
    print("Sum:", x + y)
```

### 2. Compile and run

```bash
# Compile to bytecode
python lib_binary.py hello.wd -o hello.bin

# Run the compiled bytecode
python lib_binary.py run hello.bin

# Or let it auto-detect and compile+run
python lib_binary.py hello.wd
```

## Command Line Interface

### Basic Commands

```bash
# Compile source to bytecode
python lib_binary.py source.wd -o output.bin

# Run bytecode file
python lib_binary.py run bytecode.bin

# Disassemble bytecode
python lib_binary.py disassemble bytecode.bin

# Auto-detect based on extension
python lib_binary.py program.wd    # Compiles
python lib_binary.py program.bin    # Runs
```

### Options

```bash
# Enable debug output
python lib_binary.py program.wd -d

# Very verbose debug
python lib_binary.py program.wd -dd

# Disable optimizations
python lib_binary.py program.wd --no-optimize

# Show IR during compilation
python lib_binary.py program.wd --ir-debug

# Specify output file
python lib_binary.py program.wd -o custom_name.bin
```

## Language Reference

### Syntax Overview

lib-binary uses Python-like syntax with C-style low-level features:

```python
# Function definition
func function_name(param1, param2):
    # Function body
    return result

# Variable assignment
variable = value
int x = 10          # Typed variable
ptr p = alloc(100)  # Pointer

# Control flow
if condition:
    # then block
else:
    # else block

while condition:
    # loop body

for var in range(start, end):
    # loop body
```

### Low-level Block

Use `low:` for C-style operations:

```python
low:
    ptr buffer = alloc(1024)
    store(buffer, 42)
    value = load(buffer)
    free(buffer)
```

### Data Types

- **Dynamic**: `str`, `list`, `dict`, `set` (like Python)
- **Static**: `int`, `float`, `char`, `ptr` (C-style)
- **Structs**: Custom data structures

### Standard Library

Built-in functions compatible with Python:
- `print()` - Output values
- `input()` - Read user input
- `len()` - Get length
- `range()` - Create range
- Math operations: `+`, `-`, `*`, `/`, `%`
- Bitwise: `&`, `|`, `^`, `<<`, `>>`
- Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`

### Memory Operations

- `alloc(size)` - Allocate memory
- `free(ptr)` - Free memory
- `store(ptr, value)` - Store to pointer
- `load(ptr)` - Load from pointer

## Compilation Pipeline

The lib-binary compiler follows these steps:

1. **Lexical Analysis** - Tokenizes source code
2. **Parsing** - Builds Abstract Syntax Tree (AST)
3. **IR Generation** - Converts AST to Intermediate Representation
4. **Optimization** - Optimizes IR (constant folding, dead code removal)
5. **Bytecode Generation** - Converts IR to bytecode
6. **Serialization** - Saves bytecode to .bin file

## Debug Tools

### IR Debug

```bash
# Show IR instructions
python lib_binary.py program.wd --ir-debug
```

### Bytecode Debug

```bash
# Show bytecode execution
python lib_binary.py run program.bin -d
```

### Disassembly

```bash
# Disassemble to human-readable format
python lib_binary.py disassemble program.bin

# Save disassembly to file
python lib_binary.py disassemble program.bin -o program.disasm
```

## Examples

See the `examples/` directory for complete example programs:

- `hello_world.wd` - Basic syntax
- `low_level_demo.wd` - Memory operations and bitwise
- `control_flow.wd` - Loops and conditionals
- `struct_demo.wd` - Custom data structures
- `calculator.wd` - Interactive program

## Error Handling

The compiler provides detailed error messages:

```
Compilation error: Parse error at line 5, column 10: Expected ':', got ';'
Runtime error: VM Error at instruction 12: Division by zero
```

Use `-d` flag for stack traces and debugging information.

## Performance

- **Compilation**: Fast, suitable for development
- **Execution**: Interpreted bytecode with optimizations
- **Memory**: Efficient heap simulation with garbage collection

## Limitations

Current implementation limitations:
- Limited standard library (core functions only)
- Simple memory manager (no garbage collection)
- Basic error handling
- No external library support

## Future Enhancements

Planned features:
- Expanded standard library
- Better memory management
- Type system improvements
- Module system
- Better error messages
