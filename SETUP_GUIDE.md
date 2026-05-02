# lib-binary Setup Guide

## Complete Installation and Configuration

This guide covers everything you need to get lib-binary running on your system with full file association support.

## Quick Start

### 1. Download and Install

1. **Download the lib-binary source code**
2. **Install dependencies**:
   ```bash
   pip install PyInstaller Pillow
   ```

3. **Compile to executable**:
   ```bash
   pyinstaller lib_binary_simple.spec --clean
   ```

4. **Install file associations**:
   ```bash
   install_file_association.bat
   ```

### 2. Test Your Installation

Create a test file `test.wd`:
```python
func main():
    print("Hello, lib-binary!")
    return 0
```

Double-click the file or run:
```bash
lib-binary.exe test.wd
```

## Detailed Setup Instructions

### Prerequisites

- **Windows 10 or later** (for file associations)
- **Python 3.6+** installed and in PATH
- **Administrator privileges** (for file associations)

### Step 1: Prepare the Environment

1. **Create a project directory**:
   ```bash
   mkdir lib-binary-project
   cd lib-binary-project
   ```

2. **Download all lib-binary files** to this directory

3. **Install required Python packages**:
   ```bash
   pip install PyInstaller Pillow
   ```

### Step 2: Compile the Executable

1. **Check that all files are present**:
   - `lib_binary.py` - Main compiler script
   - `lexer.py` - Lexical analyzer
   - `parser.py` - Parser
   - `ast_to_ir.py` - AST to IR converter
   - `ir.py` - Intermediate representation
   - `ir_to_bytecode.py` - IR to bytecode converter
   - `bytecode.py` - Bytecode format
   - `vm.py` - Virtual machine
   - `lib_binary_simple.spec` - PyInstaller spec file
   - `wd-logo.ico` - Icon file

2. **Compile to executable**:
   ```bash
   pyinstaller lib_binary_simple.spec --clean
   ```

3. **Verify compilation**:
   - Check that `dist/lib-binary.exe` was created
   - Test the executable: `dist/lib-binary.exe --help`

### Step 3: Install File Associations

1. **Run the installer as Administrator**:
   ```bash
   # Right-click and "Run as administrator"
   install_file_association.bat
   ```

2. **Verify installation**:
   - `.wd` files should now show the lib-binary icon
   - Right-clicking `.wd` files should show lib-binary options
   - You can create new `.wd` files from the context menu

### Step 4: Test the Complete Setup

1. **Create a test program** (`hello.wd`):
   ```python
   func main():
       print("Hello, World!")
       x = 10
       y = 20
       print("Sum:", x + y)
       return x + y
   ```

2. **Test double-click compilation**:
   - Double-click `hello.wd`
   - Should compile to `hello.bin`

3. **Test context menu options**:
   - Right-click `hello.wd`
   - Try "Compile and Run"

4. **Test command line**:
   ```bash
   lib-binary.exe hello.wd
   lib-binary.exe run hello.bin
   ```

## File Association Features

### What Gets Installed

- **File type association**: `.wd` files linked to lib-binary
- **Custom icon**: The transparent lib-binary logo
- **Context menu options**:
  - Compile with lib-binary
  - Compile and Run
  - Edit (opens in Notepad)
- **New file template**: Create new `.wd` files from context menu

### Context Menu Options

#### Right-click on `.wd` files:

1. **Compile with lib-binary**
   - Compiles `file.wd` to `file.bin`
   - Shows compilation status

2. **Compile and Run**
   - Compiles and immediately runs the program
   - Shows output in console window

3. **Edit**
   - Opens the file in Notepad for editing

#### Right-click in folder background:

1. **New → lib-binary Source File**
   - Creates a new `.wd` file with template content
   - Opens it in Notepad

## Manual Configuration

If the automatic installer doesn't work, you can manually configure file associations:

### Registry Entries

Create these registry entries:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.wd]
@="libbinaryfile"

[HKEY_CLASSES_ROOT\libbinaryfile]
@="lib-binary Source File"

[HKEY_CLASSES_ROOT\libbinaryfile\DefaultIcon]
@="C:\\path\\to\\wd-logo.ico"

[HKEY_CLASSES_ROOT\libbinaryfile\shell\compile\command]
@="\"C:\\path\\to\\lib-binary.exe\" \"%1\""

[HKEY_CLASSES_ROOT\libbinaryfile\shell\compileandrun\command]
@="cmd /c \"\"C:\\path\\to\\lib-binary.exe\" \"%1\" -o \"%~dpn1.bin\" && \"C:\\path\\to\\lib-binary.exe\" run \"%~dpn1.bin\" && pause\""

