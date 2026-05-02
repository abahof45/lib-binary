"""
Binary bytecode format for lib-binary programming language
Defines the .bin file format and serialization/deserialization
"""

import struct
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from ir import *


class BytecodeOpcode(Enum):
    """Bytecode opcodes"""
    # Control flow (0-9)
    LABEL = 0x01
    JUMP = 0x02
    JUMP_IF_TRUE = 0x03
    JUMP_IF_FALSE = 0x04
    CALL = 0x05
    RETURN = 0x06
    
    # Stack operations (10-19)
    PUSH = 0x10
    POP = 0x11
    DUP = 0x12
    
    # Memory operations (20-29)
    LOAD_CONST = 0x20
    LOAD_VAR = 0x21
    STORE_VAR = 0x22
    ALLOC = 0x23
    FREE = 0x24
    LOAD_PTR = 0x25
    STORE_PTR = 0x26
    
    # Arithmetic operations (30-39)
    ADD = 0x30
    SUB = 0x31
    MUL = 0x32
    DIV = 0x33
    MOD = 0x34
    NEG = 0x35
    
    # Bitwise operations (40-49)
    BIT_AND = 0x40
    BIT_OR = 0x41
    BIT_XOR = 0x42
    BIT_LEFT_SHIFT = 0x43
    BIT_RIGHT_SHIFT = 0x44
    
    # Comparison operations (50-59)
    EQ = 0x50
    NEQ = 0x51
    LT = 0x52
    GT = 0x53
    LTE = 0x54
    GTE = 0x55
    
    # Logical operations (60-69)
    AND = 0x60
    OR = 0x61
    NOT = 0x62
    
    # Standard library calls (70-79)
    PRINT = 0x70
    INPUT = 0x71
    LEN = 0x72
    RANGE = 0x73
    
    # Type operations (80-89)
    CAST_INT = 0x80
    CAST_FLOAT = 0x81
    CAST_STR = 0x82


class BytecodeConstantType(Enum):
    """Types of constants in the constant pool"""
    INT = 0x01
    FLOAT = 0x02
    STRING = 0x03
    BOOL = 0x04
    NONE = 0x05


class BytecodeInstruction:
    """Single bytecode instruction"""
    
    def __init__(self, opcode: BytecodeOpcode, operands: List[Any]):
        self.opcode = opcode
        self.operands = operands
    
    def __repr__(self):
        return f"{self.opcode.name}({', '.join(map(str, self.operands))})"


class BytecodeFunction:
    """Bytecode function definition"""
    
    def __init__(self, name: str, params: List[str], instructions: List[BytecodeInstruction], 
                 locals_count: int, return_type: Optional[str] = None):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.locals_count = locals_count
        self.return_type = return_type
    
    def __repr__(self):
        return f"BytecodeFunction({self.name}, params={self.params}, {len(self.instructions)} instructions)"


class BytecodeModule:
    """Complete bytecode module"""
    
    def __init__(self):
        self.functions: Dict[str, BytecodeFunction] = {}
        self.constants: List[Any] = []
        self.strings: List[str] = []
        self.structs: Dict[str, List[tuple]] = {}
        self.entry_point: Optional[str] = None
    
    def __repr__(self):
        return f"BytecodeModule({len(self.functions)} functions, {len(self.constants)} constants)"


