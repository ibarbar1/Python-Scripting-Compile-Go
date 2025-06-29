# Python Scripting Project

This project automates the process of:

- Finding game directories in a source folder
- Copying them to a target directory
- Compiling any Go code inside those folders
- Creating metadata as a JSON file

## Features

✅ **Find Game Directories**
- Looks for folders whose names contain `game` (case-insensitive)

✅ **Copy Files**
- Copies all files and subfolders to the target directory
- Supports repeated runs without errors (`dirs_exist_ok=True`)

✅ **Compile Go Code**
- Finds `.go` files in each copied folder
- Runs `go build` to compile them

✅ **Generate Metadata**
- Saves a JSON file listing all games and their count

## Requirements

- Python 3.7+
- Go installed and added to your system PATH

## Usage

Run the script like this:

```bash
python get_game_data_test.py <source_folder> <target_folder> e.g python get_game_data_test.py data target

This will:

- Search data for game directories
- Copy them into target
- Compile Go code inside each copied folder
- Create metadata.json inside target