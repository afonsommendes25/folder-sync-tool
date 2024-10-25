# Folder Synchronization Tool
This project is a Python script for synchronizing two folders at regular intervals. It copies new or modified files from a source folder to a replica folder, ensuring that both folders remain identical. The tool also logs all synchronization activities to a specified log file.

## Features

- **Automated Synchronization:** Syncs files from the source folder to the replica folder at set intervals.
- **MD5 Checksum Verification:** Verifies files by their content using MD5 hashes to ensure only modified files are updated.
- **Logging:** Logs synchronization actions (e.g. files copied or deleted) to a specified log file.
- **Command-Line Interface:** Accepts command-line arguments for easy setup and usage.

## Requirements

- **Modules Used:** pathlib, time, hashlib, logging, shutil, argparse

## Arguments

- **source_folder:** Path to the source folder, where you sync from
- **replica_folder:** Path to the replica folder, to where you sync to
- **interval:** Time interval (in seconds) between each sync 
- **log_file:** Path to the logging file for reccording sync actions

```bash
python sync_files.py <source_folder> <replica_folder> <interval> <log_file>
```

## Example

```bash
python sync_files.py /path/to/source /path/to/replica 60 /path/to/log
```

This example syncs the `source folder` with the `replica` folder every 120 seconds, logging actions to the `log` file.
