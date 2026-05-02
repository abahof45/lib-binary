# lib-binary Example Programs

This directory contains example programs demonstrating various features of the lib-binary programming language.

## Examples

### hello_world.wd
Basic "Hello, World!" program showing fundamental syntax and arithmetic operations.

**Usage:**
```bash
lib-binary compile hello_world.wd -o hello_world.bin
lib-binary run hello_world.bin
```

### low_level_demo.wd
Demonstrates low-level memory operations, bitwise operators, and the `low:` block for C-style programming.

**Features shown:**
- Bitwise operations (`&`, `|`, `^`, `<<`, `>>`)
- Memory allocation and deallocation (`alloc`, `free`)
- Pointer operations (`store`, `load`)
- Type casting (`cast_str`)

### control_flow.wd
Shows control flow structures including conditionals, loops, and recursion.

**Features shown:**
- If/else statements
- While loops
- For loops with `range()`
- Function definitions and calls
- Recursion (fibonacci)

### struct_demo.wd
Demonstrates struct definitions and usage for custom data structures.

**Features shown:**
- Struct definitions
- Field access and assignment
- Passing structs to functions

### calculator.wd
Interactive calculator program showing user input and arithmetic operations.

**Features shown:**
- User input with `input()`
- String to integer conversion
- Conditional logic
- Function-based architecture

## Running Examples

To compile and run any example:

```bash
# Compile
lib-binary compile examples/[filename].wd -o [filename].bin

# Run
lib-binary run [filename].bin

# Or combine (automatic detection)
lib-binary examples/[filename].wd  # Will compile and run
```

## Debug Mode

To see IR instructions during compilation:

```bash
lib-binary compile examples/[filename].wd -o [filename].bin --ir-debug
```

To see bytecode execution:

```bash
lib-binary run [filename].bin -d
```

## Disassembly

To disassemble compiled bytecode:

```bash
lib-binary disassemble [filename].bin
```
