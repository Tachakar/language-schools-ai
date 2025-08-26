## 1. Setup
- Create python venv: `python3 -m venv .venv`
- Install requirements: `pip install -r requirements.txt`
- Ensure your machine has **cuBLAS (CUDA 12)** and **cuDNN 9 (CUDA 12)**  
  → [Installation guide]([https://github.com/guillaumekln/faster-whisper#installation](https://github.com/SYSTRAN/faster-whisper?tab=readme-ov-file#requirements))

## 2. Run
- Export your API key:  
  `export YOUTUBE_API_KEY="your_api_key_here"`
- Run pipeline:  
  `python main.py`
