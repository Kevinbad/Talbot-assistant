@echo off
echo Ejecutando ingest.py...
python ingest.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Ejecutando index.py...
python index.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Build completado.
pause