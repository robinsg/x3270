#!/usr/bin/env python3
"""
Cleanup script to reduce x3270 repository size by removing components
not needed for building s3270 and c3270 only.

This script removes:
- All Windows-specific components (wc3270, ws3270, wb3270, etc.)
- X11 GUI components (x3270)
- Backend components (b3270)
- TCL integration (tcl3270)
- Additional utilities (playback, mitm)
- Development tools (VisualStudio, Webpage, ReleaseTools, ConvTools)
- External dependencies that aren't needed

Preserves:
- Common/ (shared source code)
- s3270/, c3270/ (target components)
- lib/ (required libraries)
- include/, Shared/ (headers and shared files)
- Core build infrastructure
"""

import os
import shutil
import sys
from pathlib import Path

# Root directory
ROOT_DIR = Path(__file__).parent

# Directories to completely remove
REMOVE_DIRS = [
    # Windows components
    "wc3270",
    "ws3270", 
    "wb3270",
    "wpr3287",
    "wx3270if",
    "wmitm",
    "wplayback",
    
    # X11 GUI
    "x3270",
    
    # Backend
    "b3270",
    
    # TCL integration
    "tcl3270",
    
    # Utilities
    "playbook",
    "mitm",
    
    # Development tools
    "VisualStudio",
    "Webpage", 
    "ReleaseTools",
    "ConvTools",
    
    # Test/relay tools
    "st-relay",
]

# Directories to keep (essential for s3270/c3270)
KEEP_DIRS = [
    "Common",      # Shared source code
    "s3270",       # s3270 component  
    "c3270",       # c3270 component
    "lib",         # Required libraries (3270, 3270i, 32xx, 3270stubs)
    "include",     # Header files
    "Shared",      # Shared files
    "pr3287",      # Print utility (used by s3270/c3270)
    "x3270if",     # Interface utility (used by s3270/c3270)
    "ibm_hosts",   # Host configuration (used by c3270)
    ".git",        # Git repository
    ".vscode",     # IDE settings
    ".logs",       # Logs
    ".evfevent",   # Event files
]

# Files to remove (Windows-specific or unnecessary)
REMOVE_FILES = [
    "run_windows_tests.py",  # Windows testing
]

def remove_safely(path):
    """Remove a file or directory safely with error handling."""
    try:
        if path.is_file():
            path.unlink()
            print(f"Removed file: {path}")
        elif path.is_dir():
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
        else:
            print(f"Path not found: {path}")
    except Exception as e:
        print(f"Error removing {path}: {e}")

def main():
    print("Starting cleanup for s3270/c3270 only build...")
    print(f"Working directory: {ROOT_DIR}")
    
    # Confirm we're in the right directory
    if not (ROOT_DIR / "configure.in").exists():
        print("Error: Not in x3270 root directory (configure.in not found)")
        sys.exit(1)
    
    # Remove unnecessary directories
    removed_count = 0
    for dir_name in REMOVE_DIRS:
        dir_path = ROOT_DIR / dir_name
        if dir_path.exists():
            remove_safely(dir_path)
            removed_count += 1
        else:
            print(f"Directory not found (already removed?): {dir_name}")
    
    # Remove unnecessary files
    for file_name in REMOVE_FILES:
        file_path = ROOT_DIR / file_name
        if file_path.exists():
            remove_safely(file_path)
            removed_count += 1
        else:
            print(f"File not found (already removed?): {file_name}")
    
    # Clean up extern/ subdirectories but keep the main extern/ directory
    extern_dir = ROOT_DIR / "extern"
    if extern_dir.exists():
        print(f"Cleaning extern/ subdirectories...")
        for item in extern_dir.iterdir():
            if item.is_dir():
                remove_safely(item)
                removed_count += 1
    
    print(f"\nCleanup complete! Removed {removed_count} items.")
    print(f"Kept essential directories: {', '.join(KEEP_DIRS)}")
    
    # List remaining directories
    print(f"\nRemaining directories:")
    for item in sorted(ROOT_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            print(f"  {item.name}/")

if __name__ == "__main__":
    main()
