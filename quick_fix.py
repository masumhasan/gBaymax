"""
Quick fix for llama-cpp-python installation on Windows

This script uses precompiled wheels to avoid compilation issues.
"""

import subprocess
import sys

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Quick fix for llama-cpp-python installation")
    print("=" * 50)
    
    # Update pip first
    print("📦 Updating pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Try precompiled wheels
    commands = [
        # Try CPU-only precompiled wheel
        f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu",
        # Try CUDA if available
        f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cu121",
        # Fallback to binary-only
        f"{sys.executable} -m pip install llama-cpp-python --only-binary=llama-cpp-python",
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n🔧 Attempt {i}:")
        print(f"Running: {cmd}")
        
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print("✅ Success!")
            print("🎉 llama-cpp-python installed successfully!")
            
            # Test the installation
            print("\n🧪 Testing installation...")
            test_success, test_stdout, test_stderr = run_command(
                f"{sys.executable} -c \"import llama_cpp; print('Import successful!')\""
            )
            
            if test_success:
                print("✅ Import test passed!")
                print("🚀 Ready to use local models!")
                return True
            else:
                print(f"❌ Import test failed: {test_stderr}")
                
        else:
            print(f"❌ Failed: {stderr[:100]}...")
    
    print("\n❌ All attempts failed!")
    print("Please try the full installation script: python install_windows.py")
    return False

if __name__ == "__main__":
    if main():
        print("\n✅ Installation complete!")
        print("Next steps:")
        print("1. Run: python test_local_llm.py")
        print("2. Run: python nagent.py")
    else:
        print("\n❌ Installation failed!")
        print("Try: python install_windows.py")
    
    input("\nPress Enter to exit...")
