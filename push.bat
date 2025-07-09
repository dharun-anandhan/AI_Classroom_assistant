@echo off
echo --------------------------------------
echo Pushing code to GitHub...
echo --------------------------------------

REM Stage all changes
git add .

REM Prompt for commit message
set /p message="Enter commit message: "
git commit -m "%message%"

REM Push to GitHub
git push origin main

echo --------------------------------------
echo Push complete!
pause
