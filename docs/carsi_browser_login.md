# CARSI Browser Login Workflow

Use this workflow when publisher pages require institution access, CAPTCHA, or two-factor login.

The automation uses a dedicated visible Chromium profile instead of your daily browser profile.

## One-Time Setup

Install Playwright in the Python environment:

```cmd
D:\anaconda\envs\dinov3\python.exe -m pip install playwright
D:\anaconda\envs\dinov3\python.exe -m playwright install chromium
```

## Initialize Login

```cmd
set UAV_CVGL_BROWSER_PROFILE=D:\agent_browser_profile
set UAV_CVGL_COOKIE_FILE=C:\tmp\uav_cvgl_cookies.txt
set UAV_CVGL_DOWNLOAD_DIR=C:\tmp\uav_cvgl_downloads

D:\anaconda\envs\dinov3\python.exe scripts\init_carsi_login.py
```

The script opens a visible Chromium window with:

- IEEE Xplore
- ACM Digital Library
- SpringerLink
- ScienceDirect

Complete institution login manually in the browser:

1. Choose institutional sign-in, Shibboleth, OpenAthens, or CARSI.
2. Search for Sun Yat-sen University if needed.
3. Complete the SYSU CAS login, CAPTCHA, and any second-factor step.
4. Open a paper/PDF page and confirm access.
5. Return to the terminal and press Enter.

The script exports a Netscape-format cookie file to `UAV_CVGL_COOKIE_FILE`, which the leaderboard scripts can use through Python requests.

## Open a Single Publisher Page Later

```cmd
D:\anaconda\envs\dinov3\python.exe scripts\open_publisher_page.py https://ieeexplore.ieee.org/document/10520320/ --export-cookies
```

Use the visible browser to complete any extra login prompt. Press Enter in the terminal to export refreshed cookies.

## Resume Leaderboard Discovery

```cmd
set UAV_CVGL_COOKIE_FILE=C:\tmp\uav_cvgl_cookies.txt
set MINIMAX_API_KEY=your_minimax_key

D:\anaconda\envs\dinov3\python.exe scripts\rebuild_leaderboards.py review --datasets University-1652 SUES-200 DenseUAV UAV-VisLoc GTA-UAV Game4Loc --use-pdf --require-accessible-fulltext --force --force-fulltext --title-regex "Contrastive Learning Based Visual Place Recognition|Direction-Guided Multiscale|Focal Hanning Loss|MMHCA|Modern Backbone|Navigating the Metaverse" --paper-timeout 300 --progress-every 1
```

Do not commit browser profiles, exported cookies, downloaded PDFs, or real API keys.
