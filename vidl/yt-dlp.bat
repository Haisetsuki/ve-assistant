@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "OUTDIR=%~dp0Clips"
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

set /p "LINK=Please ENTER the Link: "

if not defined LINK (
    echo No link entered.
    pause
    exit /b 1
)

rem Get the date as MMDDYY
for /f %%A in ('powershell -NoProfile -Command "Get-Date -Format MMddyy"') do set "TODAY=%%A"

rem Detect the source
set "SOURCE=Unknown"
set "TEST=!LINK!"

if not "!TEST:youtube.com=!"=="!TEST!" set "SOURCE=Youtube"
if not "!TEST:youtu.be=!"=="!TEST!" set "SOURCE=Youtube"
if not "!TEST:facebook.com=!"=="!TEST!" set "SOURCE=Facebook"
if not "!TEST:fb.watch=!"=="!TEST!" set "SOURCE=Facebook"
if not "!TEST:twitter.com=!"=="!TEST!" set "SOURCE=Twitter"
if not "!TEST:x.com=!"=="!TEST!" set "SOURCE=Twitter"
if not "!TEST:instagram.com=!"=="!TEST!" set "SOURCE=Instagram"

rem Find the next available iteration number
set /a ITERATION=1

:CHECK_FILENAME
if exist "%OUTDIR%\!TODAY! !SOURCE! - !ITERATION!.*" (
    set /a ITERATION+=1
    goto CHECK_FILENAME
)

set "OUTPUT=%OUTDIR%\!TODAY! !SOURCE! - !ITERATION!.%%(ext)s"

echo.
echo Downloading as:
echo !TODAY! !SOURCE! - !ITERATION!
echo.

yt-dlp.exe ^
    -f "bv*+ba/b" ^
    --merge-output-format mp4 ^
    --windows-filenames ^
    --no-overwrites ^
    -o "!OUTPUT!" ^
    "!LINK!"

echo.
if errorlevel 1 (
    echo Download failed.
) else (
    echo Download complete.
)

pause
