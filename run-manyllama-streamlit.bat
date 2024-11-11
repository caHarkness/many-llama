@echo off
call env.bat

:loop
python\Scripts\streamlit.exe run app.py --server.address localhost --server.port 8080
rem python\Scripts\streamlit.exe run app.py
goto :loop
