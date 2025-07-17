"""
Installation script for local LLM dependencies

This script helps install the necessary dependencies for running
the local Llama.cpp model with GPU support if available.
"""

import subprocess
import sys
import os
import platform

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_gpu_support():
    """Check if GPU support is available"""
    try:
        # Check for NVIDIA GPU
        success, stdout, stderr = run_command("nvidia-smi")
        if success:
            print("✅ NVIDIA GPU detected")
            return "cuda"
        
        # Check for AMD GPU (ROCm)
        if platform.system() == "Linux":
            success, stdout, stderr = run_command("rocm-smi")
            if success:
                print("✅ AMD GPU with ROCm detected")
                return "rocm"
        
        print("ℹ️  No GPU support detected, will use CPU")
        return "cpu"
    
    except Exception as e:
        print(f"⚠️  Error checking GPU support: {e}")
        return "cpu"

def install_llama_cpp_python():
    """Install llama-cpp-python with appropriate configuration"""
    gpu_type = check_gpu_support()
    
    print("🔧 Installing llama-cpp-python...")
    
    # Check for Windows and suggest precompiled wheels
    if platform.system() == "Windows":
        print("🪟 Windows detected - trying precompiled wheels first...")
        
        # Try precompiled wheels first (faster and avoids compilation issues)
        precompiled_commands = [
            # Try CPU-only precompiled wheel
            f"{sys.executable} -m pip install llama-cpp-python --only-binary=llama-cpp-python",
            # Try with specific index
            f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu",
        ]
        
        if gpu_type == "cuda":
            print("🚀 Trying CUDA precompiled wheels...")
            precompiled_commands.insert(0, 
                f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cu121"
            )
        
        # Try precompiled wheels first
        for cmd in precompiled_commands:
            print(f"📦 Trying: {cmd}")
            success, stdout, stderr = run_command(cmd)
            if success:
                print("✅ llama-cpp-python installed successfully with precompiled wheels!")
                return True
            else:
                print(f"⚠️ Failed: {stderr[:200]}...")
        
        # If precompiled wheels fail, try manual compilation
        print("🔨 Precompiled wheels failed, attempting manual compilation...")
        print("⚠️ This requires Visual Studio Build Tools or Visual Studio with C++ support")
        print("⚠️ You can install them from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        
        # Check for Visual Studio Build Tools
        vs_paths = [
            "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\Common7\\Tools\\VsDevCmd.bat",
            "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\Common7\\Tools\\VsDevCmd.bat",
            "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat",
            "C:\\Program Files\\Microsoft Visual Studio\\2019\\Community\\Common7\\Tools\\VsDevCmd.bat",
        ]
        
        vs_found = False
        for vs_path in vs_paths:
            if os.path.exists(vs_path):
                vs_found = True
                break
        
        if not vs_found:
            print("❌ Visual Studio Build Tools not found!")
            print("🔧 Please install Visual Studio Build Tools:")
            print("   1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
            print("   2. Install with 'C++ build tools' workload")
            print("   3. Restart your terminal and try again")
            return False
    
    # Original compilation approach
    if gpu_type == "cuda":
        print("📦 Installing with CUDA support...")
        # For CUDA support
        env = os.environ.copy()
        env["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
        env["FORCE_CMAKE"] = "1"
        
        success, stdout, stderr = run_command(
            f"{sys.executable} -m pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir"
        )
        
    elif gpu_type == "rocm":
        print("📦 Installing with ROCm support...")
        # For ROCm support
        env = os.environ.copy()
        env["CMAKE_ARGS"] = "-DLLAMA_HIPBLAS=on"
        env["FORCE_CMAKE"] = "1"
        
        success, stdout, stderr = run_command(
            f"{sys.executable} -m pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir"
        )
        
    else:
        print("📦 Installing CPU-only version...")
        # CPU-only installation
        success, stdout, stderr = run_command(
            f"{sys.executable} -m pip install llama-cpp-python"
        )
    
    if success:
        print("✅ llama-cpp-python installed successfully!")
        return True
    else:
        print(f"❌ Failed to install llama-cpp-python: {stderr}")
        print("\n🔧 Troubleshooting suggestions:")
        if platform.system() == "Windows":
            print("1. Install Visual Studio Build Tools with C++ support")
            print("2. Try the precompiled wheels approach above")
            print("3. Use conda instead: conda install -c conda-forge llama-cpp-python")
        print("4. Check the GitHub issues: https://github.com/abetlen/llama-cpp-python/issues")
        return False

def install_requirements():
    """Install all requirements"""
    print("📦 Installing requirements...")
    
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install -r requirements.txt"
    )
    
    if success:
        print("✅ Requirements installed successfully!")
        return True
    else:
        print(f"❌ Failed to install requirements: {stderr}")
        return False

def main():
    """Main installation function"""
    print("🚀 Local LLM Setup Script")
    print("=" * 40)
    
    # Check if model file exists
    model_path = "models/gemma-3n-E2B-it-IQ4_XS.gguf"
    if not os.path.exists(model_path):
        print(f"⚠️  Model file not found: {model_path}")
        print("Please ensure the Gemma model is in the models directory.")
        return False
    else:
        print(f"✅ Model file found: {model_path}")
    
    # Install requirements first
    if not install_requirements():
        return False
    
    # Install llama-cpp-python with GPU support if available
    if not install_llama_cpp_python():
        return False
    
    print("\n🎉 Installation completed successfully!")
    print("\nNext steps:")
    print("1. Run the agent: python nagent.py")
    print("2. Test text chat: python text_chat_example.py")
    print("3. Use the HTML client: open test_client.html")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
