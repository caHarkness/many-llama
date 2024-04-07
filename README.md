###### Notes

* This application was written for and tested in a Debian 12 virtual machine with an NVIDIA RTX 4090, the CUDA SDK version 12.3.1, and Python 3.11.2

* Steps 1-5 and 7 were tested on Windows 11 with no NVIDIA support

---

###### Linux Requirements

1. Ensure the following packages are installed via `apt`:

   ```
   apt update
   apt install python3.11-venv gcc cmake build-essential
   ```

   **Note:** For Debian systems, `python3.11-venv` is required to make virtual environments

---

###### Windows Requirements

1. Install Visual Studio with C++ and CMake support: <https://learn.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio>

---

###### Setup

1. Clone this repository

2. Open a Bash shell in newly cloned repository directory

3. Create a Python 3.11.2 virtual environment:

    * For Windows users, run `python -m venv venv`

    * For Debian users, run `python3 -m venv venv`

4. Activate the newly created Python virtual environment by running `source ./venv/bin/activate`

5. Install the required packages using pip by running `pip install -r requirements.txt`

6. Optionally, reinstall `llama-cpp-python` with NVIDIA support:

    * For Debian users, run:

        ```
        CUDACXX=/usr/local/cuda-12/bin/nvcc CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade
        ```

    * For Windows users, follow this guide: https://medium.com/@piyushbatra1999/installing-llama-cpp-python-with-nvidia-gpu-acceleration-on-windows-a-short-guide-0dfac475002d

7. Start the interactive chat command line interface by running `./app.sh`

    **Note:** For Linux systems, you will need to ensure the executable bit via the following `chmod +x app.sh`

    **Note:** The first run will download the `TheBloke/dolphin-2.6-mistral-7B-GGUF` model from Hugging Face automatically. The model works with reasonable performance on even CPU-only installations. Enjoy!