class BytecodeSerializer:
    """Serializes bytecode module to binary format"""
    
    MAGIC_HEADER = b'LB\x00\x01'  # lib-binary v0.1
    SECTION_CONSTANTS = 0x01
    SECTION_STRINGS = 0x02
    SECTION_STRUCTS = 0x03
    SECTION_FUNCTIONS = 0x04
    SECTION_ENTRY = 0x05
    
    def __init__(self):
        self.label_addresses: Dict[str, int] = {}
    
    def serialize(self, module: BytecodeModule) -> bytes:
        """Serialize bytecode module to bytes"""
        data = bytearray()
        
        # Write magic header
        data.extend(self.MAGIC_HEADER)
        
        # Write constants section
        data.extend(self._serialize_constants(module.constants))
        
        # Write strings section
        data.extend(self._serialize_strings(module.strings))
        
        # Write structs section
        data.extend(self._serialize_structs(module.structs))
        
        # Write functions section
        data.extend(self._serialize_functions(module.functions))
        
        # Write entry point
        data.extend(self._serialize_entry_point(module.entry_point))
        
        return bytes(data)
    
    def _serialize_constants(self, constants: List[Any]) -> bytes:
        """Serialize constants section"""
        data = bytearray()
        data.append(self.SECTION_CONSTANTS)
        
        # Count
        data.extend(struct.pack('<I', len(constants)))
        
        # Constants
        for const in constants:
            if isinstance(const, int):
                data.append(BytecodeConstantType.INT.value)
                data.extend(struct.pack('<q', const))
            elif isinstance(const, float):
                data.append(BytecodeConstantType.FLOAT.value)
                data.extend(struct.pack('<d', const))
            elif isinstance(const, bool):
                data.append(BytecodeConstantType.BOOL.value)
                data.append(1 if const else 0)
            elif isinstance(const, str):
                data.append(BytecodeConstantType.STRING.value)
                string_bytes = const.encode('utf-8')
                data.extend(struct.pack('<I', len(string_bytes)))
                data.extend(string_bytes)
            elif const is None:
                data.append(BytecodeConstantType.NONE.value)
            else:
                raise ValueError(f"Unsupported constant type: {type(const)}")
        
        return bytes(data)
    
    def _serialize_strings(self, strings: List[str]) -> bytes:
        """Serialize strings section"""
        data = bytearray()
        data.append(self.SECTION_STRINGS)
        
        # Count
        data.extend(struct.pack('<I', len(strings)))
        
        # Strings
        for string in strings:
            string_bytes = string.encode('utf-8')
            data.extend(struct.pack('<I', len(string_bytes)))
            data.extend(string_bytes)
        
        return bytes(data)
    
    def _serialize_structs(self, structs: Dict[str, List[tuple]]) -> bytes:
        """Serialize structs section"""
        data = bytearray()
        data.append(self.SECTION_STRUCTS)
        
        # Count
        data.extend(struct.pack('<I', len(structs)))
        
        # Structs
        for struct_name, fields in structs.items():
            # Struct name
            name_bytes = struct_name.encode('utf-8')
            data.extend(struct.pack('<I', len(name_bytes)))
            data.extend(name_bytes)
            
            # Field count
            data.extend(struct.pack('<I', len(fields)))
            
            # Fields
            for field_name, field_type in fields:
                # Field name
                field_name_bytes = field_name.encode('utf-8')
                data.extend(struct.pack('<I', len(field_name_bytes)))
                data.extend(field_name_bytes)
                
                # Field type
                field_type_bytes = field_type.encode('utf-8')
                data.extend(struct.pack('<I', len(field_type_bytes)))
                data.extend(field_type_bytes)
        
        return bytes(data)
    
    def _serialize_functions(self, functions: Dict[str, BytecodeFunction]) -> bytes:
        """Serialize functions section"""
        data = bytearray()
        data.append(self.SECTION_FUNCTIONS)
        
        # Count
        data.extend(struct.pack('<I', len(functions)))
        
        # First pass: collect all labels and their addresses
        self.label_addresses.clear()
        current_address = 0
        
        for func_name, func in functions.items():
            # Function header will be added later
            for instr in func.instructions:
                if instr.opcode == BytecodeOpcode.LABEL:
                    self.label_addresses[instr.operands[0]] = current_address
                else:
                    # Estimate instruction size (opcode + operands)
                    current_address += 1 + len(instr.operands) * 4  # Rough estimate
        
        # Second pass: serialize functions
        for func_name, func in functions.items():
            # Function name
            name_bytes = func_name.encode('utf-8')
            data.extend(struct.pack('<I', len(name_bytes)))
            data.extend(name_bytes)
            
            # Parameter count
            data.extend(struct.pack('<I', len(func.params)))
            
            # Parameter names
            for param in func.params:
                param_bytes = param.encode('utf-8')
                data.extend(struct.pack('<I', len(param_bytes)))
                data.extend(param_bytes)
            
            # Locals count
            data.extend(struct.pack('<I', func.locals_count))
            
            # Return type
            if func.return_type:
                return_type_bytes = func.return_type.encode('utf-8')
                data.extend(struct.pack('<I', len(return_type_bytes)))
                data.extend(return_type_bytes)
            else:
                data.extend(struct.pack('<I', 0))
            
            # Instruction count
            data.extend(struct.pack('<I', len(func.instructions)))
            
            # Instructions
            for instr in func.instructions:
                data.append(instr.opcode.value)
                
                # Serialize operands based on instruction type
                if instr.opcode == BytecodeOpcode.LABEL:
                    # Labels are handled separately
                    continue
                elif instr.opcode in [BytecodeOpcode.JUMP, BytecodeOpcode.JUMP_IF_TRUE, BytecodeOpcode.JUMP_IF_FALSE]:
                    # Jump target (label)
                    label = instr.operands[0]
                    if label in self.label_addresses:
                        data.extend(struct.pack('<I', self.label_addresses[label]))
                    else:
                        data.extend(struct.pack('<I', 0))  # Will be fixed later
                elif instr.opcode == BytecodeOpcode.CALL:
                    # Function name
                    func_name_bytes = instr.operands[0].encode('utf-8')
                    data.extend(struct.pack('<I', len(func_name_bytes)))
                    data.extend(func_name_bytes)
                    # Argument count
                    data.extend(struct.pack('<I', len(instr.operands) - 1))
                else:
                    # Generic operands (integers)
                    for operand in instr.operands:
                        if isinstance(operand, int):
                            data.extend(struct.pack('<I', operand))
                        elif isinstance(operand, str):
                            operand_bytes = operand.encode('utf-8')
                            data.extend(struct.pack('<I', len(operand_bytes)))
                            data.extend(operand_bytes)
                        else:
                            raise ValueError(f"Unsupported operand type: {type(operand)}")
        
        return bytes(data)
    
    def _serialize_entry_point(self, entry_point: Optional[str]) -> bytes:
        """Serialize entry point"""
        data = bytearray()
        data.append(self.SECTION_ENTRY)
        
        if entry_point:
            entry_bytes = entry_point.encode('utf-8')
            data.extend(struct.pack('<I', len(entry_bytes)))
            data.extend(entry_bytes)
        else:
            data.extend(struct.pack('<I', 0))
        
        return bytes(data)


