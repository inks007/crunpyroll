#!/usr/bin/env python3
"""
Docker-compatible installation script for crunpyroll package.
This script handles setuptools/distutils compatibility issues in Docker environments.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, 
            check=check, 
            capture_output=capture_output, 
            text=True
        )
        if capture_output:
            print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if capture_output:
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
        raise

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 7):
        raise RuntimeError("Python 3.7 or higher is required")

def upgrade_pip_and_setuptools():
    """Upgrade pip and setuptools to compatible versions."""
    print("Upgrading pip and setuptools...")
    
    # Upgrade pip first
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install specific setuptools version that works well with Python 3.11
    run_command([
        sys.executable, "-m", "pip", "install", 
        "setuptools>=61.0,<70.0", 
        "wheel>=0.37.0"
    ])

def install_build_dependencies():
    """Install build dependencies."""
    print("Installing build dependencies...")
    run_command([
        sys.executable, "-m", "pip", "install",
        "build>=0.8.0",
        "packaging>=21.0"
    ])

def install_crunpyroll():
    """Install crunpyroll package with different methods."""
    repo_url = "git+https://github.com/Pixel-LH/crunpyroll.git"
    
    methods = [
        # Method 1: Use PEP 517 with no build isolation
        {
            "name": "PEP 517 with no build isolation",
            "cmd": [
                sys.executable, "-m", "pip", "install",
                "--use-pep517", "--no-build-isolation",
                repo_url
            ]
        },
        # Method 2: Use legacy setup.py method
        {
            "name": "Legacy setup.py method",
            "cmd": [
                sys.executable, "-m", "pip", "install",
                "--no-use-pep517",
                repo_url
            ]
        },
        # Method 3: Standard PEP 517
        {
            "name": "Standard PEP 517",
            "cmd": [
                sys.executable, "-m", "pip", "install",
                "--use-pep517",
                repo_url
            ]
        },
        # Method 4: Force reinstall with no cache
        {
            "name": "Force reinstall with no cache",
            "cmd": [
                sys.executable, "-m", "pip", "install",
                "--force-reinstall", "--no-cache-dir",
                repo_url
            ]
        }
    ]
    
    for method in methods:
        print(f"\n{'='*50}")
        print(f"Trying method: {method['name']}")
        print(f"{'='*50}")
        
        try:
            run_command(method["cmd"])
            print(f"✅ Success with method: {method['name']}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed with method: {method['name']}")
            print(f"Error: {e}")
            continue
    
    print("❌ All installation methods failed")
    return False

def verify_installation():
    """Verify that the package was installed correctly."""
    print("\nVerifying installation...")
    try:
        run_command([
            sys.executable, "-c", 
            "import crunpyroll; print(f'✅ crunpyroll imported successfully')"
        ])
        
        # Check package info
        result = run_command([
            sys.executable, "-m", "pip", "show", "crunpyroll"
        ])
        return True
    except subprocess.CalledProcessError:
        print("❌ Package verification failed")
        return False

def main():
    """Main installation function."""
    print("🐳 Docker-compatible crunpyroll installation script")
    print("=" * 60)
    
    try:
        # Step 1: Check Python version
        check_python_version()
        
        # Step 2: Upgrade pip and setuptools
        upgrade_pip_and_setuptools()
        
        # Step 3: Install build dependencies
        install_build_dependencies()
        
        # Step 4: Install crunpyroll
        if install_crunpyroll():
            # Step 5: Verify installation
            if verify_installation():
                print("\n🎉 Installation completed successfully!")
                return 0
            else:
                print("\n❌ Installation verification failed")
                return 1
        else:
            print("\n❌ Installation failed")
            return 1
            
    except Exception as e:
        print(f"\n💥 Installation script failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
