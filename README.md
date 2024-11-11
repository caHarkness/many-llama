# Many Llama

Many Llama is a lightweight, locally running ChatGPT clone made with Streamlit

---

###### Quick Start

1. Get the latest Windows release of this project on GitHub.

2. Run `install-streamlit.bat` to install Streamlit.

3. Run `download-model.bat` to download the CapybaraHermes-2.5-Mistral-7B large language model.

    **Note:** This download is just under 4 GB and will also require an NVIDIA GPU with 4 GB of VRAM to run properly.

4. Run `run-manyllama-streamlit.bat` to start the Many Llama web interface. A browser tab should open automatically.

---

###### Linux Installation

1. Make sure `build-essentials` and `cmake` are installed.

2. Make sure the CUDA toolkit is properly installed via <https://docs.nvidia.com/cuda/cuda-installation-guide-linux>.

3. Create a Python 3.11+ virtual environment using `python3 -m venv venv`.

4. Activate the virtual environment using `source ./venv/bin/activate`.

5. Install the following pip packages using:

    * `pip install llama-cpp-python`
    * `pip install streamlit`

6. Run the Streamlit application via `streamlit run app.py --server.address 0.0.0.0 --server.port 8080`.

    **Note:** Specifying the `--server.address 0.0.0.0` option allows other hosts to access this Streamlit application.
