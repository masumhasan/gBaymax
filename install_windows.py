"""
Windows-specific installation script for llama-cpp-python

This script provides multiple installation methods for Windows users
to work around common compilation issues.
"""

import subprocess
import sys
import os
import platform
import urllib.request
import json

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_visual_studio():
    """Check if Visual Studio Build Tools are installed"""
    vs_paths = [
        "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\Common7\\Tools\\VsDevCmd.bat",
        "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\Common7\\Tools\\VsDevCmd.bat",
        "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat",
        "C:\\Program Files\\Microsoft Visual Studio\\2019\\Community\\Common7\\Tools\\VsDevCmd.bat",
        "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\Enterprise\\Common7\\Tools\\VsDevCmd.bat",
        "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Enterprise\\Common7\\Tools\\VsDevCmd.bat",
    ]
    
    for vs_path in vs_paths:
        if os.path.exists(vs_path):
            return True, vs_path
    
    return False, None

def install_precompiled_wheels():
    """Try to install precompiled wheels"""
    print("🚀 Attempting to install precompiled wheels...")
    
    # Different precompiled wheel sources
    wheel_sources = [
        # CPU-only wheels
        {
            "name": "CPU-only (abetlen)",
            "url": "https://abetlen.github.io/llama-cpp-python/whl/cpu",
            "command": f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu"
        },
        # CUDA wheels (if NVIDIA GPU detected)
        {
            "name": "CUDA 12.1 (abetlen)",
            "url": "https://abetlen.github.io/llama-cpp-python/whl/cu121",
            "command": f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cu121"
        },
        # Alternative: Try binary-only from PyPI
        {
            "name": "Binary-only PyPI",
            "url": "https://pypi.org",
            "command": f"{sys.executable} -m pip install llama-cpp-python --only-binary=llama-cpp-python"
        }
    ]
    
    # Check for NVIDIA GPU
    has_nvidia, _, _ = run_command("nvidia-smi")
    if not has_nvidia:
        # Remove CUDA wheels if no NVIDIA GPU
        wheel_sources = [w for w in wheel_sources if "CUDA" not in w["name"]]
    
    for source in wheel_sources:
        print(f"📦 Trying {source['name']}...")
        success, stdout, stderr = run_command(source["command"])
        
        if success:
            print(f"✅ Successfully installed from {source['name']}!")
            return True
        else:
            print(f"❌ Failed: {stderr[:100]}...")
    
    return False

def install_with_conda():
    """Try to install with conda"""
    print("🐍 Attempting conda installation...")
    
    # Check if conda is available
    conda_available, _, _ = run_command("conda --version")
    
    if conda_available:
        print("📦 Installing with conda...")
        success, stdout, stderr = run_command("conda install -c conda-forge llama-cpp-python")
        
        if success:
            print("✅ Successfully installed with conda!")
            return True
        else:
            print(f"❌ Conda installation failed: {stderr[:100]}...")
    else:
        print("❌ Conda not available")
    
    return False

def install_with_compilation():
    """Try to install with compilation"""
    print("🔨 Attempting compilation installation...")
    
    # Check for Visual Studio
    vs_available, vs_path = check_visual_studio()
    
    if not vs_available:
        print("❌ Visual Studio Build Tools not found!")
        print("🔧 Please install Visual Studio Build Tools:")
        print("   1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("   2. Install with 'C++ build tools' workload")
        print("   3. Restart your terminal and try again")
        return False
    
    print(f"✅ Found Visual Studio at: {vs_path}")
    
    # Try compilation
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install llama-cpp-python --no-cache-dir")
    
    if success:
        print("✅ Successfully compiled and installed!")
        return True
    else:
        print(f"❌ Compilation failed: {stderr[:200]}...")
        return False

def download_alternative_model():
    """Suggest alternative models or approaches"""
    print("🔄 Alternative approaches:")
    print("1. Use a different model format (e.g., ONNX)")
    print("2. Use cloud-based models (OpenAI, Google, etc.)")
    print("3. Try Ollama (easier local model management)")
    print("4. Use Docker with pre-built images")
    
    print("\n🐳 Docker approach:")
    print("docker run -it --rm -v $(pwd):/app python:3.11 bash")
    print("cd /app && pip install llama-cpp-python")

def main():
    """Main installation function"""
    print("🪟 Windows llama-cpp-python Installation Helper")
    print("=" * 50)
    
    if platform.system() != "Windows":
        print("❌ This script is designed for Windows only!")
        return False
    
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Method 1: Try precompiled wheels
    print("\n🚀 Method 1: Precompiled Wheels")
    if install_precompiled_wheels():
        print("🎉 Installation successful!")
        return True
    
    # Method 2: Try conda
    print("\n🐍 Method 2: Conda Installation")
    if install_with_conda():
        print("🎉 Installation successful!")
        return True
    
    # Method 3: Try compilation
    print("\n🔨 Method 3: Compilation")
    if install_with_compilation():
        print("🎉 Installation successful!")
        return True
    
    # All methods failed
    print("\n❌ All installation methods failed!")
    download_alternative_model()
    
    print("\n🔧 Manual installation steps:")
    print("1. Install Visual Studio Build Tools with C++ support")
    print("2. Restart your terminal")
    print("3. Run: pip install llama-cpp-python --no-cache-dir")
    print("4. If still failing, try: pip install llama-cpp-python --no-binary llama-cpp-python")
    
    return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Ready to test!")
        print("Run: python test_local_llm.py")
    else:
        print("\n❌ Installation failed. Please try the suggested alternatives.")
        
    input("\nPress Enter to exit...")
