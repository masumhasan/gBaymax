"""
Fixed installation script for llama-cpp-python with dependency resolution

This script handles the dependency conflicts and ensures proper installation.
"""

import subprocess
import sys
import os
import time

def run_command(command, timeout=300):
    """Run a command with timeout and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def install_dependencies_first():
    """Install dependencies that might conflict first"""
    print("📦 Installing dependencies to avoid conflicts...")
    
    dependencies = [
        "diskcache>=5.6.1",
        "jinja2>=2.11.3", 
        "numpy>=1.20.0",
        "typing-extensions>=4.5.0"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        success, stdout, stderr = run_command(f"{sys.executable} -m pip install {dep}")
        if not success:
            print(f"⚠️ Warning: Failed to install {dep}: {stderr[:100]}...")
        else:
            print(f"✅ {dep} installed")

def uninstall_conflicting_packages():
    """Remove any conflicting packages"""
    print("🧹 Cleaning up conflicting packages...")
    
    # Remove llama-cpp-python if it exists
    run_command(f"{sys.executable} -m pip uninstall llama-cpp-python -y")
    
    print("✅ Cleanup complete")

def install_llama_cpp_python():
    """Install llama-cpp-python with specific version to avoid conflicts"""
    print("🔧 Installing llama-cpp-python...")
    
    # Try different approaches in order of preference
    installation_methods = [
        # Method 1: Specific version from precompiled wheels
        {
            "name": "Specific version (v0.2.90) from CPU wheels",
            "command": f"{sys.executable} -m pip install llama-cpp-python==0.2.90 --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu --force-reinstall --no-deps"
        },
        # Method 2: Latest compatible version
        {
            "name": "Latest compatible version",
            "command": f"{sys.executable} -m pip install llama-cpp-python==0.2.90 --force-reinstall"
        },
        # Method 3: Install without dependencies first, then install deps
        {
            "name": "Install without dependencies",
            "command": f"{sys.executable} -m pip install llama-cpp-python --no-deps --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu"
        },
        # Method 4: Force install latest from wheels
        {
            "name": "Force install from wheels",
            "command": f"{sys.executable} -m pip install llama-cpp-python --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu --force-reinstall --no-cache-dir"
        }
    ]
    
    for method in installation_methods:
        print(f"\n🔧 Trying: {method['name']}")
        print(f"Command: {method['command']}")
        
        success, stdout, stderr = run_command(method['command'], timeout=600)
        
        if success:
            print(f"✅ Success with {method['name']}!")
            return True
        else:
            print(f"❌ Failed: {stderr[:200]}...")
            time.sleep(2)  # Wait between attempts
    
    return False

def install_remaining_dependencies():
    """Install remaining dependencies after llama-cpp-python"""
    print("📦 Installing remaining dependencies...")
    
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    if success:
        print("✅ All dependencies installed!")
        return True
    else:
        print(f"⚠️ Some dependencies failed: {stderr[:200]}...")
        return False

def test_installation():
    """Test if llama-cpp-python is working"""
    print("🧪 Testing llama-cpp-python installation...")
    
    success, stdout, stderr = run_command(
        f"{sys.executable} -c \"import llama_cpp; print('✅ llama-cpp-python imported successfully!')\""
    )
    
    if success:
        print("✅ Installation test passed!")
        return True
    else:
        print(f"❌ Installation test failed: {stderr}")
        return False

def main():
    """Main installation function"""
    print("🚀 Fixed llama-cpp-python Installation Script")
    print("=" * 50)
    
    # Step 1: Update pip
    print("📦 Updating pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Step 2: Clean up any existing installations
    uninstall_conflicting_packages()
    
    # Step 3: Install dependencies that might conflict
    install_dependencies_first()
    
    # Step 4: Install llama-cpp-python
    if not install_llama_cpp_python():
        print("❌ Failed to install llama-cpp-python!")
        print("\n🔧 Manual installation steps:")
        print("1. pip uninstall llama-cpp-python -y")
        print("2. pip install diskcache>=5.6.1")
        print("3. pip install llama-cpp-python==0.2.90 --index-url https://abetlen.github.io/llama-cpp-python/whl/cpu --no-deps")
        print("4. pip install jinja2>=2.11.3")
        return False
    
    # Step 5: Install remaining dependencies
    install_remaining_dependencies()
    
    # Step 6: Test the installation
    if test_installation():
        print("\n🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Test the local model: python test_local_llm.py")
        print("2. Run the agent: python nagent.py")
        print("3. Test text chat: python text_chat_example.py")
        return True
    else:
        print("\n❌ Installation completed but testing failed!")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n🔧 Alternative installation method:")
        print("Try installing with conda:")
        print("conda install -c conda-forge llama-cpp-python")
        
    input("\nPress Enter to exit...")