[HKEY_CLASSES_ROOT\Directory\Background\shell\NewLibBinaryFile]
@="lib-binary Source File"

[HKEY_CLASSES_ROOT\Directory\Background\shell\NewLibBinaryFile\command]
@="cmd /c \"echo func main(): > \"%1\\new.wd\" && echo     print(\"Hello, World!\") >> \"%1\\new.wd\" && echo     return 0 >> \"%1\\new.wd\" && notepad \"%1\\new.wd\""
```

### Command Line Alternative

You can also set associations using `assoc` and `ftype` commands:

```bash
assoc .wd=libbinaryfile
ftype libbinaryfile="C:\path\to\lib-binary.exe" "%1"
```

## Troubleshooting

### Common Issues

1. **"Access denied" errors**
   - Run the installer as Administrator
   - Check antivirus software isn't blocking the installation

2. **Icon not showing**
   - Rebuild Windows icon cache
   - Restart Windows Explorer

3. **Double-click not working**
   - Check file association: `assoc .wd`
   - Check file type: `ftype libbinaryfile`
   - Verify executable path is correct

4. **Compilation errors**
   - Check that all Python files are present
   - Verify PyInstaller installation
   - Run with debug mode: `lib-binary.exe file.wd -d`

### Reset File Associations

If something goes wrong, you can reset everything:

1. **Run the uninstaller**:
   ```bash
   uninstall_file_association.bat
   ```

2. **Manually clean registry**:
   - Open `regedit`
   - Search for `libbinaryfile`
   - Delete all related entries

3. **Reinstall**:
   ```bash
   install_file_association.bat
   ```

### Verify Installation

Run these commands to verify everything is working:

```bash
# Check file association
assoc .wd

# Check file type
ftype libbinaryfile

# Test executable
lib-binary.exe --help

# Test compilation
lib-binary.exe test.wd -o test.bin

# Test execution
lib-binary.exe run test.bin
```

## IDE Integration

### Visual Studio Code

1. **Install the extension**:
   - Search for "lib-binary" in extensions
   - Or create a custom language extension

2. **Add to settings.json**:
   ```json
   {
     "files.associations": {
       "*.wd": "lib-binary"
     },
     "editor.tokenColorCustomizations": {
       "textMateRules": [
         {
           "scope": "lib-binary",
           "settings": {
             "foreground": "#000000"
           }
         }
       ]
     }
   }
   ```

### Other Editors

Most editors can be configured to recognize `.wd` files:

- **Notepad++**: Language → User-defined → Import
- **Sublime Text**: Preferences → File Types → Add
- **Atom**: Settings → File Types → Add

## Performance Tips

### Compilation Speed

1. **Use the executable** instead of Python script
2. **Enable optimizations** (default)
3. **Use debug mode only when needed**

### Runtime Performance

1. **Keep functions small**
2. **Use static types where possible**
3. **Minimize memory allocations in loops**
4. **Use built-in functions when available**

## Security Considerations

### Executable Security

1. **Only run from trusted sources**
2. **Scan with antivirus if needed**
3. **Keep Python dependencies updated**

### File Association Security

1. **Installer modifies registry**
2. **Requires administrator privileges**
3. **Can be easily removed with uninstaller**

## Next Steps

After installation:

1. **Read the language documentation**: `LANGUAGE_DOCUMENTATION.md`
2. **Try the examples**: Check the `examples/` directory
3. **Create your own programs**: Start with simple scripts
4. **Explore advanced features**: Memory management, structs, etc.

## Support

### Getting Help

1. **Check the documentation**: `LANGUAGE_DOCUMENTATION.md`
2. **Review examples**: `examples/` directory
3. **Use debug mode**: `lib-binary.exe file.wd -d`
4. **Check error messages**: They often include line numbers

### Contributing

If you find issues or want to contribute:

1. **Report bugs**: Include error messages and test cases
2. **Request features**: Describe use cases
3. **Submit improvements**: Follow the coding style

---

## Summary

With this setup, you now have:

✅ **Compiled executable** (`lib-binary.exe`)
✅ **File associations** (`.wd` files with custom icon)
✅ **Context menu integration** (right-click options)
✅ **New file template** (create from context menu)
✅ **Complete documentation** (language reference)
✅ **Example programs** (demonstrating features)

You're ready to start programming in lib-binary! The language combines Python-like simplicity with C-style power, making it perfect for both quick scripts and system-level programming.
