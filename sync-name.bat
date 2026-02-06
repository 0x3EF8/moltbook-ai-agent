@echo off
REM Sync agent name from config/register.json to documentation files
echo.
echo Syncing agent name...
echo.
python scripts\sync_agent_name.py
echo.
pause
