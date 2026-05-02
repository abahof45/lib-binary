# lib-binary Coding and Compilation Guide

## Table of Contents

1. [Language Overview](#language-overview)
2. [Syntax and Structure](#syntax-and-structure)
3. [Data Types and Variables](#data-types-and-variables)
4. [Operators and Expressions](#operators-and-expressions)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Memory Management](#memory-management)
8. [Standard Library](#standard-library)
9. [Compilation Process](#compilation-process)
10. [Bytecode Format](#bytecode-format)
11. [Virtual Machine](#virtual-machine)
12. [Debugging](#debugging)
13. [Best Practices](#best-practices)
14. [Advanced Techniques](#advanced-techniques)

## Language Overview

lib-binary is a hybrid programming language that combines Python-like syntax with C-style low-level control features. It's designed for both high-level scripting and low-level system programming.

### Key Design Principles

- **Python-like syntax** for readability and ease of use
- **C-style features** for low-level control when needed
- **Strong simplification** - remove complexity, prioritize direct execution mapping
- **Hybrid abstraction** - both high-level scripting and low-level performance operations
- **Deterministic compilation** - consistent, predictable output

### File Extensions

- `.wd` - Source files (Web Development)
- `.bin` - Compiled bytecode files
- `.disasm` - Disassembly output files

## Syntax and Structure

### Basic Structure

lib-binary uses Python-like indentation-based blocks:

```python
func main():
    print("Hello, World!")
    x = 10
    y = 20
    result = x + y
    print("Result:", result)
    return result
```

### Comments

```python
# Single line comment
# Another comment

/* Multi-line comment
   spanning multiple lines */
```

### Low-level Blocks

For C-style operations, use the `low:` block:

```python
func memory_example():
    x = 42
    print("High-level:", x)
    
    low:
        # Low-level memory operations
        ptr buffer = alloc(1024)
        store(buffer, x)
        value = load(buffer)
        print("Low-level value:", value)
        free(buffer)
```

## Data Types and Variables

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
# Explicit type declarations
int count = 100
float precision = 3.14159
char initial = 'A'
ptr memory_address = alloc(1024)
```

### Type Casting

```python
# Automatic casting functions
result = cast_int("123")     # String to int
value = cast_float(42)       # Int to float
text = cast_str(3.14)        # Float to string
```

### Variable Assignment

```python
# Basic assignment
x = 10
name = "lib-binary"

# Compound assignment
x += 5   # x = x + 5
x -= 3   # x = x - 3
x *= 2   # x = x * 2
x /= 4   # x = x / 4
```

## Operators and Expressions

### Arithmetic Operators

```python
+   Addition
-   Subtraction
*   Multiplication
/   Division
%   Modulo
**  Exponentiation
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

### Expression Examples

```python
# Arithmetic expressions
result = (a + b) * c - d / e
power = x ** 2
modulo = a % b

# Bitwise expressions
flags = value & 0xFF
mask = 1 << 3
combined = a | b

# Comparison expressions
if x > 0 and y < 100:
    print("Valid range")
```

## Control Flow

### If Statements

```python
func check_value(x):
    if x > 0:
        print("Positive")
    elif x < 0:
        print("Negative")
    else:
        print("Zero")
    return x
```

### While Loops

```python
func count_to_ten():
    i = 1
    while i <= 10:
        print(i)
        i = i + 1
```

### For Loops

```python
func iterate_range():
    for i in range(0, 10):
        print("Index:", i)
    
    # With step
    for i in range(0, 20, 2):
        print("Even:", i)
```

### Break and Continue

```python
func loop_control():
    i = 0
    while i < 100:
        if i == 50:
            break      # Exit loop
        
        if i % 2 == 0:
            i = i + 1
            continue   # Skip to next iteration
        
        print("Odd:", i)
        i = i + 1
```

## Functions

### Function Definition

```python
func function_name(param1, param2):
    # Function body
    result = param1 + param2
    return result
```

### Function with Return Type

```python
func calculate(x: int, y: int): int
    return x * y
```

### Multiple Parameters

```python
func process_data(name: str, count: int, valid: bool): str
    if valid:
        return name + ": " + cast_str(count)
    else:
        return "Invalid"
```

### Recursive Functions

```python
func factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

func fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
```

### Function Calls

```python
# Basic calls
result = add(10, 20)
message = greet("Alice")

# Built-in function calls
print("Hello, World!")
user_input = input("Enter value: ")
length = len(my_list)
```

## Memory Management

### Memory Allocation and Deallocation

```python
func memory_management():
    low:
        # Allocate memory
        ptr buffer = alloc(1024)  # 1024 bytes
        
        # Store values
        store(buffer, 42)
        store(buffer + 4, 100)
        store(buffer + 8, 200)
        
        # Read values
        value1 = load(buffer)
        value2 = load(buffer + 4)
        value3 = load(buffer + 8)
        
        print("Values:", value1, value2, value3)
        
        # Free memory
        free(buffer)
```

### Pointer Operations

```python
func pointer_operations():
    low:
        # Base pointer
        ptr base = alloc(100)
        
        # Pointer arithmetic (simplified)
        ptr offset = base + 10
        
        # Store and load through pointers
        store(offset, 123)
        value = load(offset)
        
        print("Pointer value:", value)
        
        # Clean up
        free(base)
```

### Memory Safety

```python
func safe_memory():
    low:
        ptr buffer = alloc(1024)
        
        # Always check allocation
        if buffer == 0:
            print("Allocation failed")
            return
        
        # Use memory safely
        store(buffer, 42)
        value = load(buffer)
        
        # Always free memory
        free(buffer)
```

## Standard Library

### Input/Output Functions

```python
func io_example():
    # Output
    print("Hello, World!")
    print("Value:", 42, "Count:", 3)
    
    # Input
    name = input("Enter your name: ")
    age = cast_int(input("Enter your age: "))
    
    print("Hello,", name, "Age:", age)
```

### String and List Operations

```python
func collection_operations():
    # String operations
    text = "Hello, World!"
    length = len(text)
    print("Length:", length)
    
    # List operations
    numbers = [1, 2, 3, 4, 5]
    count = len(numbers)
    print("Count:", count)
    
    # Range operations
    for i in range(0, count):
        print("Number:", numbers[i])
```

### Mathematical Operations

```python
func math_operations():
    # Basic math
    a = 10
    b = 3
    
    sum = a + b
    diff = a - b
    prod = a * b
    div = a / b
    mod = a % b
    
    print("Results:", sum, diff, prod, div, mod)
    
    # Advanced math
    power = a ** 2
    sqrt = a ** 0.5
    
    print("Power:", power, "Square root:", sqrt)
```

## Compilation Process

### Compilation Pipeline

The lib-binary compiler follows this pipeline:

```
.wd source → Lexer → Parser → AST → IR → Optimizer → Bytecode → .bin file
```

### Step 1: Lexical Analysis

The lexer tokenizes the source code:

```python
# Source: func main(): print("Hello")
# Tokens: FUNC, IDENTIFIER(main), LPAREN, RPAREN, COLON, IDENTIFIER(print), LPAREN, STRING("Hello"), RPAREN
```

### Step 2: Parsing

The parser builds an Abstract Syntax Tree (AST):

```python
# AST structure for: func main(): print("Hello")
Program(
    statements=[
        FunctionDef(
            name="main",
            params=[],
            body=[
                FunctionCall(
                    function="print",
                    args=[StringLiteral("Hello")]
                )
            ]
        )
    ]
)
```

### Step 3: IR Generation

AST is converted to Intermediate Representation:

```python
# IR Instructions
LOAD_CONST "Hello"
CALL print
RET
```

### Step 4: Optimization

IR is optimized:

```python
# Before optimization
LOAD_CONST 10
LOAD_CONST 20
ADD
STORE x
LOAD x
PRINT

# After optimization (constant folding)
LOAD_CONST 30
STORE x
LOAD x
PRINT
```

### Step 5: Bytecode Generation

IR is converted to bytecode:

```python
# Bytecode instructions
0x01 0x00 0x00 0x00  # LOAD_CONST constant_index=0
0x02 0x00 0x00 0x00  # CALL function_index=0
0x03 0x00 0x00 0x00  # RET
```

## Bytecode Format

### Binary Structure

The `.bin` file format contains:

```
Header (magic: LB\x00\x01)
├── Constants Section
├── Strings Section  
├── Structs Section
├── Functions Section
└── Entry Point
```

### Magic Header

```python
MAGIC_HEADER = b'LB\x00\x01'  # lib-binary v0.1
```

### Sections

#### Constants Section
```python
# Stores numeric constants
[
    42,           # INT
    3.14159,      # FLOAT
    True,         # BOOL
    None          # NONE
]
```

#### Strings Section
```python
# Stores string constants
[
    "Hello, World!",
    "lib-binary",
    "Error message"
]
```

#### Functions Section
```python
# Stores function bytecode
{
    "main": {
        "params": [],
        "locals_count": 2,
        "instructions": [
            BytecodeInstruction(LOAD_CONST, [0]),
            BytecodeInstruction(CALL, [0]),
            BytecodeInstruction(RET, [])
        ]
    }
}
```

### Bytecode Instructions

```python
# Instruction format: opcode + operands
BytecodeOpcode.LOAD_CONST   # Load constant from pool
BytecodeOpcode.STORE        # Store to variable
BytecodeOpcode.LOAD         # Load from variable
BytecodeOpcode.ADD          # Addition
BytecodeOpcode.SUB          # Subtraction
BytecodeOpcode.MUL          # Multiplication
BytecodeOpcode.DIV          # Division
BytecodeOpcode.CALL         # Function call
BytecodeOpcode.RET          # Return
BytecodeOpcode.JMP          # Jump
BytecodeOpcode.JZ           # Jump if zero
BytecodeOpcode.JNZ          # Jump if not zero
BytecodeOpcode.ALLOC        # Allocate memory
BytecodeOpcode.FREE         # Free memory
BytecodeOpcode.STORE_MEM    # Store to memory
BytecodeOpcode.LOAD_MEM     # Load from memory
```

## Virtual Machine

### VM Architecture

The virtual machine is stack-based with:

- **Call Stack**: For function calls and returns
- **Operand Stack**: For expression evaluation
- **Heap**: For dynamic memory allocation
- **Local Variables**: For function parameters and locals

### Execution Model

```python
# VM execution loop
while current_instruction < len(instructions):
    instruction = instructions[current_instruction]
    
    # Execute instruction
    if instruction.opcode == LOAD_CONST:
        value = constants[instruction.operands[0]]
        stack.push(value)
    
    elif instruction.opcode == ADD:
        right = stack.pop()
        left = stack.pop()
        result = left + right
        stack.push(result)
    
    # ... other instructions
    
    current_instruction += 1
```

### Memory Management

```python
# Heap simulation
class Heap:
    def __init__(self, size):
        self.memory = [0] * size
        self.allocated = [False] * size
    
    def alloc(self, size):
        # Find free block
        for i in range(len(self.memory) - size + 1):
            if all(not self.allocated[j] for j in range(i, i + size)):
                # Mark as allocated
                for j in range(i, i + size):
                    self.allocated[j] = True
                return i
        return 0  # Allocation failed
    
    def free(self, address):
        # Mark as free (simplified)
        if address < len(self.memory):
            self.allocated[address] = False
```

### Function Calls

```python
# Function call mechanism
def call_function(name, args):
    # Get function
    function = functions[name]
    
    # Create new frame
    frame = {
        'locals': {},
        'return_address': current_instruction
    }
    
    # Set parameters
    for i, param in enumerate(function.params):
        frame['locals'][param] = args[i]
    
    # Push frame to call stack
    call_stack.push(frame)
    
    # Jump to function
    current_instruction = function.start_address
```

## Debugging

### Debug Mode

Enable debug mode to see compilation details:

```bash
# Basic debug
lib-binary.exe program.wd -d

# Verbose debug
lib-binary.exe program.wd -dd

# IR debug
lib-binary.exe program.wd --ir-debug
```

### Debug Output

```
=== Compilation Debug ===
Source: program.wd
Tokens: 15
AST nodes: 8
IR instructions: 12
Bytecode size: 48 bytes
Optimizations: 2 constant folds, 1 dead code removal
=== IR Instructions ===
0: LOAD_CONST 0
1: STORE x
2: LOAD_CONST 1
3: STORE y
4: LOAD x
5: LOAD y
6: ADD
7: STORE result
8: LOAD result
9: CALL print
10: LOAD result
11: RET
=== Bytecode ===
01 00 00 00 02 00 00 00 01 01 00 00 02 01 00 00 01 02 00 00 02 03 00 00 04 02 00 00 05 02 00 00 06 00 00 00 02 04 00 00 04 04 00 00 05 04 00 00 03 00 00 00
```

### Runtime Debugging

```bash
# Debug execution
lib-binary.exe run program.bin -d

# Shows VM state
=== VM Debug ===
Stack: [30]
Call Stack: [main]
Heap: [1024 bytes allocated]
Instruction: LOAD_CONST 0
```

### Error Messages

```
Compilation error: Parse error at line 5, column 10: Expected COLON, got NEWLINE
Runtime error: VM Error at instruction 12: Division by zero
Memory error: Invalid pointer access at address 1024
```

## Best Practices

### Code Organization

```python
# Use meaningful function names
func calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# Use descriptive variable names
func process_user_data(user_name: str, user_age: int, is_active: bool): str
    if is_active and user_age >= 18:
        return "Active adult: " + user_name
    else:
        return "Inactive or minor: " + user_name
```

### Memory Management

```python
func safe_memory_operation():
    low:
        # Always check allocation
        ptr buffer = alloc(1024)
        if buffer == 0:
            print("Allocation failed")
            return
        
        # Use memory safely
        try:
            store(buffer, 42)
            value = load(buffer)
            print("Value:", value)
        finally:
            # Always free memory
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

func safe_memory_access(ptr address, size):
    if address == 0:
        print("Error: Null pointer")
        return None
    
    # Additional checks could be added here
    value = load(address)
    return value
```

### Performance Optimization

```python
# Use static types when possible
func fast_calculation(x: int, y: int): int
    return x * y + y / 2

# Avoid unnecessary allocations
func process_list(items):
    # Good: reuse variables
    result = 0
    for i in range(0, len(items)):
        result += items[i]
    
    # Avoid: creating temporary lists
    # temp = []
    # for item in items:
    #     temp.append(item * 2)
    
    return result
```

## Advanced Techniques

### Mixed High-level and Low-level Code

```python
func hybrid_programming():
    # High-level data processing
    data = [1, 2, 3, 4, 5]
    result = 0
    
    for i in range(0, len(data)):
        result += data[i]
    
    print("High-level result:", result)
    
    low:
        # Low-level memory operations
        ptr buffer = alloc(len(data) * 4)  # 4 bytes per int
        
        # Store data in memory
        for i in range(0, len(data)):
            store(buffer + i * 4, data[i])
        
        # Process with bitwise operations
        for i in range(0, len(data)):
            value = load(buffer + i * 4)
            masked = value & 0xFF
            print("Masked value:", masked)
        
        free(buffer)
```

### Recursive Data Structures

```python
func process_tree(node):
    if node == None:
        return 0
    
    left_sum = process_tree(node.left)
    right_sum = process_tree(node.right)
    
    return node.value + left_sum + right_sum
```

### Function Pointers (Conceptual)

```python
func apply_operation(x, y, operation):
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    else:
        return 0

func main():
    result1 = apply_operation(10, 5, "add")
    result2 = apply_operation(10, 5, "multiply")
    
    print("Add:", result1)
    print("Multiply:", result2)
```

### System Programming

```python
func system_example():
    # High-level interface
    print("System programming example")
    
    low:
        # Low-level system operations
        ptr system_buffer = alloc(4096)  # 4KB buffer
        
        # Simulate system call
        store(system_buffer, 0x1234)     # System call number
        store(system_buffer + 4, 0x1000)  # Buffer address
        
        # Process result
        result = load(system_buffer + 8)
        print("System result:", result)
        
        free(system_buffer)
```

## Compilation Examples

### Simple Program Compilation

```python
# Source: hello.wd
func main():
    print("Hello, World!")
    return 0

# Compilation command
lib-binary.exe hello.wd -o hello.bin

# Generated bytecode structure
Header: LB\x00\x01
Constants: [0]
Strings: ["Hello, World!"]
Functions: {
    "main": {
        "params": [],
        "locals_count": 0,
        "instructions": [
            LOAD_CONST [0],    # Load "Hello, World!"
            CALL [0],          # Call print
            LOAD_CONST [1],    # Load 0
            RET                # Return
        ]
    }
}
```

### Complex Program Compilation

```python
# Source: calculator.wd
func add(a, b):
    return a + b

func main():
    x = 10
    y = 20
    result = add(x, y)
    print("Result:", result)
    return result

# Compilation process
1. Lexer: 25 tokens
2. Parser: 2 functions, 6 statements
3. IR: 15 instructions
4. Optimizer: 1 constant fold
5. Bytecode: 60 bytes
```

### Memory-Intensive Program

```python
# Source: memory_test.wd
func memory_test():
    low:
        ptr buffer = alloc(1024)
        
        for i in range(0, 256):
            store(buffer + i * 4, i * 2)
        
        total = 0
        for i in range(0, 256):
            value = load(buffer + i * 4)
            total += value
        
        free(buffer)
        return total

# Compilation features
- Low-level block detection
- Memory allocation tracking
- Loop optimization
- Register allocation
```

## Troubleshooting

### Common Compilation Errors

```
Error: Parse error at line 3, column 5: Expected COLON, got NEWLINE
Fix: Check indentation and syntax

Error: Undefined variable: x
Fix: Ensure variable is declared before use

Error: Unsupported constant type: <class 'dict'>
Fix: Use supported types only (int, float, str, bool, None)
```

### Common Runtime Errors

```
Error: VM Error at instruction 8: Division by zero
Fix: Add zero-check before division

Error: Invalid pointer access at address 0
Fix: Check pointer validity before use

Error: Stack overflow
Fix: Reduce recursion depth or optimize
```

### Performance Issues

```
Issue: Slow compilation
Fix: Use --no-optimize only when debugging

Issue: Large bytecode files
Fix: Optimize code, reduce constants

Issue: Memory usage high
Fix: Free allocated memory, use static types
```

---

This guide covers all aspects of lib-binary coding and compilation. For additional information, see the complete language documentation and example programs.
