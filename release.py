#!/usr/bin/env python3
"""
Release helper script for HTML Cleaning Toolkit
Automates building, testing, and preparing releases
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


def run_command(cmd, description=""):
    """Run a shell command and report results."""
    if description:
        print(f"\n📦 {description}...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   ❌ FAILED: {result.stderr}")
            return False
        if result.stdout:
            print(f"   ✓ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False


def validate_version(version_str):
    """Check if version string is valid (semver)."""
    parts = version_str.split('.')
    if len(parts) != 3:
        return False
    for part in parts:
        if not part.isdigit():
            return False
    return True


def update_version_in_files(old_ver, new_ver):
    """Update version in setup.py and pyproject.toml"""
    files = {
        'setup.py': ['version="', '",'],
        'pyproject.toml': ['version = "', '"'],
    }
    
    for filepath, (prefix, suffix) in files.items():
        with open(filepath, 'r') as f:
            content = f.read()
        
        old_line = f'{prefix}{old_ver}{suffix}'
        new_line = f'{prefix}{new_ver}{suffix}'
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"   ✓ Updated {filepath}")
        else:
            print(f"   ⚠ Could not find version in {filepath}")


def run_tests():
    """Run validation and comprehensive tests."""
    print("\n🧪 Running test suite...")
    
    tests = [
        ("Validation", "python tests/validate.py"),
        ("Comprehensive", "python tests/test_comprehensive.py"),
        ("Space Preservation", "python tests/test_space_preservation.py"),
        ("Entity Fix", "python tests/test_entity_fix.py"),
        ("NBSP Removal", "python tests/test_nbsp_removal.py"),
    ]
    
    failed = []
    for test_name, cmd in tests:
        if not run_command(cmd, test_name):
            failed.append(test_name)
    
    if failed:
        print(f"\n❌ Failed tests: {', '.join(failed)}")
        return False
    
    print("\n✅ All tests passed!")
    return True


def build_package():
    """Build the executable distribution using PyInstaller."""
    print("\n🔨 Building executable...")
    
    # Clean previous builds
    run_command("rm -rf build dist *.egg-info", "Cleaning old builds")
    run_command("rmdir /S /Q __pycache__ 2>nul || true", "Cleaning cache")
    
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not installed")
        print("   Install it: pip install pyinstaller")
        return False
    
    # Build executable
    if not run_command("pyinstaller html-cleaner.spec", "Building with PyInstaller"):
        return False
    
    # Check build artifacts
    exe_path = Path("dist/html-cleaner/html-cleaner.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Build successful!")
        print(f"   - Executable: dist/html-cleaner/html-cleaner.exe ({size_mb:.2f} MB)")
        
        # Create zip file for distribution
        print("   - Creating zip archive...")
        run_command("powershell -Command \"Compress-Archive -Path dist\\html-cleaner -DestinationPath html-cleaner-win64.zip -Force\"", "Zipping")
        
        zip_path = Path("html-cleaner-win64.zip")
        if zip_path.exists():
            zip_mb = zip_path.stat().st_size / (1024 * 1024)
            print(f"   - Archive: html-cleaner-win64.zip ({zip_mb:.2f} MB)")
        
        return True
    
    print("❌ Build failed - executable not found")
    return False


def show_release_checklist():
    """Display pre-release checklist."""
    print("\n📋 Pre-Release Checklist:")
    print("""
    ☐ Version number updated (setup.py, pyproject.toml)
    ☐ CHANGELOG.md updated with changes
    ☐ All tests passing (python release.py test)
    ☐ README.md reviewed for accuracy
    ☐ No debug code left in source
    ☐ Git commits are clean and descriptive
    ☐ Git branch has no untracked files
    ☐ Executable builds locally (python release.py build)
    
    Next steps:
    1. Commit changes: git add . && git commit -m "Release v1.x.x"
    2. Create git tag: git tag -a v1.x.x -m "Release 1.x.x"
    3. Push to GitHub: git push origin main && git push origin --tags
    4. GitHub Actions will automatically:
       - Run tests on multiple Python versions
       - Build the executable on Windows
       - Attach html-cleaner.exe and .zip to release page
       
    Team members can then download from:
    github.com/alemonterocr/ddc-html-tool/releases
    """)


def main():
    """Main release helper flow."""
    print("=" * 60)
    print("HTML CLEANING TOOLKIT - Release Helper")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            success = run_tests()
            return 0 if success else 1
        
        elif command == "build":
            if not run_tests():
                print("\n❌ Tests failed - aborting build")
                return 1
            success = build_package()
            return 0 if success else 1
        
        elif command == "version":
            if len(sys.argv) < 3:
                print("Usage: python release.py version <new_version>")
                print("Example: python release.py version 1.1.0")
                return 1
            
            new_ver = sys.argv[2]
            if not validate_version(new_ver):
                print(f"❌ Invalid version format: {new_ver}")
                print("   Use semantic versioning: MAJOR.MINOR.PATCH")
                return 1
            
            # Get current version from setup.py
            with open('setup.py', 'r') as f:
                setup_content = f.read()
                for line in setup_content.split('\n'):
                    if 'version=' in line and '"' in line:
                        old_ver = line.split('"')[1]
                        break
            
            print(f"\n🔄 Updating version {old_ver} → {new_ver}")
            update_version_in_files(old_ver, new_ver)
            print("✅ Version updated successfully")
            return 0
        
        elif command == "checklist":
            show_release_checklist()
            return 0
        
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  test        - Run all tests")
            print("  build       - Run tests and build package")
            print("  version X.Y.Z - Update version")
            print("  checklist   - Show pre-release checklist")
            return 1
    
    # Interactive menu if no args
    print("\n🔍 What would you like to do?\n")
    print("1. Run tests")
    print("2. Build package (after tests)")
    print("3. Update version")
    print("4. Show pre-release checklist")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        return 0 if run_tests() else 1
    elif choice == "2":
        if not run_tests():
            print("\n❌ Tests failed - aborting build")
            return 1
        return 0 if build_package() else 1
    elif choice == "3":
        new_ver = input("Enter new version (X.Y.Z): ").strip()
        if not validate_version(new_ver):
            print("❌ Invalid version format")
            return 1
        with open('setup.py', 'r') as f:
            for line in f.read().split('\n'):
                if 'version=' in line and '"' in line:
                    old_ver = line.split('"')[1]
                    break
        update_version_in_files(old_ver, new_ver)
        print("✅ Version updated")
        return 0
    elif choice == "4":
        show_release_checklist()
        return 0
    else:
        print("Goodbye!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
