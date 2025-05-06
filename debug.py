#!/usr/bin/env python
"""Debugging script to examine the Railway deployment environment"""
import os
import sys
import subprocess

# Print environment
print("=== ENVIRONMENT VARIABLES ===")
for key, value in sorted(os.environ.items()):
    print(f"{key}: {value}")

# Print Python Path
print("\n=== PYTHON PATH ===")
for path in sys.path:
    print(path)

# Print directory structure 
print("\n=== DIRECTORY STRUCTURE ===")
subprocess.run(["ls", "-la", "/"])
subprocess.run(["ls", "-la", "."])
if os.path.exists("bailanysta_project"):
    print("\n=== BAILANYSTA_PROJECT DIRECTORY ===")
    subprocess.run(["ls", "-la", "bailanysta_project"])
    if os.path.exists("bailanysta_project/bailanysta_project"):
        print("\n=== BAILANYSTA_PROJECT/BAILANYSTA_PROJECT DIRECTORY ===")
        subprocess.run(["ls", "-la", "bailanysta_project/bailanysta_project"]) 