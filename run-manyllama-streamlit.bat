@echo off
call env.bat

set ADDRESS=localhost
set PORT=8080

start "" "http://%ADDRESS%:%PORT%/"

:loop
python\Scripts\streamlit.exe run app.py ^
    --server.address localhost ^
    --server.port 8080 ^
    --server.headless true ^
    --browser.gatherUsageStats false
rem python\Scripts\streamlit.exe run app.py
goto :loop
