# Upload Script for PyPI
# Save your PyPI token and run this script

# STEP 1: Get your PyPI token
# Go to: https://pypi.org/manage/account/token/
# Create a token named "dtor-upload"
# Copy the token (starts with pyp-)

# STEP 2: Set your token as environment variable (RECOMMENDED)
# Windows PowerShell:
#   $env:TWINE_PASSWORD = "your-token-here"
#   python upload_to_pypi.py

# OR use interactive mode (less secure - token visible in terminal)

import os
import subprocess
import sys

def upload_to_pypi():
    """Upload package to PyPI"""
    
    # Check if distribution files exist
    if not os.path.exists('dist'):
        print("❌ Error: dist/ directory not found!")
        print("Run 'python -m build' first to create distribution files.")
        sys.exit(1)
    
    # Check for token in environment
    token = os.environ.get('TWINE_PASSWORD')
    
    if not token:
        print("⚠️  TWINE_PASSWORD not found in environment variables")
        print("\nOptions:")
        print("1. Set environment variable (Recommended):")
        print("   PowerShell: $env:TWINE_PASSWORD = 'your-token-here'")
        print("   Then run this script again")
        print("\n2. Enter token interactively (less secure)")
        
        choice = input("\nEnter '1' to exit and set env var, or '2' to continue: ").strip()
        
        if choice == '1':
            print("\n✋ Exiting. Please set TWINE_PASSWORD and run again.")
            sys.exit(0)
        elif choice == '2':
            token = input("\n🔑 Enter your PyPI token: ").strip()
            if not token:
                print("❌ No token provided. Exiting.")
                sys.exit(1)
        else:
            print("❌ Invalid choice. Exiting.")
            sys.exit(1)
    
    # Set up environment for twine
    env = os.environ.copy()
    env['TWINE_USERNAME'] = '__token__'
    env['TWINE_PASSWORD'] = token
    
    print("\n📦 Uploading to PyPI...")
    print("=" * 60)
    
    try:
        # Upload to PyPI
        result = subprocess.run(
            ['twine', 'upload', 'dist/*'],
            env=env,
            check=True,
            capture_output=False
        )
        
        print("=" * 60)
        print("✅ Successfully uploaded to PyPI!")
        print("\n📥 Install with: pip install dtor")
        print("🔗 View on PyPI: https://pypi.org/project/dtor/")
        
    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print(f"❌ Upload failed!")
        print(f"\nError: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'twine' not found!")
        print("Install with: pip install twine")
        sys.exit(1)

def upload_to_test_pypi():
    """Upload to TestPyPI first (for testing)"""
    
    token = os.environ.get('TEST_PYPI_TOKEN')
    
    if not token:
        print("⚠️  TEST_PYPI_TOKEN not found")
        token = input("Enter TestPyPI token (or press Enter to skip): ").strip()
        if not token:
            print("⏭️  Skipping TestPyPI upload")
            return
    
    env = os.environ.copy()
    env['TWINE_USERNAME'] = '__token__'
    env['TWINE_PASSWORD'] = token
    
    print("\n📦 Uploading to TestPyPI...")
    
    try:
        subprocess.run(
            ['twine', 'upload', '--repository', 'testpypi', 'dist/*'],
            env=env,
            check=True
        )
        print("✅ TestPyPI upload successful!")
        print("Test install: pip install --index-url https://test.pypi.org/simple/ dtor")
        
    except subprocess.CalledProcessError:
        print("⚠️  TestPyPI upload failed (may already exist)")

if __name__ == '__main__':
    print("🚀 dtor PyPI Upload Script")
    print("=" * 60)
    
    # Ask if user wants to test on TestPyPI first
    test_first = input("\n🧪 Upload to TestPyPI first? (y/n): ").strip().lower()
    
    if test_first == 'y':
        upload_to_test_pypi()
        
        proceed = input("\n➡️  Continue to real PyPI? (y/n): ").strip().lower()
        if proceed != 'y':
            print("✋ Stopped. Run again when ready for PyPI.")
            sys.exit(0)
    
    # Upload to real PyPI
    upload_to_pypi()
