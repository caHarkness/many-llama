@echo off
call env.bat

python\python.exe -m pip install huggingface_hub[cli]

mkdir %MODEL_DIR%\%MODEL_REPO_WIN%
python\Scripts\huggingface-cli.exe download "%MODEL_REPO%" %MODEL_GGUF% --local-dir "%MODEL_DIR%/%MODEL_REPO_WIN%" --local-dir-use-symlinks False

echo Done downloading %MODEL_GGUF%.
pause > nul
