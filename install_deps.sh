#!/bin/bash
set -e  # Exit immediately if any command fails

# Initialize flag for Ollama installation (default: disabled)
INSTALL_OLLAMA=false

# Function to print help information
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Install system dependencies for VisionInfer (with optional Ollama backend)"
    echo ""
    echo "Options:"
    echo "  --backend ollama   Install Ollama in addition to core system dependencies"
    echo "  -h, --help         Show this help message and exit"
    echo ""
    echo "Examples:"
    echo "  Install only core dependencies:  $0"
    echo "  Install core dependencies + Ollama:  $0 --backend ollama"
}

# Parse command line arguments (POSIX compatible)
while [ $# -gt 0 ]; do
    case "$1" in
        --backend)
            if [ "$2" = "ollama" ]; then
                INSTALL_OLLAMA=true
                shift 2  # Skip --backend and ollama
            else
                echo "Error: Invalid argument for --backend. Only 'ollama' is supported."
                print_help
                exit 1
            fi
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'"
            print_help
            exit 1
            ;;
    esac
done

# Print welcome message and reminders
echo "============================================="
echo "Starting to install system dependencies for VisionInfer"
echo "Note: This script requires sudo privileges (for apt package installation). Ensure your current user has sudo access."
echo "============================================="

# Install core system dependencies (ffmpeg, python3-pip, pipx)
echo "Step 1: Update apt package index and install core system dependencies..."
sudo apt update && sudo apt install -y ffmpeg python3-pip pipx

# Install Ollama only if the flag is enabled (POSIX compatible)
if [ "$INSTALL_OLLAMA" = true ]; then
    echo "Step 2: Install Ollama backend..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Step 2: Skipping Ollama installation (--backend ollama not specified)"
fi

# Post-installation confirmation
echo "============================================="
echo "✅ Installation completed!"
echo "Core dependencies verified: Run 'pipx --version' (pipx) / 'ffmpeg -version' (ffmpeg)"
if [ "$INSTALL_OLLAMA" = true ]; then
    echo "Ollama verified: Run 'ollama --version'"
fi
echo "============================================="