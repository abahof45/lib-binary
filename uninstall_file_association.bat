@echo off
REM Windows File Association Uninstaller for lib-binary .wd files
REM This script removes file associations and registry entries

echo Uninstalling lib-binary file associations...

REM Remove file type association
echo Removing file type association...
assoc .wd=

REM Remove registry entries
echo Removing registry entries...
reg delete "HKCR\libbinaryfile" /f
reg delete "HKCR\libbinaryfile\DefaultIcon" /f
reg delete "HKCR\libbinaryfile\shell" /f
reg delete "HKCR\libbinaryfile\shell\compile" /f
reg delete "HKCR\libbinaryfile\shell\compile\command" /f
reg delete "HKCR\libbinaryfile\shell\compileandrun" /f
reg delete "HKCR\libbinaryfile\shell\compileandrun\command" /f
reg delete "HKCR\libbinaryfile\shell\edit" /f
reg delete "HKCR\libbinaryfile\shell\edit\command" /f

REM Remove context menu entry
echo Removing context menu entry...
reg delete "HKCR\Directory\Background\shell\NewLibBinaryFile" /f
reg delete "HKCR\Directory\Background\shell\NewLibBinaryFile\command" /f

echo.
echo File association uninstalled successfully!
echo.
echo You may need to restart Windows Explorer to see the changes.
echo.
pause
