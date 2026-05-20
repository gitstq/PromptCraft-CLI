#!/usr/bin/env python3
"""
PromptCraft CLI - Main Entry Point
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptcraft.cli import main

if __name__ == "__main__":
    sys.exit(main())
