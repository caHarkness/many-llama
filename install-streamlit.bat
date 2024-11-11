@echo off
call env.bat

echo Press ENTER to install Streamlit:
echo Note: you will need to reinstall this every time you move this repository!
pause > nul

python\python.exe -m pip install streamlit --force

echo Done installing Streamlit.
pause > nul
