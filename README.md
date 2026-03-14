# vinfer
Lightweight VLM Inference Tool (supports camera/VOD/live stream)

## Install
### 1. Install system dependencies
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Install FFmpeg (Ubuntu/Debian)
sudo apt install ffmpeg libgl1-mesa-glx

# Install pipx (for isolated run)
python3 -m pip install --user pipx
python3 -m pipx ensurepath