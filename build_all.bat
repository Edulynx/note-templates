@echo off
echo ============================================
echo   EduLynx - Build All Notes PDFs
echo ============================================
echo.

cd /d "%~dp0"

if not exist notes (
    echo No notes found. Create one first with new_note.bat
    echo.
    pause
    exit /b
)

set count=0
for /d %%D in (notes\*) do (
    echo Building %%~nxD...
    cd "%%D"
    lualatex -interaction=nonstopmode *.tex >nul 2>&1
    if exist *.pdf (echo   Done.) else (echo   FAILED - see troubleshooting in User Guide)
    cd "%~dp0"
    set /a count+=1
)

if %count%==0 (
    echo No notes found. Create one first with new_note.bat
) else (
    echo.
    echo ============================================
    echo   All done! PDFs are inside notes\each-note\
    echo ============================================
)
echo.
pause
