#!/usr/bin/env python3
"""
Alias runner for EYESPY Covert Morse Framework.
Allows running via: python script.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eyespy import main

if __name__ == "__main__":
    main()