class BytecodeDeserializer:
    """Deserializes binary format to bytecode module"""
    
    def __init__(self):
        self.constants: List[Any] = []
        self.strings: List[str] = []
        self.structs: Dict[str, List[tuple]] = {}
    
    def deserialize(self, data: bytes) -> BytecodeModule:
        """Deserialize bytes to bytecode module"""
        offset = 0
        
        # Check magic header
        if data[offset:offset+4] != BytecodeSerializer.MAGIC_HEADER:
            raise ValueError("Invalid bytecode file format")
        offset += 4
        
        module = BytecodeModule()
        
        # Read sections
        while offset < len(data):
            section_type = data[offset]
            offset += 1
            
            if section_type == BytecodeSerializer.SECTION_CONSTANTS:
                offset, self.constants = self._deserialize_constants(data, offset)
            elif section_type == BytecodeSerializer.SECTION_STRINGS:
                offset, self.strings = self._deserialize_strings(data, offset)
            elif section_type == BytecodeSerializer.SECTION_STRUCTS:
                offset, self.structs = self._deserialize_structs(data, offset)
            elif section_type == BytecodeSerializer.SECTION_FUNCTIONS:
                offset, functions = self._deserialize_functions(data, offset)
                module.functions.update(functions)
            elif section_type == BytecodeSerializer.SECTION_ENTRY:
                offset, module.entry_point = self._deserialize_entry_point(data, offset)
            else:
                raise ValueError(f"Unknown section type: {section_type}")
        
        module.constants = self.constants
        module.strings = self.strings
        module.structs = self.structs
        
        return module
    
    def _deserialize_constants(self, data: bytes, offset: int) -> tuple[int, List[Any]]:
        """Deserialize constants section"""
        count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        constants = []
        for _ in range(count):
            const_type = data[offset]
            offset += 1
            
            if const_type == BytecodeConstantType.INT.value:
                value = struct.unpack('<q', data[offset:offset+8])[0]
                offset += 8
                constants.append(value)
            elif const_type == BytecodeConstantType.FLOAT.value:
                value = struct.unpack('<d', data[offset:offset+8])[0]
                offset += 8
                constants.append(value)
            elif const_type == BytecodeConstantType.BOOL.value:
                value = bool(data[offset])
                offset += 1
                constants.append(value)
            elif const_type == BytecodeConstantType.STRING.value:
                length = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                string_bytes = data[offset:offset+length]
                offset += length
                value = string_bytes.decode('utf-8')
                constants.append(value)
            elif const_type == BytecodeConstantType.NONE.value:
                constants.append(None)
            else:
                raise ValueError(f"Unknown constant type: {const_type}")
        
        return offset, constants
    
    def _deserialize_strings(self, data: bytes, offset: int) -> tuple[int, List[str]]:
        """Deserialize strings section"""
        count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        strings = []
        for _ in range(count):
            length = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            string = data[offset:offset+length].decode('utf-8')
            offset += length
            strings.append(string)
        
        return offset, strings
    
    def _deserialize_structs(self, data: bytes, offset: int) -> tuple[int, Dict[str, List[tuple]]]:
        """Deserialize structs section"""
        count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        structs = {}
        for _ in range(count):
            # Struct name
            name_length = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            struct_name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            
            # Field count
            field_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            # Fields
            fields = []
            for _ in range(field_count):
                # Field name
                field_name_length = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                field_name = data[offset:offset+field_name_length].decode('utf-8')
                offset += field_name_length
                
                # Field type
                field_type_length = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                field_type = data[offset:offset+field_type_length].decode('utf-8')
                offset += field_type_length
                
                fields.append((field_name, field_type))
            
            structs[struct_name] = fields
        
        return offset, structs
    
    def _deserialize_functions(self, data: bytes, offset: int) -> tuple[int, Dict[str, BytecodeFunction]]:
        """Deserialize functions section"""
        count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        functions = {}
        for _ in range(count):
            # Function name
            name_length = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            func_name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            
            # Parameter count
            param_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            # Parameter names
            params = []
            for _ in range(param_count):
                param_length = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                param = data[offset:offset+param_length].decode('utf-8')
                offset += param_length
                params.append(param)
            
            # Locals count
            locals_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            # Return type
            return_type_length = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            return_type = None
            if return_type_length > 0:
                return_type = data[offset:offset+return_type_length].decode('utf-8')
                offset += return_type_length
            
            # Instruction count
            instr_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            
            # Instructions
            instructions = []
            for _ in range(instr_count):
                opcode = BytecodeOpcode(data[offset])
                offset += 1
                
                # Deserialize operands based on instruction type
                operands = []
                if opcode == BytecodeOpcode.LABEL:
                    # Label name
                    label_length = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    label = data[offset:offset+label_length].decode('utf-8')
                    offset += label_length
                    operands.append(label)
                elif opcode in [BytecodeOpcode.JUMP, BytecodeOpcode.JUMP_IF_TRUE, BytecodeOpcode.JUMP_IF_FALSE]:
                    # Jump target address
                    target = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    operands.append(target)
                elif opcode == BytecodeOpcode.CALL:
                    # Function name
                    func_name_length = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    call_func_name = data[offset:offset+func_name_length].decode('utf-8')
                    offset += func_name_length
                    operands.append(call_func_name)
                    
                    # Argument count
                    arg_count = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    # Arguments are handled at runtime
                else:
                    # Generic operands
                    # This is simplified - in a real implementation, you'd need to know
                    # how many operands each instruction expects
                    pass
                
                instructions.append(BytecodeInstruction(opcode, operands))
            
            functions[func_name] = BytecodeFunction(func_name, params, instructions, locals_count, return_type)
        
        return offset, functions
    
    def _deserialize_entry_point(self, data: bytes, offset: int) -> tuple[int, Optional[str]]:
        """Deserialize entry point"""
        length = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        if length > 0:
            entry_point = data[offset:offset+length].decode('utf-8')
            offset += length
            return offset, entry_point
        else:
            return offset, None


