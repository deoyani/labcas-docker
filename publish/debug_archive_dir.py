import os
import pathlib
import sys
import subprocess

archive_dir = '/data/archive'
print(f"DEBUG: Using archive_dir: {archive_dir}")
if not pathlib.Path(archive_dir).exists():
    print(f"DEBUG: archive_dir does NOT exist: {archive_dir}")
    sys.stderr.write(f"ERROR: archive_dir does NOT exist: {archive_dir}\n")
else:
    print(f"DEBUG: archive_dir exists: {archive_dir}")

# Run the original publishing pipeline
subprocess.run(["python3", "-u", "/opt/publish/publishing_pipeline.py"], check=True)