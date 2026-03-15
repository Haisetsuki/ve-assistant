@echo off
cd /d "%~dp0"
pushd "%~dp0vidl"  || (echo vidl folder not found & pause & exit /b 1)
call ".venv\Scripts\activate.bat"
python main.py
popd
pause