def serialize_bytecode(module: BytecodeModule) -> bytes:
    """Convenience function to serialize bytecode module"""
    serializer = BytecodeSerializer()
    return serializer.serialize(module)


def deserialize_bytecode(data: bytes) -> BytecodeModule:
    """Convenience function to deserialize bytecode"""
    deserializer = BytecodeDeserializer()
    return deserializer.deserialize(data)


if __name__ == "__main__":
    # Test serialization/deserialization
    module = BytecodeModule()
    module.constants = [42, 3.14, "hello"]
    module.strings = ["world", "test"]
    module.entry_point = "main"
    
    # Add a simple function
    func = BytecodeFunction("main", [], [
        BytecodeInstruction(BytecodeOpcode.LOAD_CONST, [0]),
        BytecodeInstruction(BytecodeOpcode.PRINT, []),
        BytecodeInstruction(BytecodeOpcode.RETURN, [])
    ], 0)
    module.functions["main"] = func
    
    # Serialize
    data = serialize_bytecode(module)
    print(f"Serialized {len(data)} bytes")
    
    # Deserialize
    restored = deserialize_bytecode(data)
    print(f"Restored: {restored}")
    print(f"Constants: {restored.constants}")
    print(f"Strings: {restored.strings}")
    print(f"Entry point: {restored.entry_point}")
