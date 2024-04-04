###### Notes

* This application was written for and tested in a Debian 12 virtual machine with an NVIDIA RTX 4090, the CUDA SDK version 12.3.1, and Python 3.11.2

---

###### Prerequisites

1. Install llama-cpp-python with the following command for NVIDIA GPUs:

    ```
    CUDACXX=/usr/local/cuda-12/bin/nvcc CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade
    ```

2. Download the model to use with this application direct form Hugging Face:

    ```
    export MODEL="TheBloke/dolphin-2.6-mistral-7B-GGUF" && export MODEL_FILE="dolphin-2.6-mistral-7b.Q4_K_M.gguf" && mkdir -p "models/$MODEL" && huggingface-cli download "$MODEL" $MODEL_FILE --local-dir "models/$MODEL" --local-dir-use-symlinks False
    ```
