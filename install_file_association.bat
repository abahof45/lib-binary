@echo off
REM Windows File Association Installer for lib-binary .wd files
REM This script creates file associations and sets up the icon

echo Installing lib-binary file associations...

REM Get the current directory where this script is located
set SCRIPT_DIR=%~dp0
set ICON_PATH=%SCRIPT_DIR%wd-logo.ico
set EXE_PATH=%SCRIPT_DIR%dist\lib-binary.exe

REM Check if executable exists
if not exist "%EXE_PATH%" (
    echo Error: lib-binary.exe not found at %EXE_PATH%
    echo Please compile the executable first using: pyinstaller lib_binary_simple.spec
    pause
    exit /b 1
)

REM Check if icon exists
if not exist "%ICON_PATH%" (
    echo Error: Icon file not found at %ICON_PATH%
    pause
    exit /b 1
)

echo Found lib-binary.exe at %EXE_PATH%
echo Found icon at %ICON_PATH%

REM Create file type association
echo Creating file type association...
assoc .wd=libbinaryfile
ftype libbinaryfile="%EXE_PATH%" "%%1"

REM Set description for the file type
echo Setting file type description...
reg add "HKCR\libbinaryfile" /v "" /t REG_SZ /d "lib-binary Source File" /f

REM Set default icon
echo Setting file icon...
reg add "HKCR\libbinaryfile\DefaultIcon" /v "" /t REG_SZ /d "%ICON_PATH%" /f

REM Add shell commands
echo Adding shell commands...

REM Compile command
reg add "HKCR\libbinaryfile\shell\compile" /v "" /t REG_SZ /d "Compile with lib-binary" /f
reg add "HKCR\libbinaryfile\shell\compile\command" /v "" /t REG_SZ /d "\"%EXE_PATH%\" \"%%1\"" /f

REM Compile and Run command
reg add "HKCR\libbinaryfile\shell\compileandrun" /v "" /t REG_SZ /d "Compile and Run" /f
reg add "HKCR\libbinaryfile\shell\compileandrun\command" /v "" /t REG_SZ /d "cmd /c \"\"%EXE_PATH%\" \"%%1\" -o \"%%~dpn1.bin\" && \"%EXE_PATH%\" run \"%%~dpn1.bin\" && pause\"" /f

REM Edit command
reg add "HKCR\libbinaryfile\shell\edit" /v "" /t REG_SZ /d "Edit" /f
reg add "HKCR\libbinaryfile\shell\edit\command" /v "" /t REG_SZ /d "notepad \"%%1\"" /f

REM Add to Windows Explorer context menu
echo Adding context menu entries...
reg add "HKCR\Directory\Background\shell\NewLibBinaryFile" /v "" /t REG_SZ /d "lib-binary Source File" /f
reg add "HKCR\Directory\Background\shell\NewLibBinaryFile\command" /v "" /t REG_SZ /d "cmd /c \"echo func main(): > \"%%1\new.wd\" && echo     print(\"Hello, World!\") >> \"%%1\new.wd\" && echo     return 0 >> \"%%1\new.wd\" && notepad \"%%1\new.wd\"" /f

echo.
echo File association installed successfully!
echo.
echo You can now:
echo - Double-click .wd files to compile them
echo - Right-click .wd files for more options
echo - Create new .wd files from the context menu
echo.
echo To uninstall, run: uninstall_file_association.bat
echo.
pause
