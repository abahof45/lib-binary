#!/usr/bin/env python3
"""
Test script to verify lib-binary compiler works end-to-end
"""

import os
import sys
from lib_binary import LibBinaryCompiler

def test_hello_world():
    """Test basic hello world compilation and execution"""
    print("=== Testing Hello World ===")
    
    compiler = LibBinaryCompiler(debug=True)
    
    # Compile hello world
    success = compiler.compile_file(
        "examples/hello_world.wd",
        "test_output/hello_world.bin"
    )
    
    if success:
        print("✓ Compilation successful")
        
        # Run the compiled bytecode
        success = compiler.run_bytecode_file(
            "test_output/hello_world.bin",
            debug=False
        )
        
        if success:
            print("✓ Execution successful")
        else:
            print("✗ Execution failed")
    else:
        print("✗ Compilation failed")
    
    return success

def test_low_level():
    """Test low-level operations"""
    print("\n=== Testing Low-Level Operations ===")
    
    compiler = LibBinaryCompiler(debug=False)
    
    # Compile low-level demo
    success = compiler.compile_file(
        "examples/low_level_demo.wd",
        "test_output/low_level.bin"
    )
    
    if success:
        print("✓ Low-level compilation successful")
        
        # Run the compiled bytecode
        success = compiler.run_bytecode_file(
            "test_output/low_level.bin",
            debug=False
        )
        
        if success:
            print("✓ Low-level execution successful")
        else:
            print("✗ Low-level execution failed")
    else:
        print("✗ Low-level compilation failed")
    
    return success

def test_control_flow():
    """Test control flow structures"""
    print("\n=== Testing Control Flow ===")
    
    compiler = LibBinaryCompiler(debug=False)
    
    # Compile control flow demo
    success = compiler.compile_file(
        "examples/control_flow.wd",
        "test_output/control_flow.bin"
    )
    
    if success:
        print("✓ Control flow compilation successful")
        
        # Run the compiled bytecode
        success = compiler.run_bytecode_file(
            "test_output/control_flow.bin",
            debug=False
        )
        
        if success:
            print("✓ Control flow execution successful")
        else:
            print("✗ Control flow execution failed")
    else:
        print("✗ Control flow compilation failed")
    
    return success

def main():
    """Run all tests"""
    print("lib-binary Compiler Test Suite")
    print("=" * 40)
    
    # Create test output directory
    os.makedirs("test_output", exist_ok=True)
    
    # Run tests
    tests = [
        test_hello_world,
        test_low_level,
        test_control_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
