@echo off
setlocal

cd /d "%~dp0\.."

if not defined MINIMAX_MODEL set "MINIMAX_MODEL=MiniMax-M3"
if not defined MINIMAX_BASE_URL set "MINIMAX_BASE_URL=https://api.minimaxi.com/v1"
if not defined UAV_CVGL_COOKIE_FILE set "UAV_CVGL_COOKIE_FILE=C:\tmp\uav_cvgl_cookies.txt"
if not defined LEADERBOARD_DISCOVERY_TIMEOUT set "LEADERBOARD_DISCOVERY_TIMEOUT=300"

if not defined MINIMAX_API_KEY (
  echo MINIMAX_API_KEY is not set. Set it in this CMD window before running review.
  pause
  exit /b 2
)

if not exist "%UAV_CVGL_COOKIE_FILE%" (
  echo Cookie file not found: %UAV_CVGL_COOKIE_FILE%
  echo Run scripts\init_carsi_login.py first, complete browser login, and press Enter there to export cookies.
  pause
  exit /b 2
)

set "PYTHON_EXE=D:\anaconda\envs\dinov3\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

echo Repository: %CD%
echo Cookie file: %UAV_CVGL_COOKIE_FILE%
echo MiniMax model: %MINIMAX_MODEL%
echo Paper timeout: %LEADERBOARD_DISCOVERY_TIMEOUT%s
echo.

"%PYTHON_EXE%" scripts\rebuild_leaderboards.py review --datasets University-1652 SUES-200 DenseUAV UAV-VisLoc GTA-UAV Game4Loc --use-pdf --require-accessible-fulltext --force --force-fulltext --title-regex "Contrastive Learning Based Visual Place Recognition|Direction-Guided Multiscale|Focal Hanning Loss|MMHCA|Modern Backbone|Navigating the Metaverse" --paper-timeout %LEADERBOARD_DISCOVERY_TIMEOUT% --progress-every 1
if errorlevel 1 goto done

"%PYTHON_EXE%" scripts\rebuild_leaderboards.py build
if errorlevel 1 goto done

"%PYTHON_EXE%" scripts\rebuild_leaderboards.py validate

:done
echo.
echo Remaining full-text retry finished with exit code %ERRORLEVEL%.
pause
