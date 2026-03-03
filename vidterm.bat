@echo off
REM Terminal ASCII Video Player - Windows Batch Launcher

if "%~1"=="" (
    echo Usage: vidterm.bat "VIDEO_URL" [--quality 480p] [--pure-at]
    echo.
    echo Examples:
    echo   vidterm.bat "https://www.youtube.com/watch?v=XXXXXXXXXXX"
    echo   vidterm.bat "https://www.youtube.com/watch?v=XXX" --quality 720p
    echo   vidterm.bat "https://x.com/user/status/000" --pure-at
    echo.
    exit /b 1
)

python "%~dp0vidterm.py" %*
pause
