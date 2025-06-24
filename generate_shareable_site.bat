@echo off
echo BeRAM Website - Static Site Generator
echo =====================================
echo.
echo This script will create a shareable version of the BeRAM website.
echo.
echo Step 1: Installing required packages...
pip install requests beautifulsoup4
echo.
echo Step 2: Starting the Flask application...
start cmd /k "python run.py"
echo.
echo Step 3: Waiting for Flask to start...
timeout /t 5
echo.
echo Step 4: Generating static site...
python static_site_generator.py
echo.
echo Step 5: Creating ZIP file...
powershell Compress-Archive -Path beram_static_site -DestinationPath BeRAM_Website_Shareable.zip -Force
echo.
echo =====================================
echo COMPLETE! The shareable website has been created.
echo.
echo You can find the following files:
echo - beram_static_site folder: Contains the static website
echo - BeRAM_Website_Shareable.zip: Compressed version ready to share
echo.
echo To share with investors:
echo 1. Send them the BeRAM_Website_Shareable.zip file
echo 2. They can extract it and open index.html in any browser
echo 3. No installation or technical skills required
echo.
pause
