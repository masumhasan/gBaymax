"""
Simple dependency fix script

This script fixes the immediate dependency conflict issue.
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
    print("🔧 Fixing dependency conflicts...")
    
    # Step 1: Uninstall conflicting packages
    print("1. Removing conflicting packages...")
    run_command(f"{sys.executable} -m pip uninstall llama-cpp-python -y")
    
    # Step 2: Install dependencies separately
    print("2. Installing dependencies...")
    deps = ["diskcache>=5.6.1", "jinja2>=2.11.3", "numpy>=1.20.0", "typing-extensions>=4.5.0"]
    for dep in deps:
        print(f"   Installing {dep}...")
        run_command(f"{sys.executable} -m pip install {dep}")
    
    # Step 3: Install llama-cpp-python without dependencies
    print("3. Installing llama-cpp-python...")
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install llama-cpp-python==0.2.90 --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu --no-deps"
    )
    
    if success:
        print("✅ llama-cpp-python installed successfully!")
        
        # Test import
        success, stdout, stderr = run_command(
            f"{sys.executable} -c \"import llama_cpp; print('Import successful!')\""
        )
        
        if success:
            print("✅ Installation test passed!")
        else:
            print(f"❌ Import test failed: {stderr}")
            
    else:
        print(f"❌ Installation failed: {stderr}")
        
    # Step 4: Install remaining requirements
    print("4. Installing remaining requirements...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    print("🎉 Done!")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
