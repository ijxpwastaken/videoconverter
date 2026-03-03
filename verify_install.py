#!/usr/bin/env python3
"""
Installation Verification Script

Checks if all required packages are installed and working correctly.
Run this before running vidterm.py to diagnose installation issues.
"""

import sys
import os

def check_package(name, import_name):
    """Check if a package is installed and importable."""
    try:
        __import__(import_name)
        print(f"✓ {name:20} OK")
        return True
    except ImportError:
        print(f"✗ {name:20} NOT INSTALLED")
        return False

def check_python_version():
    """Check Python version."""
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 7:
        print(f"✓ Python Version:        {major}.{minor} OK")
        return True
    else:
        print(f"✗ Python Version:        {major}.{minor} (need 3.7+)")
        return False

def check_windows():
    """Check if running on Windows."""
    if os.name == 'nt':
        print(f"✓ Operating System:      Windows OK")
        return True
    else:
        print(f"✗ Operating System:      {os.name} (Windows required)")
        return False

def check_msvcrt():
    """Check if msvcrt is available (Windows-only)."""
    try:
        import msvcrt
        print(f"✓ msvcrt (keyboard):     OK")
        return True
    except ImportError:
        print(f"✗ msvcrt (keyboard):     NOT AVAILABLE")
        return False

def check_colorama():
    """Check colorama version and functionality."""
    try:
        import colorama
        print(f"✓ colorama (ANSI):       OK (v{colorama.__version__})")
        return True
    except ImportError:
        print(f"✗ colorama (ANSI):       NOT INSTALLED")
        return False

def check_opencv():
    """Check OpenCV version and video support."""
    try:
        import cv2
        print(f"✓ opencv-python (cv2):   OK (v{cv2.__version__})")
        return True
    except ImportError:
        print(f"✗ opencv-python (cv2):   NOT INSTALLED")
        return False

def check_pil():
    """Check Pillow version."""
    try:
        from PIL import Image
        import PIL
        print(f"✓ Pillow (PIL):          OK (v{PIL.__version__})")
        return True
    except ImportError:
        print(f"✗ Pillow (PIL):          NOT INSTALLED")
        return False

def check_yt_dlp():
    """Check yt-dlp version."""
    try:
        import yt_dlp
        print(f"✓ yt-dlp:                OK (v{yt_dlp.__version__})")
        return True
    except ImportError:
        print(f"✗ yt-dlp:                NOT INSTALLED")
        return False

def main():
    print("═" * 60)
    print("  Installation Verification")
    print("═" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Windows OS", check_windows),
        ("Packages", None),  # Section header
    ]

    results = []

    # System checks
    print("SYSTEM")
    print("─" * 60)
    for name, check_func in checks:
        if check_func:
            results.append(check_func())
    print()

    # Package checks
    print("PACKAGES")
    print("─" * 60)
    results.append(check_yt_dlp())
    results.append(check_opencv())
    results.append(check_pil())
    results.append(check_colorama())
    results.append(check_msvcrt())
    print()

    # Summary
    print("═" * 60)
    passed = sum(results)
    total = len(results)

    if all(results):
        print(f"✓ All checks passed! ({passed}/{total})")
        print()
        print("You're ready to use vidterm.py!")
        print()
        print("Example:")
        print('  python vidterm.py "https://www.youtube.com/watch?v=VIDEO_ID"')
        return 0
    else:
        failed = [i for i, r in enumerate(results) if not r]
        print(f"✗ {len(failed)} check(s) failed. ({passed}/{total})")
        print()
        print("Install missing packages with:")
        print("  pip install yt-dlp opencv-python Pillow colorama")
        print()
        if not check_windows():
            print("Note: This tool is designed for Windows.")
        if not check_msvcrt():
            print("Note: msvcrt is built-in to Windows; this is a compatibility issue.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
