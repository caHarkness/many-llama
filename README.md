###### Notes

* This application was written for and tested in a Debian 12 virtual machine with an NVIDIA RTX 4090, the CUDA SDK version 12.3.1, and Python 3.11.2

---

###### Setup

1. Install the required software:

    * For Debian users, run the following:

        ```
        apt update
        apt install python3.11-venv gcc cmake build-essential
        ```

    * For Windows users, follow the guide to install Visual Studio C++ with CMake support: <https://learn.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio>

2. Clone this repository and change to its directory with the following two commands:

    ```
    git clone https://github.com/caHarkness/many-llama.git
    cd many-llama
    ```

3. Open a Bash shell in the newly cloned repository directory by running `bash`

4. Create a Python 3.11.2 virtual environment:

    * For Debian users, run `python3 -m venv venv`

    * For Windows users, run `python -m venv venv`

5. Activate the newly created Python virtual environment:

    * For Debian users, run `source ./venv/bin/activate`
    
    * For Windows users, run `source ./venv/Scripts/activate`

6. Install the required packages using pip by running `pip install -r requirements.txt`

    **Note:** if the required C++ build tools, including CMake, are not installed, this step will fail when attempting to build `llama-cpp-python`

7. Optionally, reinstall `llama-cpp-python` with NVIDIA support:

    * For Debian users, run:

        ```
        CUDACXX=/usr/local/cuda-12/bin/nvcc CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade
        ```

    * For Windows users, follow this guide: https://medium.com/@piyushbatra1999/installing-llama-cpp-python-with-nvidia-gpu-acceleration-on-windows-a-short-guide-0dfac475002d

        **Note:** This guide outlines how to install Visual Studio with C++ with CMake support. The takeaways from the guide are the following:

        * Install the CUDA 12.3 SDK

        * Ensure CUDA is installed by running `nvcc --version` and that the variable CUDA_PATH is set by running `echo $CUDA_PATH` in Bash

        * Run the following line-by-line in Bash:

            ```
            export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
            export FORCE_CMAKE="1"
            pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
            ```

8. Start the interactive chat command line interface by running `./app.sh`

    **Note:** For Linux systems, you will need to ensure the executable bit via the following `chmod +x app.sh`

    **Note:** The first run will download the `TheBloke/dolphin-2.6-mistral-7B-GGUF` model from Hugging Face automatically. The model works with reasonable performance on even CPU-only installations. Enjoy!
