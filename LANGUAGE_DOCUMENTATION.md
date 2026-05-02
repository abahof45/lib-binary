# lib-binary Programming Language Documentation

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Language Syntax](#language-syntax)
5. [Data Types](#data-types)
6. [Variables and Constants](#variables-and-constants)
7. [Operators](#operators)
8. [Control Flow](#control-flow)
9. [Functions](#functions)
10. [Structs](#structs)
11. [Memory Management](#memory-management)
12. [Standard Library](#standard-library)
13. [Error Handling](#error-handling)
14. [Compilation and Execution](#compilation-and-execution)
15. [Examples](#examples)
16. [Advanced Features](#advanced-features)

## Overview

lib-binary is a systems programming language that combines Python-like syntax with C-style low-level control features. It provides:

- **Python-like syntax** with indentation-based blocks
- **C-style features** for low-level control (pointers, memory operations, bitwise operators)
- **Hybrid abstraction** supporting both high-level scripting and low-level performance
- **Strong simplification** prioritizing readability and direct execution mapping
- **Built-in standard library** compatibility with core Python functions

### Design Goals

- **Fast execution** through optimized bytecode
- **Simple syntax** for rapid development
- **Hybrid abstraction** for both high-level and low-level programming
- **Deterministic output** with consistent compilation results

## Installation

### Requirements

- Python 3.6 or higher
- PyInstaller (for creating executables)

### Installation Steps

1. Clone or download the lib-binary source code
2. Install dependencies:
   ```bash
   pip install PyInstaller Pillow
   ```
3. Compile to executable (optional):
   ```bash
   python lib_binary.py --help  # Show usage
   ```

## Getting Started

### Your First Program

Create a file `hello.wd`:

```python
# Hello World in lib-binary
func main():
    print("Hello, World!")
    x = 10
    y = 20
    print("Sum:", x + y)
```

### Compile and Run

```bash
# Compile source to bytecode
python lib_binary.py hello.wd -o hello.bin

# Run bytecode
python lib_binary.py run hello.bin

# Or let it auto-detect
python lib_binary.py hello.wd
```

## Language Syntax

### Basic Structure

lib-binary uses Python-like indentation-based blocks:

```python
func function_name(param1, param2):
    # Function body
    statement1
    statement2
    
    # Nested block
    if condition:
        nested_statement
```

### Comments

```python
# Single line comment
# Another comment

/* Multi-line comment
   spanning multiple lines */
```

### File Extensions

- Source files: `.wd` (Web Development)
- Compiled bytecode: `.bin`
- Configuration: `.spec` (PyInstaller spec)

## Data Types

### Dynamic Types (Python-like)

```python
# String
name = "lib-binary"

# Integer
age = 25

# Float
price = 19.99

# Boolean
is_valid = True

# None/null
nothing = None
```

### Static Types (C-style)

```python
# Explicit type declaration
int count = 100
float precision = 3.14159
char initial = 'A'
ptr memory_address = alloc(1024)
```

### Type Casting

```python
# Automatic casting
result = cast_int("123")  # String to int
value = cast_float(42)    # Int to float
text = cast_str(3.14)     # Float to string
```

## Variables and Constants

### Variable Declaration

```python
# Dynamic typing
x = 10
name = "lib-binary"

# Static typing
int counter = 0
float ratio = 1.5
ptr buffer = alloc(1024)
```

### Assignment Operators

```python
# Basic assignment
x = 10

# Compound assignment
x += 5   # x = x + 5
x -= 3   # x = x - 3
x *= 2   # x = x * 2
x /= 4   # x = x / 4
```

### Constants

lib-binary doesn't have explicit constants, but you can use uppercase variables:

```python
PI = 3.14159
MAX_SIZE = 1024
```

## Operators

### Arithmetic Operators

```python
+   Addition
-   Subtraction
*   Multiplication
/   Division
%   Modulo
```

### Bitwise Operators

```python
&   Bitwise AND
|   Bitwise OR
^   Bitwise XOR
<<  Left shift
>>  Right shift
```

### Comparison Operators

```python
==  Equal
!=  Not equal
<   Less than
>   Greater than
<=  Less than or equal
>=  Greater than or equal
```

### Logical Operators

```python
and  Logical AND
or   Logical OR
not  Logical NOT
```

## Control Flow

### If Statements

```python
if condition:
    # then block
    statement1
    statement2
elif another_condition:
    # else if block
    statement3
else:
    # else block
    statement4
```

### While Loops

```python
while condition:
    # loop body
    statement1
    statement2
```

### For Loops

```python
for variable in range(start, end):
    # loop body
    print(variable)
```

### Break and Continue

```python
while True:
    if condition:
        break      # Exit loop
    if another_condition:
        continue   # Skip to next iteration
```

## Functions

### Function Definition

```python
func function_name(param1, param2):
    # function body
    result = param1 + param2
    return result
```

### Function with Return Type

```python
func calculate(x: int, y: int): int
    return x * y
```

### Function Calls

```python
# Basic call
result = function_name(arg1, arg2)

# Built-in functions
print("Hello")
user_input = input("Enter value: ")
length = len(my_list)
```

### Recursive Functions

```python
func factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

## Structs

### Struct Definition

```python
struct Person:
    name: str
    age: int
    email: str
```

### Struct Usage

```python
# Create struct instance
person = Person()
person.name = "Alice"
person.age = 30
person.email = "alice@example.com"

# Pass to functions
func display_person(p: Person):
    print("Name:", p.name)
    print("Age:", p.age)
```

## Memory Management

### Memory Allocation

```python
low:
    # Allocate memory
    ptr buffer = alloc(1024)  # Allocate 1024 bytes
    
    # Store values
    store(buffer, 42)
    store(buffer + 4, 100)
    
    # Read values
    value1 = load(buffer)
    value2 = load(buffer + 4)
    
    # Free memory
    free(buffer)
```

### Pointer Operations

```python
low:
    # Pointer arithmetic (simplified)
    ptr base = alloc(100)
    ptr offset = base + 10
    
    # Store and load
    store(offset, 123)
    value = load(offset)
```

## Standard Library

### Input/Output

```python
# Output
print("Hello, World!")
print("Value:", x, "Count:", y)

# Input
name = input("Enter your name: ")
age = cast_int(input("Enter your age: "))
```

### String Operations

```python
# Length
text = "Hello, World!"
length = len(text)

# String concatenation
greeting = "Hello, " + name
```

### List Operations

```python
# Create list
numbers = [1, 2, 3, 4, 5]

# Length
count = len(numbers)

# Range
for i in range(0, 10):
    print(i)
```

### Mathematical Functions

```python
# Basic math
result = x + y * z
power = x ** 2
square_root = x ** 0.5
```

## Error Handling

### Common Errors

1. **Parse Errors**: Syntax issues in source code
2. **Type Errors**: Invalid type operations
3. **Memory Errors**: Invalid pointer operations
4. **Runtime Errors**: Division by zero, etc.

### Error Messages

```
Compilation error: Parse error at line 5, column 10: Expected COLON, got NEWLINE
Runtime error: VM Error at instruction 12: Division by zero
```

### Debug Mode

```bash
# Enable debug output
python lib_binary.py program.wd -d

# Very verbose debug
python lib_binary.py program.wd -dd
```

## Compilation and Execution

### Compilation Process

1. **Lexical Analysis**: Tokenizes source code
2. **Parsing**: Builds Abstract Syntax Tree (AST)
3. **IR Generation**: Converts AST to Intermediate Representation
4. **Optimization**: Optimizes IR (constant folding, dead code removal)
5. **Bytecode Generation**: Converts IR to bytecode
6. **Serialization**: Saves bytecode to .bin file

### Command Line Options

```bash
# Basic compilation
python lib_binary.py source.wd -o output.bin

# With debug output
python lib_binary.py source.wd -d -o output.bin

# Disable optimizations
python lib_binary.py source.wd --no-optimize

# Show IR instructions
python lib_binary.py source.wd --ir-debug

# Run bytecode
python lib_binary.py run output.bin

# Disassemble bytecode
python lib_binary.py disassemble output.bin
```

### File Extensions

- `.wd` - Source files
- `.bin` - Compiled bytecode
- `.spec` - PyInstaller specification files

## Examples

### Hello World

```python
func main():
    print("Hello, World!")
    x = 10
    y = 20
    print("Sum:", x + y)
```

### Calculator

```python
func add(a, b):
    return a + b

func subtract(a, b):
    return a - b

func main():
    print("Simple Calculator")
    a = cast_int(input("Enter first number: "))
    b = cast_int(input("Enter second number: "))
    
    print("Sum:", add(a, b))
    print("Difference:", subtract(a, b))
```

### Memory Operations

```python
func main():
    print("Memory Operations Demo")
    
    low:
        # Allocate memory for 5 integers
        ptr numbers = alloc(5 * 4)  # 5 integers, 4 bytes each
        
        # Store values
        for i in range(0, 5):
            store(numbers + i * 4, i * 10)
        
        # Read and display values
        for i in range(0, 5):
            value = load(numbers + i * 4)
            print("Value", i, ":", value)
        
        # Free memory
        free(numbers)
```

### Recursive Functions

```python
func fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

func main():
    print("Fibonacci Sequence")
    for i in range(0, 10):
        result = fibonacci(i)
        print("fib(", i, ") =", result)
```

## Advanced Features

### Low-level Programming

```python
func main():
    # High-level code
    x = 42
    print("High-level:", x)
    
    low:
        # Low-level code with manual memory management
        ptr buffer = alloc(100)
        store(buffer, x)
        
        # Bitwise operations
        result = x & 0xFF
        shifted = x << 2
        
        print("Low-level result:", result)
        print("Shifted:", shifted)
        
        free(buffer)
```

### Type System

```python
# Dynamic typing
func dynamic_example():
    x = 10        # int
    x = "hello"   # str
    x = 3.14      # float
    return x

# Static typing
func static_example():
    int x = 10
    str name = "lib-binary"
    float pi = 3.14159
    return x
```

### Standard Library Integration

```python
func main():
    # Python-like functions
    numbers = [1, 2, 3, 4, 5]
    print("Length:", len(numbers))
    
    for i in range(0, len(numbers)):
        print("Index", i, ":", numbers[i])
    
    # User interaction
    name = input("Enter your name: ")
    print("Hello,", name)
```

## Performance Considerations

### Optimization

The compiler performs several optimizations:

1. **Constant Folding**: `2 + 2` becomes `4`
2. **Dead Code Removal**: Unreachable code is eliminated
3. **Constant Propagation**: Variables with constant values are inlined

### Memory Management

- **Stack-based execution** for efficiency
- **Heap simulation** for dynamic allocation
- **Manual memory management** in low-level blocks
- **Garbage collection** for high-level code

### Bytecode Execution

- **Virtual Machine** with optimized instruction set
- **Just-in-time compilation** concepts (planned)
- **Native integration** possibilities

## Best Practices

### Code Organization

```python
# Use meaningful function names
func calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# Use structs for data organization
struct Item:
    name: str
    price: float
    quantity: int
```

### Memory Management

```python
func safe_memory_operation():
    low:
        ptr buffer = alloc(1024)
        
        # Always check allocation
        if buffer == 0:
            print("Allocation failed")
            return
        
        # Always free memory
        try:
            # Use memory
            store(buffer, 42)
            value = load(buffer)
            print("Value:", value)
        finally:
            free(buffer)
```

### Error Handling

```python
func safe_division(a, b):
    if b == 0:
        print("Error: Division by zero")
        return 0
    else:
        return a / b
```

## Troubleshooting

### Common Issues

1. **Parse Errors**: Check syntax and indentation
2. **Type Errors**: Ensure compatible types in operations
3. **Memory Errors**: Validate pointer operations
4. **Import Errors**: Ensure all modules are available

### Debug Tips

```bash
# Use debug mode for detailed output
python lib_binary.py program.wd -d

# Check IR instructions
python lib_binary.py program.wd --ir-debug

# Disassemble bytecode
python lib_binary.py disassemble program.bin
```

### Getting Help

- Check the error messages for line numbers
- Use debug mode to trace execution
- Review examples in the `examples/` directory
- Test with simple programs first

## Future Features

### Planned Enhancements

- **Expanded Standard Library**: More built-in functions
- **Module System**: Import and export capabilities
- **Type System Improvements**: Better static typing
- **Performance Optimizations**: JIT compilation
- **IDE Integration**: Syntax highlighting and autocomplete
- **Package Manager**: Dependency management

### Version History

- **v1.0.0**: Initial release with core features
- **v1.1.0**: Planned - Enhanced standard library
- **v1.2.0**: Planned - Module system
- **v2.0.0**: Planned - JIT compilation

---

## Conclusion

lib-binary provides a unique combination of Python-like simplicity and C-style power. Whether you're writing high-level scripts or low-level system code, lib-binary offers the flexibility and performance you need.

For more examples and advanced usage, see the `examples/` directory and the test suite.
