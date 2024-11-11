@echo off
cd %~dp0

echo Press ENTER to install and compile llama-cpp-python:
echo.
echo Note: you will need the following installed:
echo * Microsoft Visual C++ Build Tools (https://visualstudio.microsoft.com/downloads)
echo * CMake for Windows x64 3.31.0+ (https://cmake.org/download)
echo * NVIDIA CUDA Toolkit 12.6 (https://developer.nvidia.com/cuda-downloads)
echo.
echo (This is not necessary if you have downloaded the Windows release from GitHub.)
pause > nul

set "CMAKE_ARGS=-DGGML_CUDA=on"
set "FORCE_CMAKE=1"

python\python.exe -m pip install scikit-build-core
python\python.exe -m pip install llama-cpp-python --no-cache-dir --no-build-isolation -v

echo Done installing llama-cpp-python.
pause > nul
