# lib-binary Programming Language

A systems programming language that combines Python-like syntax with C-style low-level control.

## Features

- **Python-like syntax** with indentation-based blocks
- **Built-in standard library** compatibility with core Python functions
- **C-style features** for low-level control (pointers, memory operations, bitwise ops)
- **Strongly simplified**: prioritizes readability and direct execution mapping
- **Hybrid abstraction**: supports both high-level scripting and low-level performance

## Language Specification

### Syntax Rules
- Python-like indentation-based blocks
- Optional C-style braces allowed for low-level sections
- Dynamic typing unless explicitly declared (int, float, ptr, struct)
- Functions defined with `func name(params):`
- Low-level blocks with `low:` keyword

### Data Types
- **Dynamic**: str, list, dict, set (like Python)
- **Static**: int, float, char, ptr (C-style)
- **Structs**: Custom data structures

### Standard Library
- `print()`, `input()`, `len()`, `range()`
- Math operations, string manipulation
- File read/write operations
- List/dict/set handling

### Low-Level Features
- Pointers (simplified, no unsafe arithmetic)
- Bitwise operations: `&`, `|`, `^`, `<<`, `>>`
- Manual memory allocation: `alloc()`, `free()`
- Struct definitions

## Compilation

```bash
# Compile source to bytecode
lib-binary app.wd -o app.bin

# Run bytecode
lib-binary run app.bin

# Debug mode (shows IR instructions)
lib-binary run app.bin --debug
```

## Example

```python
func main():
    x = 10
    y = 20
    print(x + y)
    
    low:
        ptr a = alloc(10)
        store(a, 5)
        free(a)
```

## Architecture

1. **Compiler Pipeline**: Lexer → Parser → AST → IR → Optimizer → Bytecode
2. **Binary Format**: Structured bytecode (.bin) with function tables, instruction set, constant pool
3. **Runtime**: VM interpreter that loads bytecode and executes instructions
4. **Virtual Machine**: Stack-based execution with heap simulation and function call stack
