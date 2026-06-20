@echo off
setlocal

cd /d "%~dp0\.."

if not defined MINIMAX_MODEL set "MINIMAX_MODEL=MiniMax-M3"
if not defined MINIMAX_BASE_URL set "MINIMAX_BASE_URL=https://api.minimaxi.com/v1"
if not defined LEADERBOARD_DISCOVERY_TIMEOUT set "LEADERBOARD_DISCOVERY_TIMEOUT=300"
if not defined LEADERBOARD_REVIEW_PROGRESS set "LEADERBOARD_REVIEW_PROGRESS=25"

if not defined MINIMAX_API_KEY (
  echo MINIMAX_API_KEY is not set. Set it in this CMD window before running review.
  echo Example:
  echo   set MINIMAX_API_KEY=your_key_here
  pause
  exit /b 2
)

set "PYTHON_EXE=D:\anaconda\envs\dinov3\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

echo Repository: %CD%
echo MiniMax model: %MINIMAX_MODEL%
echo MiniMax base URL: %MINIMAX_BASE_URL%
echo Paper timeout: %LEADERBOARD_DISCOVERY_TIMEOUT%s
echo Progress every: %LEADERBOARD_REVIEW_PROGRESS%
echo Search tools override: MINIMAX_SEARCH_TOOLS_JSON or MINIMAX_SEARCH_TOOL_VARIANTS_JSON
echo.

"%PYTHON_EXE%" scripts\rebuild_leaderboards.py review --datasets University-1652 SUES-200 DenseUAV UAV-VisLoc GTA-UAV Game4Loc --use-pdf --require-accessible-fulltext --paper-timeout %LEADERBOARD_DISCOVERY_TIMEOUT% --progress-every %LEADERBOARD_REVIEW_PROGRESS% %*

echo.
echo Review command finished with exit code %ERRORLEVEL%.
pause
